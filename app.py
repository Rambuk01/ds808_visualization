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
data = pd.read_csv('archive/listings_cleaned_v2.csv', sep=',', encoding='utf-8')
ms_df = pd.read_csv('archive/violin_data_v2.csv', sep=',', encoding='utf-8')# Load the GeoJSON file # https://www.opendata.dk/city-of-copenhagen/bydele
weekly_df = pd.read_csv('archive/weekly_prices_v2.csv', sep=',', encoding='utf-8')
with open('archive/cph_fred_dist.geojson') as f:
    geojson_data = json.load(f)


types = data['room_type'].unique()
room_type_options = [{'label': i, 'value': i} for i in types]
room_type_options.append({'label': 'All room types', 'value': 'all'})
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
sun_pie = get_sunburst_and_piechart()


sidebar_wrapper = html.Div(
    className = 'sidebar-container w25 p1 box-shadow',
    children=[
        dropdowns,
        html.Div(className="", children='', style={'height': '30px'}),
        html.Div(className="logo flex flex-center bd", children=[
                html.Img(src="/assets/hosthelper.png", style={"width": "100%",}),
            ]
        ),
        #plot_type_dropdown,
    ],
    style={'height': 1295}
)

info_right = html.Div(className='info-right flex', children=[
    sun_pie,
    html.Div(className='info-right-text m1', children=[
        html.H1(className='header left', children="General information"),
        html.Div(className="spacer-1", children=''),
        html.P(id='text-area', className='para', children="This bar chart provides an overview of the distribution of Airbnb listings across different neighborhoods in Copenhagen."),
        html.Div(className="spacer-2", children=''),
        html.H4(className='header left', children=["Room Type Distribution"]),
        html.H4(id='neighborhood-name', className='header left', children=["by Neighbourhood - Copenhagen"]),
        html.P(id='count', className='para m1', children="Number of rooms: 12543", style={"marginBottom": "12px", "marginLeft": "25px"}),
        html.P(className='para bold', children="Average prices"),
        html.P(id='avg-price-apt', className='para m1 text-box-blue', children="Private room: 532,-", style={"marginLeft": "25px"}),
        html.P(id='avg-price-private', className='para m1 text-box-red', children="Entire home / apartment: 1145,-", style={"marginLeft": "25px"}),
        html.P(id='avg-price', className='para m1 text-right', children="Total: 956,-", style={"marginLeft": "25px"}),
    ]),
])


violin_plot_wrapper = html.Div(
        className="violin-plot-wrapper m1 p1 bgw",
        children=[
            dcc.Graph(id="violin-plot"),
        ],
    )
info_bottom = html.Div(className='info-bottom', children=[
    # html.H1(className='header', children="Info Bottom"),
    # Add a container for the violin plot
    violin_plot_wrapper,
])

predict_content = get_predict_content()

content_wrapper = html.Div(
    className = 'content-wrapper w100',
    children=[
        
        html.H1(className='header none',children="Airbnb - Copenhagen"),
        
        html.Div(className='top-content flex flex-space-evenly', children=[
            html.Div(className='map-wrapper bd w40 m1 p1 bgw box-shadow' ,children=[
                map_html,
            ]),
            html.Div(className='info-right-wrapper bd fg1 m1 bgw box-shadow', children=[
                info_right,
            ]),
        ]),
        html.Div(className='flex flex-space-evenly', children=[
            html.Div(className='info-bottom-wrapper w60 bd m1 p1 bgw box-shadow', children=[
                info_bottom,
            ]),
            html.Div(
                className='predict-wrapper w40 bd m1 p1 bgw box-shadow',
                children=[
                    predict_content
                ]
            )
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

        Output(component_id='violin-plot', component_property='clickData'),
        Output(component_id='violin-plot', component_property='selectedData'),

        Output(component_id='sunburst-chart', component_property='clickData'),
        Output(component_id='sunburst-chart', component_property='selectedData'),

        Output(component_id='count', component_property='children'),
        Output(component_id='avg-price', component_property='children'),
        Output(component_id='avg-price-apt', component_property='children'),
        Output(component_id='avg-price-private', component_property='children'),

        Output(component_id='text-area', component_property='children'),
        Output(component_id='neighborhood-name', component_property='children')
    ],
    [
        Input(component_id='room_types', component_property='value'),
        Input(component_id='map-type', component_property='value'),
        Input(component_id='cph-map', component_property='clickData'),
        Input(component_id='cph-map', component_property='selectedData'),

    ]
)
def generate_map(room_types, map_type, click_data, selected_data):
    ndata = data[data['price'] < 7000]
    
    if room_types != 'all':
        ndata = ndata[ndata['room_type'] == room_types]
    
    # Default selected points
    selected_indices = []

    # If lasso selection is made, extract indices
    if selected_data:
        selected_indices = [point['pointIndex'] for point in selected_data['points']]
    
    if map_type != 'choropleth':
        fig = px.scatter_mapbox(
            data_frame=ndata,
            title=f"Airbnb Listings - {room_types}" if room_types != "all" else "Airbnb Listings - All Room Types",
            lat="latitude",
            lon="longitude",
            hover_data=["neighbourhood_cleansed", "id"],
            size="price",
            color="price",
            color_continuous_scale=[
                #"rgba(0, 0, 0, 1)",  # Black for lowest prices
                "rgba(239, 11, 22, 0.89)",   # Bright red for highest prices
                #"rgba(100, 3, 8, 0.89)",  # Dark red (close to black)
                "rgba(50, 3, 8, 0.89)",  # Dark red (close to black)
            ],
            center={"lat": 55.6741, "lon": 12.5683},
            zoom=10,
            height=map_height,
            mapbox_style="open-street-map"
        )
        if selected_data:
            # Apply selectedpoints to highlight selected indices
            fig.update_traces(
                selectedpoints=selected_indices,  # Highlight the selected points
                marker=dict(
                    opacity=0.6,  # Decrease opacity for unselected points
                    #size=10
                ),
                selected=dict(
                    marker=dict(
                        opacity=1.0,  # Full opacity for selected points
                        #size=15       # Larger size for selected points
                    )
                )
            )
    
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
            center={"lat": 55.6741, "lon": 12.5683},
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
        mapbox=dict(
            uirevision='constant',  # Keeps zoom level and position when updating
        )
    )

    # Default values for text components
    total_rooms = f"Number of rooms: {len(ndata)}"
    avg_price = f"Total: {ndata['price'].mean():.2f},-"
    text_area = "Click on a neighborhood to see more details."
    text_area = f"This bar chart provides an overview of the distribution of Airbnb listings across different neighborhoods in Copenhagen."
    neighborhood_name = f"in Copenhagen."
    
    if selected_data:
        listings_to_keep = {'id': []}
        for listing in selected_data['points']:
            id = listing['customdata'][1]
            listings_to_keep['id'].append(id)
        ndata = ndata[ndata['id'].isin(listings_to_keep['id'])]
    
    # Update based on clicked map point
    if selected_data:
        text_area = "Here you see the distribution of Airbnb listings across the area you selected."
        neighborhood_name = 'in the selected area'
        
    elif click_data:
        clicked_neighborhood = click_data['points'][0]['hovertext']
        ndata = ndata[ndata['neighbourhood_cleansed'] == clicked_neighborhood]

        avg_price = f"Total: {ndata['price'].mean():.2f},-"
        text_area = f"Details for ."
        text_area = f"Here you see the distribution of Airbnb listings across {clicked_neighborhood}."
        neighborhood_name = f"by Neighbourhood - {clicked_neighborhood}"
    
    avg_price = f"Total average: {ndata['price'].mean():.2f},-"
    total_rooms = f"Number of rooms: {len(ndata)}"
    apt = f"Entire home / apartment: {ndata['price'][ndata['room_type'] == 'Entire home/apt'].mean():.2f},-"
    private = f"Private room: {ndata['price'][ndata['room_type'] == 'Private room'].mean():.2f},-"
    
    return [fig, None, None, None, None, total_rooms, avg_price, apt, private, text_area, neighborhood_name] ## None None are placeholders, for the clickdata and selected data.


""" VIOLIN AND RIDGE """
# RIDGE PLOT VIOLIN PLOT - Define a single callback to handle both plot types
@app.callback(
    [
        Output("violin-plot", "figure"),  # Use the same output for simplicity
    ],
    [
        Input("plot-type", component_property="value"),
        Input("violin-category", component_property="value"),
        Input("cph-map", component_property="clickData"),
        Input("cph-map", component_property="selectedData"),
        Input("check-list", component_property='value')
    ],
)
def generate_plot(plot_type, selected_category, click_data, selected_data, fake_data):
    # IF YOU CLICK ON THE CHOROPLETH MAP
    if selected_data:
        listings_to_keep = {'id': []}
        for listing in selected_data['points']:
            id = listing['customdata'][1]
            listings_to_keep['id'].append(id)
        
    if click_data:
        hovertext = click_data['points'][0]['hovertext']
        id = click_data['points'][0]['location']
        listings_to_keep = data[data['neighbourhood_cleansed'] == hovertext]
    
    violin_yaxis = [0, 3000]

    # Define colors for specific categories
    custom_colors = None
    

    # Filter data based on category type
    if selected_category == "month":
        filtered_data = ms_df[ms_df["category"].isin(month_names)]
        category_labels = month_names  # Use the predefined order of months
        x_label = "Month"


    elif selected_category == "season":
        filtered_data = ms_df[ms_df["category"].isin(season_names)]
        """
        filtered_data['price'] = filtered_data.apply(
            lambda row: row['price'] * 1.5 if row['category'] == 'Summer' else row['price'],
            axis=1
        )
        """
        category_labels = season_names  # Use the predefined order of seasons
        x_label = "Season"
        custom_colors = {
            "Winter": "rgb(135, 206, 250)",  # Bluish for Winter
            "Spring": "rgb(60, 179, 113)",   # Green for Spring
            "Summer": "rgb(255, 165, 0)",    # Warm orange for Summer
            "Fall": "rgb(165, 42, 42)",      # Brown for Fall
        }
    elif selected_category == "day_of_week":
        filtered_data = weekly_df[weekly_df["day_of_week"].isin(day_names)]
        category_labels = day_names  # Use the predefined order of days
        x_label = "Day of the Week"

    elif selected_category in ['bedrooms', 'beds', 'accommodates', 'bathrooms']:
        filtered_data = data[data['bedrooms'] != -1]
        category_labels = sorted(filtered_data[selected_category].unique())  # Unique bedroom counts sorted
        x_label = f"Number of {selected_category.title()}"
        violin_yaxis = [0, 6000]

    # Remove extreme outliers
    filtered_data = functions.handle_outliers(filtered_data)

    # IF YOU CLICK ON THE CHOROPLETH MAP!
    if click_data or selected_data:
        key = 'id' if selected_category in ['bedrooms', 'beds', 'accommodates', 'bathrooms'] else 'listing_id'
        filtered_data = filtered_data[filtered_data[key].isin(listings_to_keep['id'])]
    if selected_category == 'month' and fake_data != None:
        if "true" in fake_data:
            filtered_data = functions.apply_fake_data(filtered_data, selected_category)

    # Generate the plot based on plot type
    if plot_type == "violin":
        violin_colors = None
        if selected_category == 'season':
            violin_colors = "category" if selected_category in ["month", "season"] else (
                    "day_of_week" if selected_category == "day_of_week" else "bedrooms"
                )
            
        if selected_category == "bedrooms":
            print(f"Number of bedrooms with 6: {filtered_data[filtered_data['bedrooms'] == 6].count()}")
            print(f"Number of bedrooms with 1: {filtered_data[filtered_data['bedrooms'] == 1].count()}")
        # Efter min mening, bør vi klar få 12. VI får ikke under 10.
        x = "category" if selected_category in ["month", "season"] else selected_category
        # Generate the violin plot
        fig = px.violin(
            filtered_data,
            x=x,
            y="price",
            box=True,  # Add boxplot inside the violin
            points=False,  # Hide all data points
            title=f"Violin Plot of Prices by {x_label}",
            color=violin_colors,
            category_orders={
                "category": category_labels
            } if selected_category in ["month", "season"] else {
                "day_of_week": category_labels
            } if selected_category == "day_of_week" else {
                selected_category: category_labels
            },  # Ensure correct order
            color_discrete_map=custom_colors,  # Map custom colors if available
        )
        fig.update_layout(
            xaxis_title=x_label,
            yaxis_title="Price",
            yaxis_range=violin_yaxis,  # Set the y-axis range
            margin={"r": 0, "t": 30, "l": 20, "b": 20},
            height=600,
            #plot_bgcolor="#f4f4f4",  # Background of the plot area
            #paper_bgcolor="#ffffff"  # Background of the entire figure
            plot_bgcolor='#fff', #plot_bgcolor,  # Background of the plotting area
            #paper_bgcolor=paper_bgcolor,  # Background of the entire figure
            yaxis=dict(
                gridcolor="lightblue",  # Horizontal gridline color
                gridwidth=1,            # Horizontal gridline width
                zerolinecolor="blue",   # Zero line color (if applicable)
                zerolinewidth=2         # Zero line width (if applicable)
            ),
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
                    #line_color=custom_colors[category] if selected_category == "season" else color,
                    line_color='blue',
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

    return [fig]

""" PIE, SUNBURST, BAR """
@app.callback(
    Output("sunburst-chart", 'figure'),
    [
        Input("plot-type", "value"),
        Input(component_id='cph-map', component_property='clickData'),
        Input(component_id='cph-map', component_property='selectedData'),
    ],
)
def generate_sunburst_pie(plot_type, click_data, selected_data):
    ndata = data
    # PLOT TYPE
    plot_type = 'pie' if click_data or selected_data else 'bar'

    # IF YOU SELECT ON THE MAP
    if selected_data:
        listings_to_keep = {'id': []}
        for listing in selected_data['points']:
            id = listing['customdata'][1]
            listings_to_keep['id'].append(id)
        
    if click_data:
        hovertext = click_data['points'][0]['hovertext']
        id = click_data['points'][0]['location']
        listings_to_keep = data[data['neighbourhood_cleansed'] == hovertext]

    if selected_data or click_data:
        ndata = ndata[ndata['id'].isin(listings_to_keep['id'])]
        ndata = ndata.groupby(['room_type']).size().reset_index(name='count')

    if plot_type == "sunburst":
        ndata = ndata.groupby(['neighbourhood_cleansed', 'room_type']).agg({'room_type':'count'})        
        ndata = ndata.groupby(['neighbourhood_cleansed', 'room_type']).size().reset_index(name='count')
        ndata['neighbourhood_cleansed'] = ndata['neighbourhood_cleansed'].replace({
            "Vesterbro-Kongens Enghave": "Vesterbro",
            "Brønshøj-Husum": "Brønshøj",
            "Amager Øst": "Amager Ø.",
            "Amager Vest": "Amager V.",
        })

        # Create a Sunburst chart
        fig = px.sunburst(
            ndata,
            path=["neighbourhood_cleansed", "room_type"],  # Hierarchical levels
            values="count",  # Use the count for the size of the segments
            color="room_type",  # Optional: Color by room type
            height=450,
            width=450,
        )
    
    if plot_type == "pie":
        # Create a Pie chart
        fig = px.pie(
            ndata,
            names="room_type",
            values="count",
            color="room_type",
            color_discrete_map={
                "Entire home/apt": '#636EFF',
                "Private room": '#FF7C43',
            },
            height=450,
            width=450,
        )
        # Update the layout and add labels inside the pie chart
        fig.update_traces(
            textinfo="label+value",  # Display both label (name) and value (count) inside the chart
            textposition="inside",  # Position the text inside the pie segments
            insidetextorientation="radial",  # Orient text radially for better readability
            textfont=dict(color="white"),  # Set text color to white
        )
        # Remove the legend
        fig.update_layout(showlegend=False)
    elif plot_type == "bar":
        # Aggregate data for a bar chart
        bar_data = data.groupby(["neighbourhood_cleansed", "room_type"]).size().reset_index(name='count')
        bar_data['neighbourhood_cleansed'] = bar_data['neighbourhood_cleansed'].replace({
            "Vesterbro-Kongens Enghave": "Vesterbro",
            "Brønshøj-Husum": "Brønshøj",
            "Amager Øst": "Amager Ø.",
            "Amager Vest": "Amager V.",
            # Add more replacements if needed
        })
        bar_data = bar_data.sort_values(by='count', ascending=False)
        # Create a Bar chart
        fig = px.bar(
            bar_data,
            x="neighbourhood_cleansed",
            y="count",
            color="room_type",
            color_discrete_map = {
                "Entire home/apt": "rgb(99, 110, 250)",
                "Private room": "#FF7C43",
            },
            #title="Room Type Distribution by Neighbourhood",
            height=450,
            width=650,
        )
        # Update bar chart layout for better readability
        fig.update_layout(
            xaxis_title="Neighbourhood",
            yaxis_title="Count",
            showlegend=False  # Optionally hide the legend
        )
    else:
        raise ValueError("Invalid plot_type. Use 'sunburst', 'pie', or 'bar'.")

    return fig

@app.callback(
    Output('prediction-output', 'children'),
    [
        Input('room-type-dropdown', 'value'),
        Input('neighbourhood-dropdown', 'value'),
        Input('bedrooms-input', 'value'),
        Input('beds-input', 'value'),
        Input('accommodates-input', 'value'),
    ]
)
def predict_price(room_type, neighbourhood, bedrooms, beds, accommodates):
    # Ensure all inputs are provided
    if not all([room_type, neighbourhood, bedrooms, beds, accommodates]):
        return ''
        return "Please fill in all fields."

    # Prepare input data
    input_data = pd.DataFrame([{
        'room_type': room_type,
        'neighbourhood_cleansed': neighbourhood,
        'bedrooms': bedrooms,
        'beds': beds,
        'accommodates': accommodates
    }])

    # Convert to dummy variables
    #input_data = pd.get_dummies(input_data)
    #input_data = input_data.reindex(columns=X.columns, fill_value=0)  # Match training columns

    # Make prediction
    #predicted_price = model.predict(input_data)[0]
    
    #return f"Predicted Price: {954:.2f} DKK"


if __name__ == '__main__':
    app.run_server(debug=True, port=8888)

"""
En maskinlæringstilgang til FFR i det Danske EL-marked

En maskinlæringstilgang til Fast Frequency Response mængder og priser i det danske EL-marked
"""