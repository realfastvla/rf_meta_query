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

    from frb.surveys import survey_utils

    from rf_meta_query import frb_cand
    from rf_meta_query import meta_io
    from rf_meta_query import dm
    from rf_meta_query import survey_defs
    from rf_meta_query import catalog_utils

    # ADD HERE
    survey_names = ['SDSS', 'NVSS', 'FIRST', 'DES', 'DECaL']

    # FRB Candidate object
    ra, dec = pargs.radec.split(',')
    frbc = frb_cand.build_frb_cand(ra, dec, 11111)

    # Load surveys
    surveys = {}
    for survey_name in survey_names:
        radius = survey_defs.realfast_params[survey_name]['radius']
        surveys[survey_name] = survey_utils.load_survey_by_name(survey_name, frbc['coord'], radius)

    summary_list = ['----------------------------------------------------------------']
    summary_list += ['FRB Candidate ID-{:d} towards {:s}'.format(frbc['id'], frb_cand.jname(frbc))]

    # Meta dir
    meta_dir = meta_io.meta_dir(frbc, create=pargs.write_meta)

    # Load catalog and generate simple summary
    for survey_name in surveys.keys():
        # Generate catalog (as possible)
        survey = surveys[survey_name]
        _ = survey.get_catalog()
        # Summarize
        summary_list += catalog_utils.summarize_catalog(
            frbc, survey.catalog,
            survey_defs.realfast_params[survey_name]['summary_radius'],
            survey_defs.realfast_params[survey_name]['phot_clm'],
            survey_defs.realfast_params[survey_name]['phot_mag'])
        # Write catalog?
        if pargs.write_meta and (len(survey.catalog) > 0):
            survey.write_catalog(out_dir=meta_dir)

    # DM? -- SDSS only for now
    if 'SDSS' in surveys.keys():
        survey = surveys['SDSS']
        if len(survey.catalog) > 0:
            # Closest within 5" ?
            if survey.catalog['separation'][0] < (5./60):
                # Valid value?
                if survey.catalog['photo_z'][0] > -9000.:
                    frbc['z'] = survey.catalog['photo_z'][0]
                    DM = dm.best_dm_from_z(frbc)
                    summary_list += ['DM:  Using the photo_z of the closest galaxy within 5", DM={:0.1f}'.format(DM)]

    # Cut-out
    cutout_order = ['DES', 'SDSS']
    if pargs.write_meta:
        for corder in cutout_order:  # Loop until we generate one
            survey = surveys[corder]
            # Query if the catalog exists.  If empty, assume a cut-out cannot be made
            if len(survey.catalog) == 0:
                continue
            # Generate
            _ = survey.get_cutout(survey_defs.realfast_params[corder]['cutout_size'])
            # Write
            survey.write_cutout(output_dir=meta_dir)
            break



    # Finish by writing the FRB candidate object too
    if pargs.write_meta:
        meta_io.write_frbc(frbc, meta_dir)

    # Print me
    summary_list += ['----------------------------------------------------------------']
    for item in summary_list:
        print(item)
