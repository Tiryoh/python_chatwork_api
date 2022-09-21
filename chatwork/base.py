# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Daisuke Sato

import urllib
import requests
from chatwork.rooms import Room


class ChatworkError(Exception):
    pass


class BaseAPI(object):
    def __init__(self, api_key):
        self.base_url = "https://api.chatwork.com/v2/"
        # self.base_url = "http://127.0.0.1/"
        self.api_key = api_key
        self._build_api()

    def _build_api(self):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def invoke_method(self, method, uri, query_param={}, request_param={}, headers=None, **kwargs):
        """
        Delegate requests to get/post/delete method.
        Each method implements by any http client, default client is requests.
        :param method: HTTP Method. supports GET/POST/DELETE
        :param uri: API Endpoint. 'uri' expects a URI excluded '/v2/' prefix
        :param query_param: dict of URL parameter. this will be url-encoded string
        :param request_param: dict of body parameter. this will use when invoke post request
        :param headers: HTTP Header dict. Recommend value is None. if None, then use default implements of http client(requests).
        :return: http response object
        """
        method = method.lower()

        if method == "get":
            resp = self.get(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "post":
            resp = self.post(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "delete":
            resp = self.delete(method, uri, query_param, request_param, headers, **kwargs)

        elif method == "patch":
            resp = self.patch(method, uri, query_param, request_param, headers, **kwargs)

        else:
            raise ChatworkError("Not supported http method: {}".format(method))

        return resp

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def post(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def delete(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError

    def patch(self, method, uri, query_param, request_param, headers, **kwargs):
        """Sorry, not implemented yet
        """
        raise NotImplementedError


class ChatworkAPI(BaseAPI):
    def _build_api(self):
        self.room = Room(self)

    def get(self, method, uri, query_param, request_param, headers, **kwargs):
        if len(query_param) == 0:
            _url = self.base_url + uri
        else:
            params = urllib.parse.urlencode(query_param)
            _url = self.base_url + uri + f"?{params}"

        if headers is not None:
            resp = requests.get(_url, params=query_param, headers=headers, **kwargs)
        else:
            resp = requests.get(_url, params=query_param, headers={"x-chatworktoken": f"{self.api_key}"}, **kwargs)

        if resp.status_code // 100 == 2:
            return resp

        raise ChatworkError(f"Http response {resp.status_code}: {resp.text} {_url}")

    def post(self, method, uri, query_param={}, request_param={}, headers=None, **kwargs):
        _url = self.base_url + uri

        if len(request_param) == 0:
            request_param = {}
        else:
            request_param = urllib.parse.urlencode(request_param)

        if headers is not None:
            resp = requests.post(_url, data=request_param, headers=headers, **kwargs)
        else:
            resp = requests.get(_url, data=request_param, headers={"x-chatworktoken": f"{self.api_key}"}, **kwargs)

        if resp.status_code // 100 == 2:
            return resp

        raise ChatworkError(f"Http response {resp.status_code}: {resp.text} {_url} {request_param}")
