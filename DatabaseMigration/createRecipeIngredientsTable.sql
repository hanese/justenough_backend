-- Table: public.recipe_ingredients

-- DROP TABLE IF EXISTS public.recipe_ingredients;

CREATE TABLE IF NOT EXISTS public.recipe_ingredients
(
    recipe_id integer,
    id integer NOT NULL,
    text character varying COLLATE pg_catalog."default",
    CONSTRAINT recipe_ingredients_pkey PRIMARY KEY (id),
    CONSTRAINT recipe_ingredients_recipe_id_fkey FOREIGN KEY (recipe_id)
        REFERENCES public.recipe (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.recipe_ingredients
    OWNER to postgres;