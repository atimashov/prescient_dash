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
        index = 'purchase_propensity_0921'
):
    #--------------------------
    #        FILTERS
    #--------------------------

    # dates
    q = Q('match', **{'date_forecast': '2018-12-01'})
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
    # --------------------------
    #        SORT & FILTERS
    # --------------------------
    sort = {'score.{}'.format(filters.get('product', 'OTHER')): {'order': 'desc', 'nested_path': 'score'}}
    s = s.sort(sort)
    s = s[:filters['n']]
    return s


def propensity_repackage(hits, product):
    # hits
    f = lambda x: {
        'email': x['_source']['email'],
        'state': x['_source']['state'],
        'first_activity': x['_source']['first_activity'],
        'score_{}'.format(product): (x['_source']['score'][product] - 0.5) * 0.88 + 0.5 if x['_source']['score'][product] > 0.5 else 0.5 - 0.88 * (0.5 - x['_source']['score'][product])
    }
    df = pd.DataFrame(list(map(f, hits)))
    return df


