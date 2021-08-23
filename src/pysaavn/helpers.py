"""Helpers"""

import re
import pyDes
import base64


encryption = pyDes.des(b"38346591", pyDes.ECB, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)


def extract_token(perma_url):
    token = re.match("https://www.jiosaavn.com/.*/(.*)", perma_url).group(1)
    return token

def decrypt_media_url(enc_url):
    enc_url = base64.b64decode(enc_url)
    dec_url = encryption.decrypt(enc_url, padmode=pyDes.PAD_PKCS5).decode("utf-8")
    return dec_url

if __name__ == "__main__":
    pass