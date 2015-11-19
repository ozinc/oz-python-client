import os
from urllib import urlencode

import requests

class OZCoreApi(object):
    BASE_URL = os.environ['OZ_API_URL'] if os.environ.has_key('OZ_API_URL') else 'https://core.oz.com'

    def __init__(self, username, password):
        required_env = ['OZ_CLIENT_ID', 'OZ_CLIENT_SECRET']
        for var in required_env:
            if not os.environ.has_key(var):
                raise Exception('The required variable {0} was not set.'.format(var))

        self.client_id, self.client_secret = map(lambda var: os.environ[var], required_env)

        self.access_token = self._authenticate_user(username, password)

    def fetch_collection_by_external_id(self, external_id, **kwargs):
        params = {
                'externalId': external_id,
                'all': 'true'
        }
        params.update(kwargs)
        url = self._append_query_params(
                '{0}/channels/{1}/collections'.format(self.BASE_URL, self.channel_id),
                **params)
        return self._fetch_object_at_uri(url)

    def fetch_video_by_external_id(self, external_id, **kwargs):
        params = {
                'externalId': external_id,
                'all': 'true'
        }
        params.update(kwargs)
        url = self._append_query_params(
                '{0}/channels/{1}/videos'.format(self.BASE_URL, self.channel_id),
                **params)
        return self._fetch_object_at_uri(url)

    def fetch_slot_by_external_id(self, external_id, **kwargs):
        params = {
                'externalId': external_id
        }
        params.update(kwargs)
        url = self._append_query_params(
                '{0}/channels/{1}/slots'.format(self.BASE_URL, self.channel_id),
                **params)
        return self._fetch_object_at_uri(url)

    def create_collection(self, collection, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/collections'.format(self.BASE_URL, self.channel_id),
                **kwargs)
        return self._create_object_at_uri(collection, url)

    def create_slot(self, slot, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/slots'.format(self.BASE_URL, self.channel_id),
                **kwargs)
        return self._create_object_at_uri(slot, url)

    def create_video(self, video, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/videos'.format(self.BASE_URL, self.channel_id),
                **kwargs)
        return self._create_object_at_uri(video, url)

    def update_collection(self, collection, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/collections/{2}'.format(self.BASE_URL, self.channel_id, collection['id']),
                **kwargs)
        return self._update_object_at_uri(collection, url)

    def update_video(self, video, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/videos/{2}'.format(self.BASE_URL, self.channel_id, video['id']),
                **kwargs)
        return self._update_object_at_uri(video, url)

    def update_slot(self, slot, **kwargs):
        url = self._append_query_params(
                '{0}/channels/{1}/slots/{2}'.format(self.BASE_URL, self.channel_id, slot['id']),
                **kwargs)
        return self._update_object_at_uri(slot, url)

    def _append_query_params(self, url, **kwargs):
        if kwargs:
            url += '?' + urlencode(kwargs)
        return url

    def _update_object_at_uri(self, obj, uri):
        r = requests.patch(uri, json=obj, headers={'Authorization': 'Bearer ' + self.access_token})
        if r.status_code is 200:
            return r.json()['data']
        elif r.status_code is 404:
            return None
        else:
            raise Exception('an error occurred when updating an object, status was: {0}'.format(r.status_code))

    def _create_object_at_uri(self, obj, uri):
        r = requests.post(uri, json=obj, headers={'Authorization': 'Bearer ' + self.access_token})
        if r.status_code is 201:
            return r.json()['data']
        else:
            raise Exception('an error occurred when creating an object, status was: {0}'.format(r.status_code))

    def _fetch_object_at_uri(self, uri):
        r = requests.get(uri, headers={'Authorization': 'Bearer ' + self.access_token})
        if r.status_code is 200:
            objects = r.json()['data']
            if len(objects) is 0:
                return None
            else:
                return objects[0]
        else:
            raise Exception('an error occurred when fetching object, status was: {0}'.format(r.status_code))

    def _authenticate_user(self, username, password):
        url = '{0}/oauth2/token'.format(self.BASE_URL)
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        r = requests.post(url, data=data)
        if r.status_code is 200:
            return r.json()['access_token']
        else:
            raise Exception('An error occurred when authorizing, status was: {0}'.format(r.status_code))
