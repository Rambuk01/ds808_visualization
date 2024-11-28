#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:33:15 2023

@author: mariofestersen
"""
import functions
import pandas as pd
import json
from html_builder import *


bg_color = "#171B33"
font_color = '#9fa6b7'

""" INITIATE """
app = dash.Dash(__name__)
data = pd.read_csv('archive/listings_cleaned.csv', sep=',', encoding='utf-8')
ms_df = pd.read_csv('archive/violin_data.csv', sep=',', encoding='utf-8')# Load the GeoJSON file # https://www.opendata.dk/city-of-copenhagen/bydele
weekly_df = pd.read_csv('archive/weekly_prices.csv', sep=',', encoding='utf-8')
with open('archive/cph_fred_dist.geojson') as f:
    geojson_data = json.load(f)


types = data['room_type'].unique()
room_type_options = [{'label': i, 'value': i} for i in types]
room_type_options.append({'label': 'Any room type', 'value': 'all'})
dropdown_options = {'room_type_options': room_type_options}

# Convert date column to datetimes. Then convert them to year strings.


## 2 Maps - scatter and area - area is standard

## Dropdown choices
## Beds, Bedrooms, Room type, Bathrooms

## Violin plots
# price vs. seasons

# How often do we get rent out? Cant be answered.

map_html = get_map()
dropdowns = get_dropdowns(dropdown_options)



sidebar_wrapper = html.Div(
    className = 'sidebar-container w25 p1 box-shadow',
    children=[
        dropdowns,
        #plot_type_dropdown,
    ],
    style={'height': 1295}
)

info_right = html.Div(className='info-right', children=[
    html.H1(className='header', children="Info right")
])


violin_plot_wrapper = html.Div(
        className="violin-plot-wrapper m1 p1 bgw",
        children=[
            dcc.Graph(id="violin-plot"),
        ],
    )
info_bottom = html.Div(className='info-bottom', children=[
    html.H1(className='header', children="Info Bottom"),
    # Add a container for the violin plot
    violin_plot_wrapper
])

content_wrapper = html.Div(
    className = 'content-wrapper w100',
    children=[
        
        html.H1(className='header none',children="Airbnb - Copenhagen"),
        
        html.Div(className='top-content flex flex-space-evenly', children=[
            html.Div(className='map-wrapper bd w60 m1 p1 bgw box-shadow' ,children=[
                map_html,
            ]),
            html.Div(className='info-right-wrapper bd w50 m1 p1 bgw box-shadow', children=[
                info_right,
            ]),
        ]),
        html.Div(className='info-bottom-wrapper w60 bd m1 p1 bgw box-shadow', children=[
            info_bottom,
        ])
        
    ]
)


# Add dropdowns and the plot to the app layout
#sidebar_wrapper.children.append(violin_dropdowns)

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
                            zoom=10,
                            height=map_height,
                            mapbox_style="open-street-map")
    
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
            zoom=10.5,
            center={"lat": 55.6761, "lon": 12.5683},
            opacity=0.5,
            height=map_height,
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
        #scrollZoom=True,  # Enable scroll zooming

        mapbox=dict(
            uirevision='constant',  # Keeps zoom level and position when updating
        )
    )

    return [fig]


# RIDGE PLOT VIOLIN PLOT - Define a single callback to handle both plot types
@app.callback(
    Output("violin-plot", "figure"),  # Use the same output for simplicity
    [
        Input("plot-type", "value"),  # New input for plot type
        Input("violin-category", "value"),
    ],
)
def generate_plot(plot_type, selected_category):
    # Filter data based on category type
    if selected_category == "month":
        filtered_data = ms_df[ms_df["category"].isin(month_names)]
        category_labels = month_names  # Use the predefined order of months
        x_label = "Month"
    elif selected_category == "season":
        filtered_data = ms_df[ms_df["category"].isin(season_names)]
        category_labels = season_names  # Use the predefined order of seasons
        x_label = "Season"
    elif selected_category == "day_of_week":
        filtered_data = weekly_df[weekly_df["day_of_week"].isin(day_names)]
        category_labels = day_names  # Use the predefined order of days
        x_label = "Day of the Week"
    elif selected_category == 'bedrooms':
        filtered_data = data[data['bedrooms'] != -1]
        category_labels = sorted(filtered_data["bedrooms"].unique())  # Unique bedroom counts sorted
        x_label = "Number of Bedrooms"

    # Remove extreme outliers
    filtered_data = functions.handle_outliers(filtered_data)

    # Generate the plot based on plot type
    if plot_type == "violin":
        # Generate the violin plot
        fig = px.violin(
            filtered_data,
            x="category" if selected_category in ["month", "season"] else (
                "day_of_week" if selected_category == "day_of_week" else "bedrooms"
            ),
            y="price",
            box=True,  # Add boxplot inside the violin
            points=False,  # Hide all data points
            title=f"Violin Plot of Prices by {x_label}",
            color="category" if selected_category in ["month", "season"] else (
                "day_of_week" if selected_category == "day_of_week" else "bedrooms"
            ),
            category_orders={
                "category": category_labels
            } if selected_category in ["month", "season"] else {
                "day_of_week": category_labels
            } if selected_category == "day_of_week" else {
                "bedrooms": category_labels
            },  # Ensure correct order
        )
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title="Price",
            yaxis_range=[-2000, 5000],  # Set the y-axis range
            margin={"r": 0, "t": 30, "l": 20, "b": 20},
            height=600,
        )
    elif plot_type == "ridgeline":
        # Generate the ridgeline plot
        colors = n_colors(
            "rgb(5, 200, 200)", "rgb(200, 10, 10)", len(category_labels), colortype="rgb"
        )
        fig = go.Figure()
        for idx, (category, color) in enumerate(zip(category_labels, colors)):
            if selected_category in ["month", "season"]:
                data_subset = filtered_data[filtered_data["category"] == category]["price"]
            elif selected_category == "day_of_week":
                data_subset = filtered_data[filtered_data["day_of_week"] == category]["price"]
            elif selected_category == "bedrooms":
                data_subset = filtered_data[filtered_data["bedrooms"] == category]["price"]
            fig.add_trace(
                go.Violin(
                    x=data_subset,
                    line_color=color,
                    name=str(category),  # Use the bedroom count as the name
                    spanmode="hard",  # Ensures traces don't overlap vertically
                )
            )
        fig.update_traces(
            orientation="h",
            side="positive",
            width=3,  # Adjust the width of the violins for better spacing
            points=False,  # Hide individual data points
        )
        fig.update_layout(
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            xaxis_range=[0, 6000],  # Adjust x-axis range for ridgeline
            yaxis=dict(
                tickmode="array",
                tickvals=list(range(len(category_labels))),
                ticktext=[str(label) for label in category_labels],  # Use friendly category labels
            ),
            xaxis_title="Price",
            yaxis_title=x_label,
            title=f"Ridgeline Plot by {x_label}",
            height=600,
            margin={"r": 0, "t": 30, "l": 20, "b": 20},
        )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8893)

