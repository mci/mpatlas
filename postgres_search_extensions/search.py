from psycopg2.extensions import adapt
from django.contrib.postgres.search import SearchQuery


class PrefixedPhraseQuery(SearchQuery):
    """
    Alter the tsquery executed by SearchQuery
    """

    def __init__(self, value, search_type="raw", all_partial=False, **kwargs):
        # all_partial=True puts :* after every term, otherwise only the last term is partial
        self.all_partial = all_partial
        glue = ":* & " if self.all_partial else " & "
        value_prefix = "%s:*" % glue.join(value.split())
        super(PrefixedPhraseQuery, self).__init__(
            value_prefix, search_type=search_type**kwargs
        )
