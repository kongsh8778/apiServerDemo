#encoding=utf-8

from gloryRoadApi.application import db
from gloryRoadApi.models import User
from flask_restful import reqparse
from flask import request
from flask_restful import Resource
from gloryRoadApi.common import util
from gloryRoadApi.common.log import logger



# Register接口
class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, help='用户名验证错误',location = 'json')
        # location = 'json'表示请求的参数是json格式的
        self.reqparse.add_argument('password', type=str, help='密码验证错误',location = 'json')
        self.reqparse.add_argument('email', type= str, help='邮箱错误',location = 'json')
        # 取到接口需要用到的参数信息
        self.args = self.reqparse.parse_args()

    # 处理post请求及参数验证
    def post(self):
        try:
            logger.info("########################[Register]########################")
            logger.info("self.args.keys(): %s" % self.args.keys())
            json_data = request.get_json(force = True)
            logger.info("json_data: %s" % json_data)
            userName = json_data['username'] if ('username' in json_data.keys()) else ""
            #userName = self.args['username']
            logger.info("username: %s" % userName)
            #userPassword = sel.args['password']
            userPassword = json_data['password'] if ('password' in json_data.keys()) else ""
            logger.info("userPassword: %s" % userPassword)
            email = json_data['email'] if ('email' in json_data.keys()) else ""
            #email = self.args['email']
            logger.info("email: %s" % email)
            neededParams = self.args.keys()
            logger.info("neededParams: %s" % neededParams)
            logger.info("#####request: %s " % request)
            logger.info("#####request.json: %s " % request.json)
            logger.info("#####dir(request): %s " % dir(request))
            logger.info("#####request.host: %s " % request.host)
            logger.info("#####request.headers: %s " % request.headers)
            logger.info("#####request.endpoint: %s " % request.endpoint)
            logger.info("#####request.data: %s " % request.data)
            logger.info("#####request.content_type: %s " % request.content_type)
            logger.info("#####request.form: %s " % request.form)
            requestParams = request.json.keys()
            logger.info("requestParams: %s" % requestParams)

            # 判断参数是否都有传过来，是否多了，是否错了
            if userName and userPassword and email and util.paramsNumResult(neededParams, requestParams):
            #if userName and userPassword and email:
                userNameResult = util.validateUsername(userName)
                emailResult = util.validateEmail(email)
                passwordResult = util.validatePassword(userPassword)

                #校验各个参数值是否合法
                if userNameResult and emailResult and passwordResult:
                    if not User.query.filter(User.username == userName).all():  # 查询数据库里是否存在该username
                        userNew = User(username=userName, password=userPassword, email=email)
                        db.session.add(userNew)
                        db.session.commit()
                        return {"code": "00", "userid": userNew.id, "message": u"成功"}
                    else:
                        # 数据库里有重名的
                        return {"code": "01", "message": u"参数值不合法，用户名已存在"}
                else:
                    return {"code": "02", "message": u"参数值不合法，不符合约束条件"}
            else:
                return {"code": "03","message": u"参数错误，可能原因：参数少传了、多传了、写错了、参数值为空"}

        except Exception as e:
            logger.error("error of register: %s" % e)
            return {"code": "999","message": u"未知错误"}