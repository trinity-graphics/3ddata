import polars as pl

def _filter_min(df: pl.DataFrame, column: str, min_value: int = None, strict: bool = False):
    if min_value is not None:
        filter_map = pl.col(column) >= min_value if strict else pl.col(column) > min_value
        return df.filter(filter_map)
    return None

def _filter_max(df: pl.DataFrame, column: str, max_value: int = None, strict: bool = False):
    if max_value is not None:
        filter_map = pl.col(column) <= max_value if strict else pl.col(column) < max_value
        return df.filter(filter_map)
    return None

# Area
def filter_area_min(df: pl.DataFrame, min_area: int = None, strict: bool = False):
    return _filter_min(df, 'mesh_area', min_area, strict)

def filter_area_max(df: pl.DataFrame, max_area: int = None, strict: bool = False):
    return _filter_max(df, 'mesh_area', max_area, strict)

# Volume
def filter_volume_min(df: pl.DataFrame, min_vol: int = None, strict: bool = False):
    return _filter_min(df, 'mesh_volume', min_vol, strict)

def filter_volume_max(df: pl.DataFrame, max_vol: int = None, strict: bool = False):
    return _filter_max(df, 'mesh_volume', max_vol, strict)

# Vertices
def filter_num_vertices_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'num_vertices', min_val, strict)

def filter_num_vertices_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'num_vertices', max_val, strict)

# Faces
def filter_num_faces_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'num_faces', min_val, strict)

def filter_num_faces_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'num_faces', max_val, strict)

# Internal edges
def filter_num_internal_edges_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'num_internal_edges', min_val, strict)

def filter_num_internal_edges_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'num_internal_edges', max_val, strict)

# Boundary edges
def filter_num_boundary_edges_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'num_boundary_edges', min_val, strict)

def filter_num_boundary_edges_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'num_boundary_edges', max_val, strict)

# Connectivity
def filter_min_connectivity(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'min_connectivity', min_val, strict)

def filter_max_connectivity(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'max_connectivity', max_val, strict)

def filter_avg_connectivity_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'avg_connectivity', min_val, strict)

def filter_avg_connectivity_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'avg_connectivity', max_val, strict)

# Components
def filter_num_components_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'num_components', min_val, strict)

def filter_num_components_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'num_components', max_val, strict)

# Smallest component
def filter_smallest_component_vertices_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'smallest_component_vertices', min_val, strict)

def filter_smallest_component_vertices_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'smallest_component_vertices', max_val, strict)

def filter_smallest_component_faces_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'smallest_component_faces', min_val, strict)

def filter_smallest_component_faces_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'smallest_component_faces', max_val, strict)

# Largest component
def filter_largest_component_vertices_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'largest_component_vertices', min_val, strict)

def filter_largest_component_vertices_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'largest_component_vertices', max_val, strict)

def filter_largest_component_faces_min(df: pl.DataFrame, min_val: int = None, strict: bool = False):
    return _filter_min(df, 'largest_component_faces', min_val, strict)

def filter_largest_component_faces_max(df: pl.DataFrame, max_val: int = None, strict: bool = False):
    return _filter_max(df, 'largest_component_faces', max_val, strict)