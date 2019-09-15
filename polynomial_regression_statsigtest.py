import numpy as np
import math as m
import statslib
from scipy import special

def polynomtest(x,y,degree=2):

    y_prime = y - y.mean()
    ss_tot = np.sum(y_prime**2)
    print(('ss_tot: '+str(ss_tot)))

    ### first linear regression
    b_linear, rsq_linear = linreg.linreg(x,y)
    df_linear = len(y) - 2
    ypred_linear = b_linear[1]*x + b_linear[0]
    error_linear = y - ypred_linear
    error_ss_linear = np.sum(error_linear**2)
    rsq_linear2 = 1.-(error_ss_linear/ss_tot)
    df_linear = len(y) - 2
    print(('df_linear: '+str(df_linear)))
    print(('b_linear: '+str(b_linear)))
    print(('rsq_linear: '+str(rsq_linear)))
    print(('rsq_linear2: '+str(rsq_linear2)))
    print(('error_ss_linear: '+str(error_ss_linear)))
    print('')

    

    if degree <= 1:
        return b_linear
    else:
        ### next quadratic
        quadratic_b = np.polyfit(x,y,2)
        ypred_quadratic = np.polyval(quadratic_b, x)
        error_quadratic = y - ypred_quadratic
        error_ss_quadratic = np.sum(error_quadratic**2)
        rsq_quadratic = 1.-(error_ss_quadratic/ss_tot)
        df_quadratic = len(y) - 3
        fstat2_quadratic = (error_ss_quadratic - error_ss_linear) / (error_ss_quadratic / df_quadratic)
        f_stat_quadratic = df_quadratic * (rsq_quadratic - rsq_linear) / (1.- rsq_quadratic)
        p_quadratic = special.fdtrc(2,df_quadratic, f_stat_quadratic)
        

        print(('df_quadratic: '+str(df_quadratic)))
        print(('quadratic_b: '+str(quadratic_b)))
        print(('rsq_quadratic: '+str(rsq_quadratic)))
        print(('error_ss_quadratic: '+str(error_ss_quadratic)))
        print(('fstat2_quadratic: '+str(fstat2_quadratic)))
        print(('f_stat_quadratic: '+str(f_stat_quadratic)))
        print(('p_quadratic: '+str(p_quadratic)))
        print('')
        
        if degree <= 2:
            return quadratic_b
        else:
            ### next cubic
            cubic_b = np.polyfit(x,y,3)
            ypred_cubic = np.polyval(cubic_b, x)
            error_cubic = y - ypred_cubic
            error_ss_cubic = np.sum(error_cubic**2)
            rsq_cubic = 1.-(error_ss_cubic/ss_tot)
            df_cubic = len(y) - 4
            f_stat_cubic = df_cubic * (rsq_cubic - rsq_quadratic) / (1.- rsq_cubic)
            p_cubic = special.fdtrc(2,df_cubic, f_stat_cubic)
            print(('cubic_b: '+str(cubic_b)))
            print(('rsq_cubic: '+str(rsq_cubic)))
            print(('f_stat_cubic: '+str(f_stat_cubic)))
            print(('p_cubic: '+str(p_cubic)))
                            
            return cubic_b
            


