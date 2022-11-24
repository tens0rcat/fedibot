from modules import Mysql as mysql

retval = mysql.init()
mydb = retval[0]
mycursor = retval[1]

sql_gettags = "SELECT * FROM tags"
sql_getusers = "SELECT * FROM users"
sql_getuseridsfromtaguser = "SELECT tagid, userid FROM taguser"
sql_getlinkswithtag = "SELECT t1, t2 FROM links WHERE t1 = %s OR t2 = %s"

outputdetail = 20

def outputtagsCSV(_tagusers, _tags) -> None:
    # output the final tag users
    for tu in _tagusers:
        if _tagusers[tu] < outputdetail:
            continue
        print("\"" + _tags[tu] + "\", " + str(_tagusers[tu]))


def outputlinkspertagCSV(_tag, _tags, _tagusers, _linkswithtag) -> None:
    # Output users per tab\g
    for l in _linkswithtag:
        # print(str(tag) + ":" + str(l))
        if _tagusers[l] < outputdetail:
            continue
        print("\"" + _tags[_tag] + "\"," + str(_tagusers[_tag]
                                               ) + ",\"" + _tags[l] + "\"," + str(_tagusers[l]))

# Build the tags list (id, name)
mycursor.execute(sql_gettags)
tmp = mycursor.fetchall()
tags = {}
for t in tmp:
    tags[t[0]] = t[1]

# Build the users list (userid, name)
mycursor.execute(sql_getusers)
tmp = mycursor.fetchall()
users = {}
for t in tmp:
    users[t[0]] = t[1]

# Build tagusers, for each tag count how many users have posted to it
tagusers = {}
mycursor.execute(sql_getuseridsfromtaguser)
tmp = mycursor.fetchall()
for t in tmp:
    if t[0] not in tagusers:
        tagusers[t[0]] = 1
    else:
        tagusers[t[0]] += 1
outputtagsCSV(tagusers, tags)

# Build link table
for tag in tags:
    val = (tag, tag)
    mycursor.execute(sql_getlinkswithtag, val)
    links = mycursor.fetchall()
    linkswithtag = []
    for link in links:
        if tagusers[link[0]] < outputdetail or tagusers[link[1]] < outputdetail:
            continue
        if link[0] == tag:
            if link[1] not in links:
                linkswithtag.append(link[1])
        else:
            if link[0] not in links:
                linkswithtag.append(link[0])

    # output to stdout
    outputlinkspertagCSV(tag, tags, tagusers, linkswithtag)
