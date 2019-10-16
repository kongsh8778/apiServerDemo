#encoding=utf-8
import os

project_path=os.path.dirname(os.path.dirname(__file__))
# 添加mysql数据地址mysql://用户名:密码@ip:端口/库名称

dbuser = 'root'
dbpassword = '123456'
dbhost = '127.0.0.1'
dbport = '3306'
dbname = 'api16'
dbUrl = 'mysql+pymysql://' + '%s:%s@%s:%s/%s' % (dbuser, dbpassword, dbhost, dbport, dbname)

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
# 从环境变量里取，如果没有，则用DBInitialize里的dbUrl
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dbUrl)


if __name__ == '__main__':
    print(__file__)
    print(project_path)

