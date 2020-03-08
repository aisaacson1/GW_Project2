import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

import pandas as pd

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
                        'marginRight': 10
                        }),

    # dcc.Graph(id='Mygraph'),


    # html.Div(id='display-selected-values'),
    html.Br(),
    html.Label(id='data-type-text'),
    html.Br(),
    html.Div(id='choosen_columns_data'),
    html.Br(),
    html.Div(id='submit_button'),
    html.Br(),
    html.Label(id='dropdown-values')
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
 
        return [html.Label("Select at least two columns to visualize:")]

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
            return [html.Label("Select the data type for each column, then click submit:")]
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

    try:    
        for i in selected_col:
            # if len(ddcreator) >= 0:
            #     col_width = 100/len(ddcreator)
            # else:
            #     col_width = 25

            dd =html.Div(
                    html.Label(
                        [i,
                        dcc.Dropdown(
                            # id=f"mydropdown{i}",
                            id="mydropdown1",
                            options = ddoptions,
                            persistence_type = 'session',
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

    print(ddcreator)
    print("-----------------------------")
    print(len(ddcreator))
    print("-----------------------------")
    # print(col_width)
    # print("-----------------------------")


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
            button = html.Button(id='submit-button',
                    n_clicks=0,
                    children='Submit'
                    )
            return button
    except:
        None

## Get dropdown values to make data pairs
@app.callback(
                Output('dropdown-values', 'values'),
                [
                Input('submit-button', 'n_clicks'),
                Input('choosen_columns_data', 'values'),
                ],
                # State('choosen_columns_data', 'values'),
            )

def update_columns(n_clicks, ddvalues):

    if n_clicks < 1:
        print("no drop down values")
        return []

    else:
        print("-----------------------------")
        print(ddvalues)
        print("-----------------------------")

        return ddvalues

# ## Show selected column names
# @app.callback(
#     Output('display-selected-values', 'children'),
#     [Input('column-checklist', 'value')]
#     )
# def set_display_children(selected_column):
#     return u'{} is the column you selected'.format(
#         selected_column
#     )

# def update_table(contents, filename):
#     table = html.Div()

#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_data(contents, filename)
#         column_head = [{'label': i, 'value': i} for i in df.columns]

#         table = html.Div([
#             html.H5('Select columns to graph:'),
#             dcc.Checklist(options=column_head,
#             labelStyle = dict(display='inline')),
#             html.H5(filename),
#             dash_table.DataTable(
#                 id='user_data',
#                 data=df.to_dict('rows'),
#                 columns=[{'name': i, 'id': i, "selectable": True} for i in df.columns],
#                 fixed_rows={ 'headers': True, 'data': 0 },
#                 column_selectable = 'multi',
#                 selected_columns=[],
#                 # filter_action="native",
#                 sort_action="native",
#                 sort_mode="multi",
#                 page_action="native",
#                 page_size= 20,
#                 style_table={
#                     'maxHeight': '500px',
#                     # 'overflowY': 'scroll',
#                     'overflowX': 'scroll',
#                 },
#                 style_cell_conditional=create_conditional_style(df)
#             ),
#         ])
#         # print(table)
#         column_head = [{'label': i, 'value': i} for i in df.columns]
#     # return table, column_head
#         # app.layout = serve_layout
#     return table

# def create_conditional_style(df):
#     style=[]
#     for col in df.columns:
#         name_length = len(col)
#         pixel = 50 + round(name_length*1)
#         pixel = str(pixel) + "px"
#         style.append({'if': {'column_id': col}, 'minWidth': pixel})

#     return style

if __name__ == '__main__':
    app.run_server(debug=True)