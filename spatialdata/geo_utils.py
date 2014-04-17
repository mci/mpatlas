#from models import Meow, meow_mapping

dl_geom = ''

def fix_geom_dateline(geom):
    # First do a validity check, then fix topology using PostGIS 2.0 tools
    if ST_IsValid(geom):
        ST_MakeValid(geom)
    envpoly = ST_Envelope(geom)
    bbox = Box2D(geom)  # BOX(1 2,5 6)
    xmax = ST_XMax(bbox)  # or ST_XMax(envpoly)
    xmin = ST_XMin(bbox)  # or ST_XMin(envpoly)
    xmax = ST_XMax(geom)
    xmin = ST_XMin(geom)
    if xmin < -180 or xmin > 180:
        # Some coords are outside -180 to 180.
        # Shift things around until everything is clipped between -180 to 180.
        # Polygons across dateline will be split into 2 pieces on each side.
        # This should now be safe to bring into PostGIS as a geometry or geography
        geom = 'select g from ST_AsText(ST_WrapX(ST_WrapX(ST_GeometryFromText(%s,4326), 0, 360), 180, -360)) as g' % wkt
    return geom

def geom2geog(geom):
    geom_out = geom
    if ST_XMin(geom == -180 && ST_XMax(geom) == 180:
        # Polygon reaches across entire world, mostly likely because it's split
        # at the dateline, with one piece touching -180 and another at 180
        # First, try moving western hemisphere over 360 degrees (longitudes are now 0-360)
        geom_shift = select g from ST_WrapX(geom, 0, 360)
        # Check new min/max, if they're less than 360, transform this shifted geometry into geography,
        # otherwise transform original geometry in geography
        if (ST_XMax(geom_shift) - ST_XMin(geom_shift) < 360):
            geom_out = geom_shift
    # Transform to Plate Carree in meters (32662) then back to lat/lon (4326)
    # This will modify all points to -180 to 180 range
    geom = select g from ST_Transform(ST_Transform(geom_out, 32662), 4326)::geography as g

def geog2geom(geog):
    # Transform to geometry
    # small=UTM, polar=polar stereographic, large=mercator
    _ST_BestSRID(geog)
    _ST_BestSRID(geog1, geog2)