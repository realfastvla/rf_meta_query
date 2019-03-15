#!/usr/bin/env python
"""
Perform the meta query on an input coordinate
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)

import pdb


def parser(options=None):
    import argparse
    # Parse
    parser = argparse.ArgumentParser(description='Run the query for meta data on a given FRB candidate [v1.1]')
    parser.add_argument("radec", type=str, help="Comma-separated RA,DEC in deg (ICRS, J2000).  e.g. 232.23141,23.2237")
    parser.add_argument("-w", "--write_meta", default=False, help="Write Meta to folder?", action='store_true')
    parser.add_argument("-v", "--verbose", default=False, help="Verbose output?", action='store_true')

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
    from astropy import units

    from rf_meta_query import frb_cand
    from rf_meta_query import sdss, des
    from rf_meta_query import meta_io
    from rf_meta_query import images
    from rf_meta_query import dm
    from rf_meta_query import radio


    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec, 11111)

    summary_list = ['----------------------------------------------------------------']
    summary_list += ['FRB Candidate ID-{:d} towards {:s}'.format(frbc['id'], frb_cand.jname(frbc))]

    # Meta dir
    meta_dir = meta_io.meta_dir(frbc, create=pargs.write_meta)

    # SDSS
    sdss_cat, sdss_summary = sdss.query(frbc, meta_dir=meta_dir, write_meta=pargs.write_meta)
    summary_list += sdss_summary

    # FIRST
    first_cat, first_summary = radio.query_first(frbc, write_meta=pargs.write_meta)
    summary_list += first_summary

    # NVSS
    nvss_cat, nvss_summary = radio.query_nvss(frbc, write_meta=pargs.write_meta)
    summary_list += nvss_summary

    # DES
    des_cat, des_summary = des.query(frbc, meta_dir=meta_dir, write_meta=pargs.write_meta)
    summary_list += des_summary

    # Finish by writing the FRB candidate object too
    if pargs.write_meta:
        meta_io.write_frbc(frbc, meta_dir)

    # Print me
    summary_list += ['----------------------------------------------------------------']
    for item in summary_list:
        print(item)
