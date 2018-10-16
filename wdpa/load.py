import os
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from .models import Wdpa2018Poly, Wdpa2018Point, WdpaSource
from .models import wdpa2018poly_mapping, wdpa2018point_mapping, wdpasource_mapping

wdpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepolygons.shp'))
wdpapoint_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepoints.shp'))

wdpa2014gdb = os.path.abspath('/Users/russmo/Documents/MPAtlas/WDPA_Oct2014_Public/WDPA_Oct2014_Public.gdb')

wdpa_201809_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Sept2018_Public/WDPA_Sept_2018_Public/WDPA_Sept2018_Public.gdb')
wdpa_201810_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Oct2018_Public//WDPA_Oct2018_Public.gdb')

def identify_layers(source=wdpa_201810_gdb):
    ds = DataSource(source)
    layers = {'point': None, 'poly': None, 'source': None}
    for lyrid in range(0, len(ds)):
        for key in layers.keys():
            if ds[lyrid].name.find(key) > -1:
                layers[key] = lyrid
                break
    return(layers)

def clear_wdpa_tables():
    WdpaSource.objects.all().delete()
    Wdpa2018Point.objects.all().delete()
    Wdpa2018Poly.objects.all().delete()

def run_point2018(source=wdpa_201810_gdb, strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(Wdpa2018Point, source, wdpa2018point_mapping, layer=identify_layers(source=source)['point'], transform=False, encoding='utf-8')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly2018(source=wdpa_201810_gdb, strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(Wdpa2018Poly, source, wdpa2018poly_mapping, layer=identify_layers(source=source)['poly'], transform=False, encoding='utf-8')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)

def run_source2018(source=wdpa_201810_gdb):
    ds = DataSource(source)
    src = ds[identify_layers(source=source)['source']]
    print('Importing', len(src), 'records from Source table')
    for feat in src:
        obj,created = WdpaSource.objects.get_or_create(metadataid=feat.get('METADATAID'))
        for f in wdpasource_mapping.items():
            setattr(obj, f[0], feat.get(f[1]))
        obj.save()
        print(feat.fid, end='\r', flush=True)


# Old WDPA imports
from .models import WdpaPolygon, wdpapolygon_mapping, WdpaPoint, wdpapoint_mapping
from .models import Wdpa2014Polygon, wdpa2014polygon_mapping, Wdpa2014Point, wdpa2014point_mapping

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
