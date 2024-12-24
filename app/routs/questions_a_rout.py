from flask import Blueprint, request, jsonify, send_file, Response, render_template
from app.repository.for_query import *
import matplotlib.pyplot as plt
import numpy as np
import folium
import io

from app.service.folium_service import average_casualties_by_region_folium, generate_correlation_map
from app.service.plt_service import *

questions_a_blueprint = Blueprint('questions_a', __name__)


@questions_a_blueprint.route('/the_deadliest_attack_types', methods=['GET'])
def the_deadliest_attack_types():
    try:
        top_param = request.args.get('top_5', 'false').lower() == 'true'
        rating = deadliest_attack_types_rating(top_5=top_param)

        if not rating.empty:
            buf = the_deadliest_attack_types_plt(rating)

            return Response(buf.getvalue(), mimetype='image/png')
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@questions_a_blueprint.route('/average_casualties_by_region', methods=['GET'])
def average_casualties_by_region():
    try:
        top_param = request.args.get('top_5', 'false').lower() == 'true'
        region_data = casualties_with_event_coords(top_5=top_param)

        if not region_data.empty:
            folium_map = average_casualties_by_region_folium(region_data)

            # Return the map as an HTML page
            return folium_map._repr_html_()
        else:
            return jsonify({"error": "No data available"}), 404
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@questions_a_blueprint.route('/top_5_groups_by_casualties', methods=['GET'])
def top_5_groups_by_casualties_endpoint():
    try:
        group_data = top_5_groups_by_casualties()

        if not group_data.empty:
            img = top_5_groups_by_casualties_endpoint_plt(group_data)

            return send_file(img, mimetype='image/png')
        else:
            return jsonify({"error": "No data available"}), 404

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@questions_a_blueprint.route('/attack_frequency_trends', methods=['GET'])
def attack_frequency_trends_endpoint():
    try:
        # Get optional year filter from query parameters
        year_filter = request.args.get('year', default=None, type=int)

        # Get the trends
        trends = attack_frequency_trends(year_filter)

        yearly_data = pd.DataFrame(trends['yearly_trends'])
        monthly_data = pd.DataFrame(trends['monthly_trends'])

        # Generate graphs as base64 strings
        yearly_graph = generate_yearly_trends_graph(yearly_data)
        monthly_graph = generate_monthly_trends_graph(monthly_data)

        # Render HTML with the graphs
        return render_template('attack_trends.html',
                               yearly_trends_graph=yearly_graph,
                               monthly_trends_graph=monthly_graph)

    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@questions_a_blueprint.route('/events_casualties_correlation', methods=['GET'])
def events_casualties_map_endpoint():
    try:
        # Get region parameter from request
        region = request.args.get('region')

        # Calculate correlation and get data
        result = events_vs_casualties_correlation(region=region)

        if "error" in result:
            return jsonify(result), 400

        # Generate the map
        map_data = result['data']

        correlation_map = generate_correlation_map(map_data)

        # Save map to HTML file
        map_html = correlation_map._repr_html_()

        # Render the map in an HTML template
        return render_template("map.html", map_html=map_html, region=region or "All Regions")

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
