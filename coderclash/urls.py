from coderclash import handlers

urls = [
    (r'/', handlers.Index),
    (r'/.*/?', handlers.BaseHandler),
]
