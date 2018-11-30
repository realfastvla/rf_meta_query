""" utils related to SurveyCoord objects"""

from astropy import units

# Dict of em
realfast_params = {}
realfast_params['SDSS'] = dict(radius=30*units.arcsec,
                               summary_radius=5*units.arcsec,
                               cutout_size=30*units.arcsec,
                               phot_clm='petroMag_r',
                               phot_mag=True)

