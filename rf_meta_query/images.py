""" Module for image routines"""

import requests
from io import BytesIO
from PIL import Image

from matplotlib import pyplot as plt


def grab_from_url(url):
    # Simple calls
    rtv = requests.get(url)
    img = Image.open(BytesIO(rtv.content))
    # Return
    return img


def gen_snapshot_plt(img, imsize, show=False):
    plt.clf()
    plt.imshow(img, aspect='equal', extent=(-imsize / 2., imsize / 2, -imsize / 2., imsize / 2))
    # Label me
    plt.xlabel('Relative arcsec', fontsize=20)
    xpos = 0.22 * imsize
    ypos = 0.02 * imsize
    plt.text(-imsize / 2. - xpos, 0., 'EAST', rotation=90., fontsize=20)
    plt.text(0., imsize / 2. + ypos, 'NORTH', fontsize=20, horizontalalignment='center')
    # Show?
    if show:
        plt.show()
    # Return
    return plt

