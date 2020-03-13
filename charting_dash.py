import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
import pyo
# import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

import pandas as pd
import itertools as it

import chart_library as cl
import decision_tree as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{
                    'name': 'viewport',
                    'content': 'width=device-width, initial-scale=1.0'
                    }]
                )

server = app.server

app.config['suppress_callback_exceptions'] = True

ddoptions = [
    {"label": "Category", "value": "CAT"},
    {"label": "Date", "value": "DTE"},
    {"label": "Value", "value": "VAL"},
    {"label": "Boolean", "value": "BOL"},
    {"label": "Location", "value": "LOC"},
    {"label": "Latitude", "value": "LAT"},
    {"label": "Longitude", "value": "LON"},
    ]   

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '99%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Label("File List"),
    html.Br(),
    html.Ul(id="complete-upload"),

    html.Br(),
    html.Label('Once your data has been uploaded click on "Load Columns"'),

    html.Br(),
    html.Button(
        id='propagate-button',
        n_clicks=0,
        children='Load Columns'
    ),
    html.Br(),
    html.Br(),
    html.Label(id='column-checklist_text'),
    html.Br(),
    dcc.Checklist(id='column-checklist',
                    labelStyle = {
                        'display': 'inline-block',
                        'marginRight': 10,
                        'value':[]
                        }),

    # dcc.Graph(id='Mygraph'),
    # html.Div(id = 'complete-df',
    #         # children = [data_dict],
    #         style = {'display': 'none'}),

    dcc.Store(id='complete-df'),


    # html.Div(id='display-selected-values'),
    html.Br(),
    html.Label(id='data-type-text'),
    html.Br(),
    html.Div(id='choosen_columns_data'),
    html.Br(),
    html.Div(id='submit_button'),

    html.Label(id ='mydropdown-1'),
    html.Label(id ='mydropdown-2'),
    html.Label(id ='mydropdown-3'),
    html.Label(id ='mydropdown-4'),
    html.Label(id ='mydropdown-5'),
    html.Label(id ='mydropdown-6'),

    html.Br(),
    # html.Div(id='dropdown-values2', style = {'display': 'none'}),
    # html.Div(id='dropdown-values3', style = {'display': 'none'}),
    # html.Div(id='dropdown-values4', style = {'display': 'none'}),
    # html.Div(id='dropdown-values5', style = {'display': 'none'}),
    # html.Div(id='dropdown-values6', style = {'display': 'none'}),


    html.Div(id='reset_button', style = {'display': 'none'}),
 

    html.Div(id='dropdown-values2'),
    html.Div(id='dropdown-values3'),
    html.Div(id='dropdown-values4'),
    html.Div(id='dropdown-values5'),
    html.Div(id='dropdown-values6'),
    ])

##Upload Data

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

##Show when a file is uploaded
@app.callback(
                Output('complete-upload', 'children'),

                [Input('upload-data', 'filename')]
            )

def upload_complete(filename):

    filename = filename

    if filename is None:
        return [html.Li("No files have been loaded yet!")]
    else:
        return [html.Li(filename) for filename in filename]

####Create dataframe

@app.callback(
                Output('complete-df', 'data'),

                [
                Input('propagate-button', 'n_clicks'),
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
                ]
            )


def create_df(n_clicks_update, contents, filename):

    if n_clicks_update < 1:
        print("df empty")
        return []

    else:

        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            df = df.to_json()
            
        # return df.to_dict('records')
        return df


## Display Select Columns Text
@app.callback(
                Output('column-checklist_text', 'children'),
                [
                Input('propagate-button', 'n_clicks'),
                ]
            )

def update_columns(n_clicks_update):

    if n_clicks_update < 1:
        print("df empty")
        return []

    else:
 
        return [html.Label("Select between two and six columns to visualize:")]

## Get Column Names when button is clicked and create check list
@app.callback(
                Output('column-checklist', 'options'),
                [
                Input('propagate-button', 'n_clicks'),
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
                ]
            )

def update_columns(n_clicks_update, contents, filename):

    if n_clicks_update < 1:
        print("df empty")
        return []

    else:

        if contents:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            column_head = [{'label': i, 'value': i} for i in df.columns]

        return column_head

## Display Select Data type Text
@app.callback(
                Output('data-type-text', 'children'),
                [
                Input('column-checklist', 'value'),
                ]
            )

def update_columns(col_value):
    
    try:
        if len(col_value) is None:
            print("df empty")
            return []
        else:
            print(len(col_value))
            return [html.Label("Select the data type for each column:")]
    except:
        None



# hide unused graph id's
@app.callback(
                
                Output('dropdown-values2', 'style'),
                [
                Input('column-checklist', 'value'),
                ],
                [
                State('dropdown-values2', 'style')    
                ]
            )

def hide_ids2(col_values, current_style):

    try: 
        if len(col_values) == 2:
            current_style['display'] = ''
            print(f"{len(col_values)}s have been clicked display all 2")
        else:
            current_style['display'] = 'none'
            print(f"{len(col_values)}s have been clicked dont display 2")
        return current_style

    except:
        None

# hide unused graph id's
@app.callback(
                Output('dropdown-values3', 'style'),
                [
                Input('column-checklist', 'value'),
                ],
                [
                State('dropdown-values3', 'style')    
                ]
            )

def hide_ids3(col_values, current_style):

    try:
        if len(col_values) == 3:
            current_style['display'] = ''
            print(f"{len(col_values)}s have been clicked display all 3")
        else:
            current_style['display'] = 'none'
            print(f"{len(col_values)}s have been clicked dont display 3")
        return current_style

    except:
        None

# hide unused graph id's
@app.callback(
                Output('dropdown-values4', 'style'),
                [
                Input('column-checklist', 'value'),
                ],
                [
                State('dropdown-values4', 'style')    
                ]
            )

def hide_ids4(col_values, current_style):

    try:
        if len(col_values) == 4:
            current_style['display'] = ''
            print(f"{len(col_values)}s have been clicked display all 4")
        else:
            current_style['display'] = 'none'
            print(f"{len(col_values)}s have been clicked dont display 4")
        return current_style

    except:
        None

# hide unused graph id's
@app.callback(
                Output('dropdown-values5', 'style'),
                [
                Input('column-checklist', 'value'),
                ],
                [
                State('dropdown-values5', 'style')    
                ]
            )

def hide_ids5(col_values, current_style):

    try:
        if len(col_values) == 5:
            current_style['display'] = ''
            print(f"{len(col_values)}s have been clicked display all 5")
        else:
            current_style['display'] = 'none'
            print(f"{len(col_values)}s have been clicked dont display 5")
        return current_style

    except:
        None


# hide unused graph id's
@app.callback(
                Output('dropdown-values6', 'style'),
                [
                Input('column-checklist', 'value'),
                ],
                [
                State('dropdown-values6', 'style')    
                ]
            )

def hide_ids6(col_values, current_style):

    try:
        if len(col_values) == 6:
            current_style['display'] = ''
            print(f"{len(col_values)}s have been clicked display all 6")
        else:
            current_style['display'] = 'none'
            print(f"{len(col_values)}s have been clicked dont display 6")
        return current_style

    except:
        None


# List selected columns with dropdowns for data type
@app.callback(
                Output('choosen_columns_data', 'children'),
                [
                Input('column-checklist', 'value'),
                ]
            )

def create_dropdowns(selected_col):

    ddcreator = []

    x=0
    try:    
        print(len(selected_col))
        for i in selected_col:
            x+=1
            dd =html.Div(
                    html.Label(
                        [i,
                        dcc.Dropdown(
                            id=f"mydropdown-{x}",
                            # id="mydropdown-1",
                            className=i,
                            options = ddoptions,
                            persistence_type = 'memory',
                            persistence = True
                            )
                        ]
                    ),
                style={'width': '20%','marginRight': 10, 'display': 'inline-block'}
                # style={'width': f'{col_width}%','marginRight': 10, 'display': 'inline-block'}
                )
            

            ddcreator.append(dd)
    except:
        None


    return ddcreator

## Submit Button
@app.callback(
                Output('submit_button', 'children'),
                [
                # Input('choosen_columns_data', 'values'),
                Input('column-checklist', 'value'),
                ]
            )

def update_columns(values):

    try:    
        if len(values) < 1:
            print("df empty")
            return []
        else:
            button = html.Div([
                    html.Button(id='submit-button',
                    n_clicks=0,
                    children='Submit'
                    ),
                    html.Button(id='refresh-button',
                    n_clicks=0,
                    children='Reset',
                    style={
                        'marginRight': 10
                    }
                    )
                ])

            return button
    except:
        None

##reset page
@app.callback(
                Output('reset_button', 'children'),
                [
                Input('refresh_button', 'n_clicks'),
                ]
            )

def reset_page(
                    n_clicks,
                    ):

    try:
        if n_clicks < 1:
            print("reset button has not been clicked")
            return []

        else:
            reset = html.A('Refresh', href='/')

            return reset
        
    except:
        None


##Call Back for 6 Columns
@app.callback(
                Output('dropdown-values6', 'children'),
                [
                Input('submit_button', 'n_clicks'),
                Input('choosen_columns_data', 'value'),
                Input('complete-df', 'data'),
                ],
                [
                State('mydropdown-1', 'className'),
                State('mydropdown-1', 'value'),
                State('mydropdown-2', 'className'),
                State('mydropdown-2', 'value'),
                State('mydropdown-3', 'className'),
                State('mydropdown-3', 'value'),
                State('mydropdown-4', 'className'),
                State('mydropdown-4', 'value'),
                State('mydropdown-5', 'className'),
                State('mydropdown-5', 'value'),
                State('mydropdown-6', 'className'),
                State('mydropdown-6', 'value'),
                ]
            )

def update_columns6(
                    n_clicks,
                    ddvalues,
                    dfdata, 
                    dd1class, dd1value,
                    dd2class, dd2value,
                    dd3class, dd3value,
                    dd4class, dd4value,
                    dd5class, dd5value,
                    dd6class, dd6value,
                    # *ddclass, **ddvalue,
                    ):

    try:
        if n_clicks < 1:
            print("no drop down values")
            return []

        else:
            list1 = []
            list2 = []

            # for i in ddclass:
            #     list1.append(ddclass)

            # print(list1)
            
            list1.append(dd1class)
            list1.append(dd2class)
            list1.append(dd3class)
            list1.append(dd4class)
            list1.append(dd5class)
            list1.append(dd6class)


            list2.append(dd1value)
            list2.append(dd2value)
            list2.append(dd3value)
            list2.append(dd4value)
            list2.append(dd5value)
            list2.append(dd6value)

            zipped = zip(list1, list2)
            d = dict(zipped)


            all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
            all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]

            # all_pairs3 = [{j: d[j] for j in i} for i in it.combinations(d, 3)]
            # all_pairs2 = [{j: d[j] for j in i} for i in it.combinations(d, 2)]
        

            data_pairsv = []
            data_pairsk = []
            data_pairsv1 = []
            data_pairsk1 = []


            for p in all_pairs2:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs2:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for p in all_pairs3:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs3:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for v in data_pairsv:
                data_pairsv1.append('vs'.join(v))

            for k in data_pairsk:
                data_pairsk1.append('vs'.join(k))

            zippedpairs = zip(data_pairsk1, data_pairsv1)
            finalpairs = dict(zippedpairs)

            # print(finalpairs)
            
            for k,v in finalpairs.items():
                if v == "CATvsVAL":
                    a = dt.decision([1,1,0,0,0,0])
                elif v == "CATvsLATvsLON":
                    # a = dt.decision([1,0,0,1,0,0])
                    a = ['Map']
                elif v == "LOCvsVAL":
                    a = dt.decision([1,0,0,1,0,0])
                elif v == "DTEvsVAL":
                    a = dt.decision([1,0,0,0,1,0])
                elif v == "VALvsVAL":
                    a = dt.decision([1,0,0,0,0,1])
                elif v == "VALvsBOL" or v == "CATvsBOL":
                    a = dt.decision([1,0,1,0,0,0])
                else:
                    a = "None"
                finalpairs[k] = a[0]

            # print(finalpairs)

            for k,v in list(finalpairs.items()):
                if v == "N":
                    del finalpairs[k]            
                        
            print(finalpairs)

            df = pd.read_json(dfdata)

            charts = []

            chartnum = 0

            for k,v in finalpairs.items():
                gcol = k.split('vs')
                xcol = gcol[0]
                ycol = gcol[1]
                try:
                    zcol = gcol[2]
                except:
                    None
                xval = df[xcol]
                yval = df[ycol]
                try:
                    zval = df[zcol]
                except:
                    None
                chartnum+=1
                if v == "Bar":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bar_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Map":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.map_function(xval,yval,zval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Rings":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.rings_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Bubble":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bubble_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Table":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.table_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Scatter":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.scatter_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Pie":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.pie_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Line":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.line_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))

            return charts
        
    except:
        None

# ##Call Back for 5 Columns
@app.callback(
                Output('dropdown-values5', 'children'),
                [
                Input('submit_button', 'n_clicks'),
                Input('choosen_columns_data', 'value'),
                Input('complete-df', 'data'),
                ],
                [
                State('mydropdown-1', 'className'),
                State('mydropdown-1', 'value'),
                State('mydropdown-2', 'className'),
                State('mydropdown-2', 'value'),
                State('mydropdown-3', 'className'),
                State('mydropdown-3', 'value'),
                State('mydropdown-4', 'className'),
                State('mydropdown-4', 'value'),
                State('mydropdown-5', 'className'),
                State('mydropdown-5', 'value'),
                ]
            )

def update_columns5(n_clicks, ddvalues,
                    dfdata, 
                    dd1class, dd1value,
                    dd2class, dd2value,
                    dd3class, dd3value,
                    dd4class, dd4value,
                    dd5class, dd5value,
                    ):
    try:

        if n_clicks < 1:
            print("no drop down values")
            return []

        else:

            list1 = []
            list2 = []
            
            list1.append(dd1class)
            list1.append(dd2class)
            list1.append(dd3class)
            list1.append(dd4class)
            list1.append(dd5class)

            list2.append(dd1value)
            list2.append(dd2value)
            list2.append(dd3value)
            list2.append(dd4value)
            list2.append(dd5value)

            zipped = zip(list1, list2)
            d = dict(zipped)


            all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
            all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]

            # all_pairs3 = [{j: d[j] for j in i} for i in it.combinations(d, 3)]
            # all_pairs2 = [{j: d[j] for j in i} for i in it.combinations(d, 2)]
        

            data_pairsv = []
            data_pairsk = []
            data_pairsv1 = []
            data_pairsk1 = []


            for p in all_pairs2:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs2:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for p in all_pairs3:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs3:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for v in data_pairsv:
                data_pairsv1.append('vs'.join(v))

            for k in data_pairsk:
                data_pairsk1.append('vs'.join(k))

            zippedpairs = zip(data_pairsk1, data_pairsv1)
            finalpairs = dict(zippedpairs)
            
            for k,v in finalpairs.items():
                if v == "CATvsVAL":
                    a = dt.decision([1,1,0,0,0,0])
                elif v == "CATvsLATvsLON":
                    # a = dt.decision([1,0,0,1,0,0])
                    a = ['Map']
                elif v == "LOCvsVAL":
                    a = dt.decision([1,0,0,1,0,0])
                elif v == "DTEvsVAL":
                    a = dt.decision([1,0,0,0,1,0])
                elif v == "VALvsVAL":
                    a = dt.decision([1,0,0,0,0,1])
                elif v == "VALvsBOL" or v == "CATvsBOL":
                    a = dt.decision([1,0,1,0,0,0])
                else:
                    a = "None"
                finalpairs[k] = a[0]

            # print(finalpairs)

            for k,v in list(finalpairs.items()):
                if v == "N":
                    del finalpairs[k]            
                        
            print(finalpairs)

            df = pd.read_json(dfdata)

            charts = []

            chartnum = 0

            for k,v in finalpairs.items():
                gcol = k.split('vs')
                xcol = gcol[0]
                ycol = gcol[1]
                try:
                    zcol = gcol[2]
                except:
                    None
                xval = df[xcol]
                yval = df[ycol]
                try:
                    zval = df[zcol]
                except:
                    None
                chartnum+=1
                if v == "Bar":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bar_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Map":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.map_function(xval,yval,zval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Rings":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.rings_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Bubble":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bubble_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Table":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.table_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Scatter":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.scatter_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Pie":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.pie_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Line":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.line_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))

            return charts
    except:
        None

# ##Call Back for 4 Columns
@app.callback(
                Output('dropdown-values4', 'children'),
                [
                Input('submit_button', 'n_clicks'),
                Input('choosen_columns_data', 'value'),
                Input('complete-df', 'data'),
                ],
                [
                State('mydropdown-1', 'className'),
                State('mydropdown-1', 'value'),
                State('mydropdown-2', 'className'),
                State('mydropdown-2', 'value'),
                State('mydropdown-3', 'className'),
                State('mydropdown-3', 'value'),
                State('mydropdown-4', 'className'),
                State('mydropdown-4', 'value'),
                ]
            )

def update_columns4(n_clicks, ddvalues,
                    dfdata,
                    dd1class, dd1value,
                    dd2class, dd2value,
                    dd3class, dd3value,
                    dd4class, dd4value,
                    ):

    try:
        if n_clicks < 1:
            print("no drop down values")
            return []

        else:

            list1 = []
            list2 = []
            
            list1.append(dd1class)
            list1.append(dd2class)
            list1.append(dd3class)
            list1.append(dd4class)


            list2.append(dd1value)
            list2.append(dd2value)
            list2.append(dd3value)
            list2.append(dd4value)

            zipped = zip(list1, list2)
            d = dict(zipped)


            all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
            all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]

            # all_pairs3 = [{j: d[j] for j in i} for i in it.combinations(d, 3)]
            # all_pairs2 = [{j: d[j] for j in i} for i in it.combinations(d, 2)]
        

            data_pairsv = []
            data_pairsk = []
            data_pairsv1 = []
            data_pairsk1 = []


            for p in all_pairs2:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs2:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for p in all_pairs3:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs3:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for v in data_pairsv:
                data_pairsv1.append('vs'.join(v))

            for k in data_pairsk:
                data_pairsk1.append('vs'.join(k))

            zippedpairs = zip(data_pairsk1, data_pairsv1)
            finalpairs = dict(zippedpairs)
            
            for k,v in finalpairs.items():
                if v == "CATvsVAL":
                    a = dt.decision([1,1,0,0,0,0])
                elif v == "CATvsLATvsLON":
                    # a = dt.decision([1,0,0,1,0,0])
                    a = ['Map']
                elif v == "LOCvsVAL":
                    a = dt.decision([1,0,0,1,0,0])
                elif v == "DTEvsVAL":
                    a = dt.decision([1,0,0,0,1,0])
                elif v == "VALvsVAL":
                    a = dt.decision([1,0,0,0,0,1])
                elif v == "VALvsBOL" or v == "CATvsBOL":
                    a = dt.decision([1,0,1,0,0,0])
                else:
                    a = "None"
                finalpairs[k] = a[0]

            # print(finalpairs)

            for k,v in list(finalpairs.items()):
                if v == "N":
                    del finalpairs[k]            
                        
            print(finalpairs)

            df = pd.read_json(dfdata)

            charts = []

            chartnum = 0

            for k,v in finalpairs.items():
                gcol = k.split('vs')
                xcol = gcol[0]
                ycol = gcol[1]
                try:
                    zcol = gcol[2]
                except:
                    None
                xval = df[xcol]
                yval = df[ycol]
                try:
                    zval = df[zcol]
                except:
                    None
                chartnum+=1
                if v == "Bar":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bar_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Map":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.map_function(xval,yval,zval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Rings":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.rings_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Bubble":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bubble_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Table":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.table_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Scatter":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.scatter_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Pie":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.pie_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Line":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.line_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))

            print('4 columns')
            
            return charts

    except:
        None

# ##Call Back for 3 Columns
@app.callback(
                Output('dropdown-values3', 'children'),
                [
                Input('submit_button', 'n_clicks'),
                Input('choosen_columns_data', 'value'),
                Input('complete-df', 'data'),
                ],
                [
                State('mydropdown-1', 'className'),
                State('mydropdown-1', 'value'),
                State('mydropdown-2', 'className'),
                State('mydropdown-2', 'value'),
                State('mydropdown-3', 'className'),
                State('mydropdown-3', 'value'),
                ]
            )

def update_columns3(n_clicks, ddvalues,
                    dfdata, 
                    dd1class, dd1value,
                    dd2class, dd2value,
                    dd3class, dd3value,
                    ):

    try:
        if n_clicks < 1:
            print("no drop down values")
            return []

        else:

            list1 = []
            list2 = []
            
            list1.append(dd1class)
            list1.append(dd2class)
            list1.append(dd3class)

            list2.append(dd1value)
            list2.append(dd2value)
            list2.append(dd3value)

            zipped = zip(list1, list2)
            d = dict(zipped)


            # all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
            # all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]

            all_pairs3 = [{j: d[j] for j in i} for i in it.combinations(d, 3)]
            all_pairs2 = [{j: d[j] for j in i} for i in it.combinations(d, 2)]
        

            data_pairsv = []
            data_pairsk = []
            data_pairsv1 = []
            data_pairsk1 = []


            for p in all_pairs2:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs2:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for p in all_pairs3:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs3:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for v in data_pairsv:
                data_pairsv1.append('vs'.join(v))

            for k in data_pairsk:
                data_pairsk1.append('vs'.join(k))

            zippedpairs = zip(data_pairsk1, data_pairsv1)
            finalpairs = dict(zippedpairs)
            
            for k,v in finalpairs.items():
                if v == "CATvsVAL":
                    a = dt.decision([1,1,0,0,0,0])
                elif v == "CATvsLATvsLON":
                    # a = dt.decision([1,0,0,1,0,0])
                    a = ['Map']
                elif v == "LOCvsVAL":
                    a = dt.decision([1,0,0,1,0,0])
                elif v == "DTEvsVAL":
                    a = dt.decision([1,0,0,0,1,0])
                elif v == "VALvsVAL":
                    a = dt.decision([1,0,0,0,0,1])
                elif v == "VALvsBOL" or v == "CATvsBOL":
                    a = dt.decision([1,0,1,0,0,0])
                else:
                    a = "None"
                finalpairs[k] = a[0]

            # print(finalpairs)

            for k,v in list(finalpairs.items()):
                if v == "N":
                    del finalpairs[k]            
                        
            print(finalpairs)

            df = pd.read_json(dfdata)

            charts = []

            chartnum = 0

            for k,v in finalpairs.items():
                gcol = k.split('vs')
                xcol = gcol[0]
                ycol = gcol[1]
                try:
                    zcol = gcol[2]
                except:
                    None
                xval = df[xcol]
                yval = df[ycol]
                try:
                    zval = df[zcol]
                except:
                    None
                chartnum+=1
                if v == "Bar":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bar_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Map":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.map_function(xval,yval,zval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Rings":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.rings_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Bubble":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bubble_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Table":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.table_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Scatter":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.scatter_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Pie":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.pie_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Line":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.line_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))

            print('3 columns')

            return charts

    except:
        None

# ##Call Back for 2 Columns
@app.callback(
                Output('dropdown-values2', 'children'),
                [
                Input('submit_button', 'n_clicks'),
                Input('choosen_columns_data', 'value'),
                Input('complete-df', 'data'),
                ],
                [
                State('mydropdown-1', 'className'),
                State('mydropdown-1', 'value'),
                State('mydropdown-2', 'className'),
                State('mydropdown-2', 'value'),
                ]
            )

def update_columns2(n_clicks, ddvalues,
                    dfdata, 
                    dd1class, dd1value,
                    dd2class, dd2value,                    
                    ):

    try:
        if n_clicks < 1:
            print("no drop down values")
            return []

        else:

            list1 = []
            list2 = []
            
            list1.append(dd1class)
            list1.append(dd2class)

            list2.append(dd1value)
            list2.append(dd2value)

            zipped = zip(list1, list2)
            d = dict(zipped)


            # all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
            # all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]

            all_pairs3 = [{j: d[j] for j in i} for i in it.combinations(d, 3)]
            all_pairs2 = [{j: d[j] for j in i} for i in it.combinations(d, 2)]
        

            data_pairsv = []
            data_pairsk = []
            data_pairsv1 = []
            data_pairsk1 = []


            for p in all_pairs2:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs2:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for p in all_pairs3:
                # print(list(p.values()))
                data_pairsv.append(list(p.values()))

            for p in all_pairs3:
                # print(list(p.keys()))
                data_pairsk.append(list(p.keys()))

            for v in data_pairsv:
                data_pairsv1.append('vs'.join(v))

            for k in data_pairsk:
                data_pairsk1.append('vs'.join(k))

            zippedpairs = zip(data_pairsk1, data_pairsv1)
            finalpairs = dict(zippedpairs)
            
            for k,v in finalpairs.items():
                if v == "CATvsVAL":
                    a = dt.decision([1,1,0,0,0,0])
                elif v == "CATvsLATvsLON":
                    # a = dt.decision([1,0,0,1,0,0])
                    a = ['Map']
                elif v == "LOCvsVAL":
                    a = dt.decision([1,0,0,1,0,0])
                elif v == "DTEvsVAL":
                    a = dt.decision([1,0,0,0,1,0])
                elif v == "VALvsVAL":
                    a = dt.decision([1,0,0,0,0,1])
                elif v == "VALvsBOL" or v == "CATvsBOL":
                    a = dt.decision([1,0,1,0,0,0])
                else:
                    a = "None"
                finalpairs[k] = a[0]

            # print(finalpairs)

            for k,v in list(finalpairs.items()):
                if v == "N":
                    del finalpairs[k]            
                        
            print(finalpairs)

            df = pd.read_json(dfdata)

            charts = []

            chartnum = 0

            for k,v in finalpairs.items():
                gcol = k.split('vs')
                xcol = gcol[0]
                ycol = gcol[1]
                try:
                    zcol = gcol[2]
                except:
                    None
                xval = df[xcol]
                yval = df[ycol]
                try:
                    zval = df[zcol]
                except:
                    None
                chartnum+=1
                if v == "Bar":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bar_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Map":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.map_function(xval,yval,zval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Rings":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.rings_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Bubble":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.bubble_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Table":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.table_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Scatter":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.scatter_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Pie":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.pie_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))
                elif v == "Line":
                    charts.append(html.Div([
                            dcc.Graph(id=f'auto-graph{chartnum}',
                            figure=cl.line_function(xval,yval)),
                            html.Button(id=f'auto-graph-button{chartnum}',
                            n_clicks=0,
                            children='Download PNG')
                            ]))

            print('----------------')
            print('2 Columns')
            print('----------------')

            return charts

    except:
        None

##save png button1
@app.callback(
                Output('auto-graph-button1-1', 'children'),
                [
                Input('auto-graph-button1', 'n_clicks'),
                ]
            )

def savefig1(
                    n_clicks,
                    ):

    try:
        if n_clicks < 1:
            print("button has not been clicked")
            return []

        else:
            pyo.plot(fig,auto_open=False,image='png')


            # return charts
        
    except:
        None

if __name__ == '__main__':
    app.run_server(debug=True)