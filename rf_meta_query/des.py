"""
To download DES images for a given region
"""

import numpy as np
from astropy.coordinates import SkyCoord
from pyvo.dal import sia
from astropy import units, io, utils
import pdb

_DEF_ACCESS_URL = "https://datalab.noao.edu/sia/des_dr1"
_svc = sia.SIAService(_DEF_ACCESS_URL)


# The following function is copied directly from 
# https://datalab.noao.edu/desdr1/analysis/DwarfGalaxyDESDR1_20171101.html
# a little function to download the deepest stacked images
# adapted from R. Nikutta

#Minor modifications to io made by Sunil Simha
def download_deepest_image(coord,fov=0.1*units.deg,band='g',timeout=120):
    """
    Download image given coordinates,fov and
    photometric band
    Parameters
    ----------
    coord: astropy SkyCoord
        Coordinates of target
    fov: astropy Quantity (angular), optional
        Default value is 0.1 degrees
    band: str, optional
        DES photometric band names.
        "g","r","i","z" and "Y" are the only
        allowed values. 
    timeout: float, optional
        Image download timeout in seconds.
        Default value: 120s.
    """
    ra = coord.ra.value
    dec = coord.dec.value
    fov = fov.to(units.deg).value

    if band not in ["g","r","i","z","Y","G","R","I","Z","y"]:
        raise TypeError("Allowed values for DES photometric bands are 'g','r','i','z','Y'")

    imgTable = _svc.search((ra,dec), (fov/np.cos(dec*np.pi/180), fov), verbosity=2).to_table()
    print("The full image list contains", len(imgTable), "entries")
    
    sel0 = imgTable['obs_bandpass'].astype(str)==band
    sel = sel0 & ((imgTable['proctype'].astype(str)=='Stack') & (imgTable['prodtype'].astype(str)=='image')) # basic selection
    Table = imgTable[sel] # select
    if (len(Table)>0):
        row = Table[np.argmax(Table['exptime'].data.data.astype('float'))] # pick image with longest exposure time
        url = row['access_url'].decode() # get the download URL
        print ('downloading deepest stacked image...')
        
        #Slightly different. Instead of just getting the image, you now also have metadata.
        image = io.fits.open(utils.data.download_file(url,cache=True,show_progress=False,timeout=timeout))

    else:
        print ('No image available.')
        image=None
    
    return image[0]