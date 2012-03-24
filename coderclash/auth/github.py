import urllib
import logging
from tornado.auth import OAuth2Mixin
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat


class GithubAuthMixin(OAuth2Mixin):
    """ Github Oauth Authentication.

        To use Github OAuth authentication, first register your application
        with Github (https://github.com/settings/applications). Copy the
        Client ID & Client Secret keys to your application settings.

        Then, use this mixin on the handler your Callback URL is set to.

        Sample Usage:

        class GithubLogin(tornado.web.RequestHandler,
                          coderclash.utils.github.GithubAuthMixin):
            @tornado.web.asynchronous
            def get(self):
                if self.get_argument('code', None):
                    self.get_authenticated_user(self.async_callback(
                        self._on_auth))
                self.authorize_redirect()

            def _on_auth(self, user):
                if not user:
                    raise tornado.web.HTTPError(500, 'github auth failed.')

        The following is returned as a part of the user object:


        ``github_request()``

        """

    _OAUTH_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    _OAUTH_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
    _OAUTH_NO_CALLBACKS = False

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        http = httpclient.AsyncHTTPClient()
        qargs = dict(
            redirect_uri=redirect_uri,
            code=code,
            client_id=client_id,
            client_secret=client_secret)
        fields = set()
        http.fetch(self._oauth_request_token_url(**qargs),
            self.async_callback(self._on_access_token, redirect_uri, client_id,
                                client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         callback, fields, response):
        if response.error:
            logging.warning('Github auth error {0}'.format(str(response)))
            callback(None)
            return
        args = escape.parse_qs_bytes(escape.native_str(response.body))

        session = {}

        try:
            session['access_token'] = args.get('access_token')[0]
        except TypeError:
            session['access_token'] = ''

        self.github_request(
            path='/user',
            callback=self.async_callback(
                self._get_user_info, callback, session, fields),
            access_token=session['access_token'])

    def _get_user_info(self, callback, session, fields, user):
        if not user:
            callback(None)
            return

        fieldmap = {}
        for field in user:
            fieldmap[field] = user.get(field)
        # for field in fields:
        #     fieldmap[field] = user.get(field)
        fieldmap.update({'access_token': session['access_token']})
        callback(fieldmap)

    def github_request(self, path, callback, access_token=None,
                       post_args=None, **kwargs):
        """

        """
        url = "https://api.github.com{0}".format(path)
        query_args = {}
        if access_token:
            query_args.update({'access_token': access_token})
            query_args.update(post_args or {})
        if query_args:
            url = "{0}?{1}".format(url, urllib.urlencode(query_args))
        callback = self.async_callback(self._on_github_request, callback)

        http = httpclient.AsyncHTTPClient()
        if post_args:
            http.fetch(url, method="POST", body=urllib.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_github_request(self, callback, response):
        if response.error:
            logging.warning("Error '{0}' fetching {1}".format(
                response.error, response.request.url))
            callback(None)
            return
        callback(escape.json_decode(response.body))
