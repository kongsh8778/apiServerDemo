# apiServerDemo
基于flask-restful实现的api接口，包含注册、登录、新增博文、创建博文、删除博文和查询博文
		

用户博客管理接口说明文档

请求方式：

1、请求时，可不指定Content-Type，默认Content-Type为application/json，
即Content-Type: application/json
2、请求参数中涉及id的，不区分是否为字符串（带引号）
3、如果在一些接口请求插件（比如httprequester）中请求这些接口时，传参时，键值对间不能存在空格，并且字符串必须用双引号引起来，跟使用Python程序请求有区别。



响应码说明：

'00'：成功
'01'：用户已存在
'02'：参数值不合法，不符合约束条件，视具体接口而定
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误，程序问题，需要分析后台日志


一、登录模块
1、用户注册接口
接口格式
方法	URI	描述
POST	/register/	用户信息注册

请求参数
字段	类型	描述	参数规则
username	string	用户名	1、必填，字母、数字组成；
2、长度2~20位；
3、字母不区分大小写
password	string	密码	1、必填，长度8~20位
2、必须含有字母和数字
email	string	邮箱	必填，标准的email规则

返回参数
字段	类型	描述	参数规则
code	string	接口返回码	'00'：成功
'01'：用户已存在
'02'：参数值不合法，不符合约束条件
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误
userid	int	用户id	系统自动产生，默认为自增
message	string	接口返回消息	对应于返回码参数规则中的code说明

示例

请求示例
post	  http://39.106.41.11:8080/register/
{
    "username": "'lily'",
    "password": "'wcx123wac'",
    "email": " lily@qq.com "
}

响应示例
{
    "code": "00",
    "userid": 32,
    "message": "成功"
}



2、用户登录
接口格式
方法	URI	描述
POST	/login/	用户登录

请求参数
字段	类型	描述	参数规则
username	string	用户名	1、必填，需要注册过的用户，否则提示“参数值不合法，用户不存在” 
password	string	密码（md5加密）	1、必填，值为注册时密码的md5加密串，不匹配则提示“参数值不合法，密码不正确”

返回参数
字段	类型	描述	参数规则
token	string	登录令牌	32位字符，由字母和数字组成
code	string	接口返回码	'00'：成功
'02'：参数值不合法，用户不存在或密码不正确
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误 
userid	int	用户id	用户的id
login_time	string	登录时间	登录成功时的时间

示例

请求示例
post	  http://39.106.41.11:8080/login/
{
    "username": "wulaoshi1140",
    "password": "6b45c034135229c1f2eb54804cb404e1"
}

响应示例
{
    "token": "d10eb403c4a64a69802092f8604b8fe9",
    "code": "00",
    "userid": 1,
    "login_time": "2019-06-07 12:47:26"
}


二、博文编辑模块
1、新增博文
接口格式
方法	URI	描述
POST	/create/	新增博文

请求参数
字段	类型	描述	参数规则
userid	int	用户id	1、必填，需要是注册过的用户，否则提示“参数值不合法，用户不存在”
token	string	登录接口返回的token	1、必填，需要和用户登录时返回的token一致，否则提示"参数值不合法，token不正确"
2、有效期为1个小时，超时后会提示“参数值不合法，token已过期，请重新登录”
3、如果用户注册后尚未登录过，直接请求该接口，则提示“参数值不合法，token不正确，请登录并获取token”
title	text	博文标题	必填
content	text	博文内容	必填

返回参数
字段	类型	描述	参数规则
data	list	存博文内容和标题	list中元素为字典格式，存放博文内容和标题
----content	string	博文内容	请求参数中content的内容
----title	int	博文标题	请求参数中title的内容
code	string	响应码	'00'：成功 
'02'：参数值不合法，没登录并生成token、或token已过期、或token不正确、或用户不存在
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误
userid	int	用户id	请求参数中的userid
articleId	int	博文id	自动产生，默认为自增

示例

请求示例
post	  http://39.106.41.11:8080/create/
{
    "userid": "33",
    "token": "a07de7912b7a4ba1b1eefe9e8c6b4fd6",
    "title": "learn python",
    "content": "python is good"
}

响应示例
{
    "data": [
        {
            "content": "python is good",
            "title": "learn python"
        }
    ],
    "code": "00",
    "userid": "33",
    "articleId": 5
}




2、修改博文
接口格式
方法	URI	描述
PUT	/update/	修改博文

请求参数
字段	类型	描述	参数规则
userid	int	用户id	1、必填，需要是注册过的用户，否则提示“参数值不合法，用户不存在”
token	string	登录接口返回的token	1、必填，需要和用户登录时返回的token一致，否则提示"参数值不合法，token不正确"
2、有效期为1个小时，超时后会提示“参数值不合法，token已过期，请重新登录”
3、如果用户注册后尚未登录过，直接请求该接口，则提示“参数值不合法，token不正确，请登录并获取token”
articleId	int	博文id	必填，需要是已经存在的博文id，否则提示“参数值不合法，articleId不存在”
title	text	博文标题	必填
content	text	博文内容	必填

返回参数
字段	类型	描述	参数规则
articleId	string	博文id	请求参数中articleId的值
update_time	string	更新博文的时间	格式为%Y-%m-%d %H:%M:%S
code	string	响应码	'00'：成功
'02'：参数值不合法，articleId不存在、或没登录并生成token、或token已过期、或token不正确、或用户不存在
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误
userid	int	用户id	博文对应的userid

示例

请求示例
post	  http://39.106.41.11:8080/update/
{
    "userid": 33,
    "token": "a07de7912b7a4ba1b1eefe9e8c6b4fd6",
    "articleId": 7,
    "title": "update title",
    "content": "update test"
}

响应示例
{
    "articleId": 7,
    "update_time": "2019-06-08 12:04:15",
    "code": "00",
    "userid": 33
}


3、查询用户的博文
接口格式
方法	URI	描述
POST	/ getBlogsOfUser/	查询用户的博文

请求参数
字段	类型	描述	参数规则
userid	int	用户id	1、必填，需要是注册过的用户，否则提示“参数值不合法，用户不存在”
token	string	登录接口返回的token	1、必填，需要和用户登录时返回的token一致，否则提示"参数值不合法，token不正确"
2、有效期为1个小时，超时后会提示“参数值不合法，token已过期，请重新登录”
3、如果用户注册后尚未登录过，直接请求该接口，则提示“参数值不合法，token不正确，请登录并获取token”
offset	text	偏移量	1、非必填，offset与lines结合使用，表示跳过offset条取lines条数据，当不传offset或不传lines时，获取用户全部博文；
2、当用户博文数不够跳offset条时，返回空，表示都跳过了
lines	text	指定所取条数	1、非必填, offset与lines结合使用，表示跳过offset条取lines条数据，当不传offset或不传lines时，获取用户全部博文；
2、当跳过offset条后，博文数不够取lines条数据时，返回跳过offset条后所有的blog；

返回参数
字段	类型	描述	参数规则
data	list	存博文信息	list中元素为字典格式，存放博文信息
----update_time	string	更新博文的时间	博文的更新时间，没有则为null
格式为：%Y-%m-%d %H:%M:%S

----title	string	博文标题	博文标题
----content	string	博文内容	博文内容
----articleId	int	博文id	博文id
----owner	string	博文作者id	博文作者的userid
----posted_on	string	博文创建时间	
code	string	响应码	'00'：成功 
'02'：参数值不合法，没登录并生成token、或token已过期、或token不正确、或用户不存在
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
'999'：未知错误
userid	int	用户id	请求参数中的userid

示例

请求示例
post	  http://39.106.41.11:8080/getBlogsOfUser/
{
    "userid": 33,
    "token": "94bd60a989524873aa742bab73306a92",
    "offset": "3",
    "lines": "2"
}

响应示例
{
    "data": [
        {
            "update_time": null,
            "title": "mysql ",
            "content": "mysql learn",
            "articleId": 6,
            "owner": 33,
            "posted_on": "2019-06-08 11:26:47"
        },
        {
            "update_time": "2019-06-08 12:22:08",
            "title": "update title",
            "content": "update test",
            "articleId": 7,
            "owner": 33,
            "posted_on": "2019-06-08 11:28:42"
        }
    ],
    "code": "00",
    "userid": 33
}

4、查询博文内容
接口格式
方法	URI	描述
GET	/ getBlogContent/	查询博文内容

请求参数
字段	类型	描述	参数规则
articleId	int	博文id	1、必填，需要对应已经存在的博文，否则提示“参数值不合法，articleId不存在”

返回参数
字段	类型	描述	参数规则
code	string	响应码	'00'：成功
'02'：参数值不合法，articleId不存在
'999'：未知错误
data	list	存博文信息	list中元素为字典格式，存放博文信息
----update_time	string	更新博文的时间	博文的更新时间，没有则为null
----title	string	博文标题	博文标题
----content	string	博文内容	博文内容
----articleId	int	博文id	博文id
----owner	string	博文作者id	博文作者的userid
----posted_on	string	博文创建时间	格式为：%Y-%m-%d %H:%M:%S

示例

请求示例
get	  http://39.106.41.11:8080/getBlogContent/7

响应示例
{
    "code": "00",
    "data": [
        {
            "update_time": "2019-06-08 12:22:08",
            "title": "update title",
            "content": "update test",
            "articleId": "7",
            "owner": 33,
            "posted_on": "2019-06-08 11:28:42"
        }
    ]
}

5、批量查询博文
接口格式
方法	URI	描述
GET	/ getBlogsContent/	批量查询博文内容

请求参数
字段	类型	描述	参数规则
articleIds	string	博文id组成的字符串，以逗号隔开	1、必填，博文id组成的字符串，以逗号隔开，
需要是存在的博文id，否则提示“参数值不合法，不存在articleId: （id号）”
2、需要是数字，否则提示“参数值不合法，articleId: （参数值）不是数字”

返回参数
字段	类型	描述	参数规则
code	string	响应码	'00'：成功
'02'：参数值不合法，url中没携带'articleIds='参数、或url中'articleIds='后没有传值、或articleId不存在、或articleId不是数字
'999'：未知错误
data	list	存博文信息	list中元素为字典格式，存放博文信息
----update_time	string	更新博文的时间	博文的更新时间，没有则为null
----title	string	博文标题	博文标题
----content	string	博文内容	博文内容
----articleId	int	博文id	博文id
----owner	string	博文作者id	博文作者的userid
----posted_on	string	博文创建时间	格式为：%Y-%m-%d %H:%M:%S

示例

请求示例
get	  http://39.106.41.11:8080/getBlogsContent/articleIds=3,7

响应示例
{
    "code": "00",
    "data": [
        {
            "update_time": null,
            "title": "始发地",
            "content": "斯蒂芬",
            "articleId": 3,
            "owner": 33,
            "posted_on": "2019-06-08 11:10:03"
        },
        {
            "update_time": "2019-06-08 12:22:08",
            "title": "update title",
            "content": "update test",
            "articleId": 7,
            "owner": 33,
            "posted_on": "2019-06-08 11:28:42"
        }
    ]
}

6、删除博文
接口格式
方法	URI	描述
DELETE	/ delete/	删除博文

请求参数
字段	类型	描述	参数规则
userid	int	用户id	1、必填，需要是注册过的用户，否则提示“参数值不合法，用户不存在”
token	string	登录接口返回的token	1、必填，需要和用户登录时返回的token一致，否则提示"参数值不合法，token不正确"
2、有效期为1个小时，超时后会提示“参数值不合法，token已过期，请重新登录”
3、如果用户注册后尚未登录过，直接请求该接口，则提示“参数值不合法，token不正确，请登录并获取token”
articleId	int	博文id列表	1、必填，为列表形式，否则提示“参数值不合法，articleId传的不是列表”
2、需要是存在的博文id，否则提示“参数值不合法，articleId：（博文id）不存在”

返回参数
字段	类型	描述	参数规则
articleId	int	博文id	请求参数中传入的articleId
code	string	响应码	'00'：成功
'02'：参数值不合法，articleId不存在、或articleId传的不是列表、或没登录并生成token、或token已过期、或token不正确、或用户不存在
'03'：参数错误（可能原因：参数少传了、多传了、写错了、参数值为空）
 '999'：未知错误
userid	Int	用户id	请求参数中的userid

示例

请求示例
delete	  http://39.106.41.11:8080/delete/
{
    "userid": 33,
    "token": "a77e762ea66c480897a7d9c7c76dd242",
    "articleId": [
        9,
        10
    ]
}

响应示例
{
    "articleId": [
        9,
        10
    ],
    "code": "00",
    "userid": 33
}

遗留问题：
返回码为“00”、“02”时，返回的字典需要携带请求的参数，这个待添加，并更新文档
