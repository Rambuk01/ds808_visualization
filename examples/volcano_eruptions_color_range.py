import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px

app = dash.Dash(__name__)


eruption_data = pd.read_csv('eruptions.csv', encoding='utf-8')

# Filter out the row with NA as value in the vei column
eruption_data = eruption_data[eruption_data['vei'].notnull()]

# Sort the table so that the high vei values are at the bottom so that larger circles overlap the smaller ;)
eruption_data = eruption_data.sort_values(by=['vei'], na_position="first", ascending=True)

mintime = int(eruption_data["start_year"].min(skipna=True))
maxtime = int(eruption_data["end_year"].max(skipna=True))

app.layout = html.Div([
    html.H1(children="The World's Volcanos",
            style={'textAlign': 'center', 'fontFamily': 'Roboto, sans-serif'}),
    html.Div([
        html.Div([
            dcc.Graph(id='volcano-map')
        ], style={'width': '46%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '2%'}),
        html.Div([
            html.Div(id='miframe')
        ], style={'width': '46%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '2%'})
    ]),
    html.Div([
        dcc.RangeSlider(
            id='time-slider',
            min=mintime,
            max=maxtime,
            step=100,
            value=[mintime, maxtime],
            marks={i: str(i) for i in range(mintime, maxtime, 500)})
    ]),
    html.Div([
        dcc.RangeSlider(
            id='vei-slider',
            min=0,
            max=8,
            step=8,
            value=[0, 8],
            marks={i: str(i)  for i in range(0, 8)})
    ]),
    html.Div(id='output-container-range-slider')
])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('time-slider', 'value')])
def update_selection(value):
    return 'You have selected {}'.format(value)


# @app.callback(
#     Output(component_id='volcano-map', component_property='figure'),
#     [
#         Input(component_id='time-slider', component_property='value'),
#         Input(component_id='vei-slider', component_property='value')
#     ]
# )
# def update_output(time, vei):
#     mydata = eruption_data
    
#     if time != [mintime, maxtime]:
#         mydata = mydata[mydata['start_year'] >= time[0]]
#         mydata = mydata[mydata['end_year'] <= time[1]]
    
#     if vei != [0, 8]:
#         mydata = mydata[mydata['vei'] >= vei[0]]
#         mydata = mydata[mydata['vei'] <= vei[1]]

#     fig = px.scatter_mapbox(data_frame=mydata,
#                             lat="latitude",
#                             lon="longitude",
#                             hover_name="volcano_name",
#                             hover_data=["vei", "start_year", "end_year"],
#                             size=[i * 2 for i in mydata['vei']],  # scale the circle size by the vei value
#                             zoom=0,
#                             height=1000,
#                             color="vei",
#                             color_continuous_scale=px.colors.sequential.YlOrRd, # from https://plotly.com/python/builtin-colorscales/
#                             range_color=(0,8),
#                             opacity=1.0,
#                             )
#     fig.update_layout(mapbox_style="open-street-map")
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 20, "b": 0})
#     return fig

@app.callback(
    Output(component_id='volcano-map', component_property='figure'),
    [
        Input(component_id='time-slider', component_property='value'),
        Input(component_id='vei-slider', component_property='value')
    ]
)
def update_output(time, vei):
    mydata = eruption_data.copy()

    # Filter by time range
    if time != [mintime, maxtime]:
        mydata = mydata[(mydata['start_year'] >= time[0]) & (mydata['end_year'] <= time[1])]

    # Filter by VEI range
    if vei != [0, 8]:
        mydata = mydata[(mydata['vei'] >= vei[0]) & (mydata['vei'] <= vei[1])]

    # Handle size attribute, converting it to a valid list or using a fallback
    if not mydata.empty and 'vei' in mydata.columns:
        size_values = mydata['vei'].fillna(1).tolist()  # Ensure non-NaN values and convert to list
        size_values = [i * 2 for i in size_values]  # Scale size by VEI value
    else:
        size_values = [1] * len(mydata)  # Default size when VEI is not available

    # Create the figure
    fig = px.scatter_mapbox(
        data_frame=mydata,
        lat="latitude",
        lon="longitude",
        hover_name="volcano_name",
        hover_data=["vei", "start_year", "end_year"],
        size=size_values,  # Ensure this is a valid list
        zoom=0,
        height=1000,
        color="vei",
        color_continuous_scale=px.colors.sequential.YlOrRd,  # Use color scale for VEI
        range_color=(0, 8),
        opacity=1.0,
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 20, "b": 0})

    return fig




@app.callback(Output('miframe', 'children'),
              [Input('volcano-map', 'clickData')])
def update_wiki(click_data):
    url = "https://en.wikipedia.org/wiki/Volcano"
    if click_data != None:
        url = "https://en.wikipedia.org/wiki/" + \
            click_data['points'][0]['hovertext'].replace(" ", "_")
    return [
        html.Iframe(src=url, style={
                    'width': '100%', 'height': '1000px', 'display': 'inline-block'})
    ]


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
