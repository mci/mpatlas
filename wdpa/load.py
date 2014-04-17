import os
from django.contrib.gis.utils import LayerMapping
from models import WdpaPolygon, wdpapolygon_mapping, WdpaPoint, wdpapoint_mapping

wdpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepolygons.shp'))
wdpapoint_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepoints.shp'))

def run_point(strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(WdpaPoint, wdpapoint_shp, wdpapoint_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly(strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(WdpaPolygon, wdpapolygon_shp, wdpapolygon_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)
