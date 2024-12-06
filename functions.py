import pandas as pd
{
    'bydel_nr': [10, 4, 2, 5, 6, 7, 1, 9, 8, 3, 11],
    'dummy_color': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 
    'area_name': ['Amager Vest','Vesterbro-Kongens Enghave', 'Østerbro', 'Valby', 'Vanløse', 'Brønshøj-Husum', 'Indre By', 'Amager Øst', 'Bispebjerg', 'Nørrebro', 'Frederiksberg']
}


def get_mean_prices(df: pd.DataFrame, geojson_data):
    
    # We create a dummy DataFrame with a column to match the GeoJSON 'properties' key
    legend_data = {
        "bydel_nr": [feature["properties"]["bydel_nr"] for feature in geojson_data["features"]],
        "area_name": [feature["properties"]["navn"] for feature in geojson_data["features"]],  # Add area names
    }

    # We create a new dataframe, grouped by neighbourhood_cleansed, with the mean of the prices in the neighbourhoods.
    df_price = df.groupby('neighbourhood_cleansed').agg({
        'price': 'mean',
    })

    # We extract the area_name and bydel_nr into a list.
    area = list(zip(legend_data['area_name'], legend_data['bydel_nr']))

    # Initiate the id column.
    df_price['id'] = None

    # We put the corresponding id, with the corresponding neighbourhood.
    for item in area:
        df_price.loc[item[0], 'id'] = item[1]

    # We add the index column, so 'neighbourhood_cleansed' becomes a normal column
    df_price.reset_index(inplace=True)
    return df_price


def handle_outliers(df, price_column='price', extreme_threshold=10000, cap_threshold=6000):
    """
    Handles outliers in the dataset by filtering and capping prices.
    
    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - price_column (str): The column name for prices.
    - extreme_threshold (float): The maximum price to keep in the dataset.
    - cap_threshold (float): The price cap for remaining data.

    Returns:
    - pd.DataFrame: The dataframe with outliers handled.
    """


    # Step 1: Filter out extreme outliers
    filtered_df = df[df[price_column] <= extreme_threshold]

    # Step 2: Cap remaining prices at the threshold
    filtered_df[price_column] = filtered_df[price_column].clip(upper=cap_threshold)

    # Step 3: Remove listeings with a price of 0
    filtered_df = filtered_df[filtered_df[price_column] > 100]
    return filtered_df

# Define a gradient function to calculate color intensity based on average price
def get_gradient_color(value, max_value, color_start=(200, 200, 255), color_end=(0, 0, 139)):
    """Calculate RGB values for a gradient color between start and end colors."""
    ratio = value / max_value
    r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
    g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
    b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
    return f"rgb({r},{g},{b})"