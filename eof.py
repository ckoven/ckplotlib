import sys
import numpy as np

### program to calculate EOFs




def eof_2d(data_in, dimension=0, mask_number=-9999., domask=False):
    

    dims = data_in.shape

    input_has_mask = isinstance(data_in,np.ma.masked_array)

    if dimension == 0:
        IM = dims[2]
        JM = dims[1]
        t = dims[0]
    else:
        sys.exit('eof_2d error: need to add ability to work on arbitrary dimension')

    x = (IM*JM)

    #convert lat/lon/time to space/time
    D=np.zeros([x,t])
    print(D.flags.writeable)
    if not input_has_mask:
        D = np.copy(np.transpose(np.reshape(data_in, [t, IM*JM])))
    else:
        D = np.copy(np.ma.getdata(np.ma.transpose(np.ma.reshape(data_in, [t, IM*JM]))))
        D_mask = np.copy(np.ma.getmask(np.ma.transpose(np.ma.reshape(data_in, [t, IM*JM]))))
        D[D_mask] = mask_number
    #  find bad points
    if domask or input_has_mask:
        goodpoints = D != mask_number
    else:
        goodpoints = np.ones([x,t])

    #subtract means at each station
    for i in range(0,x):
        thesum = 0.
        k = 0.
        for j in range(0,t):
            if goodpoints[i,j]:
                thesum = thesum + D[i,j]
                k = k+1.
        if k > 0:
            D[i,:] = D[i,:] - thesum/k

    # make bad points equal to zero
    D = D*goodpoints
    
        
    #COMPUTE CORRELATION MATRIX B=D*DT
    DT=np.transpose(D)

    B = np.dot(DT[:],D[:])


    #IF NOT AREA WEIGHTED
    B[:,:]=B[:,:]/x

    #SOLVE FOR EIGENVALUES (T array) AND PCS (T1*T2 array, where T2 # of PC and T1 AMPLITUDE)

    ## orig IDL code:: Result = EIGENQL(B, RESIDUAL = residual, EIGENVECTORS = princ)

    eigenvalues, eigenvectors = np.linalg.eigh(B)


    ## order the eigenvalues and associated eigenvectors
    order = t-1-np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:,order]

    
    print('eigenvalues')
    print(eigenvalues)
    print('sum of eigenvalues')
    print(np.sum(eigenvalues))

    spacing_error_ratio = (eigenvalues[0:t-2]-eigenvalues[1:t-1])/(eigenvalues[0:t-2]*np.sqrt(2./t))  ##  based on North et al. 1982
    print('ratio of eigenvalue spacing to relative error')
    print(spacing_error_ratio)

    var=np.zeros([t])
    for n in range(0,t):
        var[n]=eigenvalues[n]/np.sum(eigenvalues)

    print('A-O')
    print('variances')
    print(var[0:t-10])
    print(np.sum(var[:]))

    #NORMALIZE PCs (MEAN=0# VARIANCE=1)
    pc=np.zeros([t,t])
    pc=eigenvectors
    pcn=np.zeros([t,t])

    sqsyk=np.zeros([t])
    for k in range(0,t):
        sqsyk[k]=np.sum(pc[:,k]**2)

    for n in range(0,t):
        for k in range(0,t):
            pcn[n,k]=np.sqrt(t)*pc[n,k]/np.sqrt(sqsyk[k])

    #COMPUTE EOF ( X*T MATRIX, WHERE X=LOCATION AND T=# OF EOF) FROM PCs

    eofb = np.dot(D,pc)


    #NORMALIZE EOFs (Eq.15)
    eofn=np.zeros([x,t])
    for m in range(0,x):
        for k in range(0,t):
            eofn[m,k]=np.sqrt(sqsyk[k])*eofb[m,k]/np.sqrt(t)

    # print 'EOFN',eofn(100,0),eofn(200,0)
    # print 'CONTROL',correlate(D(100,*),pc(*,0)),correlate(D(200,*),pc(*,0))
    #print 'CONTROL',correlate(D(100,*),pcn(*,0),/covariance),correlate(D(200,*),pcn(*,0),/covariance)

    #first change eof back to lat/lon coordinates
    eoflatlon = np.rollaxis(np.reshape(eofn, [JM, IM, t]), 2)

    return eoflatlon, pc



################################################################################
################################################################################


def eof_1d(data_in, dimension=0, mask_number=-9999., domask=False):
    

    dims = data_in.shape

    input_has_mask = isinstance(data_in,np.ma.masked_array)

    if dimension == 0:
        nstation = dims[1]
        t = dims[0]
    else:
        sys.exit('eof_2d error: need to add ability to work on arbitrary dimension')

    x = nstation

    #convert lat/lon/time to space/time
    D=np.zeros([x,t])
    print(D.flags.writeable)
    if not input_has_mask:
        D = np.copy(data_in)
    else:
        D = np.copy(data_in)
        D_mask = np.copy(np.ma.getmask(data_in))
        D[D_mask] = mask_number

    #  find bad points
    if domask or input_has_mask:
        goodpoints = D != mask_number
    else:
        goodpoints = np.ones([x,t])

    #subtract means at each station
    for i in range(0,x):
        thesum = 0.
        k = 0.
        for j in range(0,t):
            if goodpoints[i,j]:
                thesum = thesum + D[i,j]
                k = k+1.
        if k > 0:
            D[i,:] = D[i,:] - thesum/k

    # make bad points equal to zero
    D = D*goodpoints
    
        
    #COMPUTE CORRELATION MATRIX B=D*DT
    DT=np.transpose(D)

    B = np.dot(DT[:],D[:])


    #IF NOT AREA WEIGHTED
    B[:,:]=B[:,:]/x

    #SOLVE FOR EIGENVALUES (T array) AND PCS (T1*T2 array, where T2 # of PC and T1 AMPLITUDE)

    ## orig IDL code:: Result = EIGENQL(B, RESIDUAL = residual, EIGENVECTORS = princ)

    eigenvalues, eigenvectors = np.linalg.eigh(B)


    ## order the eigenvalues and associated eigenvectors
    order = t-1-np.argsort(eigenvalues)
    eigenvalues = eigenvalues[order]
    eigenvectors = eigenvectors[:,order]

    
    print('eigenvalues')
    print(eigenvalues)
    print('sum of eigenvalues')
    print(np.sum(eigenvalues))

    spacing_error_ratio = (eigenvalues[0:t-2]-eigenvalues[1:t-1])/(eigenvalues[0:t-2]*np.sqrt(2./t))  ##  based on North et al. 1982
    print('ratio of eigenvalue spacing to relative error')
    print(spacing_error_ratio)

    var=np.zeros([t])
    for n in range(0,t):
        var[n]=eigenvalues[n]/np.sum(eigenvalues)

    print('A-O')
    print('variances')
    print(var[0:t-10])
    print(np.sum(var[:]))

    #NORMALIZE PCs (MEAN=0# VARIANCE=1)
    pc=np.zeros([t,t])
    pc=eigenvectors
    pcn=np.zeros([t,t])

    sqsyk=np.zeros([t])
    for k in range(0,t):
        sqsyk[k]=np.sum(pc[:,k]**2)

    for n in range(0,t):
        for k in range(0,t):
            pcn[n,k]=np.sqrt(t)*pc[n,k]/np.sqrt(sqsyk[k])

    #COMPUTE EOF ( X*T MATRIX, WHERE X=LOCATION AND T=# OF EOF) FROM PCs

    eofb = np.dot(D,pc)


    #NORMALIZE EOFs (Eq.15)
    eofn=np.zeros([x,t])
    for m in range(0,x):
        for k in range(0,t):
            eofn[m,k]=np.sqrt(sqsyk[k])*eofb[m,k]/np.sqrt(t)

    # print 'EOFN',eofn(100,0),eofn(200,0)
    # print 'CONTROL',correlate(D(100,*),pc(*,0)),correlate(D(200,*),pc(*,0))
    #print 'CONTROL',correlate(D(100,*),pcn(*,0),/covariance),correlate(D(200,*),pcn(*,0),/covariance)

    return eofn, pc

