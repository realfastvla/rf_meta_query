""" Methods related to SDSS/BOSS queries """

import numpy as np

from astropy import units
from astropy.coordinates import SkyCoord

from astroquery.sdss import SDSS


def get_photom(coord, radius=0.5*units.arcmin, timeout=30.):
    """

    Args:
        coord: SkyCoord
        radius: Angle (or Quantity), optional
          search radius for sources
        timeout: float, optional

    Returns:
        phot_catalog: Table

    """

    # Meta data of interest
    photoobj_fs = ['ra', 'dec', 'objid', 'run', 'rerun', 'camcol', 'field']
    mags = ['petroMag_u', 'petroMag_g', 'petroMag_r', 'petroMag_i', 'petroMag_z']
    magsErr = ['petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z']

    # Call
    phot_catalog = SDSS.query_region(coord, radius=radius, timeout=timeout,
                                     photoobj_fields=photoobj_fs + mags + magsErr)

    # Sort by offset
    phot_coords = SkyCoord(ra=phot_catalog['ra'], dec=phot_catalog['dec'], unit='deg')
    seps = coord.separation(phot_coords)
    isrt = np.argsort(seps)
    phot_catalog = phot_catalog[isrt]

    # Remove duplicates?

    # Return
    return phot_catalog

def get_url(coord, imsize, scale=0.39612, grid=None, label=None, invert=None):
    """
    Generate the SDSS URL for an image retrieval

    Parameters:
    ----------
    coord : SkyCoord
      astropy.coordiantes.SkyCoord object
      Typically held in frb_cand['coord']
    imsize: float
      Image size (rectangular) in arcmin and without units
    """

    # Pixels
    npix = round(imsize*60./scale)
    xs = npix
    ys = npix
    #from StringIO import StringIO

    # Generate the http call
    name1='http://skyservice.pha.jhu.edu/DR12/ImgCutout/'
    name='getjpeg.aspx?ra='

    name+=str(coord.ra.value) 	#setting the ra (deg)
    name+='&dec='
    name+=str(coord.dec.value)	#setting the declination
    name+='&scale='
    name+=str(scale) #setting the scale
    name+='&width='
    name+=str(int(xs))	#setting the width
    name+='&height='
    name+=str(int(ys)) 	#setting the height

    #------ Options
    options = ''
    if grid != None:
        options+='G'
    if label != None:
        options+='L'
    if invert != None:
        options+='I'
    if len(options) > 0:
        name+='&opt='+options

    name+='&query='

    url = name1+name
    return url
