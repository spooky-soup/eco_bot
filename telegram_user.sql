-- auto-generated definition
create table telegram_user
(
    uuid     bigint       not null
        primary key,
    username varchar(255) null,
    location varchar(255) null,
    score    int          null
);
