import asyncmongo
import tornado.escape
import tornado.web

from coderclash.settings import DB


class BaseHandlerMixin(object):
    """
    Base handler to rule them all. #LOTR
    """
    def get_full_url(self, url):
        """
        This is a utility method to provide a full URL
        for API calls.
        """
        if not url.startswith('/'):
            return url

        url = url.lstrip('/')
        return '{protocol}://{host}/{url}'.format(
                protocol=self.request.protocol,
                host=self.request.host,
                url=url)

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = asyncmongo.Client(**DB)
        return self._db

    def get_current_user(self):
        """
        Gets the current users info from the user cookie.
        """
        user = self.get_secure_cookie('user')
        if not user:
            return None
        return tornado.escape.json_decode(user)

    def get_error_html(self, status_code, **kwargs):
        pass
