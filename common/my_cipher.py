import base64

from Crypto.Cipher import AES

"""
AES/ECB/PKCS5Padding
"""

CHARSET_UTF8 = 'utf-8'
DEFAULT_KEY = "@lindenthink.com"


def aes_encrypt(key, text):
    aes = AES.new(key.encode(), AES.MODE_ECB)
    enc_bytes = aes.encrypt(pkcs5_pad(text.encode(CHARSET_UTF8)))
    base64_encrypted = base64.encodebytes(enc_bytes)
    return base64_encrypted.decode().replace('\n', '')


def aes_decrypt(key, enc_text):
    aes = AES.new(key.encode(), AES.MODE_ECB)
    base64_decrypted = base64.decodebytes(enc_text.encode())
    dec_bytes = aes.decrypt(base64_decrypted)
    return strip_pkcs5_pad(dec_bytes).decode(CHARSET_UTF8)


def pkcs5_pad(data):
    needSize = 16 - len(data) % 16
    if needSize == 0:
        needSize = 16
    return data + needSize.to_bytes(1, 'little') * needSize


def strip_pkcs5_pad(data):
    paddingSize = data[-1]
    return data.rstrip(paddingSize.to_bytes(1, 'little'))


def basic_auth(username, password):
    link_str = f'{username}:{password}'
    base64_encrypted = base64.encodebytes(link_str.encode())
    auth_str = f'Basic {base64_encrypted.decode()}'.replace('\n', '')
    return auth_str


def base64_enc(text):
    base64_encrypted = base64.encodebytes(text.encode())
    return base64_encrypted.decode()
