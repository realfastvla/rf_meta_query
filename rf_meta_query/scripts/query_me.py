#!/usr/bin/env python
"""
Check a DB file from specdb
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)

import pdb

try:  # Python 3
    ustr = unicode
except NameError:
    ustr = str

def parser(options=None):
    import argparse
    # Parse
    parser = argparse.ArgumentParser(description='Run the query for meta data on a given FRB candidate [v1.1]')
    parser.add_argument("radec", type=str, help="Comma-separated RA,DEC in deg (ICRS, J2000).  e.g. 232.23141,23.2237")
    #parser.add_argument("-v", "--version", default='v01', help="DB version to generate")
    #parser.add_argument("-llist", default='ISM', action='store_rue', help="Name of LineList:  ISM, HI, H2, CO, etc.")

    if options is None:
        pargs = parser.parse_args()
    else:
        pargs = parser.parse_args(options)
    return pargs


def main(pargs):
    """ Run
    Parameters
    ----------
    pargs

    Returns
    -------

    """
    import warnings
    from astropy.coordinates import SkyCoord
    from rf_meta_query import frb_cand
    from rf_meta_query import sdss
    from rf_meta_query import io as rfmq_io

    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec)

    # Meta dir
    meta_dir = rfmq_io.meta_dir(frbc)

    # SDSS
    phot_tbl = sdss.get_photom(frbc['coord'])
    rfmq_io.write_table(phot_tbl, meta_dir, 'sdss')


