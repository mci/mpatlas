import os
from django.contrib.gis.utils import LayerMapping
from models import Eez, EezSimplified, eez_mapping, eezsimplified_mapping

eez_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/World_EEZ_v6.1_20110512/World_EEZ_v6_1_20110512.shp'))
eezsimplified_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/World_EEZ_v6.1_20110512_LR/World_EEZ_v6_1_simpliefiedcoastlines_20110512.shp'))

def run_eez(strict=True, verbose=True, **kwargs):
    lm_eez = LayerMapping(Eez, eez_shp, eez_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_eez.save(strict=strict, verbose=verbose, **kwargs)

def run_eezsimplified(strict=True, verbose=True, **kwargs):
    lm_eezsimplified = LayerMapping(EezSimplified, eezsimplified_shp, eezsimplified_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_eezsimplified.save(strict=strict, verbose=verbose, **kwargs)

