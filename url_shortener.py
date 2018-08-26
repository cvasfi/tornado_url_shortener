import tornado.ioloop
import tornado.web
from http import HTTPStatus
import json
import pymongo
from bson import ObjectId
from baseconv import base16, base62

def validate_url(url):
    #TODO: implement
    return True


class InsertHandler(tornado.web.RequestHandler):
    def post(self):
        url = self.get_argument("url")
        if(validate_url(url)):
            shortened_url = self.application.host +"/"+ self.application.shorten_and_insert(url)
            self.write(json.dumps({'shortened_url':shortened_url}))
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTPStatus.OK)
        else:
            self.set_status(HTTPStatus.BAD_REQUEST, "The URL is not valid.")



class AccessHandler(tornado.web.RequestHandler):
    def get(self, id):
        long_url = self.application.fetch_long_url(id)
        if(long_url is not None):
            self.set_status(HTTPStatus.OK)
            self.redirect(long_url)
        else:
            self.set_status(HTTPStatus.NOT_FOUND, "This URL does not exist.")




class Application(tornado.web.Application):
    def __init__(self, db_port, service_port):
        handlers = [
            (r"/shorten_url", InsertHandler),
            (r"/(.*)", AccessHandler)
        ]
        self.host = "http://localhost:{}".format(service_port)

        tornado.web.Application.__init__(self, handlers)

        db_client = pymongo.MongoClient("mongodb://localhost:{}/".format(db_port))
        self.collection = db_client["URL_db"]["URL_collection"]


    def shorten_and_insert(self, url):
        data         = {"url": url}
        record       = self.collection.find_one_and_update(data,{'$set': data},upsert=True, return_document=pymongo.ReturnDocument.AFTER)
        base_obj_id  = base16.decode(str(record['_id']).upper())
        return base62.encode(base_obj_id)

    def fetch_long_url(self, shortened_url):
        #TODO: error handling
        obj_id = base16.encode(base62.decode(shortened_url))
        long_url = self.collection.find_one({'_id':ObjectId(obj_id)})
        return long_url['url'] if(long_url is not None) else None




if __name__ == "__main__":

    dbport       = 27017
    service_port = 8888
    app = Application(db_port = dbport, service_port=service_port)
    app.listen(service_port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
