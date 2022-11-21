from mastodon import Mastodon
import mysql.connector
from secrets.secrets import secrets

M_client_id = secrets['MASTODON_CLIENT_ID']
M_api_base_url = secrets['MASTODON_PRIMARY_BASE_URL']
M_email = secrets['MASTODON_PRIMARY_USER_EMAIL']
M_user_token = secrets['MASTODON_PRIMARY_USER_TOKEN']
M_login = secrets['MASTODON_PRIMARY_LOGIN']

db = secrets['MYSQL_DATABASE']
db_user = secrets['MYSQL_USER']
db_pass = secrets['MYSQL_PASSWORD']

mydb = mysql.connector.connect(
  host="localhost",
  user=db_user,
  password=db_pass,
  database=db
)

mycursor = mydb.cursor()

mastodon = Mastodon(
  client_id = M_client_id,
  api_base_url = M_api_base_url
)
mastodon.log_in(
    M_email,
    M_user_token,
    M_login
)

posts = mastodon.timeline_local() 
posts += mastodon.timeline_public()

sql_users = "INSERT IGNORE INTO users (id, name) VALUES (%s, %s)"
sql_posts = "INSERT IGNORE INTO posts (postid, userid) VALUES (%s, %s)"
sql_tagname = "INSERT IGNORE INTO tags (name) VALUES (%s)"
sql_tags = "INSERT INTO posttag (postid, tagid) VALUES (%s, %s)"
sql_gettag = "SELECT id FROM tags WHERE name = %s"

for post in posts:
  # print("NewPost " + str(post.id) + " by: " + str(post.account.id) + " - " + post.account.acct)
  val = (post.account.id, post.account.acct)
  mycursor.execute(sql_users, val)
  mydb.commit()
  # print(mycursor.rowcount, "user record inserted.")
  val = (post.id, post.account.id)
  mycursor.execute(sql_posts, val)
  mydb.commit()
  # print(mycursor.rowcount, "post record inserted.")
  for tag in post.tags:
    # print(str(post.id) + " " + tag.name)
    val = (tag.name,)
    mycursor.execute(sql_gettag, val)
    tagresult = mycursor.fetchall()
    if len(tagresult) < 1 :
      val = (tag.name.lower(),)
      mycursor.execute(sql_tagname,val)
      mydb.commit()
      mycursor.execute(sql_gettag, val)
      tagresult = mycursor.fetchall()
    #for t in tagresult:
      # print(tag.name + ": " + str(t[0]))
    if len(tagresult) > 1:
      print("Duplicate TAG ERROR: " + tag.name)
    val = (post.id, tagresult[0][0])
    mycursor.execute(sql_tags, val)
    mydb.commit()
    # print(mycursor.rowcount, "posttag")

