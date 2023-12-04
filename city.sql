-- auto-generated definition
create table city
(
    uuid         bigint auto_increment
        primary key,
    city_name    varchar(255) null,
    address_uuid bigint       null,
    constraint city_ibfk_1
        foreign key (address_uuid) references address (uuid)
);

create index address_uuid
    on city (address_uuid);
