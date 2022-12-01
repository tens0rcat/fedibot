from modules import Mastodon as mastodon
from mysecrets.nerdculturesecret import mastodonsecrets as M_sec
import time

mastodon.init("followers2list", M_sec)

mastodon = mastodon.login()

mydata = mastodon.me()
lists = mastodon.lists()
for list in lists:
  mastodon.list_delete(list.id)
lists = mastodon.lists()
followers = mastodon.account_followers(id = mydata.id)
followers = mastodon.fetch_remaining(followers)
list = mastodon.list_create("MyPeeps")
lists = mastodon.lists()
followerids = []
for follower in followers:
  followerids.append(follower.id) 
  try:
    mastodon.list_accounts_add(
      id = list.id, 
      account_ids = follower.id
    )
  except:
    print("BAD acct: " + follower.acct)
    continue
  print(follower.acct)
pass