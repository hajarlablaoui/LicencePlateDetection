import sqlite3
import mysql.connector

dbName = "carsPlates.db"

#TableSchema = """
#drop table if exists car;
#CREATE table car(
#id integer primary key autoincrement,
#plate text,
#dateEntree date,
#dateSortie date
#);
#"""

'''

#Connection
conn=sqlite3.connect(dbName)
curs=conn.cursor()

#curs.execute("INSERT INTO car VALUES (null ,'32-23M','2006-01-05','2006-01-06')")
curs.execute("SELECT * FROM car")
print(curs.fetchone())
conn.commit()
#Tables
#sqlite3.complete_statement(TableSchema)
#curs.executescript(TableSchema)

curs.close()
conn.close()
'''

mydb=mysql.connector.connect(
    host = "localhost",
    username = "root",
    passwd = "",
    database = "carsPlates",
)

mycursor=mydb.cursor()

#mycursor.execute("CREATE database carsPlates")
mycursor.execute("DROP table if exists car")
mycursor.execute("Create table car(id integer primary key AUTO_INCREMENT,plate varchar(20),dateEntree date, dateSortie date)")

sqlform = "insert into car(plate,dateEntree,dateSortie) values (%s,%s,%s)"

cars = [("34-ABC","2006-01-05","2006-01-05"),("78648AABB","2006-01-05","2006-01-05"),("OIAHDKX SJ","2006-01-05","2006-01-05")]

mycursor.executemany(sqlform,cars)

mydb.commit()


