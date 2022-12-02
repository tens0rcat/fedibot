from modules import myMysql as mysql

retval = mysql.init()
mydb = retval[0]
mycursor = retval[1]

#sql_purge = "TRUNCATE `links`; TRUNCATE `posts`; TRUNCATE `tags`; TRUNCATE `taguser`; TRUNCATE `users`;"

mycursor.execute(sql_purge)
