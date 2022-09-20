-- Table: public.airports

-- DROP TABLE IF EXISTS public.airports;

CREATE TABLE IF NOT EXISTS public.airports
(
    id smallint,
    name character varying(100) COLLATE pg_catalog."default",
    city character varying(35) COLLATE pg_catalog."default",
    country character varying(35) COLLATE pg_catalog."default",
    "3-code" character varying(3) COLLATE pg_catalog."default",
    "4-code" character varying(4) COLLATE pg_catalog."default",
    lat numeric(12,9),
    lon numeric(12,9),
    elevation smallint,
    gmt character varying(5) COLLATE pg_catalog."default",
    tz_short character varying(3) COLLATE pg_catalog."default",
    timezone character varying(30) COLLATE pg_catalog."default",
    type character varying(7) COLLATE pg_catalog."default",
    airport_type character varying(15) COLLATE pg_catalog."default",
    geom geometry
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airports
    OWNER to postgres;
-- Index: indx_airport_geom

-- DROP INDEX IF EXISTS public.indx_airport_geom;

CREATE INDEX IF NOT EXISTS indx_airport_geom
    ON public.airports USING gist
    (geom)
    TABLESPACE pg_default;
    
-- load data into table
copy airports(id ,name,city,country,"3-code","4-code",lat,lon,elevation,gmt,tz_short,timezone,type,airport_type)
from 'C:\Users\HP\Desktop\Project2\airports.csv'
DELIMITER ','
CSV HEADER;
