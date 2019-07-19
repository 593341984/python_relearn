# -*- coding:utf-8 -*-
__author__ = "ljh"
__date__ = "2019-07-17"

import hmac
import hashlib
from urllib.parse import quote


def hmac_sha256(key, message):
    """
    hmacsha256加密
    :return: 加密结果转成16进制字符串形式，并小写
    """

    message = message.encode('utf-8')
    return hmac.new(key.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest().lower()



DATA = {
    "origin": "32.979558,117.323466",
    "retCoordType": "bd09ll",
    "departureTime": 1561973223,
    "plateColor": 1,
    "plateNumber": "E83486",
    "weight": 14.12485,
    "coordType": "bd09ll",
    "destination": "31.817881,117.451349",
    "axleWeight": 4.70828333333333,
    "routeId": "f3752e526c4841e4a8531b8dc4f4f50b",
    "width": 2.42,
    "length": 9.6,
    "plateProvice": "\u8d63",
    "isTrailer": 0,
    "tactics": 1,
    "height": 2.5,
    "axleCount": 3
}

def create_canonical_request(request_data=DATA):
    http_method = 'POST'
    canonical_uri = quote('/v1/lps/logistics/direction')

    request_list = []
    for k, v in request_data.items():
        request_list.append(quote(k, safe='') + '=' + quote(v, safe=''))

    canonical_query_string = '&'.join(sorted(request_list))

    canonical_headers = ''

if __name__ == "__main__":

    s = quote(DATA['plateProvice'], safe='/')
    print(s)
    print(DATA)
