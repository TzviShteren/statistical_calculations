import folium
from folium.plugins import HeatMap


def average_casualties_by_region_folium(region_data):
    folium_map = folium.Map(location=[20, 0], zoom_start=2)

    for _, row in region_data.iterrows():
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=row['average_casualty_points'] / 5,  # Scale size for better visibility
            color='blue',
            fill=True,
            fill_opacity=0.6,
            tooltip=(
                f"<strong>Region:</strong> {row['region']}<br>"
                f"<strong>Average Casualty Points:</strong> {row['average_casualty_points']:.2f}<br>"
                f"<strong>Total Events:</strong> {row['total_events']}"
            )
        ).add_to(folium_map)

    return folium_map


def generate_correlation_map(data):
    # Filter out rows with NaN latitude or longitude
    valid_data = [row for row in data if row['latitude'] is not None and row['longitude'] is not None]

    if not valid_data:
        raise ValueError("No valid location data available for mapping.")

    # Initialize map at the center of the first valid location
    map_center = [valid_data[0]['latitude'], valid_data[0]['longitude']]
    correlation_map = folium.Map(location=map_center, zoom_start=5)

    # Add heat map
    heat_data = [
        [row['latitude'], row['longitude'], row['casualty_points']]
        for row in valid_data
    ]

    HeatMap(heat_data, radius=10, blur=15, max_zoom=1).add_to(correlation_map)

    return correlation_map
