# import decision_tree as dt
# import pandas as pd

# beg=dt.decision

# print(beg)

# beg([1,0,0,1,0,0])


# url="https://gwprojectflask.herokuapp.com/api/data/raw_results"
# df = pd.read_json(url)


# a=df['Data_Type']
# c=df['Chart_Type']
# b=df['Correct']

# bin = edges = pd.cut(b, bins=6)

# print(bin)

# categories, edges = pd.cut(b, 3, retbins=True, duplicates='drop', labels=False)
# df = pd.DataFrame({'original':b,
#                    'bin_max': edges[1:][categories]},
#                   columns = ['original', 'bin_max'])



# print(df['bin_max'].unique())

# import pandas as pd
# import dash_table

# url="https://gwprojectflask.herokuapp.com/api/data/raw_results"
# df = pd.read_json(url)

# path = "C:/Users/Aaron/Documents/GW_Data_Course/AIsaacson_GW_HW/GW_Project2_aji/sources/testing_data - dates.csv"
# df = pd.read_csv(path)
# df.head()

# a=df['Data_Type']
# c=df['Chart_Type']
# b=df['Correct']

# from plotly.subplots import make_subplots
# import datetime
# import re
# import plotly.graph_objects as go

# for i, row in enumerate(df["Date"]):
#     p = re.compile(" 00:00:00")
#     datetime = p.split(df["Date"][i])[0]
#     df.iloc[i, 1] = datetime
    
# go.Table(
#         header=dict(
#             values=[],
#             font=dict(size=10),
#             align="left"
#         ),
#         cells=dict(
#             values=[df[k].tolist() for k in df.columns[1:]],
#             align = "left")
#     )
    


# fig.update_layout(
#     height=800,
#     showlegend=False,
#     title_text="Look at your ugly table!")

import string
import secrets

# length = 10

# print("Generate a secure token using a secrets", (secrets.token_hex(16)[0:length]))
# print("Generate a secure token using a secrets", (secrets.token_hex(16)[0:length]))

def generateSecureRandomString(stringLength=50):
    """Generate a secure random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(password_characters) for i in range(stringLength))

print("Generating secure Random String using a secrets module")
print ("First Random String ", generateSecureRandomString() )
# print ("Second Random String", generateSecureRandomString(10) )


def graph_maker(df,pairs):

    charts = []

    chartnum = 0

    for k,v in pairs.items():
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
        if v[0] == "Bar":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.bar_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')

                    ])
                    )
        elif v[0] == "Map":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.map_function(xval,yval,zval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Rings":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.rings_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Bubble":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.bubble_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Table":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.table_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Scatter":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.scatter_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Pie":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.pie_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
        elif v[0] == "Line":
            charts.append(html.Div([
                    dcc.Graph(id=f'auto-graph{chartnum}',
                    figure=cl.line_function(xval,yval)),
                    html.Label("Does the above chart show what you wanted?"),
                    dcc.RadioItems(
                        id=f'auto-graph-radio{chartnum}',
                        options=[
                            {'label': 'Yes', 'value': f'y,{k},{v[1]}'},
                            {'label': 'No', 'value': f'n,{k},{v[1]}'}
                        ],
                        labelStyle={'display': 'inline-block'})
                    # html.Button(id=f'auto-graph-button{chartnum}',
                    # n_clicks=0,
                    # children='Download PNG')
                    ]))
    return charts


def feedback_maker(a):
    if a == "CATvsVAL":
        a = 'categoryvsvalue'
    elif a == "CATvsLATvsLON":
        a = 'categoryvslatvslon'
    elif a == "LOCvsVAL":
        a = 'valuevslocation'
    elif a == "DTEvsVAL":
        a = 'valuevstime'
    elif a == "VALvsVAL":
        a = 'valuevsvalue'
    elif a == "VALvsBOL" or v == "CATvsBOL":
        a = 'comparison'
    return a


def decision_func(d):
    all_pairs3 = [{j: d[j] for j in i} for i in it.permutations(d, 3)]
    all_pairs2 = [{j: d[j] for j in i} for i in it.permutations(d, 2)]
        

    data_pairsv = []
    data_pairsk = []
    data_pairsv1 = []
    data_pairsk1 = []


    for p in all_pairs2:
        data_pairsv.append(list(p.values()))

    for p in all_pairs2:
        data_pairsk.append(list(p.keys()))

    for p in all_pairs3:
        data_pairsv.append(list(p.values()))

    for p in all_pairs3:
        data_pairsk.append(list(p.keys()))

    for v in data_pairsv:
        data_pairsv1.append('vs'.join(v))

    for k in data_pairsk:
        data_pairsk1.append('vs'.join(k))

    zippedpairs = zip(data_pairsk1, data_pairsv1)
    fp = dict(zippedpairs)

    for k,v in fp.items():
        vlist = []
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
        vlist.append(a[0])
        vlist.append(v)
        fp[k] = vlist

    print(fp)

    for k,v in list(fp.items()):
        if v[0] == "N":
            del fp[k]   

    return fp


def feedback_func(rvalue):
    try:
        if len(rvalue) is None:
            print("radio empty")
            return []
        else:
            
            radioval=rvalue.split(',')

            datatype = feedback_maker(radioval[2])

            if radioval[0] == 'y':
                feedback = dict(
                    Survery_ID=generateSecureRandomString(),
                    value='data_upload_response',
                    Data_Type=datatype,
                    Chart_Type=radioval[1],
                    Correct=1
                    )
                feedback = pd.DataFrame([feedback])
    
                print(feedback)
                # print(f'"Survery_ID":"{generateSecureRandomString()}","value":"data_upload_response","Data_Type":"{datatype}","Chart_Type":"{radioval[1]}","Correct":1')

            elif radioval[0] == 'n':
                feedback = dict(
                    Survery_ID=generateSecureRandomString(),
                    value='data_upload_response',
                    Data_Type=datatype,
                    Chart_Type=radioval[1],
                    Correct=0
                    )
                feedback = pd.DataFrame([feedback])
    
                print(feedback)
                # print(f'"Survery_ID":"{generateSecureRandomString()}","value":"data_upload_response","Data_Type":"{datatype}","Chart_Type":"{radioval[1]}","Correct":0')

            # return None
            return postFeedbackHandler(feedback)
    except:
        None