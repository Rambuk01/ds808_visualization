#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:33:15 2023

@author: mariofestersen
"""
import functions
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import random
import plotly.graph_objs as go
import json



""" INITIATE """
app = dash.Dash(__name__)
data = pd.read_csv('archive/listings_cleaned.csv', sep=',', encoding='utf-8')

# Load the GeoJSON file # https://www.opendata.dk/city-of-copenhagen/kvarter
with open('archive/cph_fred_dist.geojson') as f:
    geojson_data = json.load(f)


types = data['room_type'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'Any room type', 'value': 'all'})
# Convert date column to datetimes. Then convert them to year strings.

b_style = {
    'position': 'fixed', 
    'top': '25px', 
    'right': '50px', 
    'z-index':'100',
    'padding': '10px 30px',
    'border': '1px solid black',
    'border-radius': '5px',
    'box-shadow': 'rgba(0, 0, 0, 0.35) 0px 5px 15px',
    'background-color': 'lightblue',
    }

## 2 Maps - scatter and area - area is standard

## Dropdown choices
## Beds, Bedrooms, Room type, Bathrooms

## Violin plots
# price vs. seasons

# How often do we get rent out? Cant be answered.


app.layout = html.Div([
    html.H1(children="Airbnb - Copenhagen",
            style = {'textAlign':'center', 'font-family' : 'Roboto'}),
    
    html.Div(dcc.Dropdown(
        id='room_types',
        options=type_options,
        value='all'
    )),
    html.Div([
        html.Div(
            dcc.Graph(id='cph-map'),
            style={'width':'100%','display':'inline-block','vertical-align':'top','margin':'8px 0px', 'padding':'0px'}),
        ]),
    html.H1("Copenhagen GeoJSON Map", style={'textAlign': 'center'}),
    dcc.Graph(id='geojson-map')
])

""" MAP """
@app.callback(
    [
        Output(component_id='cph-map', component_property='figure'),
    ],
    [
        Input(component_id='room_types', component_property='value'),
    ]
)
def generate_map(room_types):
    ndata = data
    if room_types != 'all':
        ndata = ndata[ndata['room_type'] == room_types]
    
    fig = px.scatter_mapbox(
                        data_frame=ndata,
                        title=f"Airbnb Listings - {room_types}" if room_types != "all" else "Airbnb Listings - All Room Types",
                        lat="latitude",
                        lon="longitude",
                        #hover_name="id",
                        hover_data=["neighbourhood_cleansed"],
                        size="price",
                        color="price",
                        #size_max=15,
                        zoom=12,
                        height=1100,
                        mapbox_style="open-street-map")
    
    fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    
    return [fig]


# Callback to generate the GeoJSON map
@app.callback(
    Output('geojson-map', 'figure'),
    [
        Input('geojson-map', 'id'),  # Trigger on load
        Input(component_id='room_types', component_property='value')
    ]
)
def display_geojson(_, room_types):
    ndata = data
    if room_types != 'all':
        ndata = ndata[ndata['room_type'] == room_types]
    
        

    # We create a dummy DataFrame with a column to match the GeoJSON 'properties' key
    legend_data = {
        "bydel_nr": [feature["properties"]["bydel_nr"] for feature in geojson_data["features"]],
        "area_name": [feature["properties"]["navn"] for feature in geojson_data["features"]],  # Add area names
    }

    df_mean_prices = functions.get_mean_prices(ndata, legend_data)

    # Create a basic map using the GeoJSON data
    fig = px.choropleth_mapbox(
        df_mean_prices,
        geojson=geojson_data,
        locations="id",             # This should match dummy_data's column
        featureidkey="properties.bydel_nr",  # Adjust if needed
        color="price",               # Use dummy color to fill the regions
        mapbox_style="carto-positron",
        hover_name="neighbourhood_cleansed",   # Show area name in the hover info
        zoom=11,
        center={"lat": 55.6761, "lon": 12.5683},
        opacity=0.5,
        height=800,
        
    )

    # Enable scroll zoom and set margins
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(
            uirevision='constant',  # Keeps zoom level and position when updating
            #scrollZoom=True         # Enables scroll zooming on the map
        )
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8893)

