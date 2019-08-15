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

def bucket_search_object(
        filters,
        index = 'testindex_kfc1506'
):
    #--------------------------
    #        FILTERS
    #--------------------------
    must_query = [Q('nested', path = 'cart', query = Q('bool', must = [Q('exists', field = 'cart')]))]
    # states & regions
    if 'states' in filters:
        tt = []
        for state in filters['states']:
            tt.append(Q('match', **{'store.state': state}))
        must_query.append(Q('nested', path='store', query = Q('bool', should=tt)))
    elif 'region' in filters and filters['region'] != 'All_Malaysia':
        tt = []
        for state in REGIONS[filters['region'].replace('_', ' ')]:
            tt.append(Q('match', **{'store.state': state}))
        must_query.append(Q('nested', path='store', query=Q('bool', should=tt)))

    # dates
    q = Q('range', created={'gte': filters['from'], 'lte': filters['to'], 'format': 'yyyy-MM-dd'})
    must_query.append(q)

    # products
    if filters.get('products', None) is not None and filters.get('products', None) != ['']:
        tt = []
        for product in filters['products']:
            tt.append(Q('match', **{'cart.name': product}))
        must_query.append(Q('nested', path='cart', query=Q('bool', should = tt)))
    #--------------------------
    #        SEARCH
    #--------------------------
    s = Search(using = get_client(), index = index)
    s.query = Q('bool', must = must_query)
    return s

def agg_bucket(s):
    #TODO
    a_nest = A('nested', path = 'cart')
    a_name = A('terms', field = 'cart.name', size = 1000)
    s.aggs.bucket('Nested', a_nest).bucket('Products', a_name).metric('Sales', 'sum', field = 'cart.price').bucket('sales_sort', 'bucket_sort', sort = {"Sales": {"order": "desc"}}, size = 1000)
    return s


def repackage_bucket(aggs, filters):
    out = dict()
    tmp = aggs['Nested']['Products']['buckets']
    sales = pd.DataFrame(list(map(lambda x: {'Product Name': x['key'], 'Sales (RM)': round(x['Sales']['value'], 2)}, tmp)))

    dockets = pd.DataFrame(list(map(lambda x: {'Product Name': x['key'], 'Dockets': x['doc_count']}, tmp))).sort_values(by = 'Dockets', ascending = False)

    if 'products' in filters and filters['products'] != None:
        sales_max = sales.loc[sales['Product Name'] == filters['products'][0], 'Sales (RM)'].values[0]
        sales = sales.loc[sales['Product Name'] != filters['products'][0]]
        sales['Sales (RM)'] = list(map(lambda x: round(x, 2), 100 * sales['Sales (RM)'] / sales_max))
        dockets_max = dockets.loc[dockets['Product Name'] == filters['products'][0], 'Dockets'].values[0]
        dockets = dockets.loc[dockets['Product Name'] != filters['products'][0]]
        dockets['Dockets'] = list(map(lambda x: round(x, 2), 100 * dockets['Dockets'] / dockets_max))
    else:
        sales['Sales (RM)'] = list(map(lambda x: round(x, 2), 100 * sales['Sales (RM)'] / sales['Sales (RM)'].sum()))
        dockets['Dockets'] = list(map(lambda x: round(x, 2), 100 * dockets['Dockets'] / dockets['Dockets'].sum()))
    sales['Number'] = range(1, sales.shape[0] + 1)
    dockets['Number'] = range(1, dockets.shape[0] + 1)

    return {
        'Sales': sales.to_dict(orient = 'records'),
        'Counts': dockets.to_dict(orient='records')
    }

