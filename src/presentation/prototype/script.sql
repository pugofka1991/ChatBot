DROP DATABASE IF EXISTS book_21;
create database book_21 default charset utf8;
use book_21;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS event;
create table event
 (
     id         int auto_increment
         primary key,
     user_id    int  not null,
     object_id  int  not null,
     start_time time not null,
     date       date null,
     constraint event_id_uindex
         unique (id)
 );

DROP TABLE IF EXISTS object;
 create table object
 (
     id          int auto_increment
         primary key,
     type_id     int                         null,
     description text                        null,
     campus_id   varchar(10) charset utf8 not null,
     floor       int                         not null,
     room        int                         null,
     constraint object_id_uindex
         unique (id)
 );

DROP TABLE IF EXISTS campus;
 create table campus
(
    id          int auto_increment
         primary key,
    campus      varchar (20) charset utf8 null,
    constraint object_id_uindex
         unique (id)
);

DROP TABLE IF EXISTS type;
 create table type
(
    id          int auto_increment
         primary key,
    type      varchar (50) charset utf8 not null,
    constraint object_id_uindex
         unique (id)
);

DROP TABLE IF EXISTS user;
 create table user
 (
     id       int auto_increment
         primary key,
     name     varchar(50) charset utf8 null,
     login    varchar(50) charset utf8 not null,
     admin    tinyint(1) default 0        not null,
     campus   varchar(50) charset utf8 not null,
     password varchar(50)                 not null,
     constraint user_id_uindex
         unique (id)
 );

INSERT INTO book_21.campus (campus) VALUES ('Moscow');
INSERT INTO book_21.campus (campus) VALUES ('Kazan');
INSERT INTO book_21.campus (campus) VALUES ('Novosibirsk');

INSERT INTO book_21.type (type) VALUES ('Kitchen');
INSERT INTO book_21.type (type) VALUES ('Sports equipment');
INSERT INTO book_21.type (type) VALUES ('Meeting room');
INSERT INTO book_21.type (type) VALUES ('Table games');

INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (1, 'Kitchen for stuff', '1', 1, 1);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (1, 'Kitchen for stuff', '1', 1, 1);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (1, 'Kitchen for students', '1', 2, 3);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (1, 'Kitchen for stuff', '2', 3, 1);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (1, 'Kitchen for students', '2', 3, 1);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (3, 'Meeting room for stuff', '1', 2, 216);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (3, 'Plasma', '1', 1, 101);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (2, 'Pong kit', '2', 2, 202);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (3, 'Meeting room for students', '3', 21, 2101);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Monopoly', '1', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Mafia', '2', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Mafia', '1', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Mafia', '3', 42, 4200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Pigs', '3', 42, 4200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Cinema', '1', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (2, 'Chessmate', '1', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (2, 'Chess', '2', 2, 200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Manchkin', '3', 42, 4200);
INSERT INTO book_21.object (type_id, description, campus_id, floor, room) VALUES (4, 'Badminton', '1', 42, 200);

INSERT INTO book_21.user (name, login, admin, campus, password) VALUES ('user', 'user', 0, '1', 'user');
INSERT INTO book_21.user (name, login, admin, campus, password) VALUES ('admin', 'admin', 1, '1', 'admin');