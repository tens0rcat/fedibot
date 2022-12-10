from modules import myMastodon as Mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec
import requests
import json
import time

local = Mastodon.init("commander", "freebot.dev", "tensorcat", M_sec)
local = Mastodon.login("pace")

big = Mastodon.init("commander", "nerdculture.de", "tensorcat", M_sec)
big = Mastodon.login()

#Get my account data
mydata = local.me()
followers = local.account_following(id = mydata.id)
followers = local.fetch_remaining(followers)

file = open("files/data/newsies", "r") #file of usernames to follow
lines = file.readlines()
file.close()

kwargs = {}
kwargs["headers"] = {
  'Authorization': "Bearer " + local.access_token,
  'User-Agent' : "api"
}

for line in lines:
  username = line[0:len(line)-1].strip(" ")
  userinlist = (0 != len(list(filter(lambda f: f["acct"] == username, followers))))
  if (userinlist): 
    continue
  time.sleep(5)
  print(username, end=" - ")
  #acct = local.account_search("@" + username)

  url = "https://freebot.dev/api/v2/search?q=" + username + "&resolve=true"
  response = requests.get(url, **kwargs)
  try:
    acct = json.loads(response.text)['accounts']
  except:
    acct = {}

  if len(acct) == 0:
    print("Not Found")
    continue
  for a in acct:
    try:
      id = a['id']
      rel = local.account_follow(id, False, False) #so does a "remote" account need to be created and try again?
      print("Followed")
    except BaseException as e:
      print("Follow Failed")
      print(e)
#  not working
pass