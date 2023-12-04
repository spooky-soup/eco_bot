-- auto-generated definition
create table region
(
    uuid        bigint auto_increment
        primary key,
    region_name varchar(255) null,
    city_uuid   bigint       null,
    constraint region_name
        unique (region_name),
    constraint region_ibfk_1
        foreign key (city_uuid) references city (uuid)
);

create index city_uuid
    on region (city_uuid);
