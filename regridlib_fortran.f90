!! this is a fortran module for regridding using fortran to make things faster than native python
!!  f2py -m regridlib_fortran -c regridlib_fortran.f90
!
! written by C. Koven 2014/06/07
!


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
subroutine integer_regrid_3d_r8(data_in, landmask_in, regrid_factor, im_o, jm_o, &
     ntim, jm_i, im_i, data_out, landmask_out)
  !
  !  regrid using a constant integer factor for the regridding.  
  !  assumes input and output data is numpy type float32
  !
  !! input arguments
  real, intent(in) :: data_in(ntim, jm_i, im_i)
  logical, intent(in) :: landmask_in(jm_i, im_i)
  integer, intent(in) :: regrid_factor, ntim, jm_i, im_i
  integer, intent(in) :: jm_o, im_o
  !
  !!! output arguments
  real, intent(out) :: data_out(ntim, jm_o, im_o)
  logical, intent(out) :: landmask_out(jm_o, im_o)
  !
  !!! local variables
  integer :: i, j, ii, jj, iii, jjj
  real :: tempsum(ntim), ngood
  real :: zero = 0.
  real :: one = 1.
  real :: eps = 0.1
  !
  !!! begin code here
  !
  do i = 1, im_o
     do j = 1, jm_o
        tempsum(:) = zero
        ngood = zero
        do ii = 1, regrid_factor
           do jj = 1, regrid_factor
              iii = (i-1) * regrid_factor + ii
              jjj = (j-1) * regrid_factor + jj
              if ( landmask_in(jjj,iii) ) then
                 tempsum(:) = tempsum(:) + data_in(:,jjj,iii)
                 ngood = ngood + one
              endif
           end do
        end do
        if ( ngood > eps) then
           data_out(:,j,i) = tempsum(:) / ngood
           landmask_out(j,i) = .true.
        else
           landmask_out(j,i) = .false.
        endif
     end do
  end do
  !
end subroutine integer_regrid_3d_r8
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

