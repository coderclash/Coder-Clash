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
    """
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(
                self.get_full_url(self.reverse_url('auth')),
                self.settings['github_client_id'],
                self.settings['github_client_secret'],
                self.get_argument('code'),
                self.async_callback(self._on_auth),
                extra_fields=set(['html_url', 'bio']))
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
        user_info = {
            'id': user.get('id'),
            'name': user.get('name'),
            'avatar_url': user.get('avatar_url')
        }
        self.set_secure_cookie("user", tornado.escape.json_encode(user_info))
        self.redirect(self.get_argument("next", "/"))
