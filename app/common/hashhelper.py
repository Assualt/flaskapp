import datetime
import hashlib
import base64
import time
import hmac
from http import cookies

def hash_md5(data, encoding='utf8') -> str:
    try:
        return hashlib.md5(data.encode(encoding)).hexdigest()
    except Exception as exp:
        raise ValueError("Calc Md5 Error. ErrMsg:{exp}".format(exp=exp))

def hash_sha1(data, encoding='utf8') -> str:
    try:
        return hashlib.sha1(data.encode(encoding)).hexdigest()
    except Exception as e:
        raise ValueError("Calc sha1 Error. ErrMsg:{exp}".format(exp=e))

def base64decode(data) -> str:
    if not len(data):
        return ""
    try:
        return base64.b64decode(data).decode()
    except Exception as exp:
        raise ValueError("decoded base64 error. err msg:{exp}".format(exp=exp))

def base64encode(data, encoding='utf-8') -> str:
    if not len(data):
        return ""
    try:
        return base64.b64encode(bytes(data, encoding=encoding)).decode()
    except Exception as exp:
        raise ValueError("encoded base64 error. err msg:{exp}".format(exp=exp))

class Token(object):
    @staticmethod
    def generate_token(key: str, account: str, expire_time: int = 3600 * 24 * 7):
        t_str = str(time.time() + expire_time)
        t_byte = t_str.encode('utf-8')
        t_sha1_str = hmac.new(key.encode(), t_byte, 'sha1').hexdigest()
        s_token = t_str + ':' + t_sha1_str + ':' + account
        b64_token = base64.urlsafe_b64encode(s_token.encode('utf-8'))
        return b64_token.decode('utf-8')

    @staticmethod
    def certify_token(key, account, token) -> str:
        try:
            token_str = base64.urlsafe_b64decode(token).decode('utf-8')
            token_list = token_str.split(':')
            if len(token_list) != 3:
                return "the token length must be 3"
            ts_str = token_list[0]
            if float(ts_str) < time.time():
                return "the token has been expired"
            known_sha1_str = token_list[1]
            known_account = token_list[2]
            if known_account != account:
                return "the token doesn't belong to {u} user".format(u=account)
            sha1_str = hmac.new(key.encode('utf-8'), ts_str.encode('utf-8'), 'sha1')
            calc_str = sha1_str.hexdigest()
            if calc_str != known_sha1_str:
                return "the token decode error."
            return ""
        except ...:
            return "certify_token failed"

    @staticmethod
    def generator_cookie_str(security_token, expire_days=30) -> str:
        expiration = datetime.datetime.now() + datetime.timedelta(days=expire_days)
        cookie = cookies.SimpleCookie()
        cookie['session'] = hash_md5(security_token)
        cookie['session']['domain'] = '.tsz.com'
        cookie['session']['path'] = '/'
        cookie['session']['expires'] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        return cookie.output() + ',' + security_token


if __name__ == '__main__':
    try:
        print(base64encode("123@.com"))
        print(base64decode(base64encode("123@.com")))
        s_token = Token.generate_token("tszid", 'admin@p.cn')
        print(s_token)
        print(Token.certify_token('tszid', 'admin@p.cn', s_token))
        print(Token.generator_cookie_str(s_token))
        print(hash_sha1('4bfcd234749aafcc4a5845c66667055e'))
        print(Token.certify_token('tsz', 'admin@p.cn',
                                  'MTU3Njc2NzczMC4wNjUxNzA4OjgxYmU3ZDdiYzM0MzhhZDY0MDM0Y2RkMDNjNTQxNDIyZjRmZmMwOTc6YWRtaW5AcC5jbg=='))
        print(hash_md5(
            'MTU3Njc2NzczMC4wNjUxNzA4OjgxYmU3ZDdiYzM0MzhhZDY0MDM0Y2RkMDNjNTQxNDIyZjRmZmMwOTc6YWRtaW5AcC5jbg=='))
    except Exception as e:
        print("e", e)
