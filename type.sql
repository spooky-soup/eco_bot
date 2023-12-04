-- auto-generated definition
create table type
(
    uuid      bigint       not null
        primary key,
    type_name varchar(255) null,
    img_link  varchar(255) null,
    score     int          null,
    constraint type_name
        unique (type_name)
);
