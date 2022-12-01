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

def init(app_name, sMasto):
  global M_client_id
  global M_server_id
  global M_api_base_url
  global M_email
  global M_user_token
  global M_login
  global M_url
  global mastodon

  M_client_id = sMasto['MASTODON_CLIENT_ID']
  M_server_id = sMasto['MASTODON_SERVER_ID']
  M_api_base_url = sMasto['MASTODON_PRIMARY_BASE_URL']
  M_email = sMasto['MASTODON_PRIMARY_USER_EMAIL']
  M_user_token = sMasto['MASTODON_PRIMARY_USER_TOKEN']
  M_login = sMasto['MASTODON_PRIMARY_LOGIN']
  M_url = M_api_base_url + M_server_id

  if not os.path.exists(M_client_id):
    Mastodon.create_app(
        app_name,
        api_base_url = M_url,
        to_file = M_client_id
    )

  mastodon = Mastodon(
      client_id = M_client_id,
      api_base_url = M_url
  )

def login(ratelimit):
  mastodon.log_in(
      M_email,
      M_user_token,
      M_login
  )
  return Mastodon(
    client_id = M_client_id,
    ratelimit_method = ratelimit
  )

def login():
  global mastodon
  mastodon.log_in(
      M_email,
      M_user_token,
      M_login
  )
  return mastodon

 
def getposts():
  return mastodon.timeline_local() + mastodon.timeline_public()