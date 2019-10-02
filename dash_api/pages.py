import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from controls import REGIONS, STATES, PRODUCTS, PRODUCTS_GROUPS
import datetime as dt
#from bucket_analysis import bucket_an


region_options = [{'label': str(region), 'value': str(region)}
                  for region in REGIONS]


product_options = [{'label': product, 'value': product} for  product in PRODUCTS]
prod_gr_options = [{'label': product, 'value': product} for  product in PRODUCTS_GROUPS]

FONT = 'Open Sans'
MAIN_COLOR = '#0074D9'

tab_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': '800',
    'font-family': FONT,
    'font-size': 18,
    'backgroundColor': '#f2f2f2', ##103350',
    'color': '#103350', #'white',
    'padding': '14px'
}

tabs_styles = {
    'height': '60px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'fontWeight': '800',
    'font-family': FONT,
    'font-size': 18,
    'backgroundColor': '#55bcad', # '#27b9f2',
    'color': '#103350', #'black',
    'padding': '14px'
}


def marks(i_min, i_max):
    dt_dict = dict()
    for i in range(i_min, i_max + 1):
        dt_iter = dt.datetime(2017, 1, 1).date() + dt.timedelta(days = i)
        if dt_iter.day ==1 and dt_iter.month % 3 == 0:
            dt_dict[i] = {
                'style': {
                    'margin-top': -35
                },
                'label': dt_iter
            }
    return dt_dict

all_buttons = dcc.Markdown(
    children = [0,0,0,0,0,0,0],
    id = 'all_buttons'
)

def f_region(id):
    text = html.P(
        'Region:',
        style = {'margin-bottom': 5}
    )
    dropdown = dcc.Dropdown(
        id = id,
        options = region_options,
        multi = False,
        value = region_options[0]['label']
    )
    out = html.Div(
        [
            text,
            dropdown
        ],
        className = 'four columns',
        style = {'margin-left': 20}
    )
    return out

def f_state(id):
    text = html.P(
        'State:',
        style = {'margin-bottom': 5}
    )
    dropdown = dcc.Dropdown(
        id = id,
        options = region_options,
        multi = True,
    )
    out = html.Div(
        [
            text,
            dropdown
        ],
        className = 'four columns',
        style = {'margin-left': 65}
    )
    return out


#---------------------------------------------------------
#                    Churn Predictor
#---------------------------------------------------------
def churn_predictor():
    filter_region = f_region('churn_regions')
    filter_state = f_state('churn_states')

    filter_days = html.Div(
        [
            html.P(
                'Extract CR greater than:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='churn_rate',
                options = [{'label': '{}%'.format(60 + 5 * x), 'value': (60 + 5 * x) /100} for x in range(8)],
                multi=False,
                value = 0.7
            ),
        ],
        className='two columns',
        style={'margin-left': 65}
    )

    button = html.Div(
        [
            html.P('Push the button:'),
            html.Button('Get CSV', id = 'churn_button')
        ],
        className = 'one column'
    )
    filters = html.Div(
        [
            filter_region,
            filter_state,
            filter_days,
            button
        ],
        className='row'
    )
    churn_graph = html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='churn_graph'
                    )
                ],
                className='twelve columns',

            ),
        ],
        className='row',
        style={'margin-top': 50}
    )

    churn_graph_comparison = html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='churn_graph_comparison'
                    )
                ],
                className='twelve columns',

            ),
        ],
        className='row',
        style={'margin-top': 100}
    )

    page = html.Div(
        [
            html.H2(
                'Churn Predictor',
                style = {
                    'margin-left': 20,
                    'margin-top': 60,
                    'margin-down': 30,
                    'font-family': FONT,
                    'font-size': '36px',
                    'fontWeight': 400,
                    'textAlign': 'center'
                }
            ),
            filters,
            html.Div(
                [
                    dcc.Markdown(id = 'churn_text')
                ],
                style={
                    'color':'red',
                    'margin-left': 20,
                    'textAlign': 'left'
                }
            ),
            churn_graph,
            churn_graph_comparison
        ]
    )
    return page

#---------------------------------------------------------
#                  Correlative Targeting
#---------------------------------------------------------
def bucket_analysis():
    filter_region = f_region('bucket_regions')
    filter_state = f_state('bucket_states')

    filter_product = html.Div(
        [
            html.P(
                'Product:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='bucket_product',
                options = product_options,
                multi=False,
                value=product_options[0]['label']
            ),
        ],
        className='two columns',
        style={'margin-left': 65}
    )
    button = html.Div(
        [
            html.P('Push the button:'),
            html.Button('Get CSV', id = 'bucket_button')
        ],
        className = 'one column'
    )
    filters = html.Div(
        [
            filter_region,
            filter_state,
            filter_product,
            button
        ],
        className='row'
    )

    # LEFT TABLE
    l_drop = html.Div(
        [
            html.P(
                'Number of products:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id = 'bucket_drop_sales',
                options = [{'label': 5 * i, 'value': 5 * i} for i in range(1, 21)],
                value = 10
            )
        ],
        className = 'three columns'
    )
    l_search = html.Div(
        [
            html.P(
                'Find product:',
                style = {'margin-bottom': 5}
            ),
            dcc.Input(
                id='bucket_search_sales',
                value = '',
                type = 'text'
            ),
        ],
        style = {'margin-left': 315},
        className='two columns'
    )
    left_table = html.Div(
        [
            html.H5('TOP products (expected value):'),
            html.Div(
                [
                    l_drop,
                    l_search
                ],
                className = 'row'
            ),
            DataTable(
                id = 'bucket_sales',
                columns=[{'name': i, 'id': i} for i in ['Number', 'Product Name', 'Sales (RM)']],
                style_table = {
                    'overflowY': 'scroll',
                    'height': '300px',
                    'margin-top': 10
                },
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': MAIN_COLOR,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            )
        ],
        className = 'five columns',
        style = {
            'margin-top': 20,
            'margin-left': 20
        }
    )

    # RIGHT TABLE
    r_drop = html.Div(
        [
            html.P(
                'Number of products:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='bucket_drop_dockets',
                options = [{'label': 5 * i, 'value': 5 * i} for i in range(1, 21)],
                value = 10
            )
        ],
        className = 'three columns'
    )
    r_search = html.Div(
        [
            html.P(
                'Find product:',
                style = {'margin-bottom': 5}
            ),
            dcc.Input(
                id = 'bucket_search_dockets',
                value = '',
                type = 'text'
            ),
        ],
        style = {'margin-left': 315},
        className='two columns'
    )
    right_table = html.Div(
        [
            html.H5('TOP products (probability):'),
            html.Div(
                [
                    r_drop,
                    r_search
                ],
                className = 'row'
            ),
            DataTable(
                id='bucket_dockets',
                columns=[{'name': i if i!= 'Dockets' else '%', 'id': i} for i in ['Number', 'Product Name', 'Dockets']],
                style_table = {
                    'overflowY': 'scroll',
                    'height': '300px',
                    'margin-top': 10
                },
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': MAIN_COLOR,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            )
        ],
        className = 'five columns',
        style = {
            'margin-top': 20,
            'margin-left': 200
        }
    )
    tables = html.Div(
        [
            left_table,
            right_table
        ],
        className='row'
    )

    page = html.Div(
        [
            html.H2(
                'Correlative Targeting',
                style = {
                    'margin-left': 20,
                    'margin-top': 60,
                    'margin-down': 30,
                    'font-family': FONT,
                    'font-size': '36px',
                    'fontWeight': 400,
                    'textAlign': 'center'
                }
            ),
            filters,
            tables
        ],
    )
    return page

#---------------------------------------------------------
#                    Purchase Propensity
#---------------------------------------------------------
def purchase_propensity():
    filter_region = f_region('propensity_regions')
    filter_state = f_state('propensity_states')

    filter_product = html.Div(
        [
            html.P(
                'Product:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id = 'propensity_product',
                options = prod_gr_options,
                multi=False,
                value = prod_gr_options[0]['label']
            ),
        ],
        className='two columns',
        style={'margin-left': 65}
    )

    button = html.Div(
        [
            html.P('Push the button:'),
            html.Button('GET CSV', id = 'propensity_button')
        ],
        className = 'one column'
    )
    filters = html.Div(
        [
            filter_region,
            filter_state,
            filter_product,
            button
        ],
        className='row'
    )

    # PLOT
    comparison_plot = html.Div(
        [
            html.H5(
                'Choose location and product to see the plot.'
            ),
            dcc.Graph(
                id='propensity_graph'
            )
        ],
        className='six columns',
        style={
            'margin-top': 20,
            'margin-left': 20
        }
    )

    # TABLE
    drop = html.Div(
        [
            html.P(
                'Number of customers:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='propensity_drop_number',
                options=[{'label': 5 * i, 'value': 5 * i} for i in range(1, 21)],
                value=10
            )
        ],
        className='three columns'
    )
    search = html.Div(
        [
            html.P(
                'Find customer:',
                style={'margin-bottom': 5}
            ),
            dcc.Input(
                id='propensity_search',
                value='',
                type='text'
            ),
        ],
        style={'margin-left': 315},
        className='two columns'
    )
    table = html.Div(
        [
            html.H5('TOP customers by score:'),
            html.Div(
                [
                    drop,
                    search
                ],
                className = 'row'
            ),
            DataTable(
                id='propensity_score',
                columns=[{'name': i, 'id': i} for i in ['Number', 'Customer Email', 'Score, %']],
                style_table={
                    'overflowY': 'scroll',
                    'height': '300px',
                    'margin-top': 10
                },
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': MAIN_COLOR,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            )
        ],
        className='five columns',
        style={
            'margin-top': 20,
            'margin-left': 20
        }
    )

    tables = html.Div(
        [
            comparison_plot,
            table
        ],
        className='row'
    )

    page = html.Div(
        [
            html.H2(
                'Purchase Propensity',
                style = {
                    'margin-left': 20,
                    'margin-top': 60,
                    'margin-down': 30,
                    'font-family': FONT,
                    'font-size': '36px',
                    'fontWeight': 400,
                    'textAlign': 'center'
                }
            ),
            filters,
            html.Div(
                [
                    dcc.Markdown(id='propensity_text')
                ],
                style={
                    'color': 'red',
                    #'margin-top': 20,
                    'margin-left': 20,
                    'textAlign': 'left'
                }
            ),
            tables
        ]
    )
    return page

#---------------------------------------------------------
#                    Mix Modeler
#---------------------------------------------------------
def mix_modeler():
    slider_press = html.Div(
        [
            html.P(
                'Press:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-press',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                #vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_outdoor = html.Div(
        [
            html.P(
                'Outdoor:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-outdoor',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                #vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_radio = html.Div(
        [
            html.P(
                'Radio:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-radio',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                # vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    filters_1 = html.Div(
        [
            slider_press,
            slider_outdoor,
            slider_radio
        ],
        className = 'row'
    )
    #----------------------
    slider_tv = html.Div(
        [
            html.P(
                'TV:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-tv',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                #vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_programmatic = html.Div(
        [
            html.P(
                'Programmatic:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-programmatic',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                #vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_search = html.Div(
        [
            html.P(
                'Search:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id = 'mix-search',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                # vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    filters_2 = html.Div(
        [
            slider_tv,
            slider_programmatic,
            slider_search
        ],
        style={'margin-top': 25},
        className = 'row'
    )
    #----------------------
    slider_video = html.Div(
        [
            html.P(
                'Video:',
                style = {'margin-bottom': 5}
            ),
            dcc.Slider(
                id = 'mix-video',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_youtube = html.Div(
        [
            html.P(
                'Youtube:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-youtube',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    slider_other = html.Div(
        [
            html.P(
                'Other Digital:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id = 'mix-other',
                min = 0,
                max = 400,
                value = 20,
                marks={i * 100: '{}'.format(i * 100000) for i in range(5)},
                # vertical='True'
            )
        ],
        className='three columns',
        style={'margin-left': 120}
    )
    filters_3 = html.Div(
        [
            slider_video,
            slider_youtube,
            slider_other
        ],
        style={'margin-top': 25},
        className = 'row'
    )
    # ----------------------
    curiosity = html.Div(
        [
            dcc.Markdown('## Curiosity'),
            dcc.Markdown(id='mix_curiosity')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 200,
            'margin-left': 120,
            'textAlign': 'center'
        }
    )
    intention = html.Div(
        [
            dcc.Markdown('## Intention'),
            dcc.Markdown(id='mix_intention')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 200,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )

    action = html.Div(
        [
            dcc.Markdown('## Action'),
            dcc.Markdown(id='mix_action')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 200,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    line = html.Div(
        [
            curiosity,
            intention,
            action
        ],
        style={
            'margin-top': 100
        },
        className='row'
    )

    investment_input = html.Div(
        [
            html.P(
                'Type investment in MYR:',
                style = {'margin-bottom': 5}
            ),
            dcc.Input(
                id = 'mix_investment',
                value = '1000000',
                type = 'text'
            ),
        ],
        className='row',
        style = {
            'margin-top': 20,
            'margin-left': 20
        }
    )

    # ----------------------
    press = html.Div(
        [
            dcc.Markdown('## Press'),
            dcc.Markdown(id='mix_press')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 120,
            'textAlign': 'center'
        }
    )
    outdoor = html.Div(
        [
            dcc.Markdown('## Outdoor'),
            dcc.Markdown(id='mix_outdoor')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    radio = html.Div(
        [
            dcc.Markdown('## Radio'),
            dcc.Markdown(id='mix_radio')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    investment_output_1 = html.Div(
        [
            press,
            outdoor,
            radio
        ],
        style={
            'margin-top': 20
        },
        className='row'
    )

    tv = html.Div(
        [
            dcc.Markdown('## TV'),
            dcc.Markdown(id='mix_tv')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 120,
            'textAlign': 'center'
        }
    )
    programmatic = html.Div(
        [
            dcc.Markdown('## Programmatic'),
            dcc.Markdown(id='mix_programmatic')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    search = html.Div(
        [
            dcc.Markdown('## Search'),
            dcc.Markdown(id='mix_search')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    investment_output_2 = html.Div(
        [
            tv,
            programmatic,
            search
        ],
        style={
            'margin-top': 20
        },
        className='row'
    )

    video = html.Div(
        [
            dcc.Markdown('## Video'),
            dcc.Markdown(id='mix_video')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 120,
            'textAlign': 'center'
        }
    )
    youtube = html.Div(
        [
            dcc.Markdown('## Youtube'),
            dcc.Markdown(id='mix_youtube')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    other_digital = html.Div(
        [
            dcc.Markdown('## Other Digital'),
            dcc.Markdown(id='mix_other_digital')
        ],
        className='four columns',
        style={
            'backgroundColor': MAIN_COLOR,
            'color': 'white',
            'width': 400,
            'height': 120,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    investment_output_3 = html.Div(
        [
            video,
            youtube,
            other_digital
        ],
        style={
            'margin-top': 20,
            'margin-down': 20,
            'padding-down': 20
        },
        className='row'
    )




    page = html.Div(
        [
            html.H2(
                'Mix modeler',
                style={
                    'margin-left': 20,
                    'margin-top': 60,
                    'margin-down': 30,
                    'font-family': FONT,
                    'font-size': '36px',
                    'fontWeight': 400,
                    'textAlign': 'center'
                }
            ),
            filters_1,
            filters_2,
            filters_3,
            line,
            html.H2(
                'Recommendation Plan',
                style={
                    'margin-left': 20,
                    'margin-top': 60
                }
            ),
            investment_input,
            investment_output_1,
            investment_output_2,
            investment_output_3,
            html.Div(style={'padding': 10})
        ],
        # style = {
        #     'backgroundColor':'#d3d3d3'
        # }
    )
    return page

#---------------------------------------------------------
#                 Sales Forecasting
#---------------------------------------------------------
def sales_forecasting():
    filter_region = f_region('forecast_regions')
    filter_state = f_state('forecast_states')

    filter_days = html.Div(
        [
            html.P(
                'Period to forecast:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='forecast_period',
                options = [{'label': x, 'value':x} for x in ['week', 'month', 'quarter', '6 months', 'year']],
                multi = False,
                value = 'month'
            ),
        ],
        className='two columns',
        style={'margin-left': 65}
    )

    button = html.Div(
        [
            html.P('Push the button:'),
            html.Button('Get CSV', id = 'forecast_button')
        ],
        className = 'one column'
    )
    filters = html.Div(
        [
            filter_region,
            filter_state,
            filter_days,
            button
        ],
        className='row'
    )
    forecast_graph = html.Div(
        [
            html.H5(
                'Choose period, location and period to forecast. After that wait for few seconds.'
            ),
            dcc.Graph(
                id = 'forecast_graph'
            )
        ],
        className = 'eight columns',
        style={
            'margin-top': 50,
            'margin-left': 20
        }
    )

    forecast_table = html.Div(
        [
            html.H5('Sales Forecasting (weekly):'),
            DataTable(
                id='forecast_table',
                columns=[{'name': i, 'id': i} for i in ['Week_Date', 'Forecast, RM']],
                style_table = {
                    'overflowY': 'scroll',
                    'height': '450px',
                    'margin-top': 5
                },
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': MAIN_COLOR,
                    'color': 'white',
                    'fontWeight': 'bold'
                },
            )
        ],
        className = 'three columns',
        style = {
            'margin-top': 50,
            'margin-left': 20
        }
    )

    page = html.Div(
        [
            html.H2(
                'Sales Forecasting',
                style={
                    'margin-left': 20,
                    'margin-top': 60,
                    'margin-down': 30,
                    'font-family': FONT,
                    'font-size': '36px',
                    'fontWeight': 400,
                    'textAlign': 'center'
                }
            ),
            filters,
            forecast_graph,
            forecast_table
        ]
    )
    return page


tabs = dcc.Tabs(
    id = 'tabs_names',
    value = 'tab-1',
    children = [
        dcc.Tab(children = churn_predictor(), label = 'Churn Predictor', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
        dcc.Tab(children = bucket_analysis(), label = 'Correlative Targeting', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
        dcc.Tab(children = purchase_propensity(), label = 'Purchase Propensity', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(children = mix_modeler(), label = 'Mix Modeler', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(children = sales_forecasting(), label = 'Sales Forecasting', value = 'tab-5', style=tab_style, selected_style=tab_selected_style),
    ],
    style = tabs_styles,
    className = 'row'
)
