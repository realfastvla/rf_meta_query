""" Module for DM calculations"""
import pdb

from frb.igm import average_DM
from ne2001 import density

def best_dm_from_z(frbc, DM_host=50., DM_MW=80.):
    """
    Calculate an estimated DM_FRB provided the candidate info

    Calls ne2001 for Galactic ISM estimate in the given direction

    Args:
        frbc: FRBCandidate object
          Must include coord and z
        DM_host: float, optional
          WAG for the host DM in pc/cm^3
        DM_MW:
          WAG for the MW halo DM in pc/cm^3

    Returns:
        DM_FRB: float
          Estimated DM in pc/cm^3

    """

    # NE2001
    ne = density.ElectronDensity()
    DM_ISM = ne.DM(frbc['coord'].galactic.l, frbc['coord'].galactic.b, 100.)

    # Cosmic
    DM_cosmic = average_DM(frbc['z']).value

    # Add em up
    DM_FRB = DM_ISM.value + DM_MW + DM_cosmic + DM_host

    # Return
    return DM_FRB

