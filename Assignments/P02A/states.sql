-- Table: public.states

-- DROP TABLE IF EXISTS public.states;

CREATE TABLE IF NOT EXISTS public.states
(
    gid integer NOT NULL DEFAULT nextval('states_gid_seq'::regclass),
    region character varying(2) COLLATE pg_catalog."default",
    division character varying(2) COLLATE pg_catalog."default",
    statefp character varying(2) COLLATE pg_catalog."default",
    statens character varying(8) COLLATE pg_catalog."default",
    geoid character varying(2) COLLATE pg_catalog."default",
    stusps character varying(2) COLLATE pg_catalog."default",
    name character varying(100) COLLATE pg_catalog."default",
    lsad character varying(2) COLLATE pg_catalog."default",
    mtfcc character varying(5) COLLATE pg_catalog."default",
    funcstat character varying(1) COLLATE pg_catalog."default",
    aland double precision,
    awater double precision,
    intptlat character varying(11) COLLATE pg_catalog."default",
    intptlon character varying(12) COLLATE pg_catalog."default",
    geom geometry(MultiPolygon,4326),
    CONSTRAINT states_pkey PRIMARY KEY (gid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.states
    OWNER to postgres;
-- Index: indx_states_geom

-- DROP INDEX IF EXISTS public.indx_states_geom;

CREATE INDEX IF NOT EXISTS indx_states_geom
    ON public.states USING gist
    (geom)
    TABLESPACE pg_default;
    
-- loading .shp data to table using cmd
shp2pgsql -s 4326 "tl_2021_us_states" states | psql -h localhost -p 5432 -U postgres -d project2
