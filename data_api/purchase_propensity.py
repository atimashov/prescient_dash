import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
from controls import REGIONS, STATES

def get_client(timeout = 150):
    host_name = 'https://search-entropia-kfc-7zxb6knn77auxxkxm3qfnbhyqa.ap-southeast-1.es.amazonaws.com'
    es = Elasticsearch(
        [host_name],
        verify_certs = False
    )
    return es

def propensity_search_object(
        filters,
        index = 'purchase_propensity_0921',
        last_month = False
):
    #--------------------------
    #        FILTERS
    #--------------------------

    # dates
    if last_month: q = Q('match', **{'date_forecast': '2018-12-01'})
    else: q = Q('range', first_activity = {'gte': filters['from'], 'lte': filters['to'], 'format': 'yyyy-MM-dd'})
    must_query = [q]


    # states & regions
    if 'states' in filters:
        tt = []
        for state in filters['states']:
            tt.append(Q('match', **{'state': state}))
        must_query.append(Q('bool', should = tt))
    elif 'region' in filters and filters['region'] != 'All_Malaysia':
        tt = []
        for state in REGIONS[filters['region'].replace('_', ' ')]:
            tt.append(Q('match', **{'state': state}))
        must_query.append(Q('bool', should = tt))
    #--------------------------
    #        SEARCH
    #--------------------------
    s = Search(using = get_client(), index = index)
    s.query = Q('bool', must = must_query)
    return s

def propensity_agg(s, filters):
    # monthly
    a_terms = A('terms', field='date_forecast', size = 100, order =  { "_key" : "asc" })
    a_nest = A('nested', path = 'score')
    a_avg = A('avg', field = 'score.{}'.format(filters.get('product', 'OTHER')))
    s.aggs.bucket('FORECAST_MONTHLY', a_terms).bucket('Nested', a_nest).bucket('average_score', a_avg)
    s = s[:0]
    return s

def propensity_list(s, filters):
    sort =  { 'score.{}'.format(filters.get('product', 'OTHER')) : {'order' : 'desc', 'nested_path': 'score'}}
    s = s.sort(sort)
    s = s[:filters['n']]
    return s

def propensity_repackage(aggs, hits, product):
    # aggregations
    tmp = aggs['FORECAST_MONTHLY']['buckets']
    f = lambda x: {
        'date': x['key_as_string'][:10],
        'avg_value': x['Nested']['average_score']['value']
    }
    out = {
        'aggs': list(map(f, tmp))
    }

    # hits
    f = lambda x: {
        'Customer Email': x['_source']['email'],
        'Score, %': x['_source']['score'][product]
    }
    df = pd.DataFrame({
        'Number': list(range(1, len(hits) + 1)),
        'Customer Email': list(map(lambda x: x['_source']['email'], hits)),
        'Score, %': list(map(lambda x: round(100 * x['_source']['score'][product], 2), hits))
    })
    out['list'] = df.to_dict('records')

    return out


