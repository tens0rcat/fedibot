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
sql_getpostswithtag = "SELECT postid FROM posttag WHERE tagid = %s"
sql_gettagsfrompost = "SELECT tagid from posttag WHERE postid = %s"
sql_getuserfrompost = "SELECT userid FROM posts WHERE postid = %s"
sql_getnamefromusers = "SELECT name FROM users WHERE id = %s"
sql_getnamefromtag = "SELECT name FROM tags WHERE id = %s"


mycursor.execute(sql_gettags)
tmp = mycursor.fetchall()
tags = {}
for t in tmp:
    tags[t[0]] = t[1]

taglist = {}
usercount = {}
for tag in tags:
    basetag = tag
    val = (basetag,)
    mycursor.execute(sql_getpostswithtag,val)
    postswithtags = mycursor.fetchall()
    taglist[basetag] = {}
    usercount[basetag] = 0
    users = []
    for post in postswithtags:
        val = (post[0],)
        mycursor.execute(sql_getuserfrompost, val)
        user = mycursor.fetchall()
        if user[0][0] not in users:
            users.append(user[0][0])
            usercount[basetag] += 1
        # val = (post[0],)
        # mycursor.execute(sql_gettagsfrompost, val)
        # adjacenttags = mycursor.fetchall()
        # for atag in adjacenttags:
        #     if atag[0] == basetag: 
        #         continue
        #     if atag[0] > basetag:
        #         t1 = basetag
        #         t2 = atag[0]
        #     else:
        #         t1 = atag[0]
        #         t2 = basetag
            
        #     if t1 in taglist[basetag]:
        #         if atag[0] in taglist[basetag]:
        #             taglist[basetag][atag[0]] += 1 
        #         else:
        #             taglist[basetag][atag[0]] = 1

    if len(users) > 1:
        val = (tag,)
        mycursor.execute(sql_getnamefromtag,val)
        tagname = mycursor.fetchone()[0]
        print("\"" + tagname + "\",  " + str(len(users)))

pass #for breakpoint

# for tag in tags:
#     #print(tags[tag] + ",")
#     for atag in taglist[tag]:
#         tagname = tags[atag]
#         tagcount = taglist[tag][atag]
#         print("\"" + tags[tag] +"\", \"" + tagname + "\", " + str(tagcount) + ", " + str(usercount[tag]) )
    

