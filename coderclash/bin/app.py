import os
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from coderclash import settings
from coderclash.urls import urls


define('port', default=settings.PORT, help="Run on the given port", type=int)
define('debug', default=settings.DEBUG, help="Run in debug mode", type=bool)
define('github_client_id', default=settings.CLIENT_ID,
    help="Github Client ID", type=str)
define('github_client_secret', default=settings.CLIENT_SECRET,
    help="Github Client Secret", type=str)
define('github_callback_url', default=settings.CALLBACK_URL,
    help="Github Callback URL", type=str)


class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'xheaders': True,
            'xsrf_cookie': True,
            'debug': options.debug,
            'template_path': os.path.join(settings.BASE_DIR, 'templates'),
            'static_path': os.path.join(settings.BASE_DIR, 'static'),
            'cookie_secret': '^&*)HLJKFD%*SDFGLJiglasfdoguasdf&^&^&',
            'login_url': '/auth/login/',
            'github_client_id': options.github_client_id,
            'github_client_secret': options.github_client_secret,
            'github_callback_url': options.github_callback_url
        }

        tornado.web.Application.__init__(self, urls, **app_settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
