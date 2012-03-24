from tornado.web import url
from coderclash import handlers

urls = [
    url(r'/', handlers.Index, name='index'),
    url(r'/auth/login/$', handlers.AuthLogin, name='auth'),
    url(r'/auth/success/$', handlers.AuthSuccess, name='auth-success'),
    (r'/.*/?', handlers.BaseHandler),
]
