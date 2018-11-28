""" Module for handling meta_query I/O """

from astropy import units

def meta_dir(frbc, precision=(2,1)):

    # JName
    Jname = 'J{:s}{:s}'.format(frbc['coord'].ra.to_string(unit=units.hour,sep='',pad=True,precision=precision[0]),
                              frbc['coord'].dec.to_string(sep='',pad=True,alwayssign=True,precision=precision[1]))
    # Name name
    name = 'meta_{:s}'.format(Jname)

    return name

