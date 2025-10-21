from filters import *

miv512_mia0d001_mac8_mic2_com10 = [
    {'filter': filter_num_vertices_max, 'params': {'max_val': 512, 'strict': True}},
    {'filter': filter_area_min, 'params': {'min_val': 0.001, 'strict': False}},
    {'filter': filter_max_connectivity, 'params': {'max_val': 8, 'strict': True}},
    {'filter': filter_min_connectivity, 'params': {'min_val': 2, 'strict': True}},
    {'filter': filter_num_components_max, 'params': {'max_val': 10, 'strict': True}},
]