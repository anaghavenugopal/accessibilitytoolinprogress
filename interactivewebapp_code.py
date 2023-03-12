import os
import math
import overpy
from pyproj import Transformer
import json
import csv
import ast
import time

import streamlit as st
st.title("Accessibility Analysis Tool")
#st.map()
st.sidebar.caption("Select the desired features to perform the analysis")

##################################################### INPUT

# Input widget to get the travel time in minutes
travel_time = st.sidebar.slider("Travel time (in minutes)", min_value=0, max_value=180, value=30, step=1)

# Input widget to get the analysis name
analysis_name = st.text_input("Analysis name", value="Default Analysis")

##st.sidebar.multiselect('Travel Time',['5 minutes','10 minutes','15 minutes','30 minutes','45 minutes','60 minutes'])
##st.sidebar.multiselect('Modes',['Walking','Cycling','Public Transit'])
##st.sidebar.multiselect('Points of Interest',['Restaurant','Bank','Pharmacy','Supermarket','Cafe','University'])

st.sidebar.multiselect('Mode',['Walking'])

st.sidebar.image("data:image/jpeg;base64,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")


# Drag and drop file widget to upload the file containing latitude and longitude information
uploaded_file = st.file_uploader("Upload your file containing latitude and longitude information", type=["csv"])


##if file is not None:
    # Read the csv file
    ##df = pd.read_csv(file)

    # Pass the selected values and the csv file to the existing code
    ##result = existing_code(df, travel_time, modes, points_of_interest)

    # Display the result
    ##st.write(result)
    
#st.caption("Select the coordinates in map by clicking the arrow icon")



########################################## OUTPUT
col_A, col_B=st.columns(2)
with col_A:
    st.button("Run and View Analysis")
with col_B:
    st.button("Download Report")
    



##############################################################################################
############code to be integrated 


os.system('cls')

file_validity = 'n'
while file_validity == 'n':

    print('ACCESSIBILITY TOOL')
    print('')
    print('Please choose an input file.')
    print('')

    file_list = os.listdir('Inputs')
    for file in file_list:
        selection_number = file_list.index(file) + 1
        print('(' + str(selection_number) + ') ' + file)
    print('')
    try:
        file_selection = int(input('Selection: '))
    except ValueError:
        os.system('cls')
        print('ACCESSIBILITY TOOL')
        print('')
        print('Please try another selection.')
        time.sleep(2)
        os.system('cls')
        continue

    if file_selection >= 1 and file_selection <= len(file_list):
        file_validity = 'y'
        file_selected = file_list[file_selection - 1]
    else:
        os.system('cls')
        print('ACCESSIBILITY TOOL')
        print('')
        print('Please try another selection.')
        time.sleep(2)
        os.system('cls')

os.system('cls')

time_validity = 'n'
while time_validity == 'n':

    print('ACCESSIBILITY TOOL')
    print('')
    try:
        walk_time = int(input('Please enter a walking time (minutes): '))
    except ValueError:
        os.system('cls')
        print('ACCESSIBILITY TOOL')
        print('')
        print('Please try another entry.')
        time.sleep(2)
        os.system('cls')
        continue
    time_validity = 'y'

os.system('cls')
print('ACCESSIBILITY TOOL')
print('')
analysis_name = input('Please give your analysis a name: ')

os.system('cls')
print('ACCESSIBILITY TOOL')
print('')

walk_speed = 5 # Kilometers per hour.
walk_budget = ((walk_speed * 1000) / 60) * walk_time # Meters.

# Opens the points.
points = []
with open('Inputs/' + file_selected, mode = 'r', encoding = 'utf-8') as infile:
    rows = []
    for row in infile:
        rows.append(row.replace('"','').rstrip('\n').split(","))
    keys = rows[0]
    for values in rows[1:]:
        points.append(dict(zip(keys, values)))

# Identifies the extents and center of the input points.
point_min_lat = math.inf
point_min_lon = math.inf
point_max_lat = -math.inf
point_max_lon = -math.inf

for point in points:
    input_lat = float(point['lat'])
    input_lon = float(point['lon'])

    if input_lat < point_min_lat:
        point_min_lat = input_lat
    if input_lat > point_max_lat:
        point_max_lat = input_lat
    if input_lon < point_min_lon:
        point_min_lon = input_lon
    if input_lon > point_max_lon:
        point_max_lon = input_lon

centroid_lat = ((point_max_lat - point_min_lat) / 2) + point_min_lat
centroid_lon = ((point_max_lon - point_min_lon) / 2) + point_min_lon

# Defines function that can determine UTM zone and CRS of points.
def utm_zone(lat, lon):
    epsg_dict = {}
    zone_numbers = list(range(1, 60))
    zone_letters = ['N','S']

    for number in zone_numbers:
        epsg_end = zone_numbers.index(number) + 1
        for letter in zone_letters:
            zone = str(number) + letter
            if letter == 'N':
                epsg_number = str(32600 + epsg_end)
            elif letter == 'S':
                epsg_number = str(32700 + epsg_end)
            epsg_dict[zone] = 'epsg:' + epsg_number
    number = str(math.ceil(lon / 6) + 30)

    if lat >= 0:
        letter = 'N'
    elif lat < 0:
        letter = 'S'

    zone = number + letter
    epsg = epsg_dict[zone]
    return {'zone':zone,'epsg':epsg}

zone = utm_zone(centroid_lat, centroid_lon)


# Transforms the municipality extents to utm.
transformer = Transformer.from_crs('epsg:4326', zone['epsg'], always_xy = True)


# Transforms the hub extents to utm.
lon_max_utm, lat_max_utm = transformer.transform(point_max_lon, point_max_lat)
lon_min_utm, lat_min_utm = transformer.transform(point_min_lon, point_min_lat)

# Expands the extents by a certain number of meters.
buffer = int(walk_budget + 1000) # Meters

lat_max_utm_buff = lat_max_utm + buffer
lat_min_utm_buff = lat_min_utm - buffer
lon_max_utm_buff = lon_max_utm + buffer
lon_min_utm_buff = lon_min_utm - buffer

# Transforms extents from utm.
transformer2 = Transformer.from_crs(zone['epsg'], 'epsg:4326', always_xy = True)
bbox_lon_max, bbox_lat_max = transformer2.transform(lon_max_utm_buff, lat_max_utm_buff)
bbox_lon_min, bbox_lat_min = transformer2.transform(lon_min_utm_buff, lat_min_utm_buff)

file_name = 'N' + str(point_max_lat).replace('.','P') + 'S' + str(point_min_lat).replace('.','P') + 'E' + str(point_max_lon).replace('.','P') + 'W' + str(point_min_lon).replace('.','P')



# Defines function to download network within a bounding box.
def download_network_bbox(min_lat, min_lon, max_lat, max_lon):
    bbox_coordinates = str(min_lat) + ',' + str(min_lon) + ',' + str(max_lat) + ',' + str(max_lon)
    api = overpy.Overpass()
    features = []

    result = api.query("""
    [timeout:3600];
    (
      way["highway"](""" + bbox_coordinates + """);
    );
    (._;>;);
    out body;""")

    for item in result.ways:
        feature = {'type':'Feature','id':item.id,'properties':{'id':item.id,'highway':item.tags['highway']},'geometry':{'type':'LineString','coordinates':[]}}
        for node in item.nodes:
            feature['geometry']['coordinates'].append([float(node.lon),float(node.lat)])
        features.append(feature)

    return {'type':'FeatureCollection','features':features}

# Defines function to create routable graph from network.
def routable_graph(network):
    nodes_all = []

    for feature in network['features']:
        for node in feature['geometry']['coordinates']:
            nodes_all.append(str(node))

    graph = {}
    nodes_unique = list(set(nodes_all))

    for node in nodes_unique:
        graph[node] = []

    for feature in network['features']:
        highway = feature['properties']['highway']
        nodes = feature['geometry']['coordinates']
        for node in nodes:
            if nodes.index(node) == 0:
                graph[str(node)].append({'x':nodes[1][0],'y':nodes[1][1],'highway':highway})
            elif nodes.index(node) > 0 and nodes.index(node) < (len(nodes) - 1):
                graph[str(node)].append({'x':nodes[nodes.index(node) - 1][0],'y':nodes[nodes.index(node) - 1][1],'highway':highway})
                graph[str(node)].append({'x':nodes[nodes.index(node) + 1][0],'y':nodes[nodes.index(node) + 1][1],'highway':highway})
            elif nodes.index(node) == (len(nodes) - 1):
                graph[str(node)].append({'x':nodes[nodes.index(node) - 1][0],'y':nodes[nodes.index(node) - 1][1],'highway':highway})

    return graph

# Defines function that cleans up the graph and returns a new network.
def clean_network(graph, network):
    main_nodes = set()
    growth = 1

    keys = list(graph.keys())

    while growth != 0:
        old_length = len(main_nodes)
        for key in keys:
            key_nodes = set()
            for node in graph[key]:
                key_node = '[' + str(node['x']) + ', ' + str(node['y']) + ']'
                key_nodes.add(key_node)
            if len(main_nodes) == 0:
                for key_node in key_nodes:
                    main_nodes.add(key_node)
            elif len(main_nodes) > 0:
                for key_node in key_nodes:
                    if key_node in main_nodes:
                        for key_node in key_nodes:
                            main_nodes.add(key_node)
            new_length = len(main_nodes)
            growth = new_length - old_length

    new_features = []
    for feature in network['features']:
        nodes = feature['geometry']['coordinates']
        for node in nodes:
            if str(node) in main_nodes:
                new_features.append(feature)
                break
            else:
                pass

    new_network = network
    new_network['features'] = new_features

    return new_network

# Checks to see if existing network exists. If it does not exist, it downloads it, if it does exist, it opens it.
print('[1/7] Checking to see if network already exists...')
time.sleep(1)

network_status = 'n'
outputs_list = os.listdir('Outputs')
for output in outputs_list:
    if output[0:7] == 'network':
        name = output[8:-8]
        name_list = name.split('_')
        name_prefix = name_list[0]
        buff_dist = int(name_list[1])
        if name_prefix == file_name and buffer <= buff_dist:
            network_status = 'y'


if network_status == 'y':
    print('[2/7] Network exists. Opening existing file...')
    file = open('Outputs/network_' + file_name + '_' + str(buff_dist) + '.geojson')
    network_clean = json.load(file)

    time.sleep(1)
else:
    print('[2/7] Network does not exist. Downloading network...')
    print('          This may take a while, go make some coffee...')
    network_raw = download_network_bbox(bbox_lat_min, bbox_lon_min, bbox_lat_max, bbox_lon_max)

    graph_routable = routable_graph(network_raw)

    print('          Cleaning network. This may also take a while...')
    network_clean = clean_network(graph_routable, network_raw)

    print('          Exporting clean network...')

    # Writes the new network to a json file.
    network_clean['crs'] = {'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::4326'}}
    with open('Outputs/network_' + file_name + '_' + str(buffer) + '.geojson', 'w') as output_file:
        json.dump(network_clean, output_file)

# Transforms the input points to meters.
hub_lon, hub_lat = transformer.transform(input_lon, input_lat)

# Defines a function that converts the WGS84 network to a projected network.
def project_network(network):

    projected_features = []
    features = network['features']
    for feature in features:
        nodes = feature['geometry']['coordinates']
        projected_nodes = []
        for node in nodes:
            lat_wgs84 = node[1]
            lon_wgs84 = node[0]
            lon_proj, lat_proj = transformer.transform(lon_wgs84, lat_wgs84)
            projected_nodes.append([lon_proj, lat_proj])
        projected_feature = feature
        projected_feature['geometry']['coordinates'] = projected_nodes
        projected_features.append(projected_feature)

    projected_network = network_clean
    projected_network['features'] = projected_features

    return projected_network

# Converts the network to a projected network.
projected_network = project_network(network_clean)

# Defines a function that snaps points to the nearest line segment and creates snap coordinates as an output. It also adds new nodes in the network for snapping.
def snap_point_to_network(point_lat, point_lon, network):

    projected_features = network['features']

    # Creates a list of individual line segments from network and a network dictionary.
    line_segments = []
    network_dict = {}
    for feature in projected_features:
        id = feature['properties']['id']
        nodes = feature['geometry']['coordinates']
        network_dict[id] = nodes
        segment_count = list(range(1, len(nodes)))
        for segment in segment_count:
            node_1 = segment - 1
            node_2 = segment
            line = {'id':id,'nodes':[nodes[node_1], nodes[node_2]]}
            line_segments.append(line)

    # Snaps the point to the nearest line segment.
    closest_id = ''
    min_snap_dist = math.inf
    for segment in line_segments:

        node_1 = segment['nodes'][0]
        node_1_lat = node_1[1]
        node_1_lon = node_1[0]
        node_2 = segment['nodes'][1]
        node_2_lat = node_2[1]
        node_2_lon = node_2[0]

        rise = node_2_lat - node_1_lat
        run = node_2_lon - node_1_lon
        slope = rise / run
        line_angle = math.degrees(math.atan(slope))

        inverse_slope = (run/rise) * -1

        node_1_lon_diff = point_lon - node_1_lon
        node_2_lon_diff = point_lon - node_2_lon

        if inverse_slope > 0:
            if node_1_lon > node_2_lon:
                min_lat = (node_1_lon_diff * inverse_slope) + node_1_lat
                max_lat = (node_2_lon_diff * inverse_slope) + node_2_lat
            elif node_1_lon < node_2_lon:
                max_lat = (node_1_lon_diff * inverse_slope) + node_1_lat
                min_lat = (node_2_lon_diff * inverse_slope) + node_2_lat
        elif inverse_slope < 0:
            if node_1_lon > node_2_lon:
                max_lat = (node_1_lon_diff * inverse_slope) + node_1_lat
                min_lat = (node_2_lon_diff * inverse_slope) + node_2_lat
            elif node_1_lon < node_2_lon:
                min_lat = (node_1_lon_diff * inverse_slope) + node_1_lat
                max_lat = (node_2_lon_diff * inverse_slope) + node_2_lat

        if point_lat >= min_lat and point_lat <= max_lat:

            rise = node_2_lat - node_1_lat
            run = node_2_lon - node_1_lon
            slope = rise / run
            line_angle = math.degrees(math.atan(slope))

            node_1_dist = math.sqrt(abs(node_1_lat - point_lat)**2 + abs(node_1_lon - point_lon)**2)
            node_1_angle = math.degrees(math.atan((node_1_lat - point_lat) / (node_1_lon - point_lon)))

            if node_1_angle > 0 and line_angle > 0:
                if line_angle > node_1_angle:
                    alpha_angle = line_angle - node_1_angle
                elif line_angle < node_1_angle:
                    alpha_angle = node_1_angle - line_angle
            elif node_1_angle > 0 and line_angle < 0:
                alpha_angle = 180 - (abs(line_angle) + abs(node_1_angle))
            elif node_1_angle < 0 and line_angle > 0:
                alpha_angle = 180 - (abs(line_angle) + abs(node_1_angle))
            elif node_1_angle < 0 and line_angle < 0:
                if abs(line_angle) > abs(node_1_angle):
                    alpha_angle = abs(line_angle) - abs(node_1_angle)
                elif abs(line_angle) < abs(node_1_angle):
                    alpha_angle = abs(node_1_angle) - abs(line_angle)

            snap_dist = math.sin(math.radians(alpha_angle)) * node_1_dist

            beta_angle = 90 - alpha_angle

            line_seg_length = abs(math.sin(math.radians(beta_angle)) * node_1_dist)

            if snap_dist < min_snap_dist:
                min_snap_dist = snap_dist
                closest_id = segment['id']

                intersect_run = math.sin(math.radians(90 - abs(line_angle))) * line_seg_length
                intersect_rise = math.sin(math.radians(abs(line_angle))) * line_seg_length

                if slope > 0:
                    if node_1_lat > node_2_lat:
                        intersect_lat = node_1_lat - intersect_rise
                        intersect_lon = node_1_lon - intersect_run
                    elif node_1_lat < node_2_lat:
                        intersect_lat = node_1_lat + intersect_rise
                        intersect_lon = node_1_lon + intersect_run
                elif slope < 0:
                    if node_1_lat > node_2_lat:
                        intersect_lat = node_1_lat - intersect_rise
                        intersect_lon = node_1_lon + intersect_run
                    elif node_1_lat < node_2_lat:
                        intersect_lat = node_1_lat + intersect_rise
                        intersect_lon = node_1_lon - intersect_run

                # Inserts the new node into the network dictionary
                preceding_node = str(node_1)
                following_node = str(node_2)
                feature_nodes = network_dict[segment['id']]
                for node in feature_nodes:
                    node_index = feature_nodes.index(node)
                    if str(node) == preceding_node and str(feature_nodes[node_index + 1]) == following_node:
                        new_node = [intersect_lon, intersect_lat]
                        network_dict[segment['id']].insert(node_index + 1, new_node)

        elif point_lat < min_lat or point_lat > max_lat:
            node_1_dist = math.sqrt(abs(node_1_lat - point_lat)**2 + abs(node_1_lon - point_lon)**2)
            node_2_dist = math.sqrt(abs(node_2_lat - point_lat)**2 + abs(node_2_lon - point_lon)**2)

            if node_1_dist < node_2_dist:
                snap_dist = node_1_dist
                snap_lat = node_1_lat
                snap_lon = node_1_lon
            elif node_1_dist > node_2_dist:
                snap_dist = node_2_dist
                snap_lat = node_2_lat
                snap_lon = node_2_lon

            if snap_dist < min_snap_dist:
                min_snap_dist = snap_dist
                closest_id = segment['id']
                intersect_lat = snap_lat
                intersect_lon = snap_lon



    # Converts the network into a network with inserted nodes.
    for feature in network['features']:
        id = feature['properties']['id']
        appended_nodes = network_dict[id]
        feature['geometry']['coordinates'] = appended_nodes

    return {'snap_feature':closest_id,'snap_distance':min_snap_dist,'snap_lat':intersect_lat,'snap_lon':intersect_lon}

print('[3/7] Snapping points to network...')
for point in points:
    input_lat = float(point['lat'])
    input_lon = float(point['lon'])

    # Transforms the input points to meters.
    hub_lon, hub_lat = transformer.transform(input_lon, input_lat)

    snap_info = snap_point_to_network(hub_lat, hub_lon, projected_network)


# Converts the projected network into a new routable graph.
projected_graph  = routable_graph(projected_network)


print('[4/7] Creating service areas...')
accessed_list = []
polygons = []
for point in points:
    input_lat = float(point['lat'])
    input_lon = float(point['lon'])
    hub_id = point['id']

    hub_lon, hub_lat = transformer.transform(input_lon, input_lat)

    # Identifies the start node for the creation of isochrones.
    unique_nodes = list(projected_graph.keys())
    min_dist = math.inf
    start_node = ''
    for node in unique_nodes:
        node_list = ast.literal_eval(node)
        node_lat = node_list[1]
        node_lon = node_list[0]
        a = abs(hub_lat - node_lat)
        b = abs(hub_lon - node_lon)
        c = math.sqrt(a**2 + b**2)
        if c < min_dist:
            min_dist = c
            start_node = node

    # walk_budget = ((walk_speed * 1000) / 60) * walk_time # Meters.
    remaining_budget = walk_budget - min_dist
    trunk_nodes = [{'t_node':start_node,'r_budget':remaining_budget}]
    accessed_nodes = set()

    # accessed_list = []

    while len(trunk_nodes) > 0:
        new_trunk_nodes = []
        for t_node in trunk_nodes:
            t_node_list = ast.literal_eval(t_node['t_node'])
            t_node_lat = t_node_list[1]
            t_node_lon = t_node_list[0]
            r_budget = t_node['r_budget']
            branch_nodes = projected_graph[t_node['t_node']]

            for b_node in branch_nodes:
                b_node_lat = b_node['y']
                b_node_lon = b_node['x']
                b_node_type = b_node['highway']

                # This section is new. It excludes segments that are just for cars.
                if b_node_type == 'motorway' or b_node_type == 'motorway_link':
                    continue

                if str([b_node_lon, b_node_lat]) in accessed_nodes:
                    continue
                c = math.sqrt(abs(t_node_lat - b_node_lat)**2 + abs(t_node_lon - b_node_lon)**2)

                if r_budget - c > 0:
                    b_budget = r_budget - c
                    t_dict = {'t_node':str([b_node_lon, b_node_lat]),'r_budget':b_budget}
                    new_trunk_nodes.append(t_dict)
                    accessed_nodes.add(str([b_node_lon, b_node_lat]))

                    access_dict = {'point_id':hub_id,'lat':b_node_lat,'lon':b_node_lon,'r_budget':b_budget}
                    accessed_list.append(access_dict)
                elif r_budget - c < 0:
                    remainder = r_budget - c
                    slope = (b_node_lat - t_node_lat) / (b_node_lon - t_node_lon)
                    line_angle = math.degrees(math.atan(slope))

                    intersect_run = math.sin(math.radians(90 - abs(line_angle))) * remainder
                    intersect_rise = math.sin(math.radians(abs(line_angle))) * remainder

                    if slope > 0:
                        if t_node_lat > b_node_lat:
                            intersect_lat = t_node_lat + intersect_rise
                            intersect_lon = t_node_lon + intersect_run
                        elif t_node_lat < b_node_lat:
                            intersect_lat = t_node_lat - intersect_rise
                            intersect_lon = t_node_lon - intersect_run
                    elif slope < 0:
                        if t_node_lat > b_node_lat:
                            intersect_lat = t_node_lat + intersect_rise
                            intersect_lon = t_node_lon - intersect_run
                        elif t_node_lat < b_node_lat:
                            intersect_lat = t_node_lat - intersect_rise
                            intersect_lon = t_node_lon + intersect_run

                    accessed_nodes.add(str([intersect_lon, intersect_lat]))

                    access_dict = {'point_id':hub_id,'lat':intersect_lat,'lon':intersect_lon,'r_budget':0}
                    accessed_list.append(access_dict)

        trunk_nodes = new_trunk_nodes



    # Defines a function to create the isochrone polygon.
    k = len(accessed_nodes)
    polygon_nodes = []

    # Converts the set of accessed nodes to a list of accessed nodes.
    accessed_nodes_list = []
    for node in accessed_nodes:
        node_list = ast.literal_eval(node)
        accessed_nodes_list.append(node_list)

    # Identifies the node with the minimum latitude. This will be the starting point.
    min_lat = math.inf
    start_node = ''
    for node in accessed_nodes_list:
        lat = node[1]
        if lat < min_lat:
            min_lat = lat
            start_node = node

    polygon_nodes.append(start_node)
    previous_node = ''
    next_k = ''
    adj_angle = 0
    traj = 90

    while next_k != polygon_nodes[0]:

        # Creates a list of the k nearest neighbors.
        k_list = []

        start_node_lat = start_node[1]
        start_node_lon = start_node[0]

        for node in accessed_nodes_list:
            if node == start_node or node == previous_node:
                continue
            if node != polygon_nodes[0] and node in polygon_nodes:
                continue
            lat = node[1]
            lon = node[0]
            distance = math.sqrt(abs(start_node_lat - lat)**2 + abs(start_node_lon - lon)**2)
            k_dict = {'id':node,'distance':distance}
            k_list.append(k_dict)

        k_list = sorted(k_list, key = lambda dict: dict['distance'])[0:k]

        min_dist = 360

        k_angle_selected = 0

        for k_node in k_list:
            k_lat = k_node['id'][1]
            k_lon = k_node['id'][0]
            k_angle = math.degrees(math.atan2(k_lat - start_node_lat, k_lon - start_node_lon))

            if k_angle < 0:
                k_angle = k_angle % 360

            if traj - 90 >= 0:
                hard_right = traj - 90
            elif traj - 90 < 0:
                hard_right = (traj - 90) + 360

            if k_angle - hard_right > 0:
                dist = k_angle - hard_right
            elif k_angle - hard_right < 0:
                dist = (360 - hard_right) + k_angle

            if dist < min_dist:
                min_dist = dist
                next_k = k_node['id']
                k_angle_selected = k_angle

        traj = k_angle_selected
        start_node = next_k

        polygon_nodes.append(next_k)

    polygon_dict = {'id':hub_id,'polygon_nodes':polygon_nodes}
    polygons.append(polygon_dict)


# Defines a function for downloading the amenities in an area.
def download_amenities(min_lat, min_lon, max_lat, max_lon):
    bbox_coordinates = str(min_lat) + ',' + str(min_lon) + ',' + str(max_lat) + ',' + str(max_lon)
    api = overpy.Overpass()
    features = []

    result = api.query("""
    (
      node["amenity"](""" + bbox_coordinates + """);
      node["shop"](""" + bbox_coordinates + """);
      node["public_transport"="stop_position"](""" + bbox_coordinates + """);
    );
    (._;>;);
    out body;""")

    for item in result.nodes:
        tag_set = item.tags.keys()
        if 'amenity' in tag_set:
            type = 'amenity'
        elif 'shop' in tag_set:
            type = 'shop'
        elif 'public_transport' in tag_set:
            type = 'public_transport'

        feature = {'id':item.id,'type':type,'description':item.tags[type],'lat':float(item.lat),'lon':float(item.lon)}
        features.append(feature)

    return features

# Checks to see if a file with the amenities already exists.
print('[5/7] Checking to see if amenities file already exists...')
time.sleep(1)

amenity_status = 'n'
outputs_list = os.listdir('Outputs')
for output in outputs_list:
    if output[0:9] == 'amenities':
        name = output[10:-4]
        name_list = name.split('_')
        name_prefix = name_list[0]
        buff_dist = int(name_list[1])
        if name_prefix == file_name and buffer <= buff_dist:
            amenity_status = 'y'

# if os.path.exists('Outputs/amenities_' + extents['name'] + '.csv') is True:
if amenity_status == 'y':
    print('[6/7] Amenities file already exists. Opening existing file...')
    time.sleep(1)

    amenities = []

    with open('Outputs/amenities_' + file_name + '_' + str(buff_dist) + '.csv', mode = 'r', encoding = 'utf-8') as infile:
        rows = []
        for row in infile:
            rows.append(row.replace('"','').rstrip('\n').split(","))
        keys = rows[0]
        for values in rows[1:]:
            amenities.append(dict(zip(keys, values)))
else:
    print('[6/7] Amenities file does not exist. Downloading amenities...')

    amenities = download_amenities(bbox_lat_min, bbox_lon_min, bbox_lat_max, bbox_lon_max)

    # Writes a csv file with the downloaded amenities.
    keys = amenities[0].keys()
    with open('Outputs/amenities_' + file_name + '_' + str(buffer) + '.csv', 'w', newline = '', encoding = 'utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(amenities)

# Transforms the decimal degree coordinates to the UTM-zone meter coordinates.
for amenity in amenities:
    amenity_lon_utm, amenity_lat_utm = transformer.transform(amenity['lon'], amenity['lat'])
    amenity['lat_utm'] = amenity_lat_utm
    amenity['lon_utm'] = amenity_lon_utm

# Measures access to amenities within the service areas.
print('[7/7] Measuring accessibility...')
time.sleep(1)
polygon_features = []
for polygon in polygons:

    polygon_nodes = polygon['polygon_nodes']
    input_id = polygon['id']

    # Identifies the extents of the service area.
    min_lat = math.inf
    min_lon = math.inf
    max_lat = -math.inf
    max_lon = -math.inf

    for p_node in polygon_nodes:
        p_node_lat = p_node[1]
        p_node_lon = p_node[0]
        if p_node_lat < min_lat:
            min_lat = p_node_lat
        if p_node_lat > max_lat:
            max_lat = p_node_lat
        if p_node_lon < min_lon:
            min_lon = p_node_lon
        if p_node_lon > max_lon:
            max_lon = p_node_lon

    # Creates list of line segments included in the service area.
    service_area_segments = []
    for p_node in polygon_nodes:
        p_node_index = polygon_nodes.index(p_node)
        if p_node_index < len(polygon_nodes) - 1:
            start_node = p_node
            start_lat = start_node[1]
            start_lon = start_node[0]
            end_node = polygon_nodes[p_node_index + 1]
            end_lat = end_node[1]
            end_lon = end_node[0]
            segment_dict = {'start':start_node,'end':end_node}
            service_area_segments.append(segment_dict)

    # Creates a dictionary that will eventually be the main output.
    amenity_types = ['stop_position','restaurant','bakery','supermarket','kindergarten','doctors','pharmacy','pub','toilets','school']
    amenity_dict = {}
    amenity_dict['id'] = input_id
    amenity_dict['walk_time'] = walk_time
    for type in amenity_types:
        amenity_dict[type] = 0

    # Counts the amenities within each category
    amenity_counter = 0
    for amenity in amenities:
        if amenity['description'] not in amenity_types:
            continue
        intersects = 0
        amenity_lat = amenity['lat_utm']
        amenity_lon = amenity['lon_utm']
        if amenity_lat <= max_lat and amenity_lat >= min_lat and amenity_lon >= min_lon and amenity_lon <= max_lon:
            for segment in service_area_segments:
                start_lat = segment['start'][1]
                start_lon = segment['start'][0]
                end_lat = segment['end'][1]
                end_lon = segment['end'][0]
                rise = end_lat - start_lat
                run = end_lon - start_lon
                slope = rise / run
                if start_lat > end_lat:
                    seg_min_lat = end_lat
                    seg_max_lat = start_lat
                elif start_lat < end_lat:
                    seg_min_lat = start_lat
                    seg_max_lat = end_lat
                if (amenity_lat <= seg_max_lat and amenity_lat >= seg_min_lat) and (amenity_lon <= start_lon or amenity_lon <= end_lon):
                    intersects += 1
        if int(intersects / 2) * 2 != intersects:
            amenity_dict[amenity['description']] += 1
            amenity_counter += 1

    polygon_features.append(amenity_dict)

# Converts the convex hull back into WGS84.
polygons_wgs84 = []
for polygon in polygons:
    polygon_wgs84 = []
    for node in polygon['polygon_nodes']:
        node_lat = node[1]
        node_lon = node[0]
        node_lon_wgs84, node_lat_wgs84 = transformer2.transform(node_lon, node_lat)
        polygon_wgs84.append([node_lon_wgs84, node_lat_wgs84])
    polygons_wgs84.append(polygon_wgs84)

convex_hull = {
"type": "FeatureCollection",
"name": "serviceareas_" + analysis_name + '_' + str(walk_time),
"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::4326" } },
"features": []
}

for polygon in polygon_features:
    polygon_index = polygon_features.index(polygon)
    feature = {"type": "Feature", "properties": polygon, "geometry": {"type": "Polygon", "coordinates": [polygons_wgs84[polygon_index]]}}
    convex_hull['features'].append(feature)

with open('Outputs/serviceareas_' + analysis_name + '_' + str(walk_time) + '.geojson', 'w') as output_file:
    json.dump(convex_hull, output_file)

# Creates summary table.
# summary_table = []
# summary_table.append(amenity_dict)
keys = polygon_features[0].keys()
with open('Outputs/summary_' + analysis_name + '_' + str(walk_time) + '.csv', 'w', newline = '', encoding = 'utf-8') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(polygon_features)

print('')
print('Process complete!')



########################################################################
