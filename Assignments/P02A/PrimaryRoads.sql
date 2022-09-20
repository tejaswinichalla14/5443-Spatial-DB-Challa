-- Table: public.primaryroads

-- DROP TABLE IF EXISTS public.primaryroads;

CREATE TABLE IF NOT EXISTS public.primaryroads
(
    gid integer NOT NULL DEFAULT nextval('primaryroads_gid_seq'::regclass),
    linearid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    rttyp character varying(1) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    geom geometry(MultiLineString,4326),
    CONSTRAINT primaryroads_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.primaryroads
    OWNER to postgres;
-- Index: indx_roads_geom

-- DROP INDEX IF EXISTS public.indx_roads_geom;

CREATE INDEX IF NOT EXISTS indx_roads_geom
    ON public.primaryroads USING gist
    (geom)
    TABLESPACE pg_default;
    
-- loading data from .shp file to table using cmd
shp2pgsql -s 4326 "tl_2019_us_primaryroads" primaryroads | psql -h localhost -p 5432 -U postgres -d project2
