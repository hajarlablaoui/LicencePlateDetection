import mysql.connector
import datetime

mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    passwd="",
    database="carsPlates",
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE database carsPlates")
# mycursor.execute("DROP table if exists facture")
# mycursor.execute("Create table car(id integer primary key AUTO_INCREMENT,plate varchar(20),dateEntree date, dateSortie date)")

# mycursor.execute("Create table park(id integer primary key AUTO_INCREMENT, plate varchar(20),dateEntree datetime, dateSortie datetime default null)")

# sqlform = "insert into park(plate,dateEntree,dateSortie) values (%s,%s,%s)"

# ars = [("34-ABC","2006-01-05","2006-01-05"),("78648AABB","2006-01-05","2006-01-05"),("OIAHDKX SJ","2006-01-05","2006-01-05")]

# mycursor.executemany(sqlform,cars)

# mycursor.execute("Create table facture(id integer primary key AUTO_INCREMENT,  parkId int,FOREIGN KEY (parkId) REFERENCES park(id),price double,datePayment datetime default null)")


mydb.commit()


def plateToDB(plate):
    # check if exists row with plate & dateSortie null
    # update row with new now date
    # else
    # insert new row with dateEntre Now

    sql = "SELECT * FROM park WHERE plate = %s and dateSortie is NULL"
    pl = (plate,)

    mycursor.execute(sql, pl)

    myresult = mycursor.fetchall()
    print(myresult)
    if len(myresult) > 0:
        sql = "UPDATE park SET dateSortie = %s where id = %s"
        pl = (datetime.datetime.now(), myresult[0][0])
        mycursor.execute(sql, pl)
        mydb.commit()
        sql = "SELECT * FROM park WHERE id = %s "
        pl = (myresult[0][0],)
        mycursor.execute(sql, pl)
        myresult1 = mycursor.fetchall()
        parcPrice(myresult1[0][0], myresult1[0][1], myresult1[0][2])
    else:
        sqlform = "insert into park(plate,dateEntree) values (%s,%s)"
        pl = (plate, datetime.datetime.now())
        mycursor.execute(sqlform, pl)
        mydb.commit()


def parcPrice(id, dateEntree, dateSortie):
    heureprix = 10
    FMT = '%Y/%d/%m %H:%M:%S'
    print(dateEntree)
    tdelta = datetime.datetime.strptime(dateSortie, FMT) - datetime.datetime.strptime(dateEntree, FMT)
    print(tdelta)
    price = 0
    if price == 0:
        price = 10
    sqlform = "insert into facture(parkId,price) values (%s,%s)"
    pl = (id, price)
    mycursor.execute(sqlform, pl)
