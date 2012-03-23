import httplib
import asyncmongo
import tornado.web
from coderclash.settings import DB


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler to rule them all.
    """

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(**DB)
        return self._db

    def get_current_user(self):
        pass

    def get_error_html(self, status_code, **kwargs):
        pass
