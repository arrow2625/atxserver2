# -*- coding: utf-8 -*-
# @Time    : 2021-10-20
# @Author  : Arrow

import base64
import binascii
import hashlib
import hmac
import time
import urllib.parse
import uuid

from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.util import unicode_type
from tornado.web import RequestHandler

from typing import List, Any, Dict, cast, Iterable, Union, Optional
import logging


class GoogleMixin(object):

    def authenticate_redirect(
            self,
            callback_uri: str = None,
            ax_attrs: List[str] = ["nickname", "email", "fullname"],
    ) -> None:
        handler = cast(RequestHandler, self)
        callback_uri = callback_uri or handler.request.uri
        assert callback_uri is not None
        args = self._openid_args(callback_uri, ax_attrs=ax_attrs)
        endpoint = self._OPENID_ENDPOINT  # type: ignore
        from pprint import pprint
        pprint(args)
        handler.redirect(endpoint + "?" + urllib.parse.urlencode(args))

    async def get_authenticated_user(
            self,
            http_client: httpclient.AsyncHTTPClient = None) -> Dict[str, Any]:
        handler = cast(RequestHandler, self)
        args = dict((k, v[-1]) for k, v in handler.request.arguments.items()
                    )  # type: Dict[str, Union[str, bytes]]
        args["openid.mode"] = u"check_authentication"
        url = 'http://cap.qa.sz.shopee.io:8805/api/getUserInfo'
        if http_client is None:
            http_client = self.get_auth_http_client()
        resp = await http_client.fetch(url)
        logging.warning(resp)
        return 'arrow'

    def get_auth_http_client(self) -> httpclient.AsyncHTTPClient:
        """Returns the `.AsyncHTTPClient` instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than
        the default.
        """
        return httpclient.AsyncHTTPClient()
