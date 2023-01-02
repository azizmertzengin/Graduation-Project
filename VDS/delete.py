import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
        user ="ngtcraf1_cryptoConnector",
        password = "3Fy^%N,eZT,z",
        host = "89.252.138.35",
        database = "ngtcraf1_crypto",
)

def deleteSQL():
    # connectSQL()

    mydb = mysql.connector.connect(
        user ="ngtcraf1_cryptoConnector",
        password = "3Fy^%N,eZT,z",
        host = "89.252.138.35",
        database = "ngtcraf1_crypto",
    )

    mycursor = mydb.cursor()
    mycursor.execute("Delete FROM signals where isCompleted = 0")
    # mydb.close()

def checkSQL():
    # connectSQL()

    mydb = mysql.connector.connect(
        user ="ngtcraf1_cryptoConnector",
        password = "3Fy^%N,eZT,z",
        host = "89.252.138.35",
        database = "ngtcraf1_crypto",
    )

    mycursor = mydb.cursor()
    mycursor.execute("Select * FROM signals where isCompleted = 0")
    myresult = mycursor.fetchall()
    # mydb.close()
    return len(myresult)

while True:
    if checkSQL():
        deleteSQL()
        print("temizlendi")
    else:
        print("boş geçti")
    sleep(30)