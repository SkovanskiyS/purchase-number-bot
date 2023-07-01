import psycopg2
host = '127.0.0.1'
username = 'postgres'
password = 'mixd13531'
db_name = 'kovanskiy_db'


connection = psycopg2.connect(
    host=host,
    user=username,
    password=password,
    database=db_name
)

connection.autocommit = True

with connection.cursor() as cursor:
    cursor.execute(
        'select version();'
    )
    #print(cursor.fetchone())

# create a table
# with connection.cursor() as cursor:
#     cursor.execute(
#         """CREATE TABLE users(
#             id serial primary key,
#             first_name varchar(5) not null,
#             username varchar(5) not null)"""
#     )

# insert data
# with connection.cursor() as cursor:
#     cursor.execute(
#         """INSERT INTO users (first_name,username) VALUES ('1','2');"""
#     )

#select data from bd



#create table
#
with connection.cursor() as cursor:
    cursor.execute(
        """create table if not exists users(
        id serial primary key,
        first_name varchar(50) not null,
        last_name varchar(50) not null
        )"""
    )

with connection.cursor() as cursor:
    cursor.execute(
        """insert into users(first_name,last_name) values ('joxa','masharipov');"""
    )
    
#get data
with connection.cursor() as cursor:
    cursor.execute(
        """select first_name from users """
    )

    print(cursor.fetchone())