from modules import Mysql as mysql

retval = mysql.init()
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
  if tagusers[tu] < 2:
    continue
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
