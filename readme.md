# 志愿北京爬虫脚本

基于`Python + requests`爬虫

支持获取志愿北京验证码，查询个人志愿时长及志愿项目信息

## 环境要求
- 需要安装`python3`
- 需要安装包`rsa, bs4, requests`

## 获取当前验证码
- 在终端启动`bv2008_query.py`
	```
	python bv2008_query.py
	```
- 得到当前验证码后输入`n`取消继续查询时长
	```
	verification code detected : 114514, continue query? [Y/n] n
	```

## 查询时长，在终端输入账号和密码
- 在终端启动`bv2008_query.py`
	```
	python bv2008_query.py
	```
- 得到当前验证码后输入`y`继续查询时长
	```
	verification code detected : 114514, continue query? [Y/n] y
	```
- 在终端中输入你的用户名和密码，为保证密码安全，输入过程中密码**不可见**，如输入出错可多次退格后重新输入：
	```
	please input your username: Y.J.Aickson
	please input your password:
	```
- 查询完成，结果形式如下
	```
	verification code detected : 114514, continue query? [Y/n] y
	please input your username: Y.J.Aickson
	please input your password:

	--------------------------------------------

	getting data from bv2008.cn ....

	{
		"sum": 114514.0,
		"result": [
			{
				"time": 114514.0,
				"text": "xxxxxx",
				"valid": true,
				"from": "xxxxxx",
				"project": "xxxxxx",
				"group": "xxxxxx",
				"date": "xxxxxx"
			}
		]
	}
	```

## 查询时长，从文件读取账号和密码
- 在终端启动`bv2008_query.py`
	```
	python bv2008_query.py
	```
- 得到当前验证码后输入`y`继续查询时长
	```
	verification code detected : 114514, continue query? [Y/n] y
	```
- 在同一目录下创建`bv2008_config.txt`，若用户名为`Y.J.Aickson`密码为`114514`，`bv2008_config.txt`的内容如下
	```
	Y.J.Aickson
	114514
	```
- 查询完成，结果形式如下
	```
	verification code detected : 114514, continue query? [Y/n] y
	config file detected, username and password will be obtained here

	--------------------------------------------

	getting data from bv2008.cn ....

	{
		"sum": 114514.0,
		"result": [
			{
				"time": 114514.0,
				"text": "xxxxxx",
				"valid": true,
				"from": "xxxxxx",
				"project": "xxxxxx",
				"group": "xxxxxx",
				"date": "xxxxxx"
			}
		]
	}
	```