import sys
import numpy as np
import mapnik

def addLayer(map, name, symbolizer, shp_file, filter=None, printloc=False):
    s = mapnik.Style()
    r = mapnik.Rule()
    r.symbols.append(symbolizer)
    if filter is not None:
        # r2 = mapnik.Rule()
        f = mapnik.Filter(filter.encode('utf-8'))
        # r.filter())
        r.filter = f
        # print("\n".join(dir(r)))
        # print(r.filter)
    s.rules.append(r)
    map.append_style(f"{name}_style", s)

    shp = mapnik.Shapefile(file=shp_file)
    # print(shp.envelope())

    layer = mapnik.Layer(f"{name}_layer")
    layer.datasource = shp
    layer.styles.append(f"{name}_style")

    map.layers.append(layer)

def genMap(filename, width, center, zoom):
    # width = 600
    # height = int(width*((np.sqrt(5)+1)/2))
    height = int(width*8/7)
    m = mapnik.Map(width,height)
    # m.background = mapnik.Color('#f6f6f6')
    m.background = mapnik.Color('#dadada')

    road_symbolizer = mapnik.LineSymbolizer()
    # road_symbolizer.stroke = mapnik.Color('#c6d4e2')
    road_symbolizer.stroke = mapnik.Color('#222222')
    if "penn" in filename:
        road_symbolizer.stroke_width = 2.0
    else:
        road_symbolizer.stroke_width = 1.5

    highway_symbolizer = mapnik.LineSymbolizer()
    # highway_symbolizer.stroke = mapnik.Color('#8ba5c1')
    highway_symbolizer.stroke = mapnik.Color('#222222')
    if "penn" in filename:
        highway_symbolizer.stroke_width = 4.0
    else:
        highway_symbolizer.stroke_width = 3.0

    water_symbolizer = mapnik.PolygonSymbolizer()
    # water_symbolizer.fill = mapnik.Color('#90daee')
    water_symbolizer.fill = mapnik.Color('#ffffff')

    park_symbolizer = mapnik.PolygonSymbolizer()
    # park_symbolizer.fill = mapnik.Color('#d3f8e2')
    park_symbolizer.fill = mapnik.Color('#9f9f9f')

    building_symbolizer = mapnik.PolygonSymbolizer()
    # building_symbolizer.fill = mapnik.Color("#333333")
    building_symbolizer.fill = mapnik.Color("#222222")
    
    if "penn_state" in filename:
        addLayer(
            m,
            "buildings",
            building_symbolizer,
            "data/penn_shp/gis_osm_buildings_a_free_1.shp",
        )
    addLayer(
        m,
        "PSU_buildings",
        building_symbolizer,
        "data/psu_buildings.shp"
    )
    addLayer(
        m,
        "natural",
        park_symbolizer,
        "data/penn_shp/gis_osm_pois_a_free_1.shp",
        filter="[fclass]='park'"
    )
    addLayer(
        m,
        "pwater",
        water_symbolizer,
        "data/tl_2023_42045_areawater.shp"
    )
    addLayer(
        m,
        "dwater",
        water_symbolizer,
        "data/tl_2023_42017_areawater.shp"
    )
    addLayer(
        m,
        "mwater",
        water_symbolizer,
        "data/tl_2023_42101_areawater.shp"
    )
    addLayer(
        m,
        "pitt_water",
        water_symbolizer,
        "data/tl_2023_42003_areawater.shp"
    )

    # addLayer(
    #     m,
    #     "land",
    #     polygon_symbolizer,
    #     "data/ne_10m_land.shp"
    # )
    # addLayer(
    #     m,
    #     "centre_sidewalks",
    #     # polygon_symbolizer2,
    #     line_symbolizer,
    #     "data/psu_sidewalks.shp",
    #     printloc=True
    # )
    # addLayer(
    #     m,
    #     "centre_roads",
    #     polygon_symbolizer2,
    #     # "data/tl_2023_42027_edges.shp"
    #     "data/psu_roads_major.shp"
    # )
    addLayer(
        m,
        "centre",
        road_symbolizer,
        "data/tl_2023_42027_edges.shp"
        # "data/psu_roads_major.shp"
    )
    addLayer(
        m,
        "bucks",
        road_symbolizer,
        "data/tl_2023_42017_edges.shp"
    )
    # addLayer(
    #     m,
    #     "bucks_addr",
    #     line_symbolizer,
    #     "data/bucks_addresses.shp"
    #     # "data/BucksCounty_Site_Address_Points202403.shp"
    # )
    # addLayer(
    #     m,
    #     "montco",
    #     line_symbolizer,
    #     "data/montco_buildings.shp"
    #     # "data/tl_2023_42091_edges.shp"
    # )
    addLayer(
        m,
        "j1_streets",
        road_symbolizer,
        "data/tl_2023_34015_roads.shp"
    )
    addLayer(
        m,
        "j2_streets",
        road_symbolizer,
        "data/tl_2023_34007_roads.shp"
    )
    addLayer(
        m,
        "j3_streets",
        road_symbolizer,
        "data/tl_2023_34005_roads.shp"
    )
    addLayer(
        m,
        "montco_streets",
        road_symbolizer,
        "data/montco_streets.shp"
        # "data/tl_2023_42091_edges.shp"
    )
    addLayer(
        m,
        "phila_streets",
        road_symbolizer,
        "data/phila_streets.shp",
    )
    addLayer(
        m,
        "phila_streets",
        road_symbolizer,
        "data/tl_2023_42003_roads.shp"
    )
    addLayer(
        m,
        "us_roads",
        highway_symbolizer,
        # "data/tl_2023_us_primaryroads.shp"
        "data/tl_2023_42_prisecroads.shp"
    )
    m.aspect_fix_mode = mapnik.aspect_fix_mode.ADJUST_BBOX_HEIGHT
    extent = mapnik.Box2d(center[1]+zoom, center[0]-zoom, center[1]-zoom, center[0]+zoom)
    m.zoom_to_box(extent)
    mapnik.render_to_file(m, filename)#, 'svg')
    # print("\n".join(dir(mapnik)))
    # print(mapnik.render(m))

width = 600
home = [40.252070, -75.207322]
penn_state = [40.801889, -77.863154]
penn_state = [40.801889, -77.863154+0.002]
phila = [39.952378, -75.163576-0.003]
pitt = [40.440749, -79.992361]
zoom = 0.015
# penn_state_zoom = 0.013
penn_state_zoom = 0.013
phila_zoom = 0.05
pitt_zoom = 0.05

# genMap("home.svg", width, home, zoom)
genMap("penn_state.svg", width, penn_state, penn_state_zoom)
genMap("phila.svg", width, phila, phila_zoom)
genMap("pitt.svg", width, pitt, pitt_zoom)
