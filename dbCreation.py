import mysql.connector
import datetime


mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    passwd="",
    database="carsPlates",
)

#cursor creation
mycursor = mydb.cursor()

#mycursor.execute("CREATE database carsPlates")
#mycursor.execute("DROP table if exists facture")
#mycursor.execute("Create table park(id integer primary key AUTO_INCREMENT, plate varchar(20),dateEntree datetime, dateSortie datetime default null)")
#mycursor.execute("Create table facture(id integer primary key AUTO_INCREMENT,  parkId int,FOREIGN KEY (parkId) REFERENCES park(id),price double,datePayment datetime default now())")
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
        parcPrice(myresult1[0][0], myresult1[0][2], myresult1[0][3])

    else:
        sqlform = "insert into park(plate,dateEntree) values (%s,%s)"
        pl = (plate, datetime.datetime.now())
        mycursor.execute(sqlform, pl)
        mydb.commit()


def parcPrice(id, dateEntree, dateSortie):
    prixheure = 10 #dh
    time=(dateSortie-dateEntree).total_seconds()
    price = (time / 3600) * prixheure
    if price < 10:
        price = 10
    sqlform = "insert into facture(parkId,price) values (%s,%s)"
    pl = (id, price)
    mycursor.execute(sqlform, pl)
