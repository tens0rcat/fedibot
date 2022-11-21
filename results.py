import mysql.connector
from secrets.secrets import secrets

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

sql_gettags = "SELECT * FROM tags"
sql_getpostswithtags = "SELECT postid FROM posttag WHERE tagid = %s"
sql_gettagsfrompost = "SELECT tagid from posttag WHERE postid = %s"

mycursor.execute(sql_gettags)
tmp = mycursor.fetchall()
tags = {}
for t in tmp:
    tags[t[0]] = t[1]

taglist = {}
for tag in tags:
    basetag = tag
    val = (basetag,)
    mycursor.execute(sql_getpostswithtags,val)
    postswithtags = mycursor.fetchall()
    taglist[basetag] = {}
    for post in postswithtags:
        val = (post[0],)
        mycursor.execute(sql_gettagsfrompost, val)
        adjacenttags = mycursor.fetchall()
        for atag in adjacenttags:
            if atag[0] == basetag: 
                continue
            if atag[0] in taglist[basetag]:
                taglist[basetag][atag[0]] += 1 
            else:
                taglist[basetag][atag[0]] = 1

for tag in tags:
    #print(tags[tag] + ",")
    for atag in taglist[tag]:
        tagname = tags[atag]
        tagcount = taglist[tag][atag]
        print("'" + tags[tag] +"', '" + tagname + "', " + str(tagcount))
    

