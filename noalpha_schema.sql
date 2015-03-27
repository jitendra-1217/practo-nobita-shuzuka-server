drop database if exists noalpha;
create database noalpha;
use noalpha;
create table doctors
(
    id integer primary key auto_increment,
    name varchar(250) not null,
    phone_no varchar(250) default null,
    avg_checkup_time integer default 15
);
create table doctor_locations
(
    id integer primary key auto_increment,
    doctor_id integer default null,
    landmark varchar(250) default null,
    locality varchar(250) default null,
    city varchar(250) default null,
    country varchar(250) default 'india',
    latitude decimal(10,7) default null,
    longitude decimal(10,7) default null,
    foreign key (doctor_id) references doctors (id)
);
create table patients
(
    id integer primary key auto_increment,
    name varchar(250) not null,
    phone_no varchar(250) default null
);
create table tokens
(
    id integer primary key auto_increment,
    serial_no integer not null,
    token_timestamp timestamp default CURRENT_TIMESTAMP,
    start_time time default null,
    finished_time time default null,
    actual_start_time time default null,
    status enum('empty', 'assigned', 'canceled by doctor', 'finished'),
    doctor_location_id integer default null,
    patient_id integer default null,
    booking_reason varchar(250) default null,
    foreign key (doctor_location_id) references doctor_locations (id),
    foreign key (patient_id) references patients (id)
)
