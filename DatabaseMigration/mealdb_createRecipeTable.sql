CREATE TABLE IF NOT EXISTS public.recipe
(
    id integer NOT NULL,
    meal character varying COLLATE pg_catalog."default",
    drink_alternate character varying COLLATE pg_catalog."default",
    category character varying COLLATE pg_catalog."default",
    area character varying COLLATE pg_catalog."default",
    instructions character varying COLLATE pg_catalog."default",
    meal_thumb character varying COLLATE pg_catalog."default",
    tags character varying COLLATE pg_catalog."default",
    youtube character varying COLLATE pg_catalog."default",
    ingredient1 character varying COLLATE pg_catalog."default",
    ingredient2 character varying COLLATE pg_catalog."default",
    ingredient3 character varying COLLATE pg_catalog."default",
    ingredient4 character varying COLLATE pg_catalog."default",
    ingredient5 character varying COLLATE pg_catalog."default",
    ingredient6 character varying COLLATE pg_catalog."default",
    ingredient7 character varying COLLATE pg_catalog."default",
    ingredient8 character varying COLLATE pg_catalog."default",
    ingredient9 character varying COLLATE pg_catalog."default",
    ingredient10 character varying COLLATE pg_catalog."default",
    ingredient11 character varying COLLATE pg_catalog."default",
    ingredient12 character varying COLLATE pg_catalog."default",
    ingredient13 character varying COLLATE pg_catalog."default",
    ingredient14 character varying COLLATE pg_catalog."default",
    ingredient15 character varying COLLATE pg_catalog."default",
    ingredient16 character varying COLLATE pg_catalog."default",
    ingredient17 character varying COLLATE pg_catalog."default",
    ingredient18 character varying COLLATE pg_catalog."default",
    ingredient19 character varying COLLATE pg_catalog."default",
    ingredient20 character varying COLLATE pg_catalog."default",

    measure1 character varying COLLATE pg_catalog."default",
    measure2 character varying COLLATE pg_catalog."default",
    measure3 character varying COLLATE pg_catalog."default",
    measure4 character varying COLLATE pg_catalog."default",
    measure5 character varying COLLATE pg_catalog."default",
    measure6 character varying COLLATE pg_catalog."default",
    measure7 character varying COLLATE pg_catalog."default",
    measure8 character varying COLLATE pg_catalog."default",
    measure9 character varying COLLATE pg_catalog."default",
    measure10 character varying COLLATE pg_catalog."default",
    measure11 character varying COLLATE pg_catalog."default",
    measure12 character varying COLLATE pg_catalog."default",
    measure13 character varying COLLATE pg_catalog."default",
    measure14 character varying COLLATE pg_catalog."default",
    measure15 character varying COLLATE pg_catalog."default",
    measure16 character varying COLLATE pg_catalog."default",
    measure17 character varying COLLATE pg_catalog."default",
    measure18 character varying COLLATE pg_catalog."default",
    measure19 character varying COLLATE pg_catalog."default",
    measure20 character varying COLLATE pg_catalog."default",

    source character varying COLLATE pg_catalog."default",
    image_source character varying COLLATE pg_catalog."default",
    creative_commons_confirmed character varying COLLATE pg_catalog."default",
    date_modified character varying COLLATE pg_catalog."default",

    CONSTRAINT recipe_pkey PRIMARY KEY (id)
)

