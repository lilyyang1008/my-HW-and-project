DROP DATABASE IF EXISTS cloned_covid19;
create database cloned_covid19 character set utf8mb4 collate utf8mb4_unicode_ci;
use cloned_covid19;
create table locations(
id int unsigned,
country_name varchar(200),
province_name varchar(200),
iso2 char(2),
iso3 char(3),
latitude float,
longitude float,
population bigint
);
update cloned_covid19.locations set iso2="NA" where id=496;
select * from cloned_covid19.locations where id=496;
select * from cloned_covid19.locations;
update cloned_covid19.locations set province_name=null where province_name='';
update cloned_covid19.locations set iso2=null where iso2 ="";
update cloned_covid19.locations set iso3=null where iso3 ="";
alter table cloned_covid19.locations add constraint primary key (id);
show keys from cloned_covid19.locations;
create table accumulative_cases(
id int unsigned,
calendar_id int unsigned,
location_id int unsigned,
confirmed bigint,
deaths bigint
);
alter table cloned_covid19.accumulative_cases add constraint primary key (id);
show keys from cloned_covid19.accumulative_cases;
alter table cloned_covid19.accumulative_cases add constraint fk_accumulative_cases_locations 
foreign key(location_id) references locations(id);
