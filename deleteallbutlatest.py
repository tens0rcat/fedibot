from modules import myMastodon as Mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec
import requests
import json
import time

local = Mastodon.init("commander", "freebot.dev", "top40hashtags", M_sec)
local = Mastodon.login("pace")

#Get my account data
mydata = local.me()

priorposts = local.account_statuses(mydata.id)
pplen = len(priorposts)
for post in reversed(priorposts):
  pplen -= 1
  if pplen < 1: break
  postdata = local.status_delete(post.id)
  pass

pass