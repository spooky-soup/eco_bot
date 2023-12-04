-- auto-generated definition
create table district
(
    uuid          bigint auto_increment
        primary key,
    district_name varchar(255) null,
    region_uuid   bigint       null,
    constraint district_name
        unique (district_name),
    constraint district_ibfk_1
        foreign key (region_uuid) references region (uuid)
);

create index region_uuid
    on district (region_uuid);
