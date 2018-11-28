"""
Run an SDSS query to get photometric points and
optionally include photmetric redshift estimates
"""

import numpy as _np
from astroquery.sdss import SDSS as _SDSS
from astropy.coordinates import SkyCoord as _sc
import astropy.units as _u

def get_catalog(coords,radius=1*_u.arcmin,photoz=True,
                        photoobj_fields=None,
                        timeout=None,
                        print_query=False):
    """
    Get all objects within a given
    radius of the input coordinates.
    Optionally get photometric redshift
    estimates.
    """

    if not photoz:
        return _SDSS.query_region(coord, radius=radius, timeout=timeout,photoobj_fields=photoobj_fields)
    
    if photoobj_fields is None:
        photoobj_fs = ['ra', 'dec', 'objid', 'run', 'rerun', 'camcol', 'field']
        mags = ['petroMag_u', 'petroMag_g', 'petroMag_r', 'petroMag_i', 'petroMag_z']
        magsErr = ['petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z']
        photoobj_fields = photoobj_fs+mags+magsErr
    
    query = "SELECT GN.distance, "
    for field in photoobj_fields:
        query += "p.{:s}, ".format(field)
    
    query += "pz.z as redshift, pz.zErr as redshift_error\n"
    query += "FROM PhotoObjAll as p\n"
    query += "JOIN dbo.fGetNearbyObjEq({:f},{:f},{:f}) AS GN\nON GN.objID=p.objID\n".format(coords.ra.value,coords.dec.value,radius.to(_u.arcmin).value)
    query += "JOIN Photoz AS pz ON pz.objID=p.objID\n"
    query += "ORDER BY distance"

    if print_query:
        print(query)
    
    return _SDSS.query_sql(query,timeout=timeout)
