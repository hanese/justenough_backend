create table public.home_storage
(
    uuid         uuid    not null
        constraint home_storage_pk
            primary key,
    item         varchar not null,
    belongs_user varchar not null
        constraint home_storage_users_username_fk
            references public.users,
    constraint home_storage_pk2
        unique (belongs_user, item)
);
