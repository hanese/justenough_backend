create table shopping_list
(
    uuid          uuid    not null
        constraint shopping_list_pk
            primary key,
    shopping_item varchar not null,
    belongs_user  varchar not null
        constraint shopping_list_users_username_fk
            references public.users
            on delete cascade
);

alter table shopping_list
    owner to postgres;

