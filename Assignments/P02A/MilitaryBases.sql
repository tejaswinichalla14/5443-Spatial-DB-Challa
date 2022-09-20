-- Table: public.militarybases

-- DROP TABLE IF EXISTS public.militarybases;

CREATE TABLE IF NOT EXISTS public.militarybases
(
    gid integer NOT NULL DEFAULT nextval('militarybases_gid_seq'::regclass),
    ansicode character varying(8) COLLATE pg_catalog."default",
    areaid character varying(22) COLLATE pg_catalog."default",
    fullname character varying(100) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    aland double precision,
    awater double precision,
    intptlat character varying(11) COLLATE pg_catalog."default",
    intptlon character varying(12) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,4326),
    CONSTRAINT militarybases_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.militarybases
    OWNER to postgres;
-- Index: indx_military_geom

-- DROP INDEX IF EXISTS public.indx_military_geom;

CREATE INDEX IF NOT EXISTS indx_military_geom
    ON public.militarybases USING gist
    (geom)
    TABLESPACE pg_default;
    
-- loading data to table
shp2pgsql -s 4326 "tl_2021_us_mil" militarybases | psql -h localhost -p 5432 -U postgres -d project2
