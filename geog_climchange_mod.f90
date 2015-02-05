
!! this is a fortran module for computing the lagrangian climate change vectors and associated statistics between two time periods of a climate model.  
!! the nested loops are too slow for the interpreted native python code so this is a much faster machinery for computing changes.
!! designed to be compiled using f2py and called as a python library:
!!  f2py -m geog_climchange_mod -c geog_climchange_mod.f90


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine calc_reduced_chisq_error(mean_obs1,mean_obs2,stddev_obs1,n, chisq)

  !!! calculate the chi-squared error statistic for the combined temperature and precip seasonal cycles
  !!! for two different climates
  
  double precision, intent(in) :: mean_obs1(n), mean_obs2(n), stddev_obs1(n)
  integer, intent(in) :: n
  double precision, intent(out) :: chisq
  
  chisq = sum((mean_obs1(:) - mean_obs2(:))**2 / stddev_obs1(:)**2 ) / real(n - 1)

end subroutine calc_reduced_chisq_error
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine calc_sed_error(mean_obs1,mean_obs2,stddev_obs1,n, sed)

  !!! calculate the standard euclidean distance error statistic for the combined temperature and precip seasonal cycles
  !!! for two different climates
  
  double precision, intent(in) :: mean_obs1(n), mean_obs2(n), stddev_obs1(n)
  integer, intent(in) :: n
  double precision, intent(out) :: sed
  
  sed = sqrt(sum((mean_obs1(:) - mean_obs2(:))**2 / stddev_obs1(:)**2 ))

end subroutine calc_sed_error
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine calc_dist(lon_i, lat_i, lon_ii, lat_ii, dist)

  !!! calculate the distance between two points in lat/lon.  assume for sake of simplicity just a flat geometry
  double precision, intent(in) :: lon_i, lat_i, lon_ii, lat_ii
  double precision, intent(out) :: dist

  dist = min(sqrt( (lon_i - lon_ii) ** 2 + (lat_i - lat_ii) ** 2), &
             sqrt( (360. + lon_i - lon_ii) ** 2 + (lat_i - lat_ii) ** 2), &
             sqrt( (lon_i - lon_ii - 360.) ** 2 + (lat_i - lat_ii) ** 2))

end subroutine calc_dist
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine get_climchange_vectors(mean_annual_cycle_future, std_annual_cycle_future, &
     mean_annual_cycle_historical, std_annual_cycle_historical, lats, lons, landmask, &
     maxdist, ntim, jm, im, &
     closest_match_I_vectorto, closest_match_J_vectorto, minimum_chisq_vectorto, &
     closest_match_I_vectorfrom, closest_match_J_vectorfrom, minimum_chisq_vectorfrom)

  !! input arguments
  double precision, intent(in) :: mean_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: mean_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: lats(jm)
  double precision, intent(in) :: lons(im)
  logical, intent(in) :: landmask(jm, im)
  double precision, intent(in) :: maxdist
  integer, intent(in) :: ntim, jm, im

  !!! output arguments
  integer, intent(out) :: closest_match_I_vectorto(jm, im)
  integer, intent(out) :: closest_match_J_vectorto(jm, im)
  double precision, intent(out) :: minimum_chisq_vectorto(jm, im)
  integer, intent(out) :: closest_match_I_vectorfrom(jm, im)
  integer, intent(out) :: closest_match_J_vectorfrom(jm, im)
  double precision, intent(out) :: minimum_chisq_vectorfrom(jm, im)

  !! local variables
  integer :: i, j, ii, jj
  double precision :: dist
  double precision :: chisq_vectorto, chisq_vectorfrom


  !!! begin code here
  write(6,*) 'beginning search through lagrangian climate change space'
  write(6,*) 'im = ', im
  write(6,*) 'jm = ', jm
  write(6,*) 'ntim = ', ntim

  !! initialize variables
  minimum_chisq_vectorto(:,:) = 1.e5
  minimum_chisq_vectorfrom(:,:) = 1.e5


  do i = 1, im
     write(6,*) 'starting longitude column i =', i
     do j = 1, jm
        if ( landmask(j,i) ) then
           do ii = 1, im
              do jj = 1, jm
                 if ( landmask(jj,ii) ) then                    
                    call calc_dist(lons(i),lats(j),lons(ii),lats(jj), dist)
                    if ( dist .le. maxdist ) then
                       !
                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest future climate gridcell to a given historical climate gridcell
                       ! i.e. where is the climate going to?
                       call calc_reduced_chisq_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,jj,ii), &
                            std_annual_cycle_historical(:,j,i), ntim, chisq_vectorto)
                       if ( chisq_vectorto .lt. minimum_chisq_vectorto(j,i) ) then
                          minimum_chisq_vectorto(j,i) = chisq_vectorto
                          closest_match_I_vectorto(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorto(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif
                       !
                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest historical climate gridcell to a given future climate gridcell
                       ! i.e. where is the climate coming from?
                       call calc_reduced_chisq_error(mean_annual_cycle_future(:,j,i), mean_annual_cycle_historical(:,jj,ii), &
                            std_annual_cycle_future(:,j,i), ntim, chisq_vectorfrom)
                       if ( chisq_vectorfrom .lt. minimum_chisq_vectorfrom(j,i) ) then
                          minimum_chisq_vectorfrom(j,i) = chisq_vectorfrom
                          closest_match_I_vectorfrom(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorfrom(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif
                    endif
                 endif
              end do
           end do
        endif
     end do
  end do
     
  

end subroutine get_climchange_vectors
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine get_climchange_vectors_v2(mean_annual_cycle_future, std_annual_cycle_future, &
     mean_annual_cycle_historical, std_annual_cycle_historical, lats, lons, landmask, &
     maxdist, ntim, jm, im, &
     closest_match_I_vectorto, closest_match_J_vectorto, minimum_chisq_vectorto, &
     closest_match_I_vectorfrom, closest_match_J_vectorfrom, minimum_chisq_vectorfrom, &
     local_chisq_error)

  !! input arguments
  double precision, intent(in) :: mean_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: mean_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: lats(jm)
  double precision, intent(in) :: lons(im)
  logical, intent(in) :: landmask(jm, im)
  double precision, intent(in) :: maxdist
  integer, intent(in) :: ntim, jm, im

  !!! output arguments
  integer, intent(out) :: closest_match_I_vectorto(jm, im)
  integer, intent(out) :: closest_match_J_vectorto(jm, im)
  double precision, intent(out) :: minimum_chisq_vectorto(jm, im)
  integer, intent(out) :: closest_match_I_vectorfrom(jm, im)
  integer, intent(out) :: closest_match_J_vectorfrom(jm, im)
  double precision, intent(out) :: minimum_chisq_vectorfrom(jm, im)
  double precision, intent(out) :: local_chisq_error(jm, im)

  !! local variables
  integer :: i, j, ii, jj
  double precision :: dist
  double precision :: chisq_vectorto, chisq_vectorfrom


  !!! begin code here
  write(6,*) 'beginning search through lagrangian climate change space'
  write(6,*) 'im = ', im
  write(6,*) 'jm = ', jm
  write(6,*) 'ntim = ', ntim

  !! initialize variables
  minimum_chisq_vectorto(:,:) = 1.e5
  minimum_chisq_vectorfrom(:,:) = 1.e5


  do i = 1, im
     write(6,*) 'starting longitude column i =', i
     do j = 1, jm
        if ( landmask(j,i) ) then
           call calc_reduced_chisq_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,j,i), &
                std_annual_cycle_historical(:,j,i), ntim, local_chisq_error(j,i))
           do ii = 1, im
              do jj = 1, jm
                 if ( landmask(jj,ii) ) then                    
                    call calc_dist(lons(i),lats(j),lons(ii),lats(jj), dist)
                    if ( dist .le. maxdist ) then

                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest future climate gridcell to a given historical climate gridcell
                       ! i.e. where is the climate going to?
                       call calc_reduced_chisq_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,jj,ii), &
                            std_annual_cycle_historical(:,j,i), ntim, chisq_vectorto)
                       if ( chisq_vectorto .lt. minimum_chisq_vectorto(j,i) ) then
                          minimum_chisq_vectorto(j,i) = chisq_vectorto
                          closest_match_I_vectorto(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorto(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif

                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest historical climate gridcell to a given future climate gridcell
                       ! i.e. where is the climate coming from?
                       call calc_reduced_chisq_error(mean_annual_cycle_future(:,j,i), mean_annual_cycle_historical(:,jj,ii), &
                            std_annual_cycle_future(:,j,i), ntim, chisq_vectorfrom)
                       if ( chisq_vectorfrom .lt. minimum_chisq_vectorfrom(j,i) ) then
                          minimum_chisq_vectorfrom(j,i) = chisq_vectorfrom
                          closest_match_I_vectorfrom(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorfrom(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif

                    endif
                 endif
              end do
           end do
        endif
     end do
  end do
     
  

end subroutine get_climchange_vectors_v2
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine get_climchange_vectors_sed(mean_annual_cycle_future, std_annual_cycle_future, &
     mean_annual_cycle_historical, std_annual_cycle_historical, lats, lons, landmask, &
     maxdist, ntim, jm, im, &
     closest_match_I_vectorto, closest_match_J_vectorto, minimum_sed_vectorto, &
     closest_match_I_vectorfrom, closest_match_J_vectorfrom, minimum_sed_vectorfrom, &
     local_sed_error)

  !! input arguments
  double precision, intent(in) :: mean_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: mean_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: lats(jm)
  double precision, intent(in) :: lons(im)
  logical, intent(in) :: landmask(jm, im)
  double precision, intent(in) :: maxdist
  integer, intent(in) :: ntim, jm, im

  !!! output arguments
  integer, intent(out) :: closest_match_I_vectorto(jm, im)
  integer, intent(out) :: closest_match_J_vectorto(jm, im)
  double precision, intent(out) :: minimum_sed_vectorto(jm, im)
  integer, intent(out) :: closest_match_I_vectorfrom(jm, im)
  integer, intent(out) :: closest_match_J_vectorfrom(jm, im)
  double precision, intent(out) :: minimum_sed_vectorfrom(jm, im)
  double precision, intent(out) :: local_sed_error(jm, im)

  !! local variables
  integer :: i, j, ii, jj
  double precision :: dist
  double precision :: sed_vectorto, sed_vectorfrom


  !!! begin code here
  write(6,*) 'beginning search through lagrangian climate change space'
  write(6,*) 'im = ', im
  write(6,*) 'jm = ', jm
  write(6,*) 'ntim = ', ntim

  !! initialize variables
  minimum_sed_vectorto(:,:) = 1.e5
  minimum_sed_vectorfrom(:,:) = 1.e5


  do i = 1, im
     write(6,*) 'starting longitude column i =', i
     do j = 1, jm
        if ( landmask(j,i) ) then
           call calc_sed_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,j,i), &
                std_annual_cycle_historical(:,j,i), ntim, local_sed_error(j,i))
           do ii = 1, im
              do jj = 1, jm
                 if ( landmask(jj,ii) ) then                    
                    call calc_dist(lons(i),lats(j),lons(ii),lats(jj), dist)
                    if ( dist .le. maxdist ) then

                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest future climate gridcell to a given historical climate gridcell
                       ! i.e. where is the climate going to?
                       call calc_sed_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,jj,ii), &
                            std_annual_cycle_historical(:,j,i), ntim, sed_vectorto)
                       if ( sed_vectorto .lt. minimum_sed_vectorto(j,i) ) then
                          minimum_sed_vectorto(j,i) = sed_vectorto
                          closest_match_I_vectorto(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorto(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif

                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                       ! calculate closest historical climate gridcell to a given future climate gridcell
                       ! i.e. where is the climate coming from?
                       call calc_sed_error(mean_annual_cycle_future(:,j,i), mean_annual_cycle_historical(:,jj,ii), &
                            std_annual_cycle_future(:,j,i), ntim, sed_vectorfrom)
                       if ( sed_vectorfrom .lt. minimum_sed_vectorfrom(j,i) ) then
                          minimum_sed_vectorfrom(j,i) = sed_vectorfrom
                          closest_match_I_vectorfrom(j,i) = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                          closest_match_J_vectorfrom(j,i) = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                       endif

                    endif
                 endif
              end do
           end do
        endif
     end do
  end do
     
  

end subroutine get_climchange_vectors_sed
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine get_climchange_vectors_onesite_sed(mean_annual_cycle_future, std_annual_cycle_future, &
     mean_annual_cycle_historical, std_annual_cycle_historical, lats, lons, landmask, i_in, j_in, &
     maxdist, ntim, jm, im, &
     closest_match_I_vectorto, closest_match_J_vectorto, sed_vectorto_array, &
     closest_match_I_vectorfrom, closest_match_J_vectorfrom, sed_vectorfrom_array, &
     sed_historicalclimate_array)

  !! input arguments
  double precision, intent(in) :: mean_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_future(ntim, jm, im)
  double precision, intent(in) :: mean_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: std_annual_cycle_historical(ntim, jm, im)
  double precision, intent(in) :: lats(jm)
  double precision, intent(in) :: lons(im)
  logical, intent(in) :: landmask(jm, im)
  double precision, intent(in) :: maxdist
  integer, intent(in) :: ntim, jm, im, i_in, j_in

  !!! output arguments
  integer, intent(out) :: closest_match_I_vectorto
  integer, intent(out) :: closest_match_J_vectorto
  double precision, intent(out) :: sed_vectorto_array(jm, im)
  integer, intent(out) :: closest_match_I_vectorfrom
  integer, intent(out) :: closest_match_J_vectorfrom
  double precision, intent(out) :: sed_vectorfrom_array(jm, im)
  double precision, intent(out) :: sed_historicalclimate_array(jm, im)


  !! local variables
  integer :: i, j, ii, jj
  double precision :: dist
  double precision :: sed_vectorto, sed_vectorfrom, sed_historicalclimate
  double precision :: minimum_sed_vectorto, minimum_sed_vectorfrom


  !! initialize variables
  minimum_sed_vectorto = 1.e5
  minimum_sed_vectorfrom = 1.e5

  write(6,*) 'i_in = ', i_in
  write(6,*) 'j_in = ', j_in

  i = i_in + 1 ! add one to convert from python 0-based indexing conventions
  j = j_in + 1 ! add one to convert from python 0-based indexing conventions
  if ( landmask(j,i) ) then
     do ii = 1, im
        do jj = 1, jm
           if ( landmask(jj,ii) ) then                    
              call calc_dist(lons(i),lats(j),lons(ii),lats(jj), dist)
              if ( dist .le. maxdist ) then
                 !
                 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                 ! calculate closest future climate gridcell to a given historical climate gridcell
                 ! i.e. where is the climate going to?
                 call calc_sed_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_future(:,jj,ii), &
                      std_annual_cycle_historical(:,j,i), ntim, sed_vectorto)
                 sed_vectorto_array(jj,ii) = sed_vectorto
                 if ( sed_vectorto .lt. minimum_sed_vectorto ) then
                    closest_match_I_vectorto = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                    closest_match_J_vectorto = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                    minimum_sed_vectorto = sed_vectorto
                 endif
                 !
                 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                 ! calculate closest historical climate gridcell to a given future climate gridcell
                 ! i.e. where is the climate coming from?
                 call calc_sed_error(mean_annual_cycle_future(:,j,i), mean_annual_cycle_historical(:,jj,ii), &
                      std_annual_cycle_future(:,j,i), ntim, sed_vectorfrom)
                 sed_vectorfrom_array(jj,ii) = sed_vectorfrom
                 if ( sed_vectorfrom .lt. minimum_sed_vectorfrom ) then
                    closest_match_I_vectorfrom = ii - 1  ! subtract one to stick with python 0-based indexing conventions
                    closest_match_J_vectorfrom = jj - 1  ! subtract one to stick with python 0-based indexing conventions
                    minimum_sed_vectorfrom = sed_vectorfrom
                 endif
                 !
                 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                 ! calculate historical climate similarity
                 call calc_sed_error(mean_annual_cycle_historical(:,j,i), mean_annual_cycle_historical(:,jj,ii), &
                      std_annual_cycle_historical(:,j,i), ntim, sed_historicalclimate)
                 sed_historicalclimate_array(jj,ii) = sed_historicalclimate
                 !
              endif
           endif
        end do
     end do
   else
      write(6,*)  'error. point chosen is outside of masked area'
   endif


end subroutine get_climchange_vectors_onesite_sed
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


