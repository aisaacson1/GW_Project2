import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

df = pd.read_csv(r"C:\Users\Aaron\Documents\GW_Data_Course\AIsaacson_GW_HW\GW_Project2\sources\Quiz_results_29FEB_noon.csv")
df.head()

# a=df['Data_Type']
a=df['Chart_Type']
b=df['Correct']

def bar_function(x,y): 

    aggs = ["count","sum","avg","median","mode","rms","stddev","min","max","first","last"]

    agg = []
    agg_func = []
    for i in range(0, len(aggs)):
        agg = dict(
            args=['transforms[0].aggregations[0].func', aggs[i]],
            label=aggs[i],
            method='restyle'
        )
        print(agg_func)
        agg_func.append(agg)

    data = [dict(
        type = 'bar',
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
        )]

    layout = dict(
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

    fig_dict = dict(data=data, layout=layout)

    return(pio.show(fig_dict, validate=False))

bar_function(a,b)