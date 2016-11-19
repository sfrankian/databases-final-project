-- Stephanie Frankian and Elizabeth Kuszmaul

-- Creating the SQL tables for our application

create table person(
       pid int not null primary key,
       email varchar(65) not null,
       pwd varchar(22) not null,
       INDEX (pid),      
) ENGINE = InnoDB;

create table poll(
       id int not null primary key,
       createdby int not null,
       datecreated date not null,
       location1 int not null,
       location2 int not null,
       location3 int,
       time1 time not null,
       time2 time not null,
       time3 time,
       INDEX (id),
       INDEX (createdby),
       INDEX (location1),
       INDEX (location2),
       INDEX (location3),
       INDEX (time1),
       INDEX (time2),
       INDEX (time2),
       foreign key (createdby) references person(pid) on delete set null,
       foreign key (time1) references poll_options(oid) on delete set null,
       foreign key (time2) references poll_options(oid) on delete set null,
       foreign key (time3) references poll_options(oid) on delete set null,
       foreign key (location1) references poll_options(oid) on delete set null,
       foreign key (location2) references poll_options(oid) on delete set null,
       foreign key (location3) references poll_options(oid) on delete set null,
) ENGINE = InnoDB;

create table poll_options(
       oid int not null,
       given_time time,
       location varchar(30),
       INDEX (oid),
       foreign key (oid) references poll(id) on delete cascade
) ENGINE = InnoDB;

create table responses(
       rid int not null,
       INDEX (rid)
) ENGINE = InnoDB;
