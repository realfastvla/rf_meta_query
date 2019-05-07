""" Module for handling meta_query I/O """

import os
import json
import io

from astropy import units

from rf_meta_query import frb_cand


def meta_dir(frbc, create=False):
    """
    Generate a folder name for the meta data

    Args:
        frbc: FRBCandidate object
        precision: tuple
          For the Jname
        create: bool, optional
          mkdir the folder if it does not exist?

    Returns:
        name: str
          Name of the meta_dir
    """

    # JName
    Jname = frb_cand.jname(frbc)
    # Name name
    name = 'meta_{:s}'.format(Jname)

    # Create?
    if create:
        if not os.path.isdir(name):
            os.mkdir(name)

    # Return
    return name


def write_frbc(frbc, meta_dir):
    """
    Write the frbc object to disk

    Pops out a few non-JSON compliant objects
    after making a copy

    Args:
        frbc: FRB Candidate object
        meta_dir: str
          Folder for output

    Returns:

    """
    # Pop out non-JSON compliant items
    j_frbc = frbc.copy()
    for key in ['coord']:
        if key in j_frbc.keys():
            j_frbc.pop(key)
    outfile = os.path.join(meta_dir, 'frbc.json')
    # Write me
    with io.open(outfile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(j_frbc, sort_keys=True, indent=4, separators=(',', ': ')))


