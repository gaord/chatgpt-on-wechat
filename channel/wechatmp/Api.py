import web
from common.log import logger
from channel.wechatmp.common import *
from config import conf
import json


class Api:
    def GET(self, subPath):
        logger.info("GET: %s" % subPath)
        if subPath == "aiRoles":
            logger.info("aiRoles: %s" % conf().get_airoles())
            return json.dumps(conf().get_airoles())
        elif subPath == "userRoles":
            data = web.input()
            aiId = data.get("aiRole")
            logger.info("userRoles: %s" % conf().get_userroles_by_aiid(aiId))
            return json.dumps(conf().get_userroles_by_aiid(aiId))
        elif subPath == "roles":
            data = web.input()
            user = data.get("userId")
            user_data = conf().get_user_data(user)
            logger.info("user_data: %s: %s" % (user, user_data))
            return json.dumps({"aiRole": user_data.get("aiRole", ""), \
                              "userRole": user_data.get("userRole", "")})
        else:
            return "unhandled GET request"

    def POST(self, subPath):
        logger.info("POST: %s" % subPath)
        if subPath == "roles":
            data = web.data()
            print(data)
            roleData = json.loads(data)
            user_data = conf().get_user_data(roleData["userId"])
            logger.info("old user_data: %s" % user_data)
            user_data["aiRole"] = roleData["aiRole"]
            user_data["gpt_model"] = roleData["aiRole"]
            user_data["userRole"] = roleData["userRole"]
            logger.info("new user_data: %s" % user_data)
            return "success"
        elif subPath == "userId":
            data = web.data()
            print(data)
            code = json.loads(data)["code"]
            access_token, openid = get_access_token_and_openid( \
                conf().get("wechatmp_app_id"), conf().get("wechatmp_app_secret"), code)
            logger.info("access_token: %s, openid: %s" % (access_token, openid))
            return openid
        else:
            return "unhandled POST request"
