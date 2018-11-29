""" Simple methods for building and using frb_cand object"""

from astropy.coordinates import SkyCoord


def build_frb_cand(ra, dec, **kwargs):
    """

    Args:
        ra: float (deg)
          RA in J2000 ICRS
        dec: float (deg)
          Dec in J2000 ICRS
        **kwargs:

    Returns:

    """
    # Dict for now, might make it a Class later
    frb_cand = {}
    frb_cand['RA'] = ra
    frb_cand['DEC'] = dec

    # Coordinate
    frb_cand['coord'] = SkyCoord(ra=ra, dec=dec, unit='deg')

    # Extras
    for key in kwargs:
        frb_cand[key] = kwargs[key]

    # Return
    return frb_cand
