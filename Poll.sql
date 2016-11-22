-- Stephanie Frankian and Elizabeth Kuszmaul

-- Creating the SQL tables for our application

drop table if exists users;
create table users(
       uid int not null primary key,
       email varchar(65) not null,
       pwd varchar(22) not null,
       INDEX (uid)      
) ENGINE = InnoDB;

drop table if exists poll;
create table poll(
       id int not null primary key,
       poll_name varchar(50) not null,
       createdby int not null,
       datecreated date not null,
       INDEX(id),
       INDEX(createdby),
       foreign key (createdby) references users(uid) on delete cascade
) ENGINE = InnoDB;

drop table if exists poll_options;
create table poll_options(
       oid int not null primary key,
       poll_id int not null,
       location varchar(30),
       given_time time,
       INDEX (poll_id),
       foreign key (poll_id) references poll(id) on delete cascade
) ENGINE = InnoDB;

drop table if exists responses;
create table responses(
       user_id int not null,
       poll_id int not null,
       oid int not null,
       response tinyint(1) not null,
       INDEX (user_id),
       INDEX (poll_id),
       INDEX (oid),
       foreign key (user_id) references users(uid) on delete cascade,
       foreign key (poll_id) references poll(id) on delete cascade,
       foreign key (oid) references poll_options(oid) on delete cascade
) ENGINE = InnoDB;
