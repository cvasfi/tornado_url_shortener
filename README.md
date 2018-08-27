# Tornado URL Shortener

This is a simple URL shortening service using Tornado with MongoDB.

The alphanumeric short URL ID is generated by converting the unique ObjectID from the database 
to base 62.

## Usage
Install the requirements:

`$ pip install -r requirements`

Run mongoDB in the background and launch the application:

`$ python app.py`

Run tests:

`$ python tests/run_tests.py`

## Notes on Scalability

We use Tornado as it is a non-blocking web server that can handle requests asynchronously on a single thread. 
This makes it possible to handle thousands of concurrent connections. The application can easily be scaled further using nginx.
