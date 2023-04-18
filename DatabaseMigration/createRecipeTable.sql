-- Table: public.recipe

-- DROP TABLE IF EXISTS public.recipe;

CREATE TABLE IF NOT EXISTS public.recipe
(
    id integer NOT NULL,
    name character varying COLLATE pg_catalog."default",
    instructions character varying COLLATE pg_catalog."default",
    servings character varying COLLATE pg_catalog."default",
    CONSTRAINT recipe_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.recipe
    OWNER to postgres;