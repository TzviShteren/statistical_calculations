import folium
from folium.plugins import MarkerCluster


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

    # Initialize MarkerCluster
    marker_cluster = MarkerCluster().add_to(correlation_map)

    # Add markers to the cluster
    for row in valid_data:
        latitude = row['latitude']
        longitude = row['longitude']
        casualty_points = row['casualty_points']
        num_killed = row['num_killed']
        num_wounded = row['num_wounded']
        location_info = f"""
        <b>Casualty Points:</b> {casualty_points}<br>
        <b>Number Killed:</b> {num_killed}<br>
        <b>Number Wounded:</b> {num_wounded}<br>
        """

        # Add marker with popup info
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(location_info, max_width=300),
            tooltip=f"Casualty Points: {casualty_points}"
        ).add_to(marker_cluster)

    return correlation_map
