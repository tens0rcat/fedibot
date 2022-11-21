from mastodon import Mastodon

Mastodon.create_app(
     'fedibot',
     api_base_url = 'https://nerdculture.de',
     to_file = 'files/secrets/fedibot.secret'
)
