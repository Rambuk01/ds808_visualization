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
import html_builder


bg_color = "#171B33"
font_color = '#9fa6b7'

""" INITIATE """
app = dash.Dash(__name__)
data = pd.read_csv('archive/listings_cleaned.csv', sep=',', encoding='utf-8')

# Load the GeoJSON file # https://www.opendata.dk/city-of-copenhagen/bydele
with open('archive/cph_fred_dist.geojson') as f:
    geojson_data = json.load(f)


types = data['room_type'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'Any room type', 'value': 'all'})
# Convert date column to datetimes. Then convert them to year strings.


## 2 Maps - scatter and area - area is standard

## Dropdown choices
## Beds, Bedrooms, Room type, Bathrooms

## Violin plots
# price vs. seasons

# How often do we get rent out? Cant be answered.

map_html = html.Div(
    className = 'map-container',
    children=[
        #html.H2(children="Map"),
        html.Div(
            dcc.Graph(id='cph-map'),
        ),
    ]
)

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
            options=type_options,
            value='all'
        )

dropdowns = html.Div(
            className="dropdowns w100",
            children= [
                html.H2(children="Dropdowns"),
                html.Div(className = 'flex flex-space-around', children=[
                    html.Div(
                        className="dropdown w50 m1",
                        children=dropdown_room_type,
                    ),
                    html.Div(
                        className='dropdown w50 m1',
                        children=dropdown_map_type,
                    ),
                ]),
            ]
        )
sidebar_wrapper = html.Div(
    className = 'sidebar-container w25 p1 box-shadow',
    children=[
        dropdowns
    ]
)

info_right = html.Div(className='info-right', children=[
    html.H1(className='header', children="Info right")
])
info_bottom = html.Div(className='info-bottom', children=[

])

content_wrapper = html.Div(
    className = 'content-wrapper w100',
    children=[
        
        html.H1(className='header none',children="Airbnb - Copenhagen"),
        html.Div(className='top-content flex flex-space-evenly', children=[
            html.Div(className='map-wrapper bd w100 m1 p1 bgw box-shadow' ,children=[
                map_html,
            ]),
            html.Div(className='info-right-wrapper bd w50 m1 p1 bgw box-shadow', children=[
                info_right,
            ]),
        ]),
        html.Div(className='info-bottom-wrapper bd m1 p1 h bgw box-shadow', children=[
            info_bottom,
        ])
        
    ]
)

app.layout = html.Div(className='page flex flex-space-around', children=[
    sidebar_wrapper,
    content_wrapper
])

""" MAP """
@app.callback(
    [
        Output(component_id='cph-map', component_property='figure'),
    ],
    [
        Input(component_id='room_types', component_property='value'),
        Input(component_id='map-type', component_property='value'),
    ]
)
def generate_map(room_types, map_type):
    ndata = data
    if room_types != 'all':
        ndata = ndata[ndata['room_type'] == room_types]
    
    if(map_type != 'choropleth'):
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
                            center={"lat": 55.6761, "lon": 12.5683},
                            zoom=11,
                            height=800,
                            mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    
    if(map_type == 'choropleth'):
        df_mean_prices = functions.get_mean_prices(ndata, geojson_data)

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
            color_continuous_scale=[
                [0, "#eff3ff"],   # Very light blue
                [0.25, "#bdd7e7"], # Light-medium blue
                [0.5, "#6baed6"], # Medium blue
                [0.75, "#3182bd"], # Dark-medium blue
                [1, "#08519c"]    # Dark blue
            ]
        )

        # Enable scroll zoom and set margins
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            mapbox=dict(
                uirevision='constant',  # Keeps zoom level and position when updating
                #scrollZoom=True         # Enables scroll zooming on the map
            )
        )

    return [fig]

if __name__ == '__main__':
    app.run_server(debug=True, port=8893)

