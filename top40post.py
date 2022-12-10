
from modules import myMastodon as Mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec
import time

def cleanup():
  priorposts = local.account_statuses(mydata.id)
  for post in priorposts:
    local.status_delete(post.id)

local = Mastodon.init("top40hashtags", "freebot.dev", "top40hashtags", M_sec)
local = Mastodon.login("pace")

#Get my account data
mydata = local.me()

cleanup()

localtime = time.asctime( time.localtime(time.time()) )   
datestr = "\n\n" + localtime + " " + str(time.tzname[0] )

posttxt = """
#TopHashTagsRightNow #FediTips
Top 40 #Hashtags in the last 6 hours.
#Trending #TrendingNow #TrendingTopics
""" + datestr + """

The Top 40 hashtag wordcloud and tags are now continuously available at @top40hashtags@freebot.dev !!! Updated every 5 minutes.  The same info is displayed on the https://tensorcat.com website.

Just a reminder, if you go to the webpage when you click a hashtag it copies the tag to your clipboard so you can easily paste it into mastodon's search box.
"""
wordcloud = "results/wordcloud.png"

wordcloud = local.media_post(
  media_file = wordcloud,
  description="Top 40 Hashtags"
)

local.status_post(
  status = posttxt,
  media_ids = wordcloud,
)

pass