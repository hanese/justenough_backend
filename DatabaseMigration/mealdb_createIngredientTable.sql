create table ingredient
(
    id          integer not null
        constraint ingredients_pkey
            primary key,
    ingredient  varchar,
    description varchar,
    type        varchar
);

alter table ingredient
    owner to postgres;

