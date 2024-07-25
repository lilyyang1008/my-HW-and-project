create  database cloned_covid19;
use cloned_covid19;
create table locations(
id int unsigned,
country_name VARCHAR(200),
iso2 CHAR(2),
iso3 CHAR(3),
longitude float,
latitude float
);
create table calendars(
id int unsigned,
recorded_on date
);
create  table accumulative_cases(
id int unsigned,
calendar_id int unsigned,
location_id int unsigned,
confirmed bigint,
deaths bigint
);
use covid19;
select * from accumulative_cases where calendar_id = 1164;
create view accumulative_cases_20230309 as select * from accumulative_cases where calendar_id = 1164;
select * from accumulative_cases_20230309;

select * from locations where iso3 in ("TWN","JPN");
create  view locations_twn_jpn as select * from locations where iso3 in ("TWN","JPN");
select * from locations_twn_jpn;

select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id  ; 
create view views_joined as select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id  ; 
select * from views_joined;

select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 left join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id ; 
create view views_left_joined as select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 left join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id ; 

select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 right join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id  ; 
create view views_right_joined as select locations_twn_jpn.country_name ,locations_twn_jpn.province_name ,accumulative_cases_20230309.confirmed , accumulative_cases_20230309.deaths 
from accumulative_cases_20230309 right join locations_twn_jpn on locations_twn_jpn.id  =accumulative_cases_20230309.location_id  ; 