import os
from django.contrib.gis.utils import LayerMapping
from .models import WdpaPolygon, wdpapolygon_mapping, WdpaPoint, wdpapoint_mapping
from .models import Wdpa2014Polygon, wdpa2014polygon_mapping, Wdpa2014Point, wdpa2014point_mapping

wdpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepolygons.shp'))
wdpapoint_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepoints.shp'))

wdpa2014gdb = os.path.abspath('/Users/russmo/Documents/MPAtlas/WDPA_Oct2014_Public/WDPA_Oct2014_Public.gdb')

def run_point2014(strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(Wdpa2014Point, wdpa2014gdb, wdpa2014point_mapping,
                      layer=1, transform=False, encoding='utf-8')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly2014(strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(Wdpa2014Polygon, wdpa2014gdb, wdpa2014polygon_mapping,
                      layer=0, transform=False, encoding='utf-8')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)


def run_point(strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(WdpaPoint, wdpapoint_shp, wdpapoint_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly(strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(WdpaPolygon, wdpapolygon_shp, wdpapolygon_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)
