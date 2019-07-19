# -*- coding: UTF-8 -*-
import hashlib
import hmac
import string
import datetime
import time

AUTHORIZATION = "authorization"
BCE_PREFIX = "x-bce-"
DEFAULT_ENCODING = 'UTF-8'

ak_id = '80dd2d273c9a4d88bdcb2f054df82513'
sk_id = '37a7cea182dc4a6da4ea73353e741c5e'


# 保存AK/SK的类
class BceCredentials(object):
    def __init__(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key


# 根据RFC 3986，除了：
#   1.大小写英文字符
#   2.阿拉伯数字
#   3.点'.'、波浪线'~'、减号'-'以及下划线'_'
# 以外都要编码
RESERVED_CHAR_SET = set(string.ascii_letters + string.digits + '.~-_')


def get_normalized_char(i):
    char = chr(i)
    if char in RESERVED_CHAR_SET:
        return char
    else:
        return '%%%02X' % i


NORMALIZED_CHAR_LIST = [get_normalized_char(i) for i in range(256)]


# 正规化字符串
def normalize_string(in_str, encoding_slash=True):
    if in_str is None:
        return ''

    # 如果输入是unicode，则先使用UTF8编码之后再编码
    in_str = str(in_str).encode(DEFAULT_ENCODING)

    # 在生成规范URI时。不需要对斜杠'/'进行编码，其他情况下都需要
    if encoding_slash:
        encode_f = lambda c: NORMALIZED_CHAR_LIST[c]
    else:
        # 仅仅在生成规范URI时。不需要对斜杠'/'进行编码
        encode_f = lambda c: NORMALIZED_CHAR_LIST[c] if c != '/' else c

    # 按照RFC 3986进行编码
    return ''.join([encode_f(ch) for ch in in_str])


# 生成规范时间戳
def get_canonical_time(timestamp=0):
    # 不使用任何参数调用的时候返回当前时间
    if timestamp == 0:
        utctime = datetime.datetime.utcnow()
    else:
        utctime = datetime.datetime.utcfromtimestamp(timestamp)

    # 时间戳格式：[year]-[month]-[day]T[hour]:[minute]:[second]Z
    return "%04d-%02d-%02dT%02d:%02d:%02dZ" % (
        utctime.year, utctime.month, utctime.day,
        utctime.hour, utctime.minute, utctime.second)


# 生成规范URI
def get_canonical_uri(path):
    # 规范化URI的格式为：/{bucket}/{object}，并且要对除了斜杠"/"之外的所有字符编码
    return normalize_string(path, False)


# 生成规范query string
def get_canonical_querystring(params):
    if params is None:
        return ''

    # 除了authorization之外，所有的query string全部加入编码
    result = ['%s=%s' % (k, normalize_string(v)) for k, v in params.items() if k.lower != AUTHORIZATION]

    # 按字典序排序
    result.sort()

    # 使用&符号连接所有字符串并返回
    query_string = '&'.join(result)
    print("query_string:", query_string)
    return query_string


# 生成规范header
def get_canonical_headers(headers, headers_to_sign=None):
    headers = headers or {}

    # 没有指定header_to_sign的情况下，默认使用：
    #   1.host
    #   2.content-md5
    #   3.content-length
    #   4.content-type
    #   5.所有以x-bce-开头的header项
    # 生成规范header
    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {"host", "content-md5", "content-length", "content-type"}

    # 对于header中的key，去掉前后的空白之后需要转化为小写
    # 对于header中的value，转化为str之后去掉前后的空白
    f = lambda tuple_x: (tuple_x[0].strip().lower(), str(tuple_x[1]).strip())

    result = []
    for k, v in map(f, headers.items()):
        # 无论何种情况，以x-bce-开头的header项都需要被添加到规范header中
        if k.startswith(BCE_PREFIX) or k in headers_to_sign:
            result.append("%s:%s" % (normalize_string(k), normalize_string(v)))

    # 按照字典序排序
    result.sort()

    # 使用\n符号连接所有字符串并返回
    return '\n'.join(result)


# 签名主算法
def sign(credentials, http_method, path, headers, params,
         timestamp=0, expiration_in_seconds=1800, headers_to_sign=None):
    headers = headers or {}
    params = params or {}

    # 1.生成sign key
    # 1.1.生成auth-string，格式为：bce-auth-v1/{accessKeyId}/{timestamp}/{expirationPeriodInSeconds}
    sign_key_info = 'bce-auth-v1/%s/%s/%d' % (
        credentials.access_key_id,
        get_canonical_time(timestamp),
        expiration_in_seconds)
    # 1.2.使用auth-string加上SK，用SHA-256生成sign key
    sign_key = hmac.new(
        credentials.secret_access_key.encode("utf-8"),
        sign_key_info.encode("utf-8"),
        hashlib.sha256).hexdigest()

    # 2.生成规范化uri
    canonical_uri = get_canonical_uri(path)

    # 3.生成规范化query string
    canonical_querystring = get_canonical_querystring(params)

    # 4.生成规范化header
    canonical_headers = get_canonical_headers(headers, headers_to_sign)

    # 5.使用'\n'将HTTP METHOD和2、3、4中的结果连接起来，成为一个大字符串
    string_to_sign = '\n'.join(
        [http_method, canonical_uri, canonical_querystring, canonical_headers])

    # 6.使用5中生成的签名串和1中生成的sign key，用SHA-256算法生成签名结果
    sign_result = hmac.new(sign_key.encode(DEFAULT_ENCODING), string_to_sign.encode(DEFAULT_ENCODING),
                           hashlib.sha256).hexdigest()

    # 7.拼接最终签名结果串
    if headers_to_sign:
        # 指定header to sign
        result = '%s/%s/%s' % (sign_key_info, ';'.join(headers_to_sign), sign_result)
    else:
        # 不指定header to sign情况下的默认签名结果串
        result = '%s//%s' % (sign_key_info, sign_result)

    return result


def request_baidu(data, headers, authorization):
    import requests
    """
    POST /v1/lps/logistics/direction HTTP/1.1
    HOST: lps.baidubce.com
    Authorization: {authorization}
    Content-Type: application/json; charset=utf-8
    x-bce-date: 2016-06-08T16:49:51Z
    x-bce-request-id: 72492aee-1470-46d0-8a4d-0dab7b8e67
    """
    headers["authorization"] = authorization
    URL = "http://lps.baidubce.com/v1/lps/logistics/direction"
    r = request.POST(URL, params=data, headers=headers)
    print("URL response")
    print(r)
    print(r.content.decode("utf-8"))


def get_content_length(data):
    length = len(data.keys()) * 2 - 1
    total = ''.join(list(data.keys()) + list([ str(x) for x in data.values()]))
    length += len(total)
    print(length)
    return str(length)


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
if __name__ == "__main__":
    credentials = BceCredentials(ak_id, sk_id)
    http_method = "POST"
    path = "/v1/lps/logistics/direction"

    headers = {"host": "lps.baidubce.com",
               "content-length": "8", #get_content_length(DATA),
               "content-md5": "0a52730597fb4ffa01fc117d9e71e3a9",
               "content-type": "application/json",
               "x-bce-date": get_canonical_time()}
    params = DATA
    timestamp = 1563434599
    result = sign(credentials, http_method, path, headers, params)
    Authorization = result
    print(result)

    request_baidu(DATA, headers, Authorization)
