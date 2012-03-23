from coderclash import handlers

urls = [
    (r'/', handlers.Index),
    (r'/auth/login/', handlers.AuthLogin),
    (r'/.*/?', handlers.BaseHandler),
]
