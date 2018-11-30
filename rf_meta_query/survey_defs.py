""" utils related to SurveyCoord objects"""

from astropy import units

# Dict of em
realfast_params = {}
realfast_params['SDSS'] = dict(radius=30*units.arcsec,
                               summary_radius=5*units.arcsec,
                               cutout_size=30*units.arcsec,
                               phot_clm='petroMag_r',
                               phot_mag=True)
realfast_params['DES'] = dict(radius=30*units.arcsec,
                               summary_radius=5*units.arcsec,
                               cutout_size=30*units.arcsec,
                               phot_clm='mag_auto_r',
                               phot_mag=True)
realfast_params['NVSS'] = dict(radius=1*units.arcmin,
                              summary_radius=30*units.arcsec,
                              cutout_size=None,
                              phot_clm='FLUX_20_CM',
                              phot_mag=False)
