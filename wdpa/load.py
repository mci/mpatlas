import os
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from .models import Wdpa2019Poly, Wdpa2019Point, WdpaSource
from .models import wdpa2019poly_mapping, wdpa2019point_mapping, wdpasource_mapping

wdpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepolygons.shp'))
wdpapoint_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepoints.shp'))

wdpa2014gdb = os.path.abspath('/Users/russmo/Documents/MPAtlas/WDPA_Oct2014_Public/WDPA_Oct2014_Public.gdb')

wdpa_201809_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Sept2018_Public/WDPA_Sept_2018_Public/WDPA_Sept2018_Public.gdb')
wdpa_201810_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Oct2018_Public//WDPA_Oct2018_Public.gdb')

wdpa_201911_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Nov2019_Public/WDPA_Nov2019_Public.gdb')


def identify_layers(source=wdpa_201911_gdb):
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
    Wdpa2019Point.objects.all().delete()
    Wdpa2019Poly.objects.all().delete()

def run_point2019(source=wdpa_201911_gdb, strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(Wdpa2019Point, source, wdpa2019point_mapping, layer=identify_layers(source=source)['point'], transform=False, encoding='utf-8')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly2019(source=wdpa_201911_gdb, strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(Wdpa2019Poly, source, wdpa2019poly_mapping, layer=identify_layers(source=source)['poly'], transform=False, encoding='utf-8')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)

def run_source2019(source=wdpa_201911_gdb):
    ds = DataSource(source)
    src = ds[identify_layers(source=source)['source']]
    print('Importing', len(src), 'records from Source table')
    for feat in src:
        obj,created = WdpaSource.objects.get_or_create(metadataid=feat.get('METADATAID'))
        for f in wdpasource_mapping.items():
            setattr(obj, f[0], feat.get(f[1]))
        obj.save()
        print(feat.fid, end='\r', flush=True)

