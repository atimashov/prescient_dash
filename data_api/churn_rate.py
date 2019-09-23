import os
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
import calendar
from dateutil.parser import parse
from datetime import datetime,timedelta
from controls import REGIONS, STATES, HOLIDAYS, HOLIDAYS_2017, HOLIDAYS_2018


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

def churn_agg(s):
    ranges = []
    for i in range(19):
        ranges.append({'from': i / 20, 'to': (i + 1) / 20})
    ranges.append({'from': 19 / 20})

    a_ranges = A('range', field = 'score', ranges = ranges)
    s.aggs.bucket('density', a_ranges)

    a_avg = A('avg', field = 'score')
    s.aggs.bucket('average_score', a_avg)
    return s


def churn_repackage(aggs):
    tmp = aggs['density']['buckets']
    out = {
        'percents': [5 * i for i in range(1, 21)],
        'amount': list(map(lambda x: x['doc_count'], tmp)),
        'avg_value': aggs['average_score']['value']
    }
    return out



