from modules import myMastodon as mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as M_sec

def dumpfollowers():
  file = open("results/followers.txt","w")
  for follower in followers:
    account = str(follower.acct)
    if "@" not in account:
      account += "@" + tmpmastodon.server()
    file.write(str(account) + "\n")
  file.close()

#initialize myMastodon module with the name of the app and the secrets
mastodon.init("followers2list", "nerdculture.de", "tensorcat", M_sec)
tmpmastodon = mastodon

#login to the instance, required if doing anything except reading public feeds (local and remote)
mastodon = mastodon.login()

#Get my account data
mydata = mastodon.me()

#Get my lists
lists = mastodon.lists()

#get the data for the followers list
followerslist = list(filter(lambda mylist: mylist["title"] == "Followers", lists))

#If it exists then set the list id, otherwize create it and set the list id
if len(followerslist) > 0:
  listid = list(filter(lambda mylist: mylist["title"] == "Followers", lists))[0].id
else:
  listid = mastodon.list_create("Followers").id
  
#Get the list of my followers
followers = mastodon.account_followers(id = mydata.id)
followers = mastodon.fetch_remaining(followers)

#Get the list of followers that have already been added to the list
followersinlist = mastodon.list_accounts(listid)
followersinlist = mastodon.fetch_remaining(followersinlist)

# For each follower
for follower in followers:
  #is the follower in the list?
  followerinlist = not (0 == len(list(filter(lambda f: f["id"] == follower.id, followersinlist))))
  #if not
  if not followerinlist:
    try: #to add the follower to the followers list
      mastodon.list_accounts_add(
        id = listid, 
        account_ids = follower.id
      )
      print("Added: " + follower.acct)
    except: #if adding the follower failed
      try:    #to follow back
        mastodon.account_follow(follower.id) 
        try: #if able to follow then try to add to the list
          mastodon.list_accounts_add(
            id = listid, 
            account_ids = follower.id
          )
          print("Added: " + follower.acct)
        except: #followed and still cant add then bad accoount (acct forwarded, deleted, or request pending)
          print("BAD acct: " + follower.acct)
          continue
      except: # couldn't follow back, just skip it.
        print("BAD acct: " + follower.acct)
        continue
    print("Added: " + follower.acct)
pass
#dump list of followers to file
dumpfollowers()
