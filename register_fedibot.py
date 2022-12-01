from mastodon import Mastodon
from mysecrets.fedibotsecrets import mastodonsecrets as sMasto

M_client_id = sMasto['MASTODON_CLIENT_ID']
M_api_base_url = sMasto['MASTODON_PRIMARY_BASE_URL']
M_email = sMasto['MASTODON_PRIMARY_USER_EMAIL']
M_user_token = sMasto['MASTODON_PRIMARY_USER_TOKEN']
M_login = sMasto['MASTODON_PRIMARY_LOGIN']

Mastodon.create_app(
    'fedibot',
    api_base_url = M_api_base_url,
    to_file = M_client_id
)
