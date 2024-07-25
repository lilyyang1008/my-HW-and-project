grant all on covid19.* to 'administrator'@'localhost';
grant select on covid19.* to 'normaluser'@'localhost';
grant select,create view on covid19.* to 'poweruser'@'localhost';


create user 'ross'@'localhost' identified by 'geller' default role 'administrator'@'localhost';
create user 'joey'@'localhost' identified by 'tribbiani' default role 'normaluser'@'localhost';
create user 'chandler'@'localhost' identified by 'bing' default role 'poweruser'@'localhost';
