import os
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from coderclash.settings import PORT, DEBUG, BASE_DIR
from coderclash.urls import urls


define('port', default=PORT, help="Run on the given port", type=int)
define('debug', default=DEBUG, help="Run in debug mode", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'xheaders': True,
            'xsrf_cookie': True,
            'debug': options.debug,
            'template_path': os.path.join(BASE_DIR, 'templates'),
            'static_path': os.path.join(BASE_DIR, 'static'),
            'cookie_secret': '^&*)HLJKFD%*SDFGLJiglasfdoguasdf&^&^&',
            'login_url': '/auth/login/'
        }

        tornado.web.Application.__init__(self, urls, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
