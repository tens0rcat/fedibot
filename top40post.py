
from modules import myMastodon as Mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec

local = Mastodon.init("top40hashtags", "freebot.dev", "top40hashtags", M_sec)
local = Mastodon.login("pace")

#Get my account data
#mydata = local.me()

posttxt = """
#TopHashTagsRightNow #FediTips
Top 40 #Hashtags in the last 6 hours.
#Trending #TrendingNow #TrendingTopics

The Top 40 hashtag wordcloud and tags are now continuously available in my profile and FINALLY at @top40hashtags !!! Updated every 5 minutes.  The same info is displayed on the https://tensorcat.com website.

Just a reminder, if you go to the webpage when you click a hashtag it copies the tag to your clipboard so you can easily paste it into mastodon's search box.
"""
wordcloud = "results/wordcloud.png"

wordcloud = local.media_post(
  media_file = wordcloud,
  description="Top 40 Hashtags listed below"
)

local.status_post(
  status = posttxt,
  media_ids = wordcloud,
)

pass