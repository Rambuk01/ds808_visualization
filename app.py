#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:33:15 2023

@author: mariofestersen
"""
import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import random
import plotly.graph_objs as go



""" INITIATE """
app = dash.Dash(__name__)
data = pd.read_csv('archive/listings.csv', sep=',', encoding='utf-8')


types = data['room_type'].unique()
type_options = [{'label': i, 'value': i} for i in types]
type_options.append({'label': 'Any room type', 'value': 'all'})
# Convert date column to datetimes. Then convert them to year strings.s

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
                 html.Div([dcc.Graph(id='price-density-map')]),

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
    mydata = data
    if room_types != 'all':
        mydata = mydata[mydata['room_type'] == room_types]
    
    fig = px.scatter_mapbox(
                        data_frame=mydata,
                        title=f"Airbnb Listings - {room_types}" if room_types != "all" else "Airbnb Listings - All Room Types",
                        lat="latitude",
                        lon="longitude",
                        #hover_name="id",
                        hover_data=["host_neighbourhood"],
                        #size="count",
                        #color="count",
                        #size_max=15,
                        zoom=12,
                        height=1100,
                        mapbox_style="open-street-map")
    
    # Generate the heatmap
    fig = px.density_mapbox(
        data_frame=mydata,
        lat="latitude",
        lon="longitude",
        z=None,  # You can specify a numeric column here if you want intensity based on a variable
        radius=5,  # Adjust this for heatmap spread
        center=dict(lat=55.6761, lon=12.5683),  # Center on Copenhagen coordinates
        zoom=11,
        height=800,
        mapbox_style="open-street-map",
        title=f"Heatmap of Airbnb Listings - {room_types}" if room_types != "all" else "Heatmap of Airbnb Listings - All Room Types",
        
        # color_continuous_scale=[
        #     "rgba(255, 255, 178, 0.1)",  # Light yellow with low opacity
        #     "rgba(254, 204, 92, 0.4)",   # Yellow with medium opacity
        #     "rgba(253, 141, 60, 0.6)",   # Orange with higher opacity
        #     "rgba(240, 59, 32, 0.8)",    # Red with higher opacity
        #     "rgba(189, 0, 38, 1.0)"      # Dark red with full opacity
        # ]
    )

    fig.update_layout(margin={"r":0,"t":0,"l":20,"b":0})
    
    return [fig]

# Callback to generate and display the density map
@app.callback(
    Output('price-density-map', 'figure'),
    Input('price-density-map', 'id')  # Trigger on load only
)
def generate_density_map(_):
    fig = px.density_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        z="price",                    # Use 'price' for density intensity
        radius=10,                    # Adjust radius for intensity spread
        center=dict(lat=55.6761, lon=12.5683),  # Center on Copenhagen
        zoom=11,
        mapbox_style="carto-positron",
        color_continuous_scale="YlOrRd",  # Color scale for price
        title="Copenhagen Airbnb Price Density"
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_colorbar=dict(title="Price Density"))
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8893)

