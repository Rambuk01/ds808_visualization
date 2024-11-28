import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import random
import plotly.graph_objs as go
from plotly.colors import n_colors

## GENERAL SETTINGS ##
map_height = 455;

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

def get_dropdowns(dropdown_options: dict):
    # Existing dropdowns
    dropdown_map_type = dcc.Dropdown(
        id='map-type',
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
    dropdown_violin_category = dcc.Dropdown(
        id='violin-category',
        options=[
            {"label": "Months", "value": "month"},
            {"label": "Seasons", "value": "season"},
            {"label": "Week days", "value": "day_of_week"},
            {"label": "Bedrooms", "value": "bedrooms"},
        ],
        value="month",  # Default to months
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
            html.H1(children="Airbnb - Copenhagen"),
            html.Div(className="spacer-1", children=''),
            html.P(className="para", children="Lorem ipsum dolor, sit amet consectetur adipisicing elit. Praesentium laboriosam sequi et velit, incidunt eaque tempore commodi enim, nemo ipsum odit distinctio error nihil in possimus. Debitis voluptate ratione perspiciatis!"),
            html.Div(className="spacer-1", children=''),
            html.H2(children="Filter Map"),
            html.Div(className='flex flex-space-around', children=[
                html.Div(
                    className="dropdown w50 m1",
                    children=dropdown_room_type,
                ),
                html.Div(
                    className='dropdown w50 m1',
                    children=dropdown_map_type,
                ),
            ]),
            html.Div(className="spacer-2", children=''),
            html.H2(children="Visualize bottom plot"),
            html.Div(className='flex flex-space-around', children=[
                html.Div(
                    className="dropdown w50 m1",
                    children=dropdown_violin_category,
                ),
                html.Div(
                    className="dropdown w50 m1",
                    children=dropdown_plot_type,
                ),
            ]),
        ]
    )

    return dropdowns