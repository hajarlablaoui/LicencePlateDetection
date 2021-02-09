import mysql.connector
import datetime

#connection à la base de données
mydb = mysql.connector.connect(
    host="localhost",
    username="root",
    passwd="",
    database="carsPlates",
)

#cursor creation
mycursor = mydb.cursor()

#mycursor.execute("CREATE database carsPlates")
#mycursor.execute("Create table park(id integer primary key AUTO_INCREMENT, plate varchar(20),dateEntree datetime, dateSortie datetime default null)")
#mycursor.execute("Create table facture(id integer primary key AUTO_INCREMENT,  parkId int,FOREIGN KEY (parkId) REFERENCES park(id),price double,datePayment datetime default now())")

mydb.commit()


#insertion des plaques dans la base de données
def plateToDB(plate):
    # vérifier si il la plaque existe avec une date de sortie null
    sql = "SELECT * FROM park WHERE plate = %s and dateSortie is NULL"
    pl = (plate,)
    mycursor.execute(sql, pl)
    myresult = mycursor.fetchall()

   #mise à jour de la ligne avec une date de sortie
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

    # inserer une nouvelle ligne avec une date d'entrée
    else:
        sqlform = "insert into park(plate,dateEntree) values (%s,%s)"
        pl = (plate, datetime.datetime.now())
        mycursor.execute(sqlform, pl)
        mydb.commit()


#calcul du prix
def parcPrice(id, dateEntree, dateSortie):
    prixheure = 10 #dh #prix par heure

    #calcul du temps dans le parking
    time = (dateSortie-dateEntree).total_seconds()
    #calcul du prix
    price = (time / 3600) * prixheure
    #définition d'un prix minimum
    if price < 10:
        price = 10
    #insertion de la facture dans la base de données
    sqlform = "insert into facture(parkId,price) values (%s,%s)"
    pl = (id, price)
    mycursor.execute(sqlform, pl)
