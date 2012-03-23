from coderclash.handlers.base import BaseHandler


class Index(BaseHandler):

    def get(self):
        self.write('hello world')
