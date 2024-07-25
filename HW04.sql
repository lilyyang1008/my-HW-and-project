create database transaction_control character set utf8mb4 collate utf8mb4_unicode_ci;
create table transaction_control.accounts(
id int unsigned,
balance double unsigned
);

create table transaction_control.transfers(
id int unsigned,
from_account_id int unsigned,
to_account_id int unsigned,
amount double
);

insert into transaction_control.accounts (id,balance) values (1,1000),(2,1000);

select *from transaction_control.accounts;
start transaction;
insert into  transaction_control.transfers (id,from_account_id,to_account_id,amount) values (1,1,2,450);
update transaction_control.accounts set balance =balance -450 where id=1;
update transaction_control.accounts set balance =balance +450 where id=2;
commit;
select *from transaction_control.transfers;
