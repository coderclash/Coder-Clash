import tornado.web
from tornado.web import url
from coderclash import handlers

urls = [
    url(r'/', handlers.Index, name='index'),
    url(r'/play/$', handlers.Play, name='play'),
    url(r'/auth/login/$', handlers.AuthLogin, name='auth'),
    (r'/.*/?', tornado.web.RequestHandler),
]
