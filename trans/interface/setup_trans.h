SUBROUTINE SETUP_TRANS(KSMAX,KDGL,KLOEN,LDSPLIT,KAPSETS,KTMAX,KRESOL)

!**** *SETUP_TRANS* - Setup transform package for specific resolution

!     Purpose.
!     --------
!     To setup for making spectral transforms. Each call to this routine
!     creates a new resolution up to a maximum of NMAX_RESOL set up in
!     SETUP_TRANS0. You need to call SETUP_TRANS0 before this routine can
!     be called.

!**   Interface.
!     ----------
!     CALL SETUP_TRANS(...)

!     Explicit arguments : KLOEN,LDSPLIT,KAPSETS are optional arguments
!     -------------------- 
!     KSMAX - spectral truncation required
!     KDGL  - number of Gaussian latitudes
!     KLOEN(:) - number of points on each Gaussian latitude [2*KDGL]
!     LDSPLIT - true if split latitudes in grid-point space [false]
!     KAPSETS - Number of apple sets in the distribution [0]
!     KTMAX - truncation order for tendencies?
!     KRESOL - the resolution identifier

!     KSMAX,KDGL,KTMAX and KLOEN are GLOBAL variables desribing the resolution
!     in spectral and grid-point space

!     LDSPLIT and KAPSETS describe the distribution among processors of
!     grid-point data and has no relevance if you are using a single processor
 
!     Method.
!     -------

!     Externals.  SET_RESOL   - set resolution
!     ----------  SETUP_DIMS  - setup distribution independent dimensions
!                 SUMP_TRANS_PRELEG - first part of setup of distr. environment
!                 SULEG - Compute Legandre polonomial and Gaussian 
!                         Latitudes and Weights
!                 SETUP_GEOM - Compute arrays related to grid-point geometry
!                 SUMP_TRANS - Second part of setup of distributed environment
!                 SUFFT - setup for FFT

!     Author.
!     -------
!        Mats Hamrud *ECMWF*

!     Modifications.
!     --------------
!        Original : 00-03-03

!     ------------------------------------------------------------------

#include "tsmbkind.h"


IMPLICIT NONE

! Dummy arguments

INTEGER_M ,INTENT(IN) :: KSMAX,KDGL
INTEGER_M ,OPTIONAL,INTENT(IN) :: KLOEN(:)
LOGICAL   ,OPTIONAL,INTENT(IN) :: LDSPLIT
INTEGER_M ,OPTIONAL,INTENT(IN) :: KAPSETS
INTEGER_M ,OPTIONAL,INTENT(IN) :: KTMAX
INTEGER_M ,OPTIONAL,INTENT(OUT):: KRESOL


END SUBROUTINE SETUP_TRANS


