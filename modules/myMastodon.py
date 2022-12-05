from mastodon import Mastodon
import os

global M_client_id
global M_server_id
global M_api_base_url
global M_email
global M_user_token
global M_login
global M_url
global mastodon

##

def init(appname, server, user, secret):
  global M_client_id
  global M_server_id
  global M_api_base_url
  global M_email
  global M_user_token
  global M_login
  global M_url
  global mastodon

  M_client_id = "mysecrets/" + appname + "_" + server + ".secret"
  M_server_id = server
  M_api_base_url = "https://" 
  M_email = secret[server][user]['MASTODON_PRIMARY_USER_EMAIL']
  M_user_token = secret[server][user]['MASTODON_PRIMARY_USER_TOKEN']
  M_login = "mysecrets/" + appname + "_" + server + "_login.secret" 

  M_url = M_api_base_url + M_server_id

  if not os.path.exists(M_client_id):
    Mastodon.create_app(
        appname,
        api_base_url = M_url,
        to_file = M_client_id
    )

  mastodon = Mastodon(
      client_id = M_client_id,
      api_base_url = M_url
  )

  return mastodon

##

def server():
  return M_server_id

##

def login(ratelimit="pace"):
  global mastodon
  mastodon.log_in(
      M_email,
      M_user_token,
      M_login
  )
  Mastodon(
    client_id = M_client_id,
    ratelimit_method = ratelimit
  )
  return mastodon

##

# def login():
#   global mastodon
#   mastodon.log_in(
#       M_email,
#       M_user_token,
#       M_login
#   )
#   return mastodon

##
 
def getposts():
  return mastodon.timeline_local() + mastodon.timeline_public()

##