import os
from django.contrib.gis.utils import LayerMapping
from models import USMpaPolygon, usmpapolygon_mapping

usmpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/shp/MPA_Inventory_2011_public.shp'))

def run_poly(strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(USMpaPolygon, usmpapolygon_shp, usmpapolygon_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)
