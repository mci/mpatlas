from psycopg2.extensions import adapt
from django.contrib.postgres.search import SearchQuery


class PrefixedPhraseQuery(SearchQuery):
    """
    Alter the tsquery executed by SearchQuery
    """

    def __init__(self, value, all_partial=False, **kwargs):
        # all_partial=True puts :* after every term, otherwise only the last term is partial
        self.all_partial = all_partial
        super(PrefixedPhraseQuery, self).__init__(value, **kwargs)

    def as_sql(self, compiler, connection):
        # Or <-> available in Postgres 9.6
        glue = ':* & ' if self.all_partial else ' & '
        value = adapt('%s:*' % glue.join(self.value.split()))

        if self.config:
            config_sql, config_params = compiler.compile(self.config)
            template = 'to_tsquery({}::regconfig, {})'\
                .format(config_sql, value)
            params = config_params

        else:
            template = 'to_tsquery({})'\
                .format(value)
            params = []

        if self.invert:
            template = '!!({})'.format(template)

        return template, params