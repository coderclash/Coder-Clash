import logging
import os
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornadio2
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

# import play and get socket server running
from coderclash.handlers import PlaySocket
PlayRouter = tornadio2.router.TornadioRouter(PlaySocket)
sock_app = tornado.web.Application(
    PlayRouter.urls,
    #flash_policy_port = 843,
    #flash_policy_file = os.path.join(settings.BASE_DIR, 'static/assets/flashpolicy.xml'),
    socket_io_port = 8001
)

def main():
    tornado.options.parse_command_line()

    # create http server
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    # Create tornadio server on port 8002, but don't start it yet
    tornadio2.server.SocketServer(sock_app, auto_start=False)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
