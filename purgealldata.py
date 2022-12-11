from modules import myMysql as mysql

retval = mysql.init()
mydb = retval[0]
mycursor = retval[1]

sql_purge = ""
#sql_purge = "TRUNCATE `links`; TRUNCATE `posts`; TRUNCATE `tags`; TRUNCATE `taguser`; TRUNCATE `users`;"

if (sql_purge == ""):
  print("If this is really what you want to do then uncomment the line above")
else:
  mycursor.execute(sql_purge)
