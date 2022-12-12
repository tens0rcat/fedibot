from modules import myMysql as mysql
from wordcloud import WordCloud, STOPWORDS
import time

html = True

cleanupperiodinhours = 24
timeperiodinhours = 6
outputdetail = 1

wordcloud_width = 700
wordcloud_height = 233

numtoptags = 40

retval = mysql.init()
mydb = retval[0]
mycursor = retval[1]

sql_gettags = "SELECT * FROM tags"
sql_getusers = "SELECT * FROM users"
sql_getuseridsfromtaguser = "SELECT tagid, userid FROM taguser WHERE created > (NOW() - INTERVAL " + str(timeperiodinhours) + " HOUR)"
sql_getlinkswithtag = "SELECT t1, t2 FROM links WHERE (t1 = %s OR t2 = %s) AND created > (NOW() - INTERVAL " + str(timeperiodinhours) + " HOUR)"
sql_cleanuplinks = "DELETE FROM links WHERE created < (NOW() - INTERVAL " + str(cleanupperiodinhours) + " HOUR)"
sql_cleanuptagusers = "DELETE FROM taguser WHERE created < (NOW() - INTERVAL " + str(cleanupperiodinhours) + " HOUR)"
sql_cleanupposts = "DELETE FROM posts WHERE created < (NOW() - INTERVAL " + str(cleanupperiodinhours) + " HOUR)"

localtime = time.asctime( time.localtime(time.time()) )   
datestr = "\n\n" + localtime + " " + str(time.tzname[0] )
lendatestr = len(datestr)

def update_profile_page(user, server):
  try:
    #initialize myMastodon module with the name of the app and the secrets
    mastodon.init("top40results", server, user, M_sec)

    #login to the instance, required if doing anything except reading public feeds (local and remote)
    authmastodon = mastodon.login()

    authmastodon.account_update_credentials(
      note = taglist,
      header = "results/wordcloud.png"
    )
  except BaseException:
    print("Error updating " + user + "@" + server) 

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

def htmlout(_post):
  htmlhead = """
  <!DOCTYPE html>
  <html>
    <head>
      <script>
        function CopyToClipboard(id)
        {
          var range = document.createRange();
          range.selectNode(document.getElementById(id));
          window.getSelection().removeAllRanges();
          window.getSelection().addRange(range);
          document.execCommand('copy');
          window.getSelection().removeAllRanges();
        }
      </script>
    </head>
    <body>
      <div>
        <img src = "wordcloud.png" alt = "Popular hashtags" style="background-color: #333333" width="700" height="200"/>
      </div>
      <br><br><hr><br>
  """

   

  htmltail = """
      <br><hr><br>
      <link href="mailto:indieauth@tensorcat.com" rel="me">
      <link href="https://github.com/tens0rcat" rel="me">
      <link href="https://live.tensorcat.com" rel="me">
      <link href="https://nerdculture.de/@tensorcat" rel="me">
      <a href="https://nerdculture.de/invite/uEPJcRfB">Follow me on Mastodon</a>
      <br>
      """ + datestr + """
      <br><hr><br>
      It's a stream, sometimes.  Feel free to watch here or drop in at <br>
      <a href="https://live.tensorcat.com">live.tensorcat.com</a> and say "Howdy!"<br><br>
      <iframe
        src="https://live.tensorcat.com/embed/video"
        title="Tensorcat Live"
        height="450px" width="800px"
        referrerpolicy="origin"
        scrolling="no"
        allowfullscreen
      >
      </iframe>
    </body>
  </html>
  """
  file = open("results/index.html","w")
  file.write(htmlhead)
  file.write(post)
  file.write(htmltail)
  file.close()
  
#cleanup the dang mess
mycursor.execute(sql_cleanuplinks)
mydb.commit()
print(str(mycursor.rowcount) + " links records deleted")

mycursor.execute(sql_cleanuptagusers)
mydb.commit()
print(str(mycursor.rowcount) + " tagusers records deleted")

mycursor.execute(sql_cleanupposts)
mydb.commit()
print(str(mycursor.rowcount) + " posts records deleted")

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
#outputtagsCSV(tagusers, tags)

# Build link table
words = {}
for lt in tagusers:
  if tagusers[lt] >= outputdetail:
    words[tags[lt]] = tagusers[lt]


sorted_words = sorted(words.items(), key=lambda x:x[1], reverse = True)
words = dict(sorted_words)
cnt = 0
postheader  = "#TopHashTagsRightNow\n<br>Top " 
postheader += str(cnt) + " #Hashtags in the last " + str(timeperiodinhours) + " hours.\n<br>" 
postheader += "#Trending #TrendingNow #TrendingTopics<br>\n<hr>-\n<br><br>"
postheader += "Click a #hashtag below and then head back to Mastodon and paste it into the search box.<br>\n" 
postheaderlen = len(postheader) + 2
post = ""

for word in words:
  if cnt >= numtoptags:
    break
  t = "#" + word
  tag = "<a href=\"#\" onclick=\"CopyToClipboard('" + t + "');return false;\"><span id=\"" + t + "\">" + t + "<span></a>\n"
  postlen = postheaderlen + len(post) + len(tag) 
  # if postlen > 500:
  #   break
  post = post + tag
  cnt += 1 
print()
postheader  = "#TopHashTagsRightNow\n<br>Top " 
postheader +=  str(cnt) + " #Hashtags in the last " + str(timeperiodinhours) + " hours.\n<br>" 
postheader +=  "#Trending #TrendingNow #TrendingTopics<br>\n<hr>-\n<br>"
postheader += "Click a #hashtag below and then head back to Mastodon and paste it into the search box.<br>\n" 
post = postheader + post

if html: 
  htmlout(post)
else:
  print(post)

if len(words) < 1:
  exit() 
stopwords = set(STOPWORDS) 
wc = WordCloud( width=wordcloud_width, 
                height=wordcloud_height,
                colormap="rainbow",
                mode="RGBA",
                background_color=None,
                max_words=numtoptags, 
                stopwords=stopwords)
out = wc.generate_from_frequencies(words)
wc.to_file("results/wordcloud.png")


from modules import myMastodon as mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec


taglist = """
#TopHashTagsRightNow #FediTips
Top 40 #Hashtags in the last 6 hours.
#Trending #TrendingNow #TrendingTopics

"""
tagheaderlen = len(taglist)
cnt = 0
for word in words:
  tag = "#" + word + " "
  if len(taglist) + len(tag) + len(datestr) < 500:
    taglist += tag
    cnt += 1
    if cnt > 39 :
      break
taglist += datestr

update_profile_page("tensorcat", "freebot.dev")
update_profile_page("tensorcat", "nerdculture.de")
update_profile_page("top40hashtags", "freebot.dev")
update_profile_page("top40hashtags", "botsin.space")
pass

#TODO: Put this back in once the front end is better
# for tag in tags:
#   val = (tag, tag)
#   mycursor.execute(sql_getlinkswithtag, val)
#   links = mycursor.fetchall()
#   linkswithtag = []
#   for link in links:
#     if tagusers[link[0]] < outputdetail or tagusers[link[1]] < outputdetail:
#       continue
#     if link[0] == tag:
#       if link[1] not in links:
#           linkswithtag.append(link[1])
#     else:
#       if link[0] not in links:
#           linkswithtag.append(link[0])

#   # output to stdout
#   outputlinkspertagCSV(tag, tags, tagusers, linkswithtag)
