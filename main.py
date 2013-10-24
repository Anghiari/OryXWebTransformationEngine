'''
Created on Jun 20, 2013

@author: acer
'''
import os.path
import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define

from communication_adapter.homehandler import HomeHandler, SessionHandler
from communication_adapter.mainhandler import MainHandler
from communication_adapter.contenthandler import ContentHandler
from communication_adapter.navigationhandler import NavigationHandler


define("port", default=5000, help="run on the given port", type=int)


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")

#===============================================================================
# Application
#===============================================================================
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
<<<<<<< .mine
            (r"/", HomeHandler),
            (r"/main", MainHandler),
            (r"/content", ContentHandler),
            (r"/nav", NavigationHandler),
            (r"/close", SessionHandler)
=======
            (r"/", IndexHandler),
            (r"/api", HomeHandler),
            (r"/api/main", MainHandler),
            (r"/api/content", ContentHandler),
            (r"/api/nav", NavigationHandler),
            (r"/api/close",SessionHandler)
>>>>>>> .r288
        ]
        

        settings = dict(
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True
        )
        
        
        tornado.web.Application.__init__(self, handlers, **settings)

        


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(os.environ.get("PORT", 5000))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
