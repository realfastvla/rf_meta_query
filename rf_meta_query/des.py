"""
To download DES images for a given region

The function `download_deepest_image has been
taken from https://datalab.noao.edu/desdr1/analysis/DwarfGalaxyDESDR1_20171101.html#resources
(credits to Knut Olsen, Robert Nikutta, Stephanie Juneau & NOAO Data Lab Team)
and modified slightly (by Sunil Simha).
"""

from __future__ import print_function
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Table
from pyvo.dal import sia
from astropy import units, io, utils
from dl import queryClient as qc, authClient as ac, helpers


token = ac.login('anonymous')

_DEF_ACCESS_URL = "https://datalab.noao.edu/sia/des_dr1"
_svc = sia.SIAService(_DEF_ACCESS_URL)


def download_deepest_image(coord,fov=0.1*units.deg,band='g',timeout=120,verbose=False):
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
        allowed latters (case-insensitive).
    timeout: float, optional
        Image download timeout in seconds.
        Default value: 120s.
    Returns
    -------
    image: fits.PrimaryHDU
        A HDU object that contains
        image data and header.
    """
    ra = coord.ra.value
    dec = coord.dec.value
    fov = fov.to(units.deg).value

    if band not in ["g","r","i","z","Y","G","R","I","Z","y"]:
        raise TypeError("Allowed letters (case-insensitive) for DES photometric bands are 'g','r','i','z','Y'")

    imgTable = _svc.search((ra,dec), (fov/np.cos(dec*np.pi/180), fov), verbosity=2).to_table()
    if verbose:
        print("The full image list contains", len(imgTable), "entries")
    
    sel0 = imgTable['obs_bandpass'].astype(str)==band
    sel = sel0 & ((imgTable['proctype'].astype(str)=='Stack') & (imgTable['prodtype'].astype(str)=='image')) # basic selection
    Table = imgTable[sel] # select
    if (len(Table)>0):
        row = Table[np.argmax(Table['exptime'].data.data.astype('float'))] # pick image with longest exposure time
        url = row['access_url'].decode() # get the download URL
        if verbose:
            print ('downloading deepest stacked image...')
        
        #Slightly different. Instead of just getting the image, you now also have metadata.
        image = io.fits.open(utils.data.download_file(url,cache=True,show_progress=False,timeout=timeout))

    else:
        print ('No image available.')
        image=None
    
    return image[0]

def get_catalog(coord,radius=1*units.arcmin, query_fields=None,
                print_query=False,qc_profile='default'):
    """
    Get DES catalog sources around the given coordinates
    within a radius.
    Parameters
    ----------
    coord: astropy SkyCoord
        Central coordinates
    radius: astropy Quantity (Angle)
        Search radius
    query_fields: list, optional
        List of strings 
    print_query: bool, optional
        Prints search query if True.
    qc_profile: str, optional
        dl query client profile. Kinda
        chooses which database to lookup.

    Returns
    -------
    cat: astropy Table
        Table of objects obtained from the 
        SQL query.
    """
    qc.set_profile(qc_profile)
    query = "SELECT "

    if query_fields is None:
        bands = ["g","r","i","z","y"]
        object_id_fields = ['coadd_object_id', 'ra','dec','tilename']
        mag_fields = ['mag_auto_{:s}'.format(band) for band in bands]
        mag_err_fields = ['magerr_auto_{:s}'.format(band) for band in bands]
        query_fields = object_id_fields+mag_fields+mag_err_fields
    
    for field in query_fields:
        query += "{:s},".format(field)
    query = query[:-1] #remove the last comma
    query += "\nFROM des_dr1.main"
    query += "\nWHERE q3c_radial_query(ra,dec,{:f},{:f},{:f})".format(coord.ra.value,coord.dec.value,radius.to(units.deg).value)

    if print_query:
        print(query)
    
    result = qc.query(token,sql=query)
    cat = helpers.convert(result)
    # TODO:: Suppress the print output from convert
    # TODO:: Dig into why the heck it doesn't want to natively
    #        output to a table when it was clearly intended to with 'outfmt=table'
    cat = Table.from_pandas(cat)
    return cat
