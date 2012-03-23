from coderclash.handlers.base import BaseHandler


class AuthLogin(BaseHandler):

    def get(self):
        return self.render('auth/login.html')


class AuthLogout(BaseHandler):
    pass
