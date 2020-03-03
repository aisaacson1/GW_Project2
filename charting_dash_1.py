import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io
import cufflinks as cf
import dash_table
from dash.dependencies import Input, Output, State



url="https://gwprojectflask.herokuapp.com/api/data/raw_results"
df = pd.read_json(url)

a=df['Data_Type']
c=df['Chart_Type']
b=df['Correct']

def bar_function(x,y): 

    aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

    agg = []
    agg_func = []
    for i in range(0, len(aggs)):
        agg = dict(
            args=['transforms[0].aggregations[0].func', aggs[i],
            'transforms[0].aggregations[1].func', aggs[i]],
            label=aggs[i],
            method='restyle'
        )
        agg_func.append(agg)

    return{
    'data' : [dict(
        type = 'bar',
        x = x,
        y = y,
        text = y,
        textposition='outside',
        transforms = [dict(
            type = 'aggregate',
            groups = x,
            aggregations = [
                dict(
                target = 'y', func = 'sum', enabled = True),
                dict(
                target = 'text', func = 'count', enabled = True),
                ]),
            # dict(
            # type = 'aggregate',
            # groups = x,
            # aggregations = [
            #     dict(
            #     target = 'text', func = 'count', enabled = True),
            #     ]
            # )
            ]

        )],

    'layout' : dict(
        title = '<b>Plotly Aggregations</b><br>use dropdown to change aggregation',
        xaxis = dict(title = x.name),
        yaxis = dict(title = y.name),
        updatemenus = [dict(
                yanchor = 'top',
                active = 1,
                showactive = False,
                buttons = agg_func
            )]
        )
    }


def line_function(x,y): 

    aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

    agg = []
    agg_func = []
    for i in range(0, len(aggs)):
        agg = dict(
            args=['transforms[0].aggregations[0].func', aggs[i]],
            label=aggs[i],
            method='restyle'
        )
        agg_func.append(agg)


    return{
    'data' : [dict(
        type = 'line',
        x = x,
        y = y,
        text = y,
        textposition='auto',
        transforms = [dict(
            type = 'aggregate',
            groups = x,
            aggregations = [
                dict(
                target = 'y', func = 'sum', enabled = True),
                # dict(
                # target = 'text', func = 'sum', enabled = True)
                ]
            )]
        )],

    'layout' : dict(
        title = '<b>Plotly Aggregations</b><br>use dropdown to change aggregation',
        xaxis = dict(title = 'Column A Header'),
        yaxis = dict(title = 'Column B Header'),
        updatemenus = [dict(
                yanchor = 'top',
                active = 1,
                showactive = False,
                buttons = agg_func
            )]
        )
    }




def pie_function(x,y): 

    aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

    agg = []
    agg_func = []
    for i in range(0, len(aggs)):
        agg = dict(
            args=['transforms[0].aggregations[0].func', aggs[i]],
            label=aggs[i],
            method='restyle'
        )
        agg_func.append(agg)
    return{
        'data' : [dict(
            type = 'pie',
            labels = x,
            values = y,
            text = x,
            textposition='auto',
            transforms = [dict(
                type = 'aggregate',
                groups = x,
                aggregations = [
                    dict(
                    target = 'values', func = 'sum', enabled = True),
                    ]
                )]
            )],

        'layout' : dict(
            title = f"<b>{x.name} by Number {y.name}</b><br>use dropdown to change aggregation",
            updatemenus = [dict(
                    yanchor = 'top',
                    active = 1,
                    showactive = False,
                    buttons = agg_func
                )]
            )
        }

def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Generate Charts Based on Actual User Feedback'),

    html.Div(children='''
        Select Which Columns you would like to be graphed
    '''),

    html.Div(generate_table(df)),

    dcc.Graph(
        id='example-graph',
        figure=pie_function(a,b)
    ),
     dcc.Graph(
        id='example-graph1',
        figure=bar_function(c,b)
    ),
     dcc.Graph(
        id='example-graph2',
        figure=line_function(c,b)
    )

])



if __name__ == '__main__':
    app.run_server(debug=True)
