import tornado.web
import tornado.httpserver
from Handlers import MainHandler, SolutionModule
from MongoInterface import StorageHandler


class Application(tornado.web.Application):
    """Create tornado web-app"""
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/storage/', StorageHandler),
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static',
            'ui_modules': {'Result': SolutionModule},
            'debug': True
        }
        tornado.web.Application.__init__(self, handlers, **settings)
