CREATE TABLE IF NOT EXISTS public.ingredient
(
    id integer PRIMARY KEY,
    ingredient character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    type character varying COLLATE pg_catalog."default"

)