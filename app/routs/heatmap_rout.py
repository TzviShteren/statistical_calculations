from flask import Blueprint, request, jsonify, send_file, Response
from folium import Map
from folium.plugins import HeatMap, HeatMapWithTime
from branca.colormap import linear

from app.repository.geographical_centers_of_terrorism import get_heatmap_data_by_time_period

heatmap_blueprint = Blueprint('heatmap', __name__)


@heatmap_blueprint.route('/', methods=['GET'])
def heatmap():
    try:
        # Get the time period from query parameters
        time_period = request.args.get('time_period', 'all')

        # Fetch the data
        heatmap_data, _ = get_heatmap_data_by_time_period(time_period=time_period)

        # Create a Folium map
        folium_map = Map(location=[0, 0], zoom_start=2)
        HeatMap(heatmap_data).add_to(folium_map)

        colormap = linear.Reds_09.scale(0, max([d[2] for d in heatmap_data]))
        colormap.caption = "amount of events"
        colormap.add_to(folium_map)

        # Return the map as HTML
        return folium_map._repr_html_()
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@heatmap_blueprint.route('/heatmap_with_time', methods=['GET'])
def heatmap_with_time():
    try:
        # Get the time period from query parameters
        time_period = request.args.get('time_period', 'all')

        # Fetch the data
        _, heatmap_with_time_data = get_heatmap_data_by_time_period(time_period=time_period)

        # Create a Folium map
        folium_map = Map(location=[0, 0], zoom_start=2)
        HeatMapWithTime(heatmap_with_time_data).add_to(folium_map)

        # Return the map as HTML
        return folium_map._repr_html_()
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
