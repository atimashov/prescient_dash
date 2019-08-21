import os
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
from controls import REGIONS, STATES, HOLIDAYS, HOLIDAYS_2017, HOLIDAYS_2018

def get_client(timeout = 150):
    host_name = '86fc4bbb23ab49e4b3282e50a5c2af0e.europe-west3.gcp.cloud.es.io'
    host_name = 'https://search-entropia-kfc-7zxb6knn77auxxkxm3qfnbhyqa.ap-southeast-1.es.amazonaws.com'
    es = Elasticsearch(
        [host_name],
        verify_certs=False
    )
    return es

def sales_search_object(
        filters,
        index = 'testindex_kfc1506'
):
    must_query = []
    # states
    if 'states' in filters:
        tt = []
        for state in filters['states']:
            tt.append(Q('match', **{'store.state': state}))
        must_query.append(Q('nested', path='store', query=Q('bool', should=tt)))
    elif 'region' in filters and filters['region'] != 'All_Malaysia':
        tt = []
        for state in REGIONS[filters['region'].replace('_', ' ')]:
            tt.append(Q('match', **{'store.state': state}))
        must_query.append(Q('nested', path='store', query=Q('bool', should=tt)))

    # dates
    q = Q('range', created={'gte': filters['from'], 'lte': filters['to'], 'format': 'yyyy-MM-dd'})
    must_query.append(q)
    # search
    s = Search(using = get_client(), index=index)
    s.query = Q('bool', must = must_query)
    return s


def agg_daily_sales(s):
    a_dates = A('date_histogram', field='created', interval='1d', format='yyyy-MM-dd')
    a_sales = A('sum', field='full_price')
    s.aggs.bucket('Date', a_dates).bucket('Sales', a_sales)
    return s


def agg_monthly_sales(s):
    a_holiday = A('filters', filters = {'holiday':{"range": {"weekday": {"gte":6}}}, 'weekday':{"range": {"weekday": {"lte":5}}}})
    a_dates = A('date_histogram', field='created', interval='1M', format='yyyy-MM-dd')
    a_sales = A('sum', field='full_price')
    s.aggs.bucket('holi_week_month', a_holiday).bucket('Month', a_dates).bucket('Sales', a_sales)
    return s

def agg_weekly_sales(s):
    a_dates = A('date_histogram', field='created', interval='1w', format='yyyy-MM-dd')
    a_sales = A('sum', field='full_price')
    s.aggs.bucket('Date', a_dates).bucket('Sales', a_sales)
    return s

def agg_weekdaily_sales(s):
    a_dates = A('terms', field='weekday')
    a_sales = A('sum', field='full_price')
    s.aggs.bucket('Weekday', a_dates).bucket('Sales', a_sales)
    return s


def agg_hourly_sales(s):
    a_holiday = A('filters', filters={'holiday': {"range": {"weekday": {"gte": 6}}}, 'weekday': {"range": {"weekday": {"lte": 5}}}})
    a_dates = A('terms', field='hour')
    a_sales = A('sum', field = 'full_price')
    s.aggs.bucket('holi_week_hour', a_holiday).bucket('Hour', a_dates).bucket('Sales', a_sales)
    return s


def repackage_sales(aggs):
    def one(doc):
        return {
            'date': doc.get('key_as_string', doc['key']),
            'sales': round(doc['Sales']['value'], 2),
            'dockets': doc['doc_count'],
            'av_purchase': None if doc['doc_count'] == 0 else round(doc['Sales']['value'] / doc['doc_count'], 2)
        }
    resp = dict()
    if 'Date' in aggs: resp['Daily'] = list(map(one, aggs['Date']['buckets']))
    if 'Weekday' in aggs: resp['Weekdaily'] = list(map(one, aggs['Weekday']['buckets']))
    if 'holi_week_month' in aggs:
        resp['Monthly'] = {
            'Weekday': list(map(one, aggs['holi_week_month']['buckets']['weekday']['Month']['buckets'])),
            'Weekend': list(map(one, aggs['holi_week_month']['buckets']['holiday']['Month']['buckets']))
        }
    if 'holi_week_hour' in aggs:
        resp['Hourly'] = {
            'Weekday': list(map(one, aggs['holi_week_hour']['buckets']['weekday']['Hour']['buckets'])),
            'Weekend': list(map(one, aggs['holi_week_hour']['buckets']['holiday']['Hour']['buckets']))
        }
    return resp