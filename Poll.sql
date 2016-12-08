-- Stephanie Frankian and Elizabeth Kuszmaul

-- Creating the SQL tables for our application

-- drop table if exists users;
-- create table users(
--       uid int not null primary key,
--       email varchar(65) not null,
--       pwd varchar(22) not null,
--       INDEX (uid)      
-- ) ENGINE = InnoDB;

drop table if exists poll;
create table poll(
       id int not null primary key auto_increment,
       poll_name varchar(50) not null,
       link varchar(30),
       datecreated date not null,
       INDEX(id)
) ENGINE = InnoDB;

drop table if exists poll_options;
create table poll_options(
       oid int not null primary key auto_increment,
       poll_id int not null,
       location varchar(30),
       given_time time,
       INDEX (poll_id)
) ENGINE = InnoDB;

drop table if exists responses;
create table responses(
       poll_id int not null,
       oid int not null,
       response smallint not null,
       INDEX (poll_id),
       INDEX (oid),
       foreign key (oid) references poll_options(oid) on delete cascade
) ENGINE = InnoDB;
