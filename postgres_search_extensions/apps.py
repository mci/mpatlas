from django.apps import AppConfig
from django.db.models import CharField, TextField
from django.utils.translation import gettext_lazy as _

from .lookups import FUnaccent

class PostgresConfig(AppConfig):
    name = 'postgres_search_extensions'
    verbose_name = _('Postres Search Extensions')

    def ready(self):
        CharField.register_lookup(FUnaccent)
        TextField.register_lookup(FUnaccent)
