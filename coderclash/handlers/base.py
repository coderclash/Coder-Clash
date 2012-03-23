import httplib
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler to rule them all.
    """

    def get_current_user(self):
        pass

    def get_error_html(self, status_code, **kwargs):
        pass
