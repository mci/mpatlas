-- Copyright (C) 2010 Sandro Santilli <strk@keybit.net>
-- 
-- This work is placed into the public domain.
--
-- SYNOPSYS:
--   ST_WrapX(geometry, wrap float8, move float8)
--
-- DESCRIPTION:
--
--   This function split the input geometries and then
--   moves every resulting component 
--   with bounding box falling on the right (for
--   negative 'move') or on the left (for positive 'move')
--   of given 'wrap' line in the direction specified
--   by the 'move' parameter finally re-unioning the pieces
--   togheter.
--
--   It is useful to "recenter" long-lat input to have features
--   of interest not spawned from one side to the other.
--
-- USAGE:
--
--	-- Move all components of the given geometries whose bounding box
--	-- falls completely on the left of x=0 to +360
--	select ST_WrapX(the_geom, 0, 360); 
--
--	-- Move all components of the given geometries whose bounding box
--	-- falls completely on the left of x=-30 to +360
--	select ST_WrapX(the_geom, -30, 360); 
--
--
CREATE OR REPLACE FUNCTION ST_WrapX(geom_in geometry, cutx float8, amount float8)
RETURNS geometry AS $$
DECLARE
	geom_out geometry;
	blade geometry;
	srid int;
	ymin float8;
	ymax float8;
BEGIN
	SELECT ST_SRID(geom_in) INTO srid;

	ymin := ST_YMin(geom_in);
	ymax := ST_YMax(geom_in);
	blade := ST_SetSrid(ST_MakeLine(
		ST_MakePoint(cutx, ymin-1),
		ST_MakePoint(cutx, ymax+1)), srid);

	-- RAISE NOTICE 'Blade is %', ST_AsText(blade);

	IF amount = 0 THEN
		RETURN geom_in;
	ELSIF amount < 0 THEN
		-- move left what overlaps or is NOT
		-- on the right of cutx
		SELECT ST_Union(component) INTO geom_out FROM (
			SELECT
			CASE WHEN geom &> ST_SetSrid(ST_MakePoint(cutx, 0), srid) THEN
				ST_Translate(geom, amount, 0)
			ELSE
				geom
			END as component
			FROM (
				SELECT (ST_Dump(ST_Split(geom_in, blade))).geom 
			) as dump
		) as processed;
	ELSE -- amount > 0
		-- move right what overlaps or is NOT
		-- on the left of cutx
		SELECT ST_Union(component) INTO geom_out FROM (
			SELECT
			CASE WHEN geom &< ST_SetSrid(ST_MakePoint(cutx, 0), srid) THEN
				ST_Translate(geom, amount, 0)
			ELSE
				geom
			END as component
			FROM (
				SELECT (ST_Dump(ST_Split(geom_in, blade))).geom 
			) as dump
		) as processed;
	END IF;

	RETURN geom_out;
END
$$ LANGUAGE 'plpgsql';
