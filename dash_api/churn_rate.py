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

def churn_search_object(
        filters,
        index = 'churn_0923',
        rate = 0
):
    #--------------------------
    #        FILTERS
    #--------------------------

    # dates
    q = Q('range', first_activity={'gte': filters['from'], 'lte': filters['to'], 'format': 'yyyy-MM-dd'})
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

    # rate
    if rate > 0:
        q = Q('range', score = {'gte': rate})
        must_query.append(q)

    #--------------------------
    #        SEARCH
    #--------------------------
    s = Search(using = get_client(), index = index)
    s.query = Q('bool', must = must_query)
    return s


def get_df_by_rate(s):
    out = []
    for hit in s.scan():
        row = {
            'email': hit.email,
            'first_actibity': hit.first_activity,
            'state': hit.state,
            'score': hit.score
        }
        out.append(row)
    return pd.DataFrame(out) if len(out) > 0 else pd.DataFrame(columns = ['email', 'first_actibity', 'state', 'score'])