import tornado.web
from coderclash.handlers.base import BaseHandlerMixin


class Index(BaseHandlerMixin, tornado.web.RequestHandler):

    def get(self):
        user = self.get_current_user()
        self.write(self.render('base.html', user=user))
