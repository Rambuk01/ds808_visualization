import pandas as pd
from dash.dependencies import Input, Output
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

data = pd.read_csv('volcanos.csv', encoding='utf-8')

types = data['primary_volcano_type'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'All Volcano Types', 'value': 'all'})

rocks = data['major_rock_1'].unique()
rock_options = [{'label': i, 'value': i} for i in rocks]
rock_options.append({'label': 'All Rock Types', 'value': 'all'})

# mintime = data['last_eruption_year'].min()
# maxtime = data['last_eruption_year'].max()
mintime = -10500
maxtime = 2100

app.layout = html.Div([
                 html.H1(children="The World's Volcanos",
                         style = {'textAlign':'center', 'font-family' : 'Roboto'}),        
                 html.Div([
                    dcc.Dropdown(
                        id='volcano_types',
                        options=type_options,
                        value='all',
                        style={'width':'50%','display':'inline-block'}
                    ),
                    dcc.Dropdown(
                        id='volcano_rocks',
                        options=rock_options,
                        value='all',
                        style={'width':'50%','display':'inline-block'}
                    )
                 ],style={'width':'100%','display':'inline-block'}),
                 html.Div([
                     html.Div([
                         dcc.Graph(id='volcano-map')
                     ],style={'width':'46%','display':'inline-block','vertical-align':'top','margin':'2%'}),
                     html.Div([
                         html.Div(id='miframe')
                     ],style={'width':'46%','display':'inline-block','vertical-align':'top','margin':'2%'})
                 ]),
                 html.Div([
                     dcc.RangeSlider(
                       id='time-slider',
                       min=mintime,
                       max=maxtime,
                       step=100,
                       value=[mintime,maxtime],
                       marks={i: str(i) for i in range(mintime, maxtime, 500)})
                 ])
])

@app.callback(
    Output(component_id='volcano-map', component_property='figure'),
    [
        Input(component_id='volcano_types', component_property='value'),
        Input(component_id='volcano_rocks', component_property='value'),
        Input(component_id='time-slider', component_property='value')
    ]
)
def update_output(volcano_type, volcano_rock, time):
    print(f"Hello there!! {volcano_rock}")
    mydata = data
    if volcano_type != 'all':
        mydata = data[data['primary_volcano_type'] == volcano_type]
    if volcano_rock != 'all':
        mydata = mydata[mydata['major_rock_1'] == volcano_rock]
    if time != [mintime,maxtime]:
        mydata = mydata[mydata['last_eruption_year'] >= time[0]]
        mydata = mydata[mydata['last_eruption_year'] <= time[1]]
    if not mydata.empty:
        size_values = [1 for _ in mydata['volcano_number']]
    else:
        size_values = [1]
        
    fig = px.scatter_mapbox(
        data_frame=mydata, 
        lat="latitude",
        lon="longitude",
        hover_name="volcano_name",
        size=size_values,  # Ensuring size is numeric
        size_max=10,
        zoom=0,
        height=1000
    )
    
#     fig = px.scatter_mapbox(data_frame=mydata, 
#                         lat="latitude",
#                         lon="longitude",
#                         hover_name="volcano_name",
# #                        hover_data=["primary_volcano_type","tectonic_settings"],
# #                        color="primary_volcano_type",
#                         size=[1 for i in mydata['volcano_number']],
#                         size_max=10,
#                         zoom=0,
#                         height=1000)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    return fig

@app.callback(Output('miframe','children'),
              [Input('volcano-map','clickData')])
def update_wiki(click_data):
    url = "https://en.wikipedia.org/wiki/Volcano"
    if click_data != None:
        url = "https://en.wikipedia.org/wiki/"+click_data['points'][0]['hovertext'].replace(" ","_")
    return [
        html.Iframe(src=url,style={'width':'100%','height':'1000px','display':'inline-block'})
    ]

if __name__ == '__main__':
    app.run_server(debug=True, port=8888)