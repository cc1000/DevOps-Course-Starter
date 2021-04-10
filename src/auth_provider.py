import os
from oauthlib.oauth2 import WebApplicationClient
import requests
from app_user import AppUser

class AuthProvider:
    READER_ROLE = 'reader'
    WRITER_ROLE = 'writer'

    def __init__(self):
        self.oauth_provider_base_uri = os.environ['OAUTH_PROVIDER_BASE_URI']
        self.oauth_api_base_uri = os.environ['OAUTH_API_BASE_URI']
        self.oauth_client_id = os.environ['OAUTH_CLIENT_ID']
        self.oauth_client_secret = os.environ['OAUTH_CLIENT_SECRET']

        self.user_role_map = {
            'cc1000': [AuthProvider.READER_ROLE, AuthProvider.WRITER_ROLE],
            'someOtherUser': [AuthProvider.READER_ROLE]
        }

    def get_login_redirect_uri(self):
        client = WebApplicationClient(self.oauth_client_id)
        return client.prepare_request_uri(f'{self.oauth_provider_base_uri}/login/oauth/authorize')

    def get_authenticated_user(self, auth_code):
        client = WebApplicationClient(self.oauth_client_id)
        
        self.get_access_token(client, auth_code)
        return self.get_user_from_response(client)

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

    def get_user_from_response(self, client):
        uri, headers, body = client.add_token(f'{self.oauth_api_base_uri}/user')

        response = requests.get(uri, headers=headers)
        response.raise_for_status()

        user_id = response.json()['login']

        return self.get_user(user_id)

    def get_user(self, user_id):
        return AppUser(user_id, self.get_roles(user_id))

    def get_roles(self, user_id):
        return self.user_role_map[user_id] if user_id in self.user_role_map else None