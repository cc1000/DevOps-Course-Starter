import os
from oauthlib.oauth2 import WebApplicationClient

class AuthProvider:
    def __init__(self):
        self.oauth_provider_base_uri = os.environ['OAUTH_PROVIDER_BASE_URI']
        self.oauth_client_id = os.environ['OAUTH_CLIENT_ID']
        self.oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']

    def get_login_redirect_uri(self):
        client = WebApplicationClient(self.oauth_client_id)
        return client.prepare_request_uri(f'{self.oauth_provider_base_uri}/login/oauth/authorize')

    def get_authenticated_user(auth_code):
        client = WebApplicationClient(self.oauth_client_id)
        
        self.get_access_token(client, auth_code)
        return self.get_user(client)

    def get_access_token(self, client, auth_code):
        token_uri, headers, body = client.prepare_token_request(
            token_url=f'{self.oauth_provider_base_uri}/login/oauth/access_token', 
            code=auth_code,
            client_secret=self.oauth_client_secret
        )
        headers['Accept'] = 'application/json'

        response = requests.post(token_uri, data=body, headers=headers)
        response.raise_for_status()

        client.parse_request_body_response(response.content)

    def get_user(self, client):
        uri, headers, body = client.add_token(f'{self.oauth_provider_base_uri}/user')

        response = requests.get(uri, headers=headers)
        response.raise_for_status()

        return AppUser(response.json()['login'])
