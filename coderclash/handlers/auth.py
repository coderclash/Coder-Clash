import tornado.web
from coderclash.handlers.base import BaseHandler
from coderclash.auth import github


class AuthLogin(BaseHandler, github.GithubAuthMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(
                self.get_full_url(self.reverse_url('auth-success')),
                self.settings['github_client_id'],
                self.settings['github_client_secret'],
                self.get_argument('code'),
                self.async_callback(self._on_auth))
        self.authorize_redirect(
            redirect_uri=self.settings['github_callback_url'],
            client_id=self.settings['github_client_id'])

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'github auth failed.')
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect(self.get_argument("next", "/"))


class AuthSuccess(BaseHandler):
    pass


# class AuthLogout(AuthMixin, BaseHandler):
#     pass
