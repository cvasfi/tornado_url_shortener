from tornado import testing, httpclient
import tornado
from bson import ObjectId
import urllib
import json
from http import HTTPStatus
import unittest
from app import Application
from common.utils import validate_url, encode_to_base62, decode_to_obj_id

class URLShortenerTests(testing.AsyncHTTPTestCase):
    port=9000
    app = Application(db_port = 27017, service_port=port)
    app.collection = app.db_client["URL_test_db"]["URL_collection"]

    def get_app(self):
        return self.app

    def test_obj_id_reconstruction(self):
        obj_id = ObjectId()
        short_url = encode_to_base62(obj_id)
        reconstructed_obj_id =decode_to_obj_id(short_url)
        self.assertEqual(obj_id, reconstructed_obj_id, "The object ID should be able to identically restored from the base 62 ID")

    def test_url_validation(self):
        self.assertEqual(validate_url("http://www.google.com"), True)
        self.assertEqual(validate_url("://www.google.com"), False)
        self.assertEqual(validate_url("_ssss.biz"), False)
        self.assertEqual(validate_url("http://FEDC:BA98:7654:3210:FEDC:BA98:7654:3210"), True)
        self.assertEqual(validate_url("http://192.0.2.1"), True)
        self.assertEqual(validate_url("aaaaaaaaaaa"), False)
        self.assertEqual(validate_url("google.com"), False)
        self.assertEqual(validate_url("ftp://www.google.com"), True)

    @tornado.testing.gen_test
    def test_url_shortening_service(self):
        test_url="https://httpbin.org/get"
        self.get_app().listen(self.port)
        original_response = yield tornado.httpclient.AsyncHTTPClient().fetch(test_url)

        short_url_response = yield tornado.httpclient.AsyncHTTPClient().fetch("http://localhost:{}/shorten_url".format(self.port), method="POST",
                                                                              body = urllib.parse.urlencode({'url' : test_url}))
        self.assertEqual(short_url_response.code, HTTPStatus.CREATED, "Insert new URL must succeed")
        short_url = json.loads(short_url_response.body)['shortened_url']

        redirected_response = yield tornado.httpclient.AsyncHTTPClient().fetch(short_url, method="GET")
        self.assertEqual(redirected_response.code, HTTPStatus.OK, "Fetch long URL must succeed")


        self.assertEqual(original_response.body, redirected_response.body, "The shortened URL must redirect to the long URL's location")



def all():
    return unittest.defaultTestLoader.loadTestsFromTestCase(URLShortenerTests)

if __name__ == '__main__':
    tornado.testing.main()