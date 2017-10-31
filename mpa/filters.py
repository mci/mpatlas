try:
    import simplejson as json
except ImportError:
    import json

sample_querystring_json = '''?
    sort=[
        {
            "f": "name",
            "dir": "ASC"
        }
    ]
    &filter=[
        {
            "depth": { "min": 0, "max": 100 }
        },
        {
            "nation": [ "USA", "NZL", "AUS", "CAN" ]
        },
        {
            "protection_level": [ "high", "med" ]
        },
        {
            "status": [ "proposed", "designated" ]
        },
        {
            "status_year": { "min": "2000", "max": "2008" }
        }
    ]
}'''
# Keeping the filter as an array of objects sorted by key name let's us ensure the querystring
# is presented in the same order on all identical requests, facilitating caching.

# INPUT: Filters take in a Django Queryset and single filter input 
# parameter (can be list, dict, string) parsed from the json query 
# string and converted to python by simplejson.
# OUTPUT: Filters return a Django Queryset object that applies the
# specified filter.  In this way multiple filters can be chained.

filters = {}

def register(name, filterfunc):
    filters[name.lower()] = filterfunc

def apply_filters(qs, filterjson):
    if (filterjson):
        try:
            filter_list = json.loads(filterjson)
        except:
            return qs
        for f in filter_list:
            for name in f:
                value = f[name]
                if name in filters:
                    try:
                        qs = filters[name](qs, value)
                    except:
                        pass
    return qs

def nation(qs, nations):
    # nations is a list of 3-char country codes
    # 'all' means don't filter on nation
    nation_list = []
    for nation in nations:
        if (nation.lower() == 'all'):
            return qs
        nation_list.append(nation.upper())
    if nation_list:
        qs = qs.filter(country__in=nation_list)
    return qs

register('nation', nation)

def protection(qs, protectionlevels):
    # protection levels by list
    # 'all' means don't filter on protection
    protection_list = []
    for protection in protectionlevels:
        if (protection.lower() == 'all'):
            return qs
        protection_list.append(protection.lower().capitalize())
    if protection_list:
        qs = qs.filter(protection_level__in=protection_list)
    return qs

register('protection', protection)

def no_take(qs, no_take_levels):
    # protection levels by list
    ## 'all' means don't filter
    no_take_list = []
    for no_take in no_take_levels:
        # if (no_take.lower() == 'all'):
        #     return qs
        no_take_list.append(no_take.lower().capitalize())
    if no_take_list:
        qs = qs.filter(no_take__in=no_take_list)
    return qs

register('no_take', no_take)

def status(qs, statuses):
    # designations by list
    # 'all' means don't filter
    status_list = []
    for status in statuses:
        if (status.lower() == 'all'):
            return qs
        status_list.append(status.lower().capitalize())
    if status_list:
        qs = qs.filter(status__in=status_list)
    return qs

register('status', status)

def status_year(qs, years):
    # designations by list
    # 'all' means don't filter
    try:
        # dict with min and/or max range values?
        if 'min' in years:
            qs = qs.filter(status_year__gte=years['min'])
        if 'max' in years:
            qs = qs.filter(status_year__lte=years['max'])
    except AttributeError:
        # list of years
        year_list = []    
        for year in years:
            if (str(year).lower() == 'all'):
                return qs
            year_list.append(int(year))
        if year_list:
            qs = qs.filter(status_year__in=year_list)
    return qs

register('status_year', status_year)