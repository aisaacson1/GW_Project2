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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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

    html.Label('Select columns to graph:'),

    dcc.Checklist(id='output-column-upload',
                 labelStyle = dict(display='inline')),

    # dcc.Graph(id='Mygraph'),
    html.Div(id='output-data-upload'),
    # html.Div(id='user_data', style={'display': 'none'}),
    # html.Div(id='datatable-interactivity-container')
])


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

@app.callback(
                Output('output-data-upload', 'children'),
            # [
            #     Output('output-data-upload', 'children'),
            #     Output('output-column-upload', 'options')
            #     ],
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                id='user_data',
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i, "selectable": True} for i in df.columns],
                fixed_rows={ 'headers': True, 'data': 0 },
                column_selectable = 'multi',
                selected_columns=[],
                # filter_action="native",
                sort_action="native",
                sort_mode="multi",
                page_action="native",
                page_size= 20,
                style_table={
                    'maxHeight': '500px',
                    # 'overflowY': 'scroll',
                    'overflowX': 'scroll',
                },
                style_cell_conditional=create_conditional_style(df)
            ),
        ])

        # column_head = [{'label': i, 'value': i} for i in df.columns]
    # return table, column_head
    return table

def create_conditional_style(df):
    style=[]
    for col in df.columns:
        name_length = len(col)
        pixel = 50 + round(name_length*1)
        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})

    return style

# @app.callback(
#                 Output('output-column-upload', 'value')
#                 ,
#                 Input('output-column-upload', 'options')
#             )
# def set_checks_value(available_options):
#     return available_options[0]['value']

@app.callback(
                Output('output-column-upload', 'options')
                ,
                Input('output-data-upload', 'children')
            )
def set_checks_value(available_options):
    return available_options[0]['value']


# @app.callback(
#     Output('datatable-interactivity-container', "children"),
#     [Input('user_data', 'selected_columns'),
#      Input('output-data-upload', "derived_virtual_selected_columns")])
# def update_graphs(columns, derived_virtual_selected_columns):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncracy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     if derived_virtual_selected_columns is None:
#         derived_virtual_selected_columns = []

#     dff = df if columns is None else pd.DataFrame(columns)

#     colors = ['#7FDBFF' if i in derived_virtual_selected_columns else '#0074D9'
#               for i in range(len(dff))]

#     return [
#         dcc.Graph(
#             id=column,
#             figure={
#                 "data": [
#                     {
#                         "x": dff["Chart_Type"],
#                         "y": dff[column],
#                         "type": "bar",
#                         "marker": {"color": colors},
#                     }
#                 ],
#                 "layout": {
#                     "xaxis": {"automargin": True},
#                     "yaxis": {
#                         "automargin": True,
#                         "title": {"text": column}
#                     },
#                     "height": 250,
#                     "margin": {"t": 10, "l": 10, "r": 10},
#                 },
#             },
#         )
#         # check if column exists - user may have deleted it
# #         # If `column.deletable=False`, then you don't
# #         # need to do this check.
# #     #     for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
#     ]

if __name__ == '__main__':
    app.run_server(debug=True)