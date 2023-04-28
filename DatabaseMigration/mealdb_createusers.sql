create table users
(
    username varchar not null
        constraint user_pk
            primary key,
    password varchar not null
);

alter table users
    owner to postgres;
