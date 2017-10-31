# -*- coding: utf-8 -*-
try:
  from .local_settings import *
except ImportError:
  from .default_settings import *
