""" Methods related to fussing with a catalog"""
import numpy as np
import pdb

from astropy.coordinates import SkyCoord
from astropy import units

from astroquery.heasarc import Heasarc

# Instantiate
heasarc = Heasarc()

def clean_heasarc(catalog):
    # RA/DEC
    catalog.rename_column("RA", "ra")
    catalog.rename_column("DEC", "dec")
    for key in ['ra', 'dec']:
        catalog[key].unit = units.deg

def query_hearsarc(frbc, mission, radius):
    """
    Use astroquery to query the HEARSARC database

    Args:
        frbc:
        mission: str
          Uses HEASARC notation
        radius: Angle

    Returns:

    """
    try:
        catalog = heasarc.query_region(frbc['coord'], mission=mission, radius=radius)
    except (ValueError, TypeError):  # No table found
        catalog = None
    else:
        catalog.meta['radius'] = radius
    return catalog


def summarize_catalog(frbc, catalog, summary_radius, photom_column, magnitude):
    """
    Generate simple text describing the sources from
    an input catalog within a given radius

    Args:
        frbc: FRB Candidate object
        catalog: astropy.table.Table
        summary_radius: Angle
        photom_column: str
          Column specifying which flux to work on
        magnitude: bool
          Is the flux a magnitude?

    Returns:
        summary_list: list
          List of comments on the catalog

    """
    # Init
    summary_list = []
    coords = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], unit='deg')
    # Find all within the summary radius
    seps = frbc['coord'].separation(coords)
    in_radius = seps < summary_radius
    # Start summarizing
    summary_list += ['{:s}: There are {:d} source(s) within {:0.1f} arcsec'.format(
        catalog.meta['survey'], np.sum(in_radius), summary_radius.to('arcsec').value)]
    # If any found
    if np.any(in_radius):
        # Brightest
        if magnitude:
            brightest = np.argmin(catalog[photom_column][in_radius])
        else:
            brightest = np.argmax(catalog[photom_column][in_radius])
        summary_list += ['{:s}: The brightest source has {:s} of {:0.2f}'.format(
            catalog.meta['survey'], photom_column,
            catalog[photom_column][in_radius][brightest])]
        # Closest
        closest = np.argmin(seps[in_radius])
        summary_list += ['{:s}: The closest source is at separation {:0.2f} arcsec and has {:s} of {:0.2f}'.format(
            catalog.meta['survey'],
            seps[in_radius][closest].to('arcsec').value,
            photom_column, catalog[photom_column][in_radius][brightest])]
    # Return
    return summary_list


