#!/usr/bin/env python
"""
Check a DB file from specdb
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

    from rf_meta_query import frb_cand
    from rf_meta_query import sdss
    from rf_meta_query import io as rfmq_io
    from rf_meta_query import images

    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec)

    # Meta dir
    meta_dir = rfmq_io.meta_dir(frbc, create=True)

    # SDSS
    phot_tbl = sdss.get_photom(frbc['coord'])
    rfmq_io.write_table(phot_tbl, meta_dir, 'sdss_phot', verbose=pargs.verbose)
    # SDSS Image
    if len(phot_tbl) is not None:  # This is a bit risky as a small radius might return None
        imsize = 30. # arcsec
        sdss_url = sdss.get_url(frbc['coord'], imsize=imsize/60.)  # arcmin
        img = images.grab_from_url(sdss_url)
        # Prep plot
        plt = images.gen_snapshot_plt(img, imsize)
        # Write
        rfmq_io.save_plt(plt, meta_dir, 'sdss_snap', verbose=pargs.verbose)



