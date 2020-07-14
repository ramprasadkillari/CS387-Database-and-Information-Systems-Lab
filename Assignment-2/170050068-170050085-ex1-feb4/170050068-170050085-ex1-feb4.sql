
create table addaUsers (loginName varchar primary key,password varchar);

create table public.order (orderId serial primary key,loginName varchar,dateTime timestamp); 

create table orderItem (orderId int,item varchar,itemQuantity int,foreign key (orderId) references public.order); 

