from coderclash.handlers.base import BaseHandler


class Index(BaseHandler):

    def get(self):
        user = self.get_current_user()
        self.write(user)
