import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import json
import urllib.request, json
import plotly.graph_objs as go
import datetime as dt
import pandas as pd
from dateutil.parser import parse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
import os

from pages import tabs, marks
from controls import REGIONS, STATES, PRODUCTS
from time import sleep
BUTTON_DELAY = 1000
URL_TXT = 'dash_api/storage.txt'
MAIN_URL = 'http://localhost:8000'


#app = dash.Dash(__name__)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
app.config['suppress_callback_exceptions'] = True
server = app.server

#--------------------------------------------
#              Parts of layout
#--------------------------------------------
logos = html.Div(
    [
        html.H1(
            'Prescient',
            className = 'eight columns'
        ),
        html.Img(
            src = 'https://raw.githubusercontent.com/timashov-ml/examples/master/Entropia-logo.png',
            className = 'two columns',
            style = {
                'height': '100',
                'width': '305',
                'float': 'right',
                'position': 'relative',
            },
        ),
    ],
    style = {
        'margin-left': 10,
        'margin-right': 10
    },
    className = 'row'
)
dates = html.Div(
    [
        html.Div(
            [
                html.P('Choose date range for report:', style = {'margin-bottom': 25}),
                dcc.RangeSlider(
                    id = 'year_slider',
                    min = 0,
                    max = (dt.datetime(2018,10,31).date() - dt.datetime(2017, 1, 1).date()).days, #in normal case choose NOW
                    value = [2, 133],
                    marks = marks(0, (dt.datetime(2018,10,31).date() - dt.datetime(2017, 1, 1).date()).days),
                ),
            ],
            style = {'margin-left': '150', 'align': 'right'},#, 'padding': 30},
            className = 'ten columns'
        ),
        #html.H1(className='one column'),
        html.Div(
            [
                html.P('Date range:', style = {'margin-bottom': 15}),
                html.H6(
                    id = 'year_text',
                )
            ],
            style = {
                #'text-align': 'right',
                'margin-top': '50'
            },
            className = 'two columns'
        ),

    ],
    style = {
        'padding-bottom': 30,
        'margin-left': 20,
        #'margin-right': 20
    },
    className = 'row'
)

#--------------------------------------------
#                 Callbacks
#--------------------------------------------

#Slider -> year text
@app.callback(Output('year_text', 'children'),
              [Input('year_slider', 'value'),])
def update_year_text(slider):
    dt_0 = dt.datetime(2017, 1, 1).date() + dt.timedelta(days = slider[0])
    dt_1 = dt.datetime(2017, 1, 1).date() + dt.timedelta(days = slider[1])
    return "{} | {}".format(dt_0, dt_1)


# --------------------------------------------
#                    Churn
# --------------------------------------------
@app.callback(
    Output(component_id = 'churn_states', component_property='options'),
    [Input(component_id = 'churn_regions', component_property='value')]
)
def update_state1(selected_region):
    return [{'label': state, 'value': state} for state in REGIONS[selected_region] if state not in ['WP (Putrajaya)', 'WP (Labuan)', 'Perlis']]

@app.callback(
    [
        Output('churn_graph', 'figure'),
        Output('churn_text', 'children'),
        Output('churn_graph_comparison', 'figure')
    ],

    [
        Input('year_text', 'children'),
        Input('churn_states', 'value'),
        Input('churn_rate', 'value'),
        Input('churn_button', 'n_clicks_timestamp'),
    ]
)
def update_figure_forecast(
        dates_text, states_list, rate, button
):
    layout = go.Layout(
        autosize=False,
        width=1820,
        height=500,
        title='Probability distribution of churn rate',
        xaxis={
            'title': 'churn probability, %',
            'ticklen': 5,
            'gridwidth': 2,
        },
        yaxis = {
            'title': 'number of people',
            'ticklen': 5,
            'gridwidth': 2,
        },
        margin=go.layout.Margin(
            l=110,
            r=110,
            b=50,
            t=50,
            pad=4
        )
    )

    layout2 = go.Layout(
        autosize=False,
        width=1820,
        height=500,
        title='Churn rate monthly',
        xaxis={
            'title': 'month',
            'ticklen': 5,
            'gridwidth': 2,
        },
        yaxis={
            'title': 'churn probability, %',
            'ticklen': 5,
            'gridwidth': 2,
        },
        margin=go.layout.Margin(
            l=110,
            r=110,
            b=50,
            t=50,
            pad=4
        )
    )
    flag = False
    if button is not None and 1000 * datetime.now().timestamp() - button < BUTTON_DELAY: flag = True
    #---------------------------------------
    dt_min, dt_max = dates_text.split(' | ')
    df = pd.read_csv('qq.csv')

    #------monthly---------
    df_m = pd.DataFrame({
        'date':[str(datetime(2017,1,1).date() + relativedelta(months = +i)) for i in range(23)],
        'churn_rate': None
    })

    if states_list is None or states_list == []: out = df.copy()
    else:
        out = pd.DataFrame(columns = df.columns)
        for state in states_list:
            out = out.append(df.loc[df['state'] == state], ignore_index = True)


    q = [1.1, 0.9, 0.95, 1.03, 1.01, 0.92, 0.98, 1.1, 1.1, 1.1, 1.05, 1.02, 1.07, 0.93, 1.02, 1.08, 1.01, 1.1, 0.9, 0.92, 0.93, 1.04, 1.1]
    for i in df_m.index:
        if i + 1 not in df_m.index: continue
        cond = (out['date'] >= df_m['date'][i]) & (out['date'] < df_m['date'][i + 1])
        df_m['churn_rate'][i] = out.loc[cond, 'prob'].mean() * q[i]

    df_m = df_m.loc[df_m['churn_rate'].notnull()]




    plot = go.Bar(x=df_m['date'], y =  df_m['churn_rate'] * 100, name = 'churn rate')

    graph_2 = {
        'data': [plot],
        'layout': layout2
    }
    # ------monthly---------
    df = df.loc[(df['date'] >= dt_min) & (df['date'] <= dt_max)]
    print(df.shape)
    if states_list is None or states_list == []: out = df.copy()
    else:
        out = pd.DataFrame(columns = df.columns)
        for state in states_list:
            out = out.append(df.loc[df['state'] == state], ignore_index = True)
    #TODO: dependency on n
    x = [5 * i for i in range(1, 21)]
    y = []
    for i in range(1, 21):
        y.append(sum((out['prob'] <= i * 5 / 100) & (out['prob'] > (i - 1) * 5 / 100)))

    plot = go.Bar(x = x, y = y, name='fact')

    graph = {
        'data': [plot],
        'layout': layout
    }
    if flag:
        out.loc[out['prob'] >= rate].sort_values(by = ['prob'], ascending = True)
        name = '{}_{}_{}_{}.csv'.format('all' if states_list is None or states_list == [] else '-'.join(states_list), dt_min, dt_max, int(100 * rate))
        out.to_csv(name, index = False)
        txt = '## Saved {} rows'.format(out.shape[0])
    else: txt = ''
    return graph, txt, graph_2
#---------------------------------------------------------
#                   BUCKET ANALYSIS
#---------------------------------------------------------
@app.callback(
    Output(component_id='bucket_states', component_property='options'),
    [Input(component_id='bucket_regions', component_property='value')]
)
def update_state1(selected_region):
    return [{'label': state, 'value': state} for state in REGIONS[selected_region] if state not in ['WP (Putrajaya)', 'WP (Labuan)', 'Perlis']]



@app.callback(
    Output('bucket_sales', 'data'),
    [
        Input('year_text', 'children'),
        Input('bucket_regions', 'value'),
        Input('bucket_states', 'value'),
        Input('bucket_product', 'value'),
        Input('bucket_drop_sales', 'value'),
        Input('bucket_search_sales', 'value')
    ]
)
def update_figure(dates_text, region, states_list, product, drop_value, search):
    dt_min, dt_max = dates_text.split(' | ')
    url_bucket = '{}/bucket_analysis?from={}&to={}'.format(MAIN_URL, dt_min, dt_max)
    if region is not None:
        url_bucket = '{}&region={}'.format(url_bucket, region.replace(' ', '_'))
    if states_list is not None and states_list != []:
        url_bucket = '{}&states={}'.format(url_bucket, ','.join(states_list))
    if product is not None:
        url_bucket = '{}&products={}'.format(url_bucket, product.replace(' ', '%20'))

    with urllib.request.urlopen(url_bucket) as url:
        data = json.loads(url.read().decode())

    df = pd.DataFrame(data['Sales']).sort_values(by = 'Sales (RM)', ascending = False)
    if search != '':
        cond = pd.Series(map(lambda x: search.lower() in x.lower(), df['Product Name']))
        df = df.loc[cond]
    df = df.reset_index()
    del df['index']
    if drop_value is None: drop_value = 1000
    return df.loc[df.index < drop_value].to_dict('records')


@app.callback(
    Output('bucket_dockets', 'data'),
    [
        Input('year_text', 'children'),
        Input('bucket_regions', 'value'),
        Input('bucket_states', 'value'),
        Input('bucket_product', 'value'),
        Input('bucket_drop_dockets', 'value'),
        Input('bucket_search_dockets', 'value')
    ]
)
def update_figure(dates_text, region, states_list, product, drop_value, search):

    dt_min, dt_max = dates_text.split(' | ')
    url_bucket = '{}/bucket_analysis?from={}&to={}'.format(MAIN_URL, dt_min, dt_max)
    if region is not None:
        url_bucket = '{}&region={}'.format(url_bucket, region.replace(' ', '_'))
    if states_list is not None and states_list != []:
        url_bucket = '{}&states={}'.format(url_bucket, ','.join(states_list))
    if product is not None:
        url_bucket = '{}&products={}'.format(url_bucket, product.replace(' ', '%20'))

    with urllib.request.urlopen(url_bucket) as url:
        data = json.loads(url.read().decode())

    df = pd.DataFrame(data['Counts']).sort_values(by = 'Dockets', ascending = False)
    if search != '':
        cond = pd.Series(map(lambda x: search.lower() in x.lower(), df['Product Name']))
        df = df.loc[cond]
    df = df.reset_index()
    del df['index']
    if drop_value is None: drop_value = 1000
    return df.loc[df.index < drop_value].to_dict('records')

# --------------------------------------------
#                    Forecasting
# --------------------------------------------
@app.callback(
    Output(component_id='forecast_states', component_property='options'),
    [Input(component_id='forecast_regions', component_property='value')]
)
def update_state(selected_region):
    return [{'label': state, 'value': state} for state in REGIONS[selected_region] if
            state not in ['WP (Putrajaya)', 'WP (Labuan)', 'Perlis']]

@app.callback(
    [
        Output('forecast_graph', 'figure'),
        Output('forecast_table', 'data')
    ],
    [
        Input('year_text', 'children'),
        Input('forecast_regions', 'value'),
        Input('forecast_states', 'value'),
        Input('forecast_period', 'value')
    ]
)
def update_figure_forecast(
        dates_text, region, states_list, period
):
    layout = go.Layout(
        autosize=False,
        width = 1200, #1820, #800, #
        height=500,
        title='Sales (fact & plan)',
        xaxis={
            'title': 'date',
            'ticklen': 5,
            'gridwidth': 2,
        },
        yaxis={
            'title': 'sales, RM',
            'ticklen': 5,
            'gridwidth': 2,
        },
        margin=go.layout.Margin(
            l=110,
            r=110,
            b=50,
            t=50,
            pad=4
        )
    )
    period_dict = {
        'week': 1,
        'month': 4,
        'quarter': 13,
        '6 months': 26,
        'year': 52
    }
    #---------------------------------------
    dt_min, dt_max = dates_text.split(' | ')
    print()
    print(dt_min, dt_max)
    url_sales = '{}/sales?from=2017-01-01&to=2018-10-28'.format(MAIN_URL) #?from={}&to={} , dt_min, dt_max

    if region is not None:
        url_sales = '{}&region={}'.format(url_sales, region.replace(' ', '_'))
    if states_list is not None and states_list != []:
        cond = '&region' in url_sales
        url_sales = '{}{}states={}'.format(url_sales,'&' if cond else '&', ','.join(states_list))

    with urllib.request.urlopen(url_sales) as url:
        data = json.loads(url.read().decode())
    df = pd.DataFrame(data['Daily'])[['date', 'sales']]

    # rolling average
    for i in range(3, df.shape[0]-3):
        if df['sales'][i] < 10000:
            df['sales'][i] = (df['sales'][(i-3):(i)].sum() + df['sales'][(i + 1):(i + 4)].sum()) / 6
    df['sales'][2:] = df['sales'].rolling(3).mean()[2:]

    # forecasting
    df['forecast'] = None

    weeks = period_dict[period]

    for i in range(1, weeks + 1):
        m = 0
        dt = datetime(2018,10,28).date() + timedelta(days = 7 * i) #parse(dt_max).date() + timedelta(days = 7 * i)
        if sum(df['date'] == str(dt)) == 1:
            ind = df[df['date'] == str(dt)].index.values[0]
            out = df.loc[df['sales'].notnull(), 'sales'].mean()
            for j in range(1, 6):
                if ind - 7 * j > max(df.index):
                    m += 1
                    continue
                elif ind - 7 * j < 0:
                    break
                out = out + df['sales' if df['sales'][ind - 7 * j] is not None else 'forecast'][ind - 7 * j]
            df['forecast'][ind] = out / (j -m)
        else:
            ind = max(df.index) + 1
            out = df.loc[df['sales'].notnull(), 'sales'].mean()
            for j in range(1, 6):
                if ind - 7 * j > max(df.index):
                    m += 1
                    continue
                elif ind - 7 * j < 0:
                    break
                tmp_value = df['sales'][ind - 7 * j]
                out = out + df['forecast' if tmp_value is None or math.isnan(tmp_value) else 'sales'][ind - 7 * j]

            tmp = {
                'date': str(dt),
                'sales': None,
                'forecast': out / (j -m)
            }
            df = df.append(tmp, ignore_index=True)

    #TODO: check file availability
    plot_daily = go.Scatter(x = df['date'], y = df['sales'], mode='lines+markers', name = 'fact')
    plot_daily_f = go.Scatter(x = df['date'], y=df['forecast'], mode='lines+markers', name='forecast')

    graph_new = {
        'data': [plot_daily, plot_daily_f],
        'layout': layout
    }

    df = df.rename(columns = {'date': 'Week_Date', 'forecast':'Forecast, RM'}).loc[df['forecast'].notnull(), ['Week_Date', 'Forecast, RM']]
    df['Forecast, RM'] = df['Forecast, RM'].apply(lambda x: round(x, 2))
    table = df.to_dict('records')
    print(table)

    return graph_new, table

# --------------------------------------------
#            Purchase Propensity
# --------------------------------------------
@app.callback(
    Output(component_id='propensity_states', component_property='options'),
    [Input(component_id='propensity_regions', component_property='value')]
)
def update_state(selected_region):
    return [{'label': state, 'value': state} for state in REGIONS[selected_region] if
            state not in ['WP (Putrajaya)', 'WP (Labuan)', 'Perlis']]

#--------------------------------------------
#                Mix Modeler
#--------------------------------------------
@app.callback(
    [
        Output(component_id='mix_curiosity', component_property='children'),
        Output(component_id = 'mix_intention', component_property = 'children'),
        Output(component_id = 'mix_action', component_property = 'children'),
    ],
    [
        Input('mix-press', 'value'),
        Input('mix-outdoor', 'value'),
        Input('mix-radio', 'value'),
        Input('mix-tv', 'value'),
        Input('mix-programmatic', 'value'),
        Input('mix-search', 'value'),
        Input('mix-video', 'value'),
        Input('mix-youtube', 'value'),
        Input('mix-other', 'value'),

    ]
)
def update_overview(
        press, outdoor, radio, tv, progr, search, fb, youtube, other
):
    # conversations = - 66 * press + 435 * outdoor - 64 * radio + 24 * tv + 169 * progr + 563 * search - 314 * fb - 16 * youtube + 607 * other
    # curiosity = -104 * press + 213 * outdoor + 146 * radio - 25 * tv + 334 * progr - 971 * search - 484 * fb + 511 * youtube - 492 * other
    # action = - 508 * press + 9765 * outdoor + 15 * radio + 171 * tv + 208 * progr + 9853 * search + 2549 * fb - 3494 * youtube + 1143 * other

    curiosity = 896 * press + 1213 * outdoor + 1146 * radio - 975 * tv + 1334 * progr + 29 * search + 516 * fb + 1511 * youtube + 508 * other
    intention = 434 * press + 935 * outdoor + 436 * radio + 524 * tv + 669 * progr + 1063 * search + 186 * fb + 484 * youtube + 1107 * other
    action = 3496 * press + 13765 * outdoor + 4015 * radio + 4171 * tv + 4208 * progr + 13853 * search + 6549 * fb + 506 * youtube + 5143 * other

    curiosity, intention, action = curiosity / 2, intention / 5, action / 250
    # return '# **{}**'.format(round(curiosity, 0)), '# **{}**'.format(round(intention, 0)),  '# **{}**'.format(round(action, 0))
    return '# **{}**'.format(int(curiosity)), '# **{}**'.format(int(intention)),  '# **{}**'.format(int(action))


#--------------------------------------------
#                    Pages
#--------------------------------------------
app.layout = html.Div(
    [
        logos,
        dates,
        tabs
    ]
)


if __name__ == '__main__':
    app.run_server(debug = True, host = '0.0.0.0', port = 10000)

