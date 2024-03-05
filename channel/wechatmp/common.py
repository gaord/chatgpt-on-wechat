import web
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
import requests
from config import conf

MAX_UTF8_LEN = 2048


class WeChatAPIException(Exception):
    pass


def verify_server(data):
    try:
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.get("echostr", None)
        token = conf().get("wechatmp_token")  # 请按照公众平台官网\基本配置中信息填写
        check_signature(token, signature, timestamp, nonce)
        return echostr
    except InvalidSignatureException:
        raise web.Forbidden("Invalid signature")
    except Exception as e:
        raise web.Forbidden(str(e))


def get_access_token_and_openid(appid, secret, code):
    """
    使用code换取access_token和openid
    :param appid: 微信公众号的AppID
    :param secret: 微信公众号的AppSecret
    :param code: 重定向URI上获取到的code参数
    :return: access_token和openid
    """
    url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {"appid": appid, "secret": secret, "code": code, "grant_type": "authorization_code"}
    response = requests.get(url, params=params)
    data = response.json()
    if "access_token" in data and "openid" in data:
        return data["access_token"], data["openid"]
    else:
        raise Exception("Failed to get access_token and openid", data)
