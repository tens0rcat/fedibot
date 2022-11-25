import mysql.connector
from mysecrets.mysecrets import mysqlsecrets as sDB

database = sDB['MYSQL_DATABASE']
db_user = sDB['MYSQL_USER']
db_pass = sDB['MYSQL_PASSWORD']

def init():
  mydb = mysql.connector.connect(
    host="localhost",
    user=db_user,
    password=db_pass,
    database=database
  )
  return (mydb, mydb.cursor())