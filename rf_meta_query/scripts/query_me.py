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

    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec)

    # Meta dir
    meta_dir = meta_io.meta_dir(frbc, create=True)

    # SDSS catalog
    sdss_cat = sdss.get_catalog(frbc['coord'])
    if len(sdss_cat) is not None:
        meta_io.write_table(sdss_cat, meta_dir, 'sdss_catalog', verbose=pargs.verbose)
    # In the database?
    if len(sdss_cat) is not None:  # This is a bit risky as a small radius might return None
        # SDSS cutout Image
        imsize = 30.  # arcsec
        sdss_url = sdss.get_url(frbc['coord'], imsize=imsize/60.)  # arcmin
        img = images.grab_from_url(sdss_url)
        # Prep plot
        plt = images.gen_snapshot_plt(img, imsize)
        # Write
        meta_io.save_plt(plt, meta_dir, 'sdss_snap', verbose=pargs.verbose)

        # SDSS DM
        close_obj = sdss_cat['separation'] < 1. # arcsec
        gdz = sdss_cat['z_error'][close_obj] > 0.
        if np.any(gdz):
            ibest = np.argmin(sdss_cat['z_error'][close_obj][gdz])
            frbc['z'] = sdss_cat['z'][close_obj][gdz][ibest]
            print("SDSS photo-z = {}".format(frbc['z']))
            # DM
            DM_best = dm.best_dm_from_z(frbc)
            print("DM_FRB = {} pc/cm^3".format(DM_best))

    # NVSS
    nvss_cat = radio.query_nvss(frbc)
    if nvss_cat is not None:
        print("The closest NVSS source has flux: {} mJy at separation {:0.2f} arcmin".format(nvss_cat[0]['FLUX_20_CM'],
                                                                            nvss_cat[0]['separation']))
        print("The brighest NVSS source in radius {} arcmin has flux: {} mJy".format(nvss_cat.meta['radius'],
                                                                         nvss_cat[0]['FLUX_20_CM']))



