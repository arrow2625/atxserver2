# -*- coding: utf-8 -*-
# @Time    : 2021-10-20
# @Author  : Arrow


from tornado import httpclient
from tornado.httputil import url_concat
from tornado.web import RequestHandler

from typing import List, Any, Dict, cast, Iterable, Union, Optional
import requests


class GoogleMixin(object):
    def authenticate_redirect(self):
        url = 'http://cap.qa.sz.shopee.io:8805/api/getUserInfo'
        resp = requests.get(url, headers={"referer": "http://10.12.189.70:4000"})
        if resp.status_code == 403:
            next_url = resp.json().get('login_url')
            self.set_cookie_sso_a(next_url)
            self.redirect(next_url)
        else:
            self.redirect('/')

    def get_authenticated_user(self, sso_c, sso_a):
        if sso_c:
            sso_x = sso_c
        else:
            sso_x = sso_a
        url = 'http://cap.qa.sz.shopee.io:8805/api/refresh_token?' + 'sso_c=' + sso_x
        resp = requests.get(url)
        if resp.status_code == 200:
            self.set_cookie_sso_c(resp.json().get('sso_c'))
            user = {'email': resp.json().get('email'), 'name': resp.json().get('username')}
            return user
        else:
            self.clear_all_cookies()
            self.redirect("/login")

    def get_auth_http_client(self) -> httpclient.AsyncHTTPClient:
        """Returns the `.AsyncHTTPClient` instance to be used for auth requests.

        May be overridden by subclasses to use an HTTP client other than
        the default.
        """
        return httpclient.AsyncHTTPClient()

    def authorize_redirect(
            self,
            redirect_uri: str = None,
            url: str = None,
            extra_params: Dict[str, Any] = None,
            response_type: str = "code",
    ) -> None:
        handler = cast(RequestHandler, self)
        args = {"response_type": response_type}
        if redirect_uri is not None:
            args["redirect_uri"] = redirect_uri
        if extra_params:
            args.update(extra_params)
        handler.redirect(url_concat(url, args))

    def set_cookie_sso_a(self, url):
        import urllib.parse as urlparse
        parsed = urlparse.urlparse(url)
        query = urlparse.parse_qs(parsed.query)
        sso_a = query.get('anonymous_sso_key')[0]
        self.set_cookie('SSO_A', sso_a)

    def set_cookie_sso_c(self, sso_c):
        self.set_cookie('SSO_C', sso_c)
