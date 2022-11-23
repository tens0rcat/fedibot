import mysql.connector
from secrets.secrets import mysqlsecrets as sDB
from collections import Counter

def db_init():
  db = sDB['MYSQL_DATABASE']
  db_user = sDB['MYSQL_USER']
  db_pass = sDB['MYSQL_PASSWORD']

  mydb = mysql.connector.connect(
    host="localhost",
    user=db_user,
    password=db_pass,
    database=db
  )

  return (mydb, mydb.cursor())

retval = db_init()
mydb = retval[0]
mycursor = retval[1]

sql_gettags = "SELECT * FROM tags"
sql_getusers = "SELECT * FROM users"
sql_getpostswithtag = "SELECT postid FROM posttag WHERE tagid = %s"
sql_gettagsfrompost = "SELECT tagid from posttag WHERE postid = %s"
sql_getuserfrompost = "SELECT userid FROM posts WHERE postid = %s"
sql_getnamefromusers = "SELECT name FROM users WHERE id = %s"
sql_getnamefromtag = "SELECT name FROM tags WHERE id = %s"
sql_getuseridsfromtaguser = "SELECT tagid, userid FROM taguser"
sql_getlinkswithtag = "SELECT t1, t2 FROM links WHERE t1 = %s OR t2 = %s"


mycursor.execute(sql_gettags)
tmp = mycursor.fetchall()
tags = {}
for t in tmp:
    tags[t[0]] = t[1]

mycursor.execute(sql_getusers)
tmp = mycursor.fetchall()
users = {}
for t in tmp:
    users[t[0]] = t[1]
    
tagusers = {}    
mycursor.execute(sql_getuseridsfromtaguser)  
tmp =  mycursor.fetchall()

for t in tmp:
  if t[0] not in tagusers:                                               
    tagusers[t[0]] = 1
  else:
    tagusers[t[0]] += 1

for tu in tagusers:
  if tagusers[tu] > 1:
      print("\"" + tags[tu] + "\", " + str(tagusers[tu]))    

# taglist = {}
for tag in tags:
  val = (tag,tag)
  mycursor.execute(sql_getlinkswithtag, val)
  links = mycursor.fetchall()
  linkswithtag = []
  for link in links:
    if link[0] == tag:
      if link[1] not in links:
        linkswithtag.append(link[1])
      else:
        if link[0] not in links:
          linkswithtag.append(link[0])
  for l in linkswithtag:
    # print(str(tag) + ":" + str(l))
    if tagusers[l] > 1:
      print("\"" + tags[tag] + "\",\"" + tags[l] + "\"" )
      


    # mycursor.execute(sql_getpostswithtag,val)
    # postswithtags = mycursor.fetchall()
    # taglist[basetag] = {}
    # usercount[basetag] = 0
    # users = []
    # for post in postswithtags:
    # #     val = (post[0],)
    # #     mycursor.execute(sql_getuserfrompost, val)
    # #     user = mycursor.fetchall()
    # #     if user[0][0] not in users:
    # #         users.append(user[0][0])
    # #         usercount[basetag] += 1
    #     val = (post[0],)
    #     mycursor.execute(sql_gettagsfrompost, val)
    #     adjacenttags = mycursor.fetchall()
    #     for atag in adjacenttags:
    #         if atag[0] == basetag: 
    #             continue
    #         if tagusers[atag[0]] > 1:
    #             print("\"" + tags[tag] + "\", \"" + tags[atag[0]] + "\"")
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

    # if len(users) > 1:
    #     val = (tag,)
    #     mycursor.execute(sql_getnamefromtag,val)
    #     tagname = mycursor.fetchone()[0]
    #     print("\"" + tagname + "\",  " + str(len(users)))

pass #for breakpoint

# for tag in tags:
#     #print(tags[tag] + ",")
#     for atag in taglist[tag]:
#         tagname = tags[atag]
#         tagcount = taglist[tag][atag]
#         print("\"" + tags[tag] +"\", \"" + tagname + "\", " + str(tagcount) + ", " + str(usercount[tag]) )
    

