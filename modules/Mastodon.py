from mastodon import Mastodon
from mysecrets.mysecrets import mastodonsecrets as sMasto

M_client_id = sMasto['MASTODON_CLIENT_ID']
M_api_base_url = sMasto['MASTODON_PRIMARY_BASE_URL']
M_email = sMasto['MASTODON_PRIMARY_USER_EMAIL']
M_user_token = sMasto['MASTODON_PRIMARY_USER_TOKEN']
M_login = sMasto['MASTODON_PRIMARY_LOGIN']

mastodon = Mastodon(
    client_id = M_client_id,
    api_base_url = M_api_base_url
)

def login():
  global mastodon
  mastodon.log_in(
      M_email,
      M_user_token,
      M_login
  )
 
def getposts():
  return mastodon.timeline_local() + mastodon.timeline_public()