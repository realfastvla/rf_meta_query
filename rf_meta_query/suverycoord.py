""" Parent class for surveying at a given coordinate"""
from abc import ABCMeta

class SurveyCoord(object):
    """

    """

    __metaclass__ = ABCMeta

    def __init__(self, coord, radius, verbose=False):
        # Load up
        self.coord = coord
        self.radius = radius
        self.verbose = verbose

        # Typically set items
        self.survey = None

        # Standard products
        self.catalog = None
        self.cutout = None
        self.cutout_size = None

    def get_catalog(self):
        pass

    def get_cutout(self, imsize):
        pass

    def get_image(self, imsize, filter):
        pass

    def validate_catalog(self):
        if len(self.catalog) > 0:
            # Columns
            assert 'ra' in self.catalog.keys()
            assert 'dec' in self.catalog.keys()
            # Meta
            assert 'radius' in self.catalog.meta.keys()
            assert 'survey' in self.catalog.meta.keys()

    def write_cutout(self):
        pass
