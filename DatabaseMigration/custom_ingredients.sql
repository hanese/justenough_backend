create table custom_ingredients
(
    ingredient   varchar not null,
    belongs_user varchar not null
        constraint custom_ingredients_users_username_fk
            references users
            on delete cascade,
    uuid         uuid    not null
        constraint custom_ingredients_pk
            primary key
);

alter table custom_ingredients
    owner to postgres;

