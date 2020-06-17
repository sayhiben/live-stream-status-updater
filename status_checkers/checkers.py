from abc import ABC, abstractmethod

import re
import requests


class StatusChecker(ABC):
    @abstractmethod
    def check_status(self):
        pass


class TwitchStatusChecker(StatusChecker):
    OAUTH_URL = 'https://id.twitch.tv/oauth2/token'
    BASE_URL = 'https://api.twitch.tv/helix'

    def __init__(self, client_id, client_secret):
        super(TwitchStatusChecker, self).__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def check_status(self, url):
        user_data = self._authorized_get(
            f"{self.BASE_URL}/users",
            params={
                'login': self._extract_login_from_url(url)
            }
        )
        stream_data = self._authorized_get(
            f"{self.BASE_URL}/streams",
            params={
                'user_id': user_data['data'][0]['id']
            }
        )
        return len(stream_data['data']) > 0

    def _extract_login_from_url(self, url):
        match = re.search('.*twitch\.tv/([^/]+).*', url)
        return match.group(1)

    def _fetch_access_token(self):
        response = requests.post(
            self.OAUTH_URL,
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            })
        return response.json()['access_token']

    def _authorized_get(self, *args, **kwargs):
        self.access_token = self.access_token or self._fetch_access_token()
        kwargs['headers'] = {
            'Authorization': f"Bearer {self.access_token}",
            'Client-ID': self.client_id
        }
        response = requests.get(*args, **kwargs)
        return response.json()


class FacebookStatusChecker(StatusChecker):
    def check_status(self):
        pass


class PeriscopeStatusChecker(StatusChecker):
    def check_status(self):
        pass


class InstagramStatusChecker(StatusChecker):
    def check_status(self):
        pass
