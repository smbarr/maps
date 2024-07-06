import geopandas as gpd

# tmp = gpd.GeoDataFrame.from_file("data/PhiladelphiaZoning201201.shp")
# tmpWGS84 = tmp.to_crs({"proj": "longlat", "ellps": "WGS84", "datum": "WGS84"})
# tmpWGS84.to_file("data/zoning.shp")

tmp = gpd.GeoDataFrame.from_file("data/penn_shp/gis_osm_natural_a_free_1.shp")
tmpWGS84 = tmp.to_crs({"proj": "longlat", "ellps": "WGS84", "datum": "WGS84"})
tmpWGS84.to_file("data/penn_natural.shp")