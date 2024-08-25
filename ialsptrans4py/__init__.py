#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Météo France (2014-)
# This software is governed by the CeCILL-C license under French law.
# http://www.cecill.info
"""
ialsptrans4py:

Contains the interface to spectral transforms from the IAL/ecTrans.
Note that this is temporary between the former package arpifs4py and a direct python interface to ecTrans.
"""

from __future__ import print_function, absolute_import, unicode_literals, division

import os
import numpy as np
import ctypesForFortran
from ctypesForFortran import addReturnCode, treatReturnCode, IN, OUT


# Shared objects library
########################

#so_filename = "IALsptrans4py.so"  # local name in the directory
so_filename = "libtrans_dp.so"
potential_locations = [os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'),
                       os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib64')
                       "/home/common/epygram/public/EPyGrAM/libs4py",  # CNRM
                       "/home/gmap/mrpe/mary/public/EPyGrAM/libs4py",  # belenos/taranis
                       "/home/acrd/public/EPyGrAM/libs4py",  # ECMWF's Atos aa-ad
                       ]
for _libs4py_dir in potential_locations:
    shared_objects_library = os.path.join(_libs4py_dir, so_filename)
    if os.path.exists(shared_objects_library):
        break
    else:
        shared_objects_library = None
if shared_objects_library is None:
    raise FileNotFoundError("'{}' was not found in any of potential locations: {}".format(so_filename, potential_locations))
ctypesFF, handle = ctypesForFortran.ctypesForFortranFactory(shared_objects_library)

# Initialization
################

def init_env(omp_num_threads=None,
             no_mpi=False):
    """
    Set adequate environment for the inner libraries.

    :param int omp_num_threads: sets OMP_NUM_THREADS
    :param bool no_mpi: environment variable DR_HOOK_NOT_MPI set to 1
    """
    # because arpifs library is compiled with MPI & openMP
    if omp_num_threads is not None:
        os.environ['OMP_NUM_THREADS'] = str(omp_num_threads)
    if no_mpi:
        os.environ['DR_HOOK_NOT_MPI'] = '1'

# Transforms interfaces
#######################

@treatReturnCode
@ctypesFF()
@addReturnCode
def w_etrans_inq(KSIZEI, KSIZEJ,
                 KPHYSICALSIZEI, KPHYSICALSIZEJ,
                 KTRUNCX, KTRUNCY,
                 KNUMMAXRESOL,
                 PDELATX, PDELATY):
    """
    Simplified wrapper to ETRANS_INQ.

    Args:\n
    1,2) KSIZEI, KSIZEJ: size of grid-point field (with extension zone)
    3,4) KPHYSICALSIZEI, KPHYSICALSIZEJ: size of physical part of grid-point field
    5,6) KTRUNCX, KTRUNCY: troncatures
    7) KNUMMAXRESOL: maximum number of troncatures handled
    8,9) PDELTAX, PDELTAY: resolution along x,y axis

    Returns:\n
    1) KGPTOT: number of gridpoints
    2) KSPEC: number of spectral coefficients
    """
    return ([KSIZEI, KSIZEJ,
             KPHYSICALSIZEI, KPHYSICALSIZEJ,
             KTRUNCX, KTRUNCY,
             KNUMMAXRESOL,
             PDELATX, PDELATY],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.float64, None, IN),
             (np.float64, None, IN),
             (np.int64, None, OUT),
             (np.int64, None, OUT)],
            None)


@treatReturnCode
@ctypesFF()
@addReturnCode
def w_trans_inq(KSIZEJ, KTRUNC, KSLOEN, KLOEN, KNUMMAXRESOL):
    """
    Simplified wrapper to TRANS_INQ.

    Args:\n
    1) KSIZEJ: number of latitudes in grid-point space
    2) KTRUNC: troncature
    3) KSLOEN: Size of KLOEN
    4) KLOEN: number of points on each latitude row
    5) KNUMMAXRESOL: maximum number of troncatures handled

    Returns:\n
    1) KGPTOT: number of gridpoints
    2) KSPEC: number of spectral coefficients
    3) KNMENG: cut-off zonal wavenumber
    """
    return ([KSIZEJ, KTRUNC, KSLOEN, KLOEN, KNUMMAXRESOL],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, (KSLOEN,), IN),
             (np.int64, None, IN),
             (np.int64, None, OUT),
             (np.int64, None, OUT),
             (np.int64, (KSLOEN,), OUT)],
            None)


@treatReturnCode
@ctypesFF()
@addReturnCode
def w_spec2gpt_lam(KSIZEI, KSIZEJ,
                   KPHYSICALSIZEI, KPHYSICALSIZEJ,
                   KTRUNCX, KTRUNCY,
                   KNUMMAXRESOL,
                   KSIZE,
                   LGRADIENT,
                   LREORDER,
                   PDELTAX, PDELTAY,
                   PSPEC):
    """
    Transform spectral coefficients into grid-point values.

    Args:\n
    1,2) KSIZEI, KSIZEJ: size of grid-point field (with extension zone)
    3,4) KPHYSICALSIZEI, KPHYSICALSIZEJ: size of physical part of grid-point field
    5,6) KTRUNCX, KTRUNCY: troncatures
    7) KNUMMAXRESOL: maximum number of troncatures handled
    8) KSIZE: size of PSPEC
    9) LGRADIENT: gradient computation
    10) LREORDER: reorder spectral coefficients or not
    11,12) PDELTAX,PDELTAY: resolution along x,y axis
    13) PSPEC: spectral coefficient array

    Returns:\n
    1) PGPT: grid-point field
    2) PGPTM: N-S derivative if LGRADIENT
    3) PGPTL: E-W derivative if LGRADIENT
    """
    return ([KSIZEI, KSIZEJ,
             KPHYSICALSIZEI, KPHYSICALSIZEJ,
             KTRUNCX, KTRUNCY,
             KNUMMAXRESOL,
             KSIZE,
             LGRADIENT,
             LREORDER,
             PDELTAX, PDELTAY,
             PSPEC],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (bool, None, IN),
             (bool, None, IN),
             (np.float64, None, IN),
             (np.float64, None, IN),
             (np.float64, (KSIZE,), IN),
             (np.float64, (KSIZEI * KSIZEJ,), OUT),
             (np.float64, (KSIZEI * KSIZEJ,), OUT),
             (np.float64, (KSIZEI * KSIZEJ,), OUT)],
            None)


@treatReturnCode
@ctypesFF()
@addReturnCode
def w_gpt2spec_lam(KSIZE,
                   KSIZEI, KSIZEJ,
                   KPHYSICALSIZEI, KPHYSICALSIZEJ,
                   KTRUNCX, KTRUNCY,
                   KNUMMAXRESOL,
                   PDELTAX, PDELTAY,
                   LREORDER,
                   PGPT):
    """
    Transform grid point values into spectral coefficients.

    Args:\n
    1) KSIZE: size of spectral field
    2,3) KSIZEI, KSIZEJ: size of grid-point field (with extension zone)
    4,5) KPHYSICALSIZEI, KPHYSICALSIZEJ: size of physical part of grid-point field
    6,7) KTRUNCX, KTRUNCY: troncatures
    8) KNUMMAXRESOL: maximum number of troncatures handled
    9,10) PDELTAX, PDELTAY: resolution along x,y axis
    11) LREORDER: reorder spectral coefficients or not
    12) PGPT: grid-point field

    Returns:\n
    1) PSPEC: spectral coefficient array
    """
    return ([KSIZE,
             KSIZEI, KSIZEJ,
             KPHYSICALSIZEI, KPHYSICALSIZEJ,
             KTRUNCX, KTRUNCY,
             KNUMMAXRESOL,
             PDELTAX, PDELTAY,
             LREORDER,
             PGPT],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.float64, None, IN),
             (np.float64, None, IN),
             (bool, None, IN),
             (np.float64, (KSIZEI * KSIZEJ,), IN),
             (np.float64, (KSIZE,), OUT)],
            None)


@treatReturnCode
@ctypesFF()
@addReturnCode
def w_spec2gpt_gauss(KSIZEJ,
                     KTRUNC,
                     KNUMMAXRESOL,
                     KGPTOT,
                     KSLOEN,
                     KLOEN,
                     KSIZE,
                     LGRADIENT,
                     LREORDER,
                     PSPEC):
    """
    Transform spectral coefficients into grid-point values.

    Args:\n
    1) KSIZEJ: Number of latitudes
    2) KTRUNC: troncature
    3) KNUMMAXRESOL: maximum number of troncatures handled
    4) KGPTOT: number of grid-points
    5) KSLOEN: Size of KLOEN
    6) KLOEN:
    7) KSIZE: Size of PSPEC
    8) LGRADIENT: compute derivatives
    9) LREORDER: reorder spectral coefficients or not
    10) PSPEC: spectral coefficient array

    Returns:\n
    1) PGPT: grid-point field
    2) PGPTM: N-S derivative if LGRADIENT
    3) PGPTL: E-W derivative if LGRADIENT
    """
    return ([KSIZEJ,
             KTRUNC,
             KNUMMAXRESOL,
             KGPTOT,
             KSLOEN,
             KLOEN,
             KSIZE,
             LGRADIENT,
             LREORDER,
             PSPEC],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, (KSLOEN,), IN),
             (np.int64, None, IN),
             (bool, None, IN),
             (bool, None, IN),
             (np.float64, (KSIZE,), IN),
             (np.float64, (KGPTOT,), OUT),
             (np.float64, (KGPTOT,), OUT),
             (np.float64, (KGPTOT,), OUT)],
            None)


@treatReturnCode
@ctypesFF()
@addReturnCode
def w_gpt2spec_gauss(KSPEC,
                     KSIZEJ,
                     KTRUNC,
                     KNUMMAXRESOL,
                     KSLOEN,
                     KLOEN,
                     KSIZE,
                     LREORDER,
                     PGPT):
    """
    Transform grid-point values into spectral coefficients.

    Args:\n
    1) KSPEC: size of spectral coefficients array
    2) KSIZEJ: Number of latitudes
    3) KTRUNC: troncature
    4) KNUMMAXRESOL: maximum number of troncatures handled
    5) KSLOEN: Size of KLOEN
    6) KLOEN
    7) KSIZE: Size of PGPT
    8) LREORDER: reorder spectral coefficients or not
    9) PGPT: grid-point field

    Returns:\n
    1) PSPEC: spectral coefficient array
    """
    return ([KSPEC,
             KSIZEJ,
             KTRUNC,
             KNUMMAXRESOL,
             KSLOEN,
             KLOEN,
             KSIZE,
             LREORDER,
             PGPT],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, None, IN),
             (np.int64, (KSLOEN,), IN),
             (np.int64, None, IN),
             (bool, None, IN),
             (np.float64, (KSIZE,), IN),
             (np.float64, (KSPEC,), OUT)],
            None)


@ctypesFF()
def w_spec2gpt_fft1d(KSIZES, KTRUNC, PSPEC, KSIZEG):
    """
    Transform spectral coefficients into grid-point values,
    for a 1D array (vertical section academic model)

    Args:\n
    1) KSIZES size of PSPEC
    2) KTRUNC: troncature
    3) PSPEC: spectral coefficient array
    4) KSIZEG: size of grid-point field (with extension zone)

    Returns:\n
    1) PGPT: grid-point field
    """
    return ([KSIZES, KTRUNC, PSPEC, KSIZEG],
            [(np.int64, None, IN),
             (np.int64, None, IN),
             (np.float64, (KSIZES,), IN),
             (np.int64, None, IN),
             (np.float64, (KSIZEG,), OUT)],
            None)
