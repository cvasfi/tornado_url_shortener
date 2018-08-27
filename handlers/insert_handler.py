import tornado.web
from http import HTTPStatus
import json
from common import utils

class InsertHandler(tornado.web.RequestHandler):
    """
    Handles the short URL creation requests
    """
    def post(self):
        url = self.get_argument("url")
        if(utils.validate_url(url)):
            shortened_url = self.application.host +"/"+ self.application.shorten_and_insert(url)
            self.write(json.dumps({'shortened_url':shortened_url}))
            self.set_header('Content-Type', 'application/json')
            self.set_status(HTTPStatus.CREATED)
        else:
            self.set_status(HTTPStatus.BAD_REQUEST, "The URL is not valid.")
            self.write("The URL is not valid.")