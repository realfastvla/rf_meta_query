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


def save_plt(plt, meta_dir, root, verbose=False, ftype='png'):
    """
    Save a matplotlib object to disk

    Args:
        plt: matplotlib.pyplot
        meta_dir: str
          Folder for output
        root: str
          Root name of the output file
        verbose: bool, optional
        ftype: str
          File type, e.g.  png, pdf

    Returns:

    """
    # Prep
    basename = root+'.{:s}'.format(ftype)
    outfile = os.path.join(meta_dir, basename)

    # Write
    plt.savefig(outfile, dpi=300)
    if verbose:
        print("Wrote: {:s}".format(outfile))


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


def write_catalog(tbl, meta_dir, ftype='ecsv', verbose=False):
    """
    Write an input astropy Table to disk

    Args:
        tbl: astropy.table.Table
        meta_dir: str
          Folder for output
        root: str
          Root name of the output file
        ftype: str, optional
          File type, e.g. ecsv
        verbose: bool, optional

    Returns:

    """
    # Check
    if ftype not in ['ecsv']:
        raise IOError("Unallowed file type: {:s}".format(ftype))
    #
    root = tbl.meta['survey']
    # Outfile
    basename = root+'.{:s}'.format(ftype)
    outfile = os.path.join(meta_dir, basename)

    # Write
    tbl.write(outfile, overwrite=True)
    if verbose:
        print("Wrote: {:s}".format(outfile))