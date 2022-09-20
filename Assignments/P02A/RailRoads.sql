-- Table: public.railroads

-- DROP TABLE IF EXISTS public.railroads;

CREATE TABLE IF NOT EXISTS public.railroads
(
    gid integer NOT NULL DEFAULT nextval('railroads_gid_seq'::regclass),
    linearid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    geom geometry(MultiLineString,4326),
    CONSTRAINT railroads_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.railroads
    OWNER to postgres;
-- Index: indx_rail_geom

-- DROP INDEX IF EXISTS public.indx_rail_geom;

CREATE INDEX IF NOT EXISTS indx_rail_geom
    ON public.railroads USING gist
    (geom)
    TABLESPACE pg_default;
    
-- loading data from .shp to table using cmd
shp2pgsql -s 4326 "tl_2019_us_rail" railroads | psql -h localhost -p 5432 -U postgres -d project2
