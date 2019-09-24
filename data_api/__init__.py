from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from datetime import datetime
import logging
import json
import calendar
import pandas as pd

from sales import sales_search_object
from sales import agg_daily_sales
from sales import agg_monthly_sales
from sales import agg_weekdaily_sales
from sales import agg_hourly_sales
from sales import agg_weekly_sales
from sales import repackage_sales

from bucket_analysis import bucket_search_object
from bucket_analysis import agg_bucket
from bucket_analysis import repackage_bucket

from churn_rate import churn_search_object
from churn_rate import churn_agg
from churn_rate import churn_repackage

from purchase_propensity import propensity_search_object
from purchase_propensity import propensity_agg
from purchase_propensity import propensity_repackage
from purchase_propensity import propensity_list

app = Flask(__name__)

def load_args(request):
    res = dict()
    date_from = request.args.get('from', '2017-01-02')
    res['from'] = date_from if date_from else '2016-01-01'
    date_to = request.args.get('to', '2018-10-31')
    res['to'] = date_to if date_to else '2018-10-31'

    region = request.args.get('region', 'All_Malaysia')
    if region != 'All_Malaysia': res['region'] = region

    states = request.args.get('states', 'all')
    states = states.split(',')
    if states != ['all']: res['states'] = states

    product = request.args.get('product', None)
    if product is not None:  res['products'] = product

    # plot type
    res['plot_type'] = request.args.get('plot_type', 'all')
    if res['plot_type'] not in ['monthly', 'daily', 'hourly', 'weekdaily']: res['plot_type'] = 'all'
    # subscribers_type
    res['subscr_type'] = request.args.get('subscr_type', 'cumulative')
    if res['subscr_type'] not in ['monthly', 'guests', 'registered_by']: res['subscr_type'] = 'cumulative'

    n = request.args.get('number', 1000)
    print('** ', n)
    res['n'] = int(n if n is not None and n != 'None' else 100)
    return res


@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/sales")
def sales():
    args = load_args(request)
    s = sales_search_object(filters = args)
    # if args['plot_type'] in ['daily', 'all']: s = agg_daily_sales(s)
    # if args['plot_type'] in ['monthly', 'all']: s = agg_monthly_sales(s)
    # if args['plot_type'] in ['weekdaily', 'all']: s = agg_weekdaily_sales(s)
    # if args['plot_type'] in ['hourly', 'all']: s = agg_hourly_sales(s)
    s = agg_weekly_sales(s)
    s = s[:0]
    logging.warning('')
    logging.warning('*********************************************************************************')
    logging.warning('')
    logging.warning(json.dumps(s.to_dict()))
    print(s.to_dict())
    out = s.execute().to_dict()
    out = repackage_sales(out['aggregations'])
    return jsonify(out)

@app.route("/bucket_analysis")
def bucket_analysis():
    args = load_args(request)
    s = bucket_search_object(filters = args)
    s = agg_bucket(s)
    #s = agg_ticket_amount(s)
    s = s[:0]
    logging.warning('')
    logging.warning('*********************************************************************************')
    logging.warning('')
    logging.warning(json.dumps(s.to_dict()))
    print(s.to_dict())
    out = s.execute().to_dict()['aggregations']
    out = repackage_bucket(out, args)
    return jsonify(out)

@app.route("/churn_rate")
def churn_rate():
    args = load_args(request)
    s = churn_search_object(filters = args)
    s = churn_agg(s)
    s = s[:0]
    logging.warning('')
    logging.warning('*********************************************************************************')
    logging.warning('')
    logging.warning(json.dumps(s.to_dict()))
    print(s.to_dict())
    out = s.execute().to_dict()['aggregations']
    out = churn_repackage(out)
    return jsonify(out)


@app.route("/purchase_propensity")
def purchase_propensity():
    args = load_args(request)
    # for plot
    s = propensity_search_object(filters = args, last_month = False)
    s = propensity_agg(s, args)
    logging.warning('')
    logging.warning(json.dumps(s.to_dict()))
    logging.warning('')
    aggs = s.execute().to_dict()['aggregations']

    # for table
    s = propensity_search_object(filters = args, last_month = True)
    s = propensity_list(s, args)
    logging.warning('')
    logging.warning(json.dumps(s.to_dict()))
    logging.warning('')
    hits = s.execute().to_dict()['hits']['hits']
    out = propensity_repackage(aggs, hits, args.get('product', 'OTHER'))
    return jsonify(out)



if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8000)