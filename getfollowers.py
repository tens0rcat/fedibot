from modules import Mastodon as mastodon
M_server_id = 'https://nerdculture.de'
M_user_token = 'A6He55%Ta70EUG^JQ#'
myAccount = mastodon.mastodon.log_in(
      mastodon.M_email,
      M_user_token,
      mastodon.M_login,
  )
 
followers = mastodon.account_followers(myAccount)
