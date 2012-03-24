import tornado.web
from coderclash.handlers.base import BaseHandler
from coderclash.auth import github


class AuthLogin(BaseHandler, github.GithubAuthMixin):
    """
    Asynchronously handles user authentication with the github api.

    The first time the URL is hit, a request is made to get the
    authentication token from github in the form of a query string
    ``code=something``

    If that code is present, authenticate the user with
    ``get_authenticated_user``

    ::todo::
        - Not all user data needs to be in the cookie. Trim it down.

    """
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(
                self.get_full_url(self.reverse_url('auth')),
                self.settings['github_client_id'],
                self.settings['github_client_secret'],
                self.get_argument('code'),
                self.async_callback(self._on_auth))
            return
        self.authorize_redirect(
            redirect_uri=self.settings['github_callback_url'],
            client_id=self.settings['github_client_id'])

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'github auth failed.')

        self.db.users.update(
            {'github_id': user.get('id')},
            {"$set": user}, True,
            callback=self.async_callback(self._finish_query, user))

    def _finish_query(self, user, response, error=None):
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


# class AuthLogout(AuthMixin, BaseHandler):
#     pass
