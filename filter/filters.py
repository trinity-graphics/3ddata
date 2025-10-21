import polars as pl

def filter_area_min(df, min_area: int = None, strict: bool = False):
    filtered_df = None
    if min_area is not None:
        filter_map = pl.col('mesh_area') >= min_area if strict else pl.col('mesh_area') > min_area
        filtered_df = merged_df.filter(filter_map)
    return filtered_df

def filter_area_max(df, max_area: int = None, strict: bool = False):
    filtered_df = None
    if max_area is not None:
        filter_map = pl.col('mesh_area') <= max_area if strict else pl.col('mesh_area') < max_area
        filtered_df = merged_df.filter(filter_map)
    return filtered_df

def filter_volume_min(df, min_vol: int = None, strict: bool = False):
    filtered_df = None
    if min_vol is not None:
        filter_map = pl.col('mesh_volume') >= min_vol if strict else pl.col('mesh_volume') > min_vol
        filtered_df = merged_df.filter(filter_map)
    return filtered_df

def filter_volume_max(df, max_vol: int = None, strict: bool = False):
    filtered_df = None
    if max_vol is not None:
        filter_map = pl.col('mesh_volume') <= max_vol if strict else pl.col('mesh_volume') < max_vol
        filtered_df = merged_df.filter(filter_map)
    return filtered_df

def filter_volume_min(df, min_vol: int = None, strict: bool = False):
    filtered_df = None
    if min_vol is not None:
        filter_map = pl.col('mesh_volume') >= min_vol if strict else pl.col('mesh_volume') > min_vol
        filtered_df = merged_df.filter(filter_map)
    return filtered_df

def filter_volume_max(df, max_vol: int = None, strict: bool = False):
    filtered_df = None
    if max_vol is not None:
        filter_map = pl.col('mesh_volume') <= max_vol if strict else pl.col('mesh_volume') < max_vol
        filtered_df = merged_df.filter(filter_map)
    return filtered_df