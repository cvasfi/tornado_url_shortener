import tornado.ioloop
import tornado.web



class InsertHandler(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument("url")
        self.write(url+"\n")

class AccessHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(id+"\n")

def make_app():
    return tornado.web.Application([
        (r"/shorten_url", InsertHandler),
        (r"/(.*)", AccessHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()