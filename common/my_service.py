import json

import requests

from common import my_cipher

SERVER_URL = 'http://47.104.243.84:9999/gamecenter/api'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36',
    'Content-Type': 'application/json'
}


def post(username=None, password=None, path='', body=None, enc_key=my_cipher.DEFAULT_KEY):
    if password is not None:
        headers['Authorization'] = my_cipher.basic_auth(username, password)
    else:
        if 'Authorization' in headers:
            del headers['Authorization']
    url = SERVER_URL + path
    enc_body = my_cipher.aes_encrypt(enc_key, json.dumps(body['data']))
    print(f'原始请求：{body}')
    body['encData'] = enc_body
    body['data'] = None
    print(f'处理后请求：{body}')
    print(f'headers：{headers}')
    try:
        res = requests.post(url, headers=headers, data=json.dumps(body))
        if res.status_code == 401 or res.status_code == 403:
            print(f'响应码：{res.status_code}')
            return {
                'code': -1,
                'message': '操作失败，您当前没有权限进行此操作！'
            }
        elif res.status_code > 499:
            print(f'响应码：{res.status_code}')
            return {
                'code': -1,
                'message': '服务暂时不可用，请稍后再试！'
            }
        res_json = res.json()
        print(f'解密前响应：{res_json}')
        res_enc_data = res_json['encData']
        if res_enc_data is not None:
            res_dec_data = my_cipher.aes_decrypt(enc_key, res_enc_data)
            res_json['data'] = json.loads(res_dec_data)
    except requests.exceptions.ConnectionError:
        res_json = {'code': -2, 'message': '连接失败，请稍后再试'}

    res_json['encData'] = None
    res_json['sign'] = None
    print(f'解密后响应：{res_json}')
    return res_json


def login(username, password, game, ver=None):
    path = '/account/login'
    req = {
        'game': game,
        'username': username,
        'data': {
            'password': password,
            'ver': ver
        }
    }
    return post(username, path=path, body=req)


def register(username, password, nickname=None, game=None):
    path = '/account/register'
    req = {
        'game': game,
        'username': username,
        'data': {
            'password': password,
            'nickname': nickname
        }
    }
    return post(username, path=path, body=req)


def activate(username, code, game=None, enc_key=None):
    path = '/cdk/activate'
    req = {
        'game': game,
        'username': username,
        'data': {
            'code': code,
        }
    }
    return post(username, path=path, body=req, enc_key=enc_key)


def checkVersion(username, password, inuseVersion, game=None, enc_key=None):
    path = '/version/check'
    req = {
        'game': game,
        'username': username,
        'data': {
            'inuseVersion': inuseVersion,
        }
    }
    return post(username, password, path=path, body=req, enc_key=enc_key)


def modifyPwd(username, oldpwd, newpwd, game=None, enc_key=None):
    path = '/account/password/modify'
    req = {
        'game': game,
        'username': username,
        'data': {
            'oldPassword': oldpwd,
            'newPassword': newpwd
        }
    }
    return post(username, oldpwd, path=path, body=req, enc_key=enc_key)


def checkRedeem(username, password, game=None, enc_key=None):
    path = '/redeem/check'
    req = {
        'game': game,
        'username': username,
        'data': {
            'type': 'WEEKLY',
        }
    }
    return post(username, password, path=path, body=req, enc_key=enc_key)
