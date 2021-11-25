import os
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.utils import LayerMapping
from .models import WdpaPoly_prev, WdpaPoint_prev, WdpaSource
from .models import wdpa2019poly_mapping, wdpa2019point_mapping, wdpasource_mapping

from .models import WdpaPoly_new, WdpaPoint_new, WdpaSource
from .models import wdpa2021poly_mapping, wdpa2021point_mapping, wdpasource_mapping

wdpapolygon_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepolygons.shp'))
wdpapoint_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/wdpa_20111014/CurrentWDPAMarinepoints.shp'))

wdpa2014gdb = os.path.abspath('/Users/russmo/Documents/MPAtlas/WDPA_Oct2014_Public/WDPA_Oct2014_Public.gdb')

wdpa_201809_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Sept2018_Public/WDPA_Sept_2018_Public/WDPA_Sept2018_Public.gdb')
wdpa_201810_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Oct2018_Public//WDPA_Oct2018_Public.gdb')

wdpa_201911_gdb = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Nov2019_Public/WDPA_Nov2019_Public.gdb')
wdpa_202012_point_gdb = os.path.abspath('/Users/russmo/Code/wdpa/202012_WDPA_WDOECM_wdpa_gdb/WDPA_WDOECM_wdpa_gdb_points.gdb')
wdpa_202012_poly_gdb = os.path.abspath('/Users/russmo/Code/wdpa/202012_WDPA_WDOECM_wdpa_gdb/WDPA_WDOECM_wdpa_gdb_polygons.gdb')
wdpa_202012_source_csv = os.path.abspath('/Users/russmo/Code/wdpa/202012_WDPA_WDOECM_wdpa_gdb/WDPA_sources.csv')

wdpa_202111_gdb = os.path.abspath('/home/mpatlas/workspace/WDPA_Nov2021_Public/WDPA_Nov2021_Public.gdb')
#wdpa_202111_source_csv = os.path.abspath('/Users/russmo/Code/wdpa/WDPA_Nov2021_Public/WDPA_sources.csv')

def identify_layers(source=wdpa_202111_gdb):
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
    WdpaPoint_new.objects.all().delete()
    WdpaPoly_new.objects.all().delete()

def run_point2021(source=wdpa_202012_point_gdb, strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(WdpaPoint_new, source, wdpa2021point_mapping, layer=identify_layers(source=source)['point'], transform=False, encoding='utf-8')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_point2021_nogeom(source=wdpa_202111_gdb):
    ds = DataSource(source)
    src = ds[identify_layers(source=source)['point']]
    pt_pids = WdpaPoint_new.objects.all().values_list('wdpa_pid', flat=True)
    for feat in src:
        if feat.get('WDPA_PID') not in pt_pids:
            print(feat.fid)
            print(feat.fid, end='\r', flush=True)
            try:
                obj = WdpaPoint_new.objects.get(wdpa_pid=feat.get('WDPA_PID'))
                print(feat.fid, 'fid', feat.get('WDPA_PID'), 'WDPA_PID already exists, overwriting fields')
            except:
                obj = WdpaPoint_new(wdpa_pid=feat.get('WDPA_PID'))
            for f in wdpa2021point_mapping.items():
                if f[0]=='geom':
                    continue
                setattr(obj, f[0], feat.get(f[1]))
            obj.save()

def run_poly2021(source=wdpa_202111_gdb, strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(WdpaPoly_new, source, wdpa2021poly_mapping, layer=identify_layers(source=source)['poly'], transform=False, encoding='utf-8')
    lm_poly.save(strict=strict, verbose=verbose, **kwargs)

def run_source2021(source=wdpa_202111_gdb):
    ds = DataSource(source)
    src = ds[identify_layers(source=source)['source']]
    print('Importing', len(src), 'records from Source table')
    for feat in src:
        obj,created = WdpaSource.objects.get_or_create(metadataid=feat.get('metadataid'))
        if not created:
            print (feat.fid, 'fid: metadataid', feat.get('metadataid'), 'already exists, overwriting fields')
        for f in wdpasource_mapping.items():
            setattr(obj, f[0], feat.get(f[1]))
        obj.save()
        print(feat.fid, end='\r', flush=True)


def run_point2019(source=wdpa_201911_gdb, strict=True, verbose=True, **kwargs):
    lm_point = LayerMapping(WdpaPoint_prev, source, wdpa2019point_mapping, layer=identify_layers(source=source)['point'], transform=False, encoding='utf-8')
    lm_point.save(strict=strict, verbose=verbose, **kwargs)

def run_poly2019(source=wdpa_201911_gdb, strict=True, verbose=True, **kwargs):
    lm_poly = LayerMapping(WdpaPoly_prev, source, wdpa2019poly_mapping, layer=identify_layers(source=source)['poly'], transform=False, encoding='utf-8')
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

