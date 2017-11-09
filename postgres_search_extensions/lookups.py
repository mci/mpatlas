from django.db.models import Transform

class FUnaccent(Transform):
	# Use the f_unaccent() IMMUTABLE function we defined in postgresql
	# This is needed for GIN indices, because regular UNACCENT() is
	# STABLE, not IMMUTABLE, and not allowed in indices.
    bilateral = True
    lookup_name = 'funaccent'
    function = 'f_unaccent'