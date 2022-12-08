import plotly.graph_objects as go
years= ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
MI_exams = [299, 389, 410, 577, 593, 936, 962, 1025, 1192, 1165]
GA_exams = [692, 884, 1037, 1261, 1536, 1658, 2033, 1914, 2095, 2257]

fig = go.Figure([go.Bar(x=years, y=MI_exams)])
fig.show()

# import plotly.express as px
# df = px.data.tips()
# fig = px.scatter(df, x="total_bill", y="tip", color="smoker",
#                  title="String 'smoker' values mean discrete colors")

# fig.show()