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
    parser.add_argument("-v", "--verbose", default=False, help="Verbose output?", action='store_true')
    #parser.add_argument("-llist", default='ISM', action='store_true', help="Name of LineList:  ISM, HI, H2, CO, etc.")

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
    import numpy as np

    from rf_meta_query import frb_cand
    from rf_meta_query import sdss
    from rf_meta_query import meta_io
    from rf_meta_query import images
    from rf_meta_query import dm
    from rf_meta_query import radio

    summary_list = []

    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec)

    # Meta dir
    meta_dir = meta_io.meta_dir(frbc, create=True)

    # SDSS
    sdss_cat, sdss_summary = sdss.query(frbc, meta_dir=meta_dir)
    summary_list += sdss_summary
    for item in summary_list:
        print(item)


    # NVSS
    nvss_cat = radio.query_nvss(frbc)
    if nvss_cat is not None:
        print("The closest NVSS source has flux: {} mJy at separation {:0.2f} arcmin".format(nvss_cat[0]['FLUX_20_CM'],
                                                                            nvss_cat[0]['separation']))
        print("The brighest NVSS source in radius {} arcmin has flux: {} mJy".format(nvss_cat.meta['radius'],
                                                                         nvss_cat[0]['FLUX_20_CM']))
        # Write to disk
        meta_io.write_table(nvss_cat, meta_dir, 'nvss_catalog', verbose=pargs.verbose)
    else:
        print("There are no NVSS sources within the search radius")

    # Finish by writing the FRB candidate object too
    meta_io.write_frbc(frbc, meta_dir)

