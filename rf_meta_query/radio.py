""" Modules related to radio catalogs, etc."""
import pdb

from astropy import units


from rf_meta_query import catalog_utils
from rf_meta_query import meta_io


def query_first(frbc, radius=1*units.arcmin, write_meta=False, verbose=False,
                meta_dir=None):
    survey = 'FIRST'
    summary_list = []

    # Meta dir
    if meta_dir is None:
        meta_dir = meta_io.meta_dir(frbc)

    # Query
    first_catalog = catalog_utils.query_hearsarc(frbc, 'first', radius)
    if first_catalog is None:
        summary_list += ["{}: There are no sources found within {}"
                         .format(survey, radius)]
        return first_catalog, summary_list

    # Meta -- FIRST specific
    first_catalog.meta['survey'] = 'FIRST'
    first_catalog.meta['radius'] = radius.to('arcmin').value
    # Clean
    catalog_utils.clean_heasarc(first_catalog)
    for key in ['FLUX_20_CM', 'FLUX_20_CM_ERROR', 'INT_FLUX_20_CM']:
        first_catalog[key].unit = units.mJy

    first_catalog.meta['phot_clm'] = 'FLUX_20_CM'
    first_catalog.meta['phot_mag'] = False

    # Summarize
    first_summary = catalog_utils.summarize_catalog(frbc, first_catalog,
                                                    1*units.arcmin)
    summary_list += [first_summary]

    # Sort by coord
    first_catalog = catalog_utils.sort_by_separation(first_catalog,
                                                     frbc['coord'],
                                                     radec=('ra', 'dec'))

    # Write?
    if write_meta:
        meta_io.write_catalog(first_catalog, meta_dir, verbose=verbose)

    # Return
    return first_catalog, first_summary


def query_nvss(frbc, radius=1*units.arcmin, write_meta=False, verbose=False,
               meta_dir=None):
    survey = 'NVSS'
    summary_list = []

    # Meta dir
    if meta_dir is None:
        meta_dir = meta_io.meta_dir(frbc)

    # Query
    nvss_catalog = catalog_utils.query_hearsarc(frbc, 'nvss', radius)
    if nvss_catalog is None:
        summary_list += ["{}: There are no sources found within {}"
                         .format(survey, radius)]
        return nvss_catalog, summary_list

    # Meta + Massage -- NVSS specific
    nvss_catalog.meta['survey'] = 'NVSS'
    nvss_catalog.meta['radius'] = radius.to('arcmin').value
    nvss_catalog.rename_column("RA", "ra")
    nvss_catalog.rename_column("DEC", "dec")
    for key in ['ra', 'dec']:
        nvss_catalog[key].unit = units.deg
    nvss_catalog['FLUX_20_CM'].unit = units.mJy
    nvss_catalog['FLUX_20_CM_ERROR'].unit = units.mJy

    nvss_catalog.meta['photom_column'] = 'FLUX_20_CM'
    nvss_catalog.meta['photom_mag'] = False

    # Summarize
    nvss_summary = catalog_utils.summarize_catalog(frbc, nvss_catalog,
                                                   1*units.arcmin)
    summary_list += [nvss_summary]

    # Sort by coord
    nvss_catalog = catalog_utils.sort_by_separation(nvss_catalog,
                                                    frbc['coord'],
                                                    radec=('ra', 'dec'))

    # Write?
    if write_meta:
        meta_io.write_catalog(nvss_catalog, meta_dir, verbose=verbose)

    # Return
    return nvss_catalog, nvss_summary
