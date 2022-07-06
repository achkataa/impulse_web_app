from base64 import urlsafe_b64encode


def base64UrlEncode(data):
    data_bytes = data.encode('ascii')
    return urlsafe_b64encode(data_bytes)