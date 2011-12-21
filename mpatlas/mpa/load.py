import os
from django.contrib.gis.utils import LayerMapping
from models import MpaCandidate, mpacandidate_mapping

mpacandidate_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/Potential_MPAs/Potential_MPAs.shp'))

def run_mpacandidate(strict=True, verbose=True, **kwargs):
    lm_mpacandidate = LayerMapping(MpaCandidate, mpacandidate_shp, mpacandidate_mapping,
                      transform=False, encoding='iso-8859-1')
    lm_mpacandidate.save(strict=strict, verbose=verbose, **kwargs)

