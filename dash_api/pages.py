import dash_html_components as html
import dash_core_components as dcc
from dash_table import DataTable
from controls import REGIONS, STATES, PRODUCTS
import datetime as dt
#from bucket_analysis import bucket_an


region_options = [{'label': str(region), 'value': str(region)}
                  for region in REGIONS]


product_options = [{'label': product, 'value': product} for  product in PRODUCTS]

tabs_styles = {
    'height': '44px'
}


tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'black',
    'color': 'white',
    'padding': '6px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
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

#---------------------------------------------------------
#                    Churn Predictor
#---------------------------------------------------------
def churn_predictor():
    filter_region = html.Div(
        [
            html.P(
                'Region:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id = 'churn_regions',
                options = region_options,
                multi = False,
                value = region_options[0]['label']
            ),
        ],
        className = 'four columns',
        style = {'margin-left': 20}
    )
    filter_state = html.Div(
        [
            html.P(
                'State:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id = 'churn_states',
                multi = True
            ),
        ],
        className = 'four columns',
        style = {'margin-left': 65}
    )

    filter_days = html.Div(
        [
            html.P(
                'Churn rate:',
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
            html.P('Download CSV:'),
            html.Button('Submit', id = 'churn_button')
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

    page = html.Div(
        [
            html.H2(
                'Churn Predictor',
                style = {
                    'margin-left': 20
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
            churn_graph
        ]
    )
    return page

#---------------------------------------------------------
#                  Purchase Propensity Score
#---------------------------------------------------------
def bucket_analysis():
    filter_region = html.Div(
        [
            html.P(
                'Region:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='bucket_regions',
                options = region_options,
                multi = False,
                value = region_options[0]['label'] # 'All Malaysia', #list(REGIONS.keys()),
            ),
        ],
        className='four columns',
        style = {'margin-left': 20}
    )
    filter_state = html.Div(
        [
            html.P(
                'State:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='bucket_states',
                multi = True
            ),
        ],
        className='four columns',
        style = {'margin-left': 65}
    )
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
            html.P('Get report:'),
            html.Button('Submit', id = 'bucket_button')
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
                    'backgroundColor': 'white',
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
#                    'width': '300px',
                    'margin-top': 10
                },
                style_cell={'textAlign': 'center'},
                style_header={
                    'backgroundColor': 'white',
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
                'Purchase Propensity Score',
                style = {
                    'margin-left': 20
                }
            ),
            filters,
            tables
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
    filter_region = html.Div(
        [
            html.P(
                'Region:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='forecast_regions',
                options = region_options,
                multi = False,
                value = region_options[0]['label'] # 'All Malaysia', #list(REGIONS.keys()),
            ),
        ],
        className='four columns',
        style = {'margin-left': 20}
    )
    filter_state = html.Div(
        [
            html.P(
                'State:',
                style = {'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='forecast_states',
                multi = True
            ),
        ],
        className='four columns',
        style = {'margin-left': 65}
    )
    filter_days = html.Div(
        [
            html.P(
                'Days to forecast:',
                style={'margin-bottom': 5}
            ),
            dcc.Dropdown(
                id='forecast_days',
                options = [{'label': x, 'value':x} for x in range(1,31)],
                multi=False,
                value = 5
            ),
        ],
        className='two columns',
        style={'margin-left': 65}
    )


    button = html.Div(
        [
            html.P('Get report:'),
            html.Button('Submit', id = 'forecast_button')
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
            html.Div(
                [
                    dcc.Graph(
                        id = 'forecast_graph'
                    )
                ],
                className = 'twelve columns',

            ),
        ],
        className='row',
        style={'margin-top': 50}
    )

    page = html.Div(
        [
            html.H2(
                'Sales Forecasting',
                style={
                    'margin-left': 20
                }
            ),
            filters,
            html.H4(
                'Choose period, location and time to forecasting. After that wait for few seconds.',
                style={
                    'margin-left': 20
                }
            ),
            # left_table,
            # right_table
            forecast_graph
        ],
        # style = {
        #     'backgroundColor':'#d3d3d3'
        # }
    )
    return page

#---------------------------------------------------------
#                    Revenue per Dollar
#---------------------------------------------------------
def revenue_per_dollar():
    pass

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
    slider_fb = html.Div(
        [
            html.P(
                'Facebook and Instagram:',
                style={'margin-bottom': 5}
            ),
            dcc.Slider(
                id='mix-fb',
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
                #vertical='True'
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
            slider_fb,
            slider_youtube,
            slider_other
        ],
        style={'margin-top': 25},
        className = 'row'
    )
    # ----------------------
    convers = html.Div(
        [
            dcc.Markdown('## Conversations (monthly)'),
            dcc.Markdown(id='mix_conv')
        ],
        className='four columns',
        style={
            'backgroundColor': '#dcf2ff',
            'width': 400,
            'height': 200,
            'margin-left': 120,
            'textAlign': 'center'
        }
    )
    curiosity = html.Div(
        [
            dcc.Markdown('## Curiosity'),
            dcc.Markdown(id='mix_curiosity')
        ],
        className='four columns',
        style={
            'backgroundColor': '#dcf2ff',
            'width': 400,
            'height': 200,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    traffic = html.Div(
        [
            dcc.Markdown('## Traffic'),
            dcc.Markdown(id='mix_traffic')
        ],
        className='four columns',
        style={
            'backgroundColor': '#dcf2ff',
            'width': 400,
            'height': 200,
            'margin-left': 80,
            'textAlign': 'center'
        }
    )
    line = html.Div(
        [
            convers,
            curiosity,
            traffic
        ],
        style={
            'margin-top': 100
        },
        className='row'
    )


    page = html.Div(
        [
            html.H2(
                'Mix modeler',
                style={
                    'margin-left': 20
                }
            ),
            filters_1,
            filters_2,
            filters_3,
            line
        ],
        # style = {
        #     'backgroundColor':'#d3d3d3'
        # }
    )
    return page



tabs = dcc.Tabs(
    id = 'tabs_names',
    value = 'tab-1',
    children = [
        dcc.Tab(children = churn_predictor(), label = 'Churn Predictor', value = 'tab-1', style = tab_style, selected_style = tab_selected_style),
        dcc.Tab(children = bucket_analysis(), label = 'Purchase Propensity Score', value = 'tab-2', style = tab_style, selected_style = tab_selected_style),
        dcc.Tab(children = sales_forecasting(), label = 'Sales Forecasting', value = 'tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(children = revenue_per_dollar(), label = 'Revenue per MYR', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(children = mix_modeler(), label = 'Mix Modeler', value='tab-5', style=tab_style, selected_style=tab_selected_style),
    ],
    style=tabs_styles,
    className='row'
)
