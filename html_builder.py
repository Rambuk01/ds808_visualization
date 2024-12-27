import dash
from dash.dependencies import Input, Output, State
from dash import dcc, ctx
from dash import html
import plotly.express as px
import random
import plotly.graph_objs as go
from plotly.colors import n_colors

## GENERAL SETTINGS ##
map_height = 455;
plot_bgcolor="rgba(50, 50, 50, 1)" # Background of the plotting area
paper_bgcolor="rgba(255, 255, 255, 1)" # Background of the entire figure
# Define the list of month names
    # Define category names
month_names = [
    "January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"
]
season_names = ["Winter", "Spring", "Summer", "Fall"]
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_map():
    map = html.Div(
        className = 'map-container',
        children=[
            #html.H2(children="Map"),
            html.Div(
                dcc.Graph(id='cph-map', config={"scrollZoom": True}),
            ),
        ]
    )
    return map

def get_radio_items(id, value, options):
    radio = html.Div(className='radio-wrapper', children=[
        dcc.RadioItems(id=id, options=options,
            value=value
        )
    ])
    return radio

def get_dropdowns(dropdown_options: dict):
    # Existing dropdowns
    dropdown_map_type = dcc.Dropdown(
        id='map-type_dd',
        options=[
            {'label': 'Choropleth Map', 'value': 'choropleth'},
            {'label': 'Scatter Mapbox', 'value': 'scatter'},
        ],
        value='choropleth',  # Default map type
        clearable=False,
    )

    dropdown_room_type = dcc.Dropdown(
        id='room_types',
        options=dropdown_options['room_type_options'],
        value='all'
    )

    # New dropdowns
    #room_type,accommodates,bedrooms,beds,price,bathrooms
    dropdown_violin_category = dcc.Dropdown(
        id='violin-category',
        options=[
            {"label": "Months", "value": "month"},
            {"label": "Seasons", "value": "season"},
            {"label": "Week days", "value": "day_of_week"},
            {"label": "Bedrooms", "value": "bedrooms"},
            {"label": "Accommodates", "value": "accommodates"},
            {"label": "Bathrooms", "value": "bathrooms"},
            {"label": "Beds", "value": "beds"},
        ],
        value="season",  # Default to months
        clearable=False,
    )

    dropdown_plot_type = dcc.Dropdown(
        id='plot-type',
        options=[
            {"label": "Violin Plot", "value": "violin"},
            {"label": "Ridgeline Plot", "value": "ridgeline"},
        ],
        value="violin",  # Default to violin plot
        clearable=False,
    )

    # Combine all dropdowns into one container
    dropdowns = html.Div(
        className="dropdowns w100",
        children=[
            html.H1(children="The Airbnb Host Helper"),
            html.Div(className="spacer-1", children=''),
            html.H4(className="para", children="Explore Copenhagens Airbnb Market: Visualize Pricing Patterns and Property Details by Neighborhood."),
            html.Div(className="spacer-1", children=''),
            html.P(className="para", children="Unlock valuable insights into Copenhagens Airbnb market with a host-focused approach giving insights into pricing based on seasons or apartment details."),

            html.Div(className="spacer-2", children=''),
            html.H3(children="Select map type"),
            get_radio_items(id = 'map-type', value = 'choropleth', options=[
                {'label': 'Choropleth', 'value': 'choropleth'},
                {'label': 'Scatter Mapbox', 'value': 'scatter_mapbox'},
            ]),
            html.Div(className="spacer-1", children=''),
            html.H3(children="Select room type"),
            html.Div(className='flex flex-space-around', children=[
                html.Div(
                    className="dropdown w100 m1",
                    children=dropdown_room_type,
                ),
                # html.Div(
                #     className='dropdown w50 m1',
                #     children=dropdown_map_type,
                # ),
            ]),
            html.Div(className="spacer-2", children=''),
            html.H3(children="Select distribution-plot type"),
            get_radio_items(id='plot-type', value = 'violin', options=[
                            {'label': 'Violin plot', 'value': 'violin'},
                            {'label': 'Ridgeline plot', 'value': 'ridgeline'},
                        ]),
            html.Div(className="spacer-1", children=''),
            html.H3(children="Visualize bottom plot"),
            html.Div(className='flex flex-space-around', children=[
                html.Div(
                    className="dropdown w100 m1",
                    children=dropdown_violin_category,
                ),
                # html.Div(
                #     className="dropdown w50 m1",
                #     children=dropdown_plot_type,
                # ),
            ]),
        ]
    )

    return dropdowns

def get_sunburst_and_piechart():
    chart = html.Div(
        className='sun_pie',
        children=[
            dcc.Graph(id="sunburst-chart"),
        ]
    )

    return chart


def get_predict_content():
    content = html.Div(
        className='predict-content-container',
        children=[
            html.H1(children='Predict hosting price per day'),
            html.Div(className='spacer-1', children=''),
            html.Div(
                className='intro-text',
                children=[
                    html.P(
                        """
                        This tool allows you to estimate Airbnb listing prices based on key parameters such as 
                        room type, neighborhood, number of bedrooms, and the maximum number of guests 
                        (accommodates). Simply fill in the details using the dropdowns and input fields below, 
                        then click the 'Predict' button to see the estimated price interval."""
                    ),
                ],
                style={'marginBottom': '20px'}
            ),
            # Dropdowns for categorical variables
            html.Label("Select Room Type:"),
            dcc.Dropdown(
                id='room-type-dropdown',
                options=[
                    {'label': 'Entire home/apt', 'value': 'Entire home/apt'},
                    {'label': 'Private room', 'value': 'Private room'},
                    {'label': 'Shared room', 'value': 'Shared room'},
                ],
                placeholder='Select room type',
                style={'marginBottom': '20px'}
            ),

            html.Label("Select Neighbourhood:"),
            dcc.Dropdown(
                id='neighbourhood-dropdown',
                options=[
                    {'label': 'Nørrebro', 'value': 'Nørrebro'},
                    {'label': 'Indre By', 'value': 'Indre By'},
                    {'label': 'Østerbro', 'value': 'Østerbro'},
                    {'label': 'Frederiksberg', 'value': 'Frederiksberg'},
                    # Add more options as needed
                ],
                placeholder='Select neighbourhood',
                style={'marginBottom': '20px'}
            ),
            html.Div(className='input-container flex flex-space-between', children=[
                # Number inputs for numeric parameters
                html.Div(className='input-item', children = [
                html.Label("Number of Bedrooms:"),
                dcc.Input(
                    id='bedrooms-input',
                    type='number',
                    placeholder='Bedrooms',
                )]),
                html.Div(className='input-item', children = [
                html.Label("Number of Beds:"),
                dcc.Input(
                    id='beds-input',
                    type='number',
                    placeholder='Beds',
                )]),
                html.Div(className='input-item', children = [
                html.Label("Accommodates:"),
                dcc.Input(
                    id='accommodates-input',
                    type='number',
                    placeholder='Accommodates',
                )]),
            ]),
            # Button to trigger prediction
            html.Button(
                id='predict-button',
                children='Predict',
                style={'marginTop': '20px'}
            ),
            html.Div(className="spacer-2", children=''),
            # Output area
            html.Div(
                id='prediction-output',
                style={'marginTop': '20px', 'fontWeight': 'bold', 'textAlign': 'center'}
            ),
            html.Div(id="canvas-container", className='flex flex-center', children=[
                html.Canvas(
                    id="myCanvas",
                    className="box-shadow",
                    style={"border": "1px solid black", "backgroundColor":"#d6e0f5", "padding":"12px", "borderRadius":"12px"}, 
                    width=600,
                    height=100
                ),
                html.Script(src="/assets/canvas_script.js"),  # Link to your JavaScript file
                
            ], style={'display':'none'})
        ]
    )
    return content