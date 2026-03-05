from flask import Flask, render_template, jsonify
import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.storage import load_json
from utils.geo import haversine_distance
from core.models.mapgraph import MapGraph
from config.settings import ROAD_CLUSTERING_FACTOR


app = Flask(__name__, template_folder='templates', static_folder='static')

# Global variable to store the map graph
map_graph = None

def generate_map():
    global map_graph
    map_graph = MapGraph()

    # Load locations
    locations_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'locations.json')
    locations = load_json(locations_path)

    # Add all locations as nodes
    for loc in locations:
        map_graph.add_location(loc['id'])

    # Calculate distances between all pairs
    n = len(locations)
    distances = {}
    for i in range(n):
        for j in range(i + 1, n):
            loc1, loc2 = locations[i], locations[j]
            dist = haversine_distance(loc1['lat'], loc1['lon'], loc2['lat'], loc2['lon'])
            distances[(loc1['id'], loc2['id'])] = dist
            distances[(loc2['id'], loc1['id'])] = dist

    # Check if an edge would be redundant (indirect path is shorter/similar)
    def is_edge_redundant(loc_a_id, loc_b_id):
        dist_ab = distances.get((loc_a_id, loc_b_id), float('inf'))
        
        for loc_c in locations:
            loc_c_id = loc_c['id']
            if loc_c_id == loc_a_id or loc_c_id == loc_b_id:
                continue
            
            dist_ac = distances.get((loc_a_id, loc_c_id), float('inf'))
            dist_cb = distances.get((loc_c_id, loc_b_id), float('inf'))
            dist_through_c = dist_ac + dist_cb
            
            # If path through c is shorter or within 5% tolerance, edge is redundant
            if dist_through_c <= dist_ab / ROAD_CLUSTERING_FACTOR:
                return True
        
        return False

    # For each location, find 3 nearest non-redundant neighbors
    added_edges = set()
    for loc in locations:
        # Get distances to all other locations
        distances_from_loc = []
        for other_loc in locations:
            if loc['id'] != other_loc['id']:
                dist = distances.get((loc['id'], other_loc['id']), float('inf'))
                distances_from_loc.append((dist, other_loc['id']))
        
        distances_from_loc.sort()
        
        # Connect to 3 nearest neighbors that don't create redundant edges
        connected = 0
        for dist, other_id in distances_from_loc:
            if connected >= 3:
                break
            
            edge = tuple(sorted([loc['id'], other_id]))
            if edge not in added_edges:
                # Check if this edge would be redundant
                if not is_edge_redundant(loc['id'], other_id):
                    added_edges.add(edge)
                    connected += 1
                else:
                    # If marked as redundant, skip to next candidate
                    continue

    # Apply edges to graph
    for loc_a_id, loc_b_id in added_edges:
        try:
            map_graph.connect(loc_a_id, loc_b_id)
        except ValueError:
            pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/api/map-data')
def map_data():
    if map_graph is None:
        return jsonify({'error': 'Map not generated'}), 500

    # Load locations for details
    locations_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'locations.json')
    locations = load_json(locations_path)

    # Create location dict for quick lookup
    loc_dict = {loc['id']: loc for loc in locations}

    nodes = []
    for node_id in map_graph.nodes:
        loc = loc_dict.get(node_id, {})
        nodes.append({
            'id': node_id,
            'name': loc.get('name', ''),
            'lat': loc.get('lat', 0),
            'lon': loc.get('lon', 0),
            'type': loc.get('location_type', '')
        })

    edges = []
    for node_id, neighbors in map_graph.adj.items():
        for neighbor in neighbors:
            # Avoid duplicates
            if node_id < neighbor:
                edges.append({
                    'source': node_id,
                    'target': neighbor
                })

    return jsonify({
        'nodes': nodes,
        'edges': edges
    })

if __name__ == '__main__':
    generate_map()
    app.run(debug=True)
