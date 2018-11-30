""" utils related to SurveyCoord objects"""

from astropy import units

from rf_meta_query.sdss import SDSS_Survey


def load_survey_by_name(name, coord, radius, **kwargs):
    allowed_surveys = ['SDSS']

    if name not in allowed_surveys:
        raise IOError("Not ready for input survey.\n These are allowed: {}".format(allowed_surveys))

    # Do it
    if name == 'SDSS':
        survey = SDSS_Survey(coord, radius, **kwargs)

    # Return
    return survey

# Dict of em
realfast_params = {}
realfast_params['SDSS'] = dict(radius=30*units.arcsec,
                               summary_radius=5*units.arcsec,
                               phot_clm='petroMag_r',
                               phot_mag=True)

