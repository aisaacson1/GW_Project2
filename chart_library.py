import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px

# url="https://gwprojectflask.herokuapp.com/api/data/raw_results"
# df = pd.read_json(url)
# # df.head()

# a=df['Data_Type']
# c=df['Chart_Type']
# b=df['Correct']

def bar_function(x,y): 

    aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

    agg = []
    agg_func = []
    for i in range(0, len(aggs)):
        agg = dict(
            args=[{'transforms[0].aggregations[0].func': aggs[i],
            'transforms[0].aggregations[1].func': aggs[i]}],
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
        hoverinfo='text',
        transforms = [dict(
            type = 'aggregate',
            groups = x,
            aggregations = [
                dict(
                target = 'y', func = 'sum', enabled = True),
                dict(
                target = 'text', func = 'sum', enabled = True),
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
        title = f'<b>{x.name} vs {y.name}</b><br>use dropdown to change aggregation',
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
        title = f'<b>{x.name} vs {y.name}</b><br>use dropdown to change aggregation',
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
def bubble_function(x,y): 

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
        type = 'bubble',
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
        title = f'<b>{x.name} vs {y.name}</b><br>use dropdown to change aggregation',
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
# var trace1 = {
#   x: [1, 2, 3, 4],
#   y: [10, 11, 12, 13],
#   mode: 'markers',
#   marker: {
#     size: [40, 60, 80, 100]
#   }
# };

# var data = [trace1];

# var layout = {
#   title: 'Marker Size',
#   showlegend: false,
#   height: 600,
#   width: 600
# };

# Plotly.newPlot('myDiv', data, layout);
def scatter_function(x,y): 

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
        type = 'scatter',
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
        title = f'<b>{x.name} vs {y.name}</b><br>use dropdown to change aggregation',
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


# def map_function (x,y):
#     return px.scatter_geo( 
#         locations=x,
#         color=y)

def map_function (x,y,z):
    
    scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]

    data = [ dict(
            type = 'scattergeo',
            # locationmode = 'USA-states',
            lon = y,
            lat = z,
            text = x,
            mode = 'markers',
            marker = dict(
                size = 8,
                opacity = 0.8,
                reversescale = True,
                autocolorscale = False,
                # symbol = 'square',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                ),
                colorscale = scl,
                cmin = 0,
                # color = df['cnt'],
                # cmax = df['cnt'].max(),
                colorbar=dict(
                    title="your map"
                )
            ))]

    layout = dict(
            title = 'Map',
            colorbar = True,
            # geo = dict(
            #     scope='usa',
            #     projection=dict( type='albers usa' ),
            #     showland = True,
            #     landcolor = "rgb(250, 250, 250)",
            #     subunitcolor = "rgb(217, 217, 217)",
            #     countrycolor = "rgb(217, 217, 217)",
            #     countrywidth = 0.5,
            #     subunitwidth = 0.5
            )
        # )

    fig = dict( data=data, layout=layout )  

    return fig
    

# var trace1 = {
#   x: [1, 2, 3, 4],
#   y: [10, 15, 13, 17],
#   mode: 'markers',
#   type: 'scatter'
# };

# var trace2 = {
#   x: [2, 3, 4, 5],
#   y: [16, 5, 11, 9],
#   mode: 'lines',
#   type: 'scatter'
# };

# var trace3 = {
#   x: [1, 2, 3, 4],
#   y: [12, 9, 15, 12],
#   mode: 'lines+markers',
#   type: 'scatter'
# };

# var data = [trace1, trace2, trace3];

# Plotly.scatter_function(a,b)
# data.show(line_function(a,b))