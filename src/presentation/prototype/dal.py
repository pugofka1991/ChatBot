from unittest import result
from mysql.connector import connect, Error
import hashlib

class DateBase:

    def __init__(self, host, user, password, database):
        try:
            self.connect = connect(
                host=host,
                user=user,
                password=password,
                database=database,
            )
            print(f"Sucsessful connect to {host}.{database}")
        except Error as e:
            print(e)
        self.cursor = self.connect.cursor()

    def value_exists(self, field, value):
        query = f"select id from user where {field} = '{value}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return bool(len(result))

    def get_user_by_tg_id(self, tg_user_id):
        query = f"select * from user where tg_id = '{tg_user_id}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def add_user(self, login, admin, campus, password):
        query = f"INSERT INTO user (name, login, admin, campus, password) VALUES (null, '{login}', {admin}, '{campus}', '{password}')"
        self.cursor.execute(query)
        result = self.connect.commit()
        return result

    def add_object(self, type, description, campus, floor, room):
        query = f"insert into object (type, description, campus, floor, room) values ('{type}', '{description}', '{campus}', '{floor}','{room}')"
        self.cursor.execute(query)
        result = self.connect.commit()
        return result

    def get_field_from_row(self, field, filter_field, value):
        query = f"select {field} from user where {filter_field} = '{value}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result[0][0]

    def get_objects_list(self, campus):
        query = f"select * from object where campus like '{campus}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_tickets(self, object_id, date):
        query = f"select * from event where object_id = {object_id} and date = '{date}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_user_id_by_login(self, login):
        query = f"select id from user where login = '{login}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def set_booking(self, user_id, object_id, date, time):
        query = f"insert into event (user_id, object_id, start_time, date) values ({user_id}, {object_id}, '{time}', '{date}')"
        self.cursor.execute(query)
        result = self.connect.commit()
        return result

    def get_user_bookings(self, user_id):
        query = f"select * from event as e left join object o on o.id = e.object_id where e.user_id = {user_id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def confirm_password(self, password, login):
        query = f"select * from user where login like '{login}' and password like '{password}'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return bool(len(result))

    def close(self):
        self.connect.close()

    def get_objects_types(self):
        query = f"select * from type"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_objects_by_id(self, id):
        query = f"select * from object where type_id = {id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_count_of_types(self):
        query = f"select count(*) from type"
        self.cursor.execute(query)
        return int(self.cursor.fetchall()[0][0])

    def get_object_by_id(self, id):
        query = f"select * from object where id = {id}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def drop_booking(self, id):
        query = f"delete from event where id = {id}"
        self.cursor.execute(query)
        self.connect.commit()


# create table g
# (
#     id         int auto_increment
#         primary key,
#     user_id    int  not null,
#     object_id  int  not null,
#     start_time time not null,
#     date       date null,
#     constraint event_id_uindex
#         unique (id)
# );

# create table object
# (
#     id          int auto_increment
#         primary key,
#     type_id        int,
#     description text                        null,
#     campus_id      varchar(10) charset utf8mb3 not null,
#     floor       int                         not null,
#     room        int                         null,
#     constraint object_id_uindex
#         unique (id)
# );

# create table user
# (
#     id       int auto_increment
#         primary key,
#     name     varchar(50) charset utf8mb3 null,
#     login    varchar(50) charset utf8mb3 not null,
#     admin    tinyint(1) default 0        not null,
#     campus   varchar(50) charset utf8mb3 not null,
#     password varchar(50)                 not null,
#     constraint user_id_uindex
#         unique (id)
# );

