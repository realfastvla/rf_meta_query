""" Module for handling meta_query I/O """

import os

from astropy import units


def meta_dir(frbc, precision=(2,1), create=False):

    # JName
    Jname = 'J{:s}{:s}'.format(frbc['coord'].ra.to_string(unit=units.hour, sep='',pad=True,precision=precision[0]),
                              frbc['coord'].dec.to_string(sep='',pad=True,alwayssign=True,precision=precision[1]))
    # Name name
    name = 'meta_{:s}'.format(Jname)

    # Create?
    if create:
        if not os.path.isdir(name):
            os.mkdir(name)

    # Return
    return name

def save_plt(plt, meta_dir, root, verbose=False, ftype='png'):
    # Prep
    basename = root+'.{:s}'.format(ftype)
    outfile = os.path.join(meta_dir, basename)

    # Write
    plt.savefig(outfile, dpi=300)
    if verbose:
        print("Wrote: {:s}".format(outfile))


def write_table(tbl, meta_dir, root, fits=True, verbose=False):
    # Outfile
    if fits:
        basename = root+'.fits'
    else:
        raise IOError("Bad table file type")
    outfile = os.path.join(meta_dir, basename)

    # Write
    tbl.write(outfile, overwrite=True)
    if verbose:
        print("Wrote: {:s}".format(outfile))