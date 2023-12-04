-- auto-generated definition
create table point
(
    uuid          bigint auto_increment
        primary key,
    avl_types     varchar(255) null,
    location      varchar(255) null,
    district_name varchar(255) null,
    region_name   varchar(255) null,
    city_uuid     bigint       null,
    address_uuid  bigint       null,
    hours         varchar(255) null,
    constraint point_ibfk_1
        foreign key (avl_types) references type (type_name),
    constraint point_ibfk_2
        foreign key (district_name) references district (district_name),
    constraint point_ibfk_3
        foreign key (region_name) references region (region_name),
    constraint point_ibfk_4
        foreign key (city_uuid) references city (uuid),
    constraint point_ibfk_5
        foreign key (address_uuid) references address (uuid)
);

create index address_uuid
    on point (address_uuid);

create index avl_types
    on point (avl_types);

create index city_uuid
    on point (city_uuid);

create index district_name
    on point (district_name);

create index region_name
    on point (region_name);
