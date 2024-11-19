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