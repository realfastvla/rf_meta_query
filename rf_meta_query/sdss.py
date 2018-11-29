""" Methods related to SDSS/BOSS queries """

import numpy as np
import pdb

from astropy import units
from astropy.coordinates import SkyCoord
from astropy.coordinates import match_coordinates_sky

from astroquery.sdss import SDSS

from rf_meta_query import catalog_utils
from rf_meta_query import meta_io
from rf_meta_query import images
from rf_meta_query import dm
from rf_meta_query import catalog_utils


def get_url(coord, imsize=30., scale=0.39612, grid=None, label=None, invert=None):
    """
    Generate the SDSS URL for an image retrieval

    Parameters:
    ----------
    coord : SkyCoord
      astropy.coordiantes.SkyCoord object
      Typically held in frb_cand['coord']
    imsize: float, optional
      Image size (rectangular) in arcsec and without units
    """

    # Pixels
    npix = round(imsize/scale)
    xs = npix
    ys = npix

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


def get_catalog(coord,radius=1*units.arcmin, photoobj_fields=None,
                timeout=None, print_query=False):
    """
    Query SDSS for all objects within a given
    radius of the input coordinates.

    Merges photometry with photo-z

    TODO -- Expand to include spectroscopy?
    TODO -- Trim down multiple sources in photometric table (probably after merging with photo-z)

    Args:
        coord: astropy.coordiantes.SkyCoord
        radius: Angle, optional
          Search radius
        photoobj_fields: list
          Fields for querying
        timeout: float, optional
        print_query: bool, optional
          Print the SQL query for the photo-z values

    Returns:
        catalog: astropy.table.Table
          Contains all measurements retieved
          *WARNING* :: The SDSS photometry table frequently has multiple entries for a given
          source, with unique objid values

    """

    if photoobj_fields is None:
        photoobj_fs = ['ra', 'dec', 'objid', 'run', 'rerun', 'camcol', 'field']
        mags = ['petroMag_u', 'petroMag_g', 'petroMag_r', 'petroMag_i', 'petroMag_z']
        magsErr = ['petroMagErr_u', 'petroMagErr_g', 'petroMagErr_r', 'petroMagErr_i', 'petroMagErr_z']
        photoobj_fields = photoobj_fs+mags+magsErr

    # Call
    photom_catalog = SDSS.query_region(coord, radius=radius, timeout=timeout,
                                     photoobj_fields=photoobj_fields)
    if photom_catalog is None:
        return None

    # Now query for photo-z

    query = "SELECT GN.distance, "
    #for field in photoobj_fields:
    #    query += "p.{:s}, ".format(field)
    query += "p.objid, "

    query += "pz.z as redshift, pz.zErr as redshift_error\n"
    query += "FROM PhotoObjAll as p\n"
    query += "JOIN dbo.fGetNearbyObjEq({:f},{:f},{:f}) AS GN\nON GN.objID=p.objID\n".format(
        coord.ra.value,coord.dec.value,radius.to('arcmin').value)
    query += "JOIN Photoz AS pz ON pz.objID=p.objID\n"
    query += "ORDER BY distance"

    if print_query:
        print(query)

    photz_cat = SDSS.query_sql(query,timeout=timeout)

    # Match em up
    matches = catalog_utils.match_ids(photz_cat['objid'], photom_catalog['objid'], require_in_match=False)
    gdz = matches > 0
    # Init
    photom_catalog['z'] = -9999.
    photom_catalog['z_error'] = -9999.
    # Fill
    photom_catalog['z'][matches[gdz]] = photz_cat['redshift'][np.where(gdz)]
    photom_catalog['z_error'][matches[gdz]] = photz_cat['redshift_error'][np.where(gdz)]

    # Trim down catalog
    trim_catalog = trim_down_catalog(photom_catalog, keep_photoz=True)

    # Sort by offset
    catalog = trim_catalog.copy()
    catalog = catalog_utils.sort_by_separation(catalog, coord, radec=('ra','dec'), add_sep=True)

    # Meta
    catalog.meta['radius'] = radius.to('arcmin').value

    # Return
    return catalog

def trim_down_catalog(catalog, keep_photoz=False, cut_within=1.5*units.arcsec):

    # All good
    keep = np.ones_like(catalog, dtype=bool)

    coords = SkyCoord(ra=catalog['ra'], dec=catalog['dec'], unit='deg')
    # Search on closest next neighbor
    idx, d2d, d3d = match_coordinates_sky(coords, coords, nthneighbor=2)
    too_close = np.where(d2d < cut_within)[0]
    for idx in too_close:
        # Already purged?
        if not keep[idx]:
            continue
        # Find the matches
        seps = coords[idx].separation(coords)
        orig_matches = np.where((seps < cut_within) & keep)[0]
        final_matches = orig_matches.copy()
        # Keep photo-z?
        if keep_photoz:
            good_pz = catalog['z'][final_matches] > -9000.
            if np.any(good_pz):
                final_matches = final_matches[good_pz]
        # Take the first one -- Any reason to do otherwise?
        final_match = final_matches[0]
        # Zero out the rest
        zero_me = orig_matches != final_match
        keep[orig_matches[zero_me]] = False
    # Finish
    return catalog[keep]


def query(frbc, meta_dir=None, verbose=False, imsize=30., write_meta=False):
    # Init
    summary_list = []
    # SDSS catalog
    sdss_cat = get_catalog(frbc['coord'])
    # In the database?
    if sdss_cat is None:  # This is a bit risky as a small radius might return None
        summary_list += ['SDSS: No sources.  Likely outside its footprint']
        return sdss_cat, summary_list

    sdss_cat.meta['survey'] = 'SDSS'
    # Write?
    if write_meta:
        meta_io.write_catalog(sdss_cat, meta_dir, verbose=verbose)
    # Summarize
    summary_list += catalog_utils.summarize_catalog(frbc, sdss_cat, 5*units.arcsec, 'petroMag_r')

    # SDSS cutout Image?
    if write_meta:
        sdss_url = get_url(frbc['coord'], imsize=imsize/60.)  # arcmin
        img = images.grab_from_url(sdss_url)
        # Prep plot
        plt = images.gen_snapshot_plt(img, imsize)
        meta_io.save_plt(plt, meta_dir, 'SDSS_snap', verbose=verbose)

    # SDSS DM
    close_obj = sdss_cat['separation'] < 1. # arcsec
    gdz = sdss_cat['z_error'][close_obj] > 0.
    if np.any(gdz):
        ibest = np.argmin(sdss_cat['z_error'][close_obj][gdz])
        frbc['z'] = sdss_cat['z'][close_obj][gdz][ibest]
        print("SDSS photo-z = {}".format(frbc['z']))
        # DM
        DM_best = dm.best_dm_from_z(frbc)
        print("DM_FRB = {} pc/cm^3".format(DM_best))

    return sdss_cat, summary_list