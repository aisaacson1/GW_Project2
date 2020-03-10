import decision_tree as dt
import pandas as pd

beg=dt.decision

print(beg)

beg([1,0,0,1,0,0])


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

