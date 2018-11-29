""" Modules related to radio catalogs, etc."""

from astropy import units

from astroquery.heasarc import Heasarc

from rf_meta_query import catalog_utils

def query_nvss(frbc, radius=1*units.arcmin):
    # Instantiate
    heasarc = Heasarc()
    # Query
    try:
        nvss_catalog = heasarc.query_region(frbc['coord'], mission='nvss', radius=radius)
    except ValueError:  # No table found
        nvss_catalog = None
    else:
        # Sort by coord
        nvss_catalog = catalog_utils.sort_by_separation(nvss_catalog, frbc['coord'], radec=("RA","DEC"))
        # Meta
        nvss_catalog.meta['radius'] = radius.to('arcmin').value

    # Return
    return nvss_catalog