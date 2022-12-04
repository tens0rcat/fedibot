from dataclasses import dataclass
from modules import myMastodon as mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec

#initialize myMastodon module with the name of the app and the secrets
mastodon.init("commander", M_sec, "dev")

#login to the instance, required if doing anything except reading public feeds (local and remote)
mastodon = mastodon.login()

#Get my account data
mydata = mastodon.me()

file = open("files/data/newsies", "r")
lines = file.readlines()
file.close()
for line in lines:
  username = line[0:len(line)-1].strip(" ")
  print(username, end=" - ")
  acct = mastodon.account_search(username)
  if len(acct) == 0:
    print("Not Found")
    continue
  mastodon.account_follow(acct[0].id,False, False)
#  not working
pass