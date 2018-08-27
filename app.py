import tornado.ioloop
import tornado.web
import pymongo
from common import utils
from handlers.insert_handler import InsertHandler
from handlers.access_handler import AccessHandler
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--db_port', default="27017", type=int,help='val folder')
parser.add_argument('--service_port', default="8888", type=int,help='val folder')



class Application(tornado.web.Application):
    def __init__(self, db_port, service_port):
        handlers = [
            (r"/shorten_url", InsertHandler),
            (r"/(.*)", AccessHandler)
        ]
        self.host = "http://localhost:{}".format(service_port)
        tornado.web.Application.__init__(self, handlers)
        self.db_client = pymongo.MongoClient("mongodb://localhost:{}/".format(db_port))
        self.collection = self.db_client["URL_db"]["URL_collection"]

    def shorten_and_insert(self, url):
        data = {"url": url}
        record = self.collection.find_one_and_update(data,{'$set': data},upsert=True, return_document=pymongo.ReturnDocument.AFTER)
        return utils.encode_to_base62(record['_id'])

    def fetch_long_url(self, shortened_url):
        try:
            long_url = self.collection.find_one({'_id': utils.decode_to_obj_id(shortened_url)})
            return long_url['url'] if(long_url is not None) else None
        except:
            return None

if __name__ == "__main__":
    args = parser.parse_args()
    dbport       = args.db_port
    service_port = args.service_port
    app = Application(db_port = dbport, service_port=service_port)
    app.listen(service_port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
