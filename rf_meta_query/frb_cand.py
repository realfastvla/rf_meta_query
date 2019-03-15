""" Simple methods for building and using frb_cand object"""

from astropy.coordinates import SkyCoord
from astropy import units


def build_frb_cand(ra, dec, id, **kwargs):
    """
    Build a simple FRB Candidate object

    Currently a dict, might become a Class

    Args:
        ra: float (deg)
          RA in J2000 ICRS
        dec: float (deg)
          Dec in J2000 ICRS
        id: int
        **kwargs:

    Returns:

    """
    # Dict for now, might make it a Class later
    frb_cand = {}
    frb_cand['ra'] = ra
    frb_cand['dec'] = dec
    frb_cand['id'] = id

    # Coordinate
    frb_cand['coord'] = SkyCoord(ra=ra, dec=dec, unit='deg')

    # Extras
    for key in kwargs:
        frb_cand[key] = kwargs[key]

    # Return
    return frb_cand

def jname(frbc, precision=(2,1)):
    Jname = 'J{:s}{:s}'.format(frbc['coord'].ra.to_string(unit=units.hour, sep='',pad=True,precision=precision[0]),
                               frbc['coord'].dec.to_string(sep='',pad=True,alwayssign=True,precision=precision[1]))
    return Jname
