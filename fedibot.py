from modules import Mastodon as mastodon
from modules import Mysql as mysql
# import mysql.connector
# from secrets.secrets import mysqlsecrets as sDB


# def db_init():
#   db = sDB['MYSQL_DATABASE']
#   db_user = sDB['MYSQL_USER']
#   db_pass = sDB['MYSQL_PASSWORD']

#   mydb = mysql.connector.connect(
#     host="localhost",
#     user=db_user,
#     password=db_pass,
#     database=db
#   )

#   return (mydb, mydb.cursor())

mastodon.login()
posts = mastodon.getposts()

retval = mysql.init()
mydb = retval[0]
mycursor = retval[1]

sql_users = "INSERT IGNORE INTO users (id, name) VALUES (%s, %s)"
sql_posts = "INSERT IGNORE INTO posts (postid, userid) VALUES (%s, %s)"
sql_tagname = "INSERT IGNORE INTO tags (name) VALUES (%s)"
sql_tags = "INSERT INTO posttag (postid, tagid) VALUES (%s, %s)"
sql_gettag = "SELECT id FROM tags WHERE name = %s"
sql_taguser = "INSERT IGNORE INTO taguser (tagid, userid) VALUES (%s, %s)"
sql_links = "INSERT IGNORE INTO links (t1, t2) VALUES (%s, %s)"
sql_countlinks = "SELECT COUNT(*) FROM links WHERE t1 = %s AND t2 = %s"
sql_inclinkcount = "UPDATE links SET count=count+1 where t1 = %s and t2 = %s"

for post in posts:
  # print("NewPost " + str(post.id) + " by: " + str(post.account.id) + " - " + post.account.acct)
  if post.account.bot:
    continue
  val = (post.account.id, post.account.acct)
  mycursor.execute(sql_users, val)
  mydb.commit()
  if mycursor.rowcount == 0:
    pass
  # print(mycursor.rowcount, "user record inserted.")
  val = (post.id, post.account.id)
  mycursor.execute(sql_posts, val)
  mydb.commit()
  if mycursor.rowcount == 0:
    # print("duplicate " + str(post.id))
    continue
  # print(mycursor.rowcount, "post record inserted.")
  for tag in post.tags:
    # print(str(post.id) + " " + tag.name)
    val = (tag.name,)
    mycursor.execute(sql_gettag, val)
    tagid = mycursor.fetchall()
    if len(tagid) < 1 :
      val = (tag.name.lower(),)
      mycursor.execute(sql_tagname,val)
      mydb.commit()
    val = (tag.name,)
    mycursor.execute(sql_gettag, val)
    tagid = mycursor.fetchall()
    val = (tagid[0][0], post.account.id)
    mycursor.execute(sql_taguser, val)
    mydb.commit()
  for tag in post.tags:
    val = (tag.name,)
    mycursor.execute(sql_gettag, val)
    tmp1 = mycursor.fetchone()[0]
    for t in post.tags:
      val = (t.name,)
      mycursor.execute(sql_gettag, val)
      tmp2 = mycursor.fetchone()[0]
      t1 = max(tmp1, tmp2)
      t2 = min(tmp1, tmp2)
      if t1 == t2:
        continue
      val = (t1, t2)
      mycursor.execute(sql_links, val)
      mydb.commit()
      # mycursor.execute(sql_inclinkcount, val)
      # mydb.commit()
    #   mycursor.execute(sql_gettag, val)
    #   tagid = mycursor.fetchall()
    # #for t in tagresult:
    #   # print(tag.name + ": " + str(t[0]))
    # if len(tagid) > 1:
    #   print("Duplicate TAG ERROR: " + tag.name)
    # val = (post.id, tagid[0][0])
    # mycursor.execute(sql_tags, val)
    # mydb.commit()
    # # print(mycursor.rowcount, "posttag")
