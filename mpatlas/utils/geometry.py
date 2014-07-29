from django.contrib.gis import geos, gdal
from django.db import connection, transaction

# unsafe use of "%s" % (varname) string format substitution, but this should never use values
# from web users.  No chance of SQL injection here.

@transaction.atomic
def fix_geom_dateline_raw(table, geomfield, pkfield, pk):
    # First do a validity check, then fix topology using PostGIS 2.0 tools
    cursor = connection.cursor()
    cursor.execute("UPDATE %s SET %s = ST_MakeValid(%s) WHERE NOT (ST_IsValid(%s)) AND %s = %s" % (table, geomfield, geomfield, geomfield, pkfield, pk) )
    # If some coords are outside -180 to 180, shift things around until 
    # everything is clipped between -180 to 180.
    # Polygons across dateline will be split into 2 pieces on each side.
    # This should now be safe to bring into PostGIS as a geometry or geography
    cursor.execute("UPDATE %s SET %s = ST_WrapX(ST_WrapX(%s, 0, 360), 180, -360) WHERE ((ST_XMin(%s) < -180) OR (ST_XMax(%s) > 180)) AND %s = %s" % (table, geomfield, geomfield, geomfield, geomfield, pkfield, pk) )

def fix_geom_dateline(obj, geomfield='geom'):
    table = obj._meta.db_table
    pkfield = obj._meta.pk.name
    pk = obj.pk
    fix_geom_dateline_raw(table=table, geomfield=geomfield, pkfield=pkfield, pk=pk)

@transaction.atomic
def geom2geog_raw(table, geomfield, geogfield, pkfield, pk):
    cursor = connection.cursor()
    # First set geog to geom as a default in all cases
    cursor.execute("UPDATE %s SET %s = %s::geography WHERE %s = %s" % (table, geogfield, geomfield, pkfield, pk) )
    # If polygon reaches across entire world, mostly likely because it's split
    # at the dateline, with one piece touching -180 and another at 180.
    # Try moving western hemisphere over 360 degrees (longitudes are now 0-360)
    # Check new min/max, if they're less than 360, transform this shifted geometry 
    # into geography, using a transform to plate caree and back to 4326 lat/lon
    # as trick to normalize all coordinates to the range -180 to 180.
    cursor.execute("""UPDATE %s SET 
        %s = ST_Transform(ST_Transform(shift.geomshift, 32662), 4326)::geography
        FROM (
            SELECT ST_WrapX(t.%s, 0, 360) as geomshift
            FROM %s as t
            WHERE t.%s = %s AND ST_XMin(t.%s) = -180 AND ST_XMax(t.%s) = 180
        ) as shift
        WHERE %s = %s AND (ST_XMax(shift.geomshift) - ST_XMin(shift.geomshift) < 360)""" % (table, geogfield, geomfield, table, pkfield, pk, geomfield, geomfield, pkfield, pk) )

def geom2geog(obj, geomfield='geom', geogfield='geog'):
    table = obj._meta.db_table
    pkfield = obj._meta.pk.name
    pk = obj.pk
    geom2geog_raw(table=table, geomfield=geomfield, geogfield=geogfield, pkfield=pkfield, pk=pk)

def geog2geom(geog):
    # Transform to geometry
    # small=UTM, polar=polar stereographic, large=mercator
    # _ST_BestSRID(geog)
    # _ST_BestSRID(geog1, geog2)
    pass

@transaction.atomic
def simplify_geom_raw(table, geomfield, simplegeomfield, tolerance, pkfield, pk):
    # First do a validity check, then fix topology using PostGIS 2.0 tools
    cursor = connection.cursor()
    cursor.execute("UPDATE %s SET %s = ST_Multi(ST_SimplifyPreserveTopology(%s, %f)) WHERE %s = %s" % (table, simplegeomfield, geomfield, tolerance, pkfield, pk) )

def simplify_geom(obj, geomfield='geom_smerc', simplegeomfield='simple_geom_smerc', tolerance=500):
    table = obj._meta.db_table
    pkfield = obj._meta.pk.name
    pk = obj.pk
    simplify_geom_raw(table=table, geomfield=geomfield, simplegeomfield=simplegeomfield, tolerance=tolerance, pkfield=pkfield, pk=pk)