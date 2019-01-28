import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Client(object):
    def __init__(self, url: str):
        self.url = url

    def get_profile(self, token):
        headers = {
            'Authorization': 'Bearer {}'.format(token),
            'Accept': 'application/json'
        }
        resp = requests.get('{}/auth/profile'.format(self.url), headers=headers)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code in (401, 403):
            raise AuthenticationFailed

        raise Exception('API issue HTTP Status {} Response {}'.format(resp.status_code, resp.content))


client = Client(settings.CONST_API['URL'])
