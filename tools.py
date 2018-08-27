import re
from baseconv import base16, base62
from bson import ObjectId

def validate_url( url):
    '''
    Uses a previous version of Django's regex URL validator as seen on: https://github.com/django/django/blob/master/django/core/validators.py
    '''
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def encode_to_base62(obj_id):
    '''
    First decodes the hexadecimal object ID and then encodes it to base 62 which will be used as the short URL ID
    '''
    return base62.encode(base16.decode(str(obj_id).upper()))

def decode_to_obj_id( id):
    '''
    #Decodes the base 62 short URL ID and then encodes it into hexadecimal format as an ObjectID
    '''
    return ObjectId(base16.encode(base62.decode(id)))