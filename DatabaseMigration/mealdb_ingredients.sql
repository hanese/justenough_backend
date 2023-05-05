create table ingredients
(
    id          integer not null
        constraint ingredients_pkey
            primary key,
    ingredient  varchar,
    description varchar,
    type        varchar
);

alter table ingredients
    owner to postgres;

