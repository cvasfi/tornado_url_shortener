import tornado.web
from http import HTTPStatus


class AccessHandler(tornado.web.RequestHandler):
    """
    Handles the redirection requests
    """
    def get(self, id):
        long_url = self.application.fetch_long_url(id)
        if(long_url is not None):
            self.set_status(HTTPStatus.OK)
            self.redirect(long_url)
        else:
            self.set_status(HTTPStatus.NOT_FOUND, "This URL does not exist.")
            self.write("This URL does not exist.")
