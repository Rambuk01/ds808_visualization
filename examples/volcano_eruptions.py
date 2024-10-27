import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import math
import plotly.express as px

app = dash.Dash(__name__)

# data = pd.read_csv('volcanos.csv', encoding='utf-8')

eruption_data = pd.read_csv('eruptions.csv', encoding='utf-8')

# types = data['primary_volcano_type'].unique()
# type_options = [{'label': i, 'value': i} for i in types]
# type_options.append({'label': 'All Volcano Types', 'value': 'all'})

# rocks = data['major_rock_1'].unique()
# rock_options = [{'label': i, 'value': i} for i in rocks]
# rock_options.append({'label': 'All Rock Types', 'value': 'all'})

# filtered_start_years =  filter(lambda number: math.isnan(float(number)) == False, eruption_data['start_year'])
#filtered_end_years =  filter(lambda number: int(float(number)), eruption_data['end_year'])

# print(filtered_start_years)


# filtered_start_years  = [int(x) for x in eruption_data["start_year"] if math.isnan(x) == False]
# filtered_end_years  = [int(x) for x in eruption_data["end_year"] if math.isnan(x) == False]
# mintime = filtered_start_years.min()
# maxtime = filtered_end_years.max()


mintime = int(eruption_data["start_year"].min(skipna=True))
maxtime = int(eruption_data["end_year"].max(skipna=True))

print(mintime)
print(maxtime)

app.layout = html.Div([
    html.H1(children="The World's Volcanos",
            style={'textAlign': 'center', 'font-family': 'Roboto, sans-serif'}),
    # html.Div([
    #     html.Label("Volcono Type"),
    #     dcc.Dropdown(
    #         id='volcano_types',
    #         options=type_options,
    #         value='all',
    #         style={'width': '80%'}
    #     )
    # ],
    #     style={'width': '50%', 'display': 'inline-block'}),
    # html.Div([
    #     html.Label("Rock Type"),
    #     dcc.Dropdown(
    #         id='volcano_rocks',
    #         options=rock_options,
    #         value='all',
    #         style={'width': '80%'}
    #     )
    # ], style={'width': '50%', 'display': 'inline-block'}),
    html.Div([
        html.Div([
            dcc.Graph(id='volcano-map')
        ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'}),
        html.Div([
            html.Div(id='miframe')
        ], style={'width': '46%', 'display': 'inline-block', 'vertical-align': 'top', 'margin': '2%'})
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
    html.Div(id='output-container-range-slider')
])


@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('time-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output(component_id='volcano-map', component_property='figure'),
    [
        # Input(component_id='volcano_types', component_property='value'),
        # Input(component_id='volcano_rocks', component_property='value'),
        Input(component_id='time-slider', component_property='value')
    ]
)
def update_output(time):
    global filter_mintime
    global filter_maxtime
    mydata = eruption_data
    # if volcano_type != 'all':
    #     mydata = data[data['primary_volcano_type'] == volcano_type]
    # if volcano_rock != 'all':
    #     mydata = mydata[mydata['major_rock_1'] == volcano_rock]
    
    if time != [mintime, maxtime]:
        mydata = mydata[mydata['start_year'] >= time[0]]
        mydata = mydata[mydata['end_year'] <= time[1]]

    filter_mintime = time[0]
    filter_maxtime = time[1]

    fig = px.scatter_mapbox(data_frame=mydata,
                            lat="latitude",
                            lon="longitude",
                            hover_name="volcano_name",
                            hover_data=["vei", "start_year", "end_year"],
                            #                        hover_data=["primary_volcano_type","tectonic_settings"],
                            #                        color="primary_volcano_type",
                            size=[i * 2 if  math.isnan(i) == False else 0 for i in mydata['vei']],
                            # size_max=10,
                            zoom=0,
                            height=1000,
                            color="vei",
                            color_continuous_scale=px.colors.cyclical.IceFire,
                            range_color=(0,10)
                            )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 20, "b": 0})
    return fig


@app.callback(Output('miframe', 'children'),
              [Input('volcano-map', 'clickData')])
def update_wiki(click_data):
    print(click_data)
    url = "https://en.wikipedia.org/wiki/Volcano"
    if click_data != None:
        url = "https://en.wikipedia.org/wiki/" + \
            click_data['points'][0]['hovertext'].replace(" ", "_")
    return [
        html.Iframe(src=url, style={
                    'width': '100%', 'height': '1000px', 'display': 'inline-block'})
    ]


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)
