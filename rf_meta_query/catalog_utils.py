""" Methods related to fussing with a catalog"""
import numpy as np
import pdb

from astropy.coordinates import SkyCoord


def sort_by_separation(catalog, coord, radec=('ra','dec'), add_sep=True):

    # Check
    for key in radec:
        if key not in catalog.keys():
            print("RA/DEC key: {:s} not in your Table".format(key))
            raise IOError("Try again..")
    # Grab coords
    cat_coords = SkyCoord(ra=catalog[radec[0]].data,
                          dec=catalog[radec[1]].data, unit='deg')

    # Separations
    seps = coord.separation(cat_coords)
    isrt = np.argsort(seps)
    # Add?
    if add_sep:
        catalog['separation'] = seps.to('arcmin').value
    # Sort
    srt_catalog = catalog[isrt]
    # Return
    return srt_catalog

