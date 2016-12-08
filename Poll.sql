-- Stephanie Frankian and Elizabeth Kuszmaul

drop table if exists poll;
create table poll(
       id int not null primary key auto_increment,
       poll_name varchar(50) not null,
       link varchar(30),
       email varchar(50),
       datecreated date not null,
       INDEX(id)
) ENGINE = InnoDB;

drop table if exists poll_options;
create table poll_options(
       poll_id int not null,
       oid int not null auto_increment,
       location varchar(30),
       given_time time,
       INDEX (oid),
       INDEX (poll_id),
       foreign key (poll_id) references poll(id) on delete cascade
) ENGINE = InnoDB;

drop table if exists responses;
create table responses(
       poll_id int not null,
       oid int not null,
       primary key (poll_id,oid),
       response smallint not null,
       INDEX (poll_id),
       INDEX (oid),
       foreign key (poll_id) references poll(id) on delete cascade
) ENGINE = InnoDB;