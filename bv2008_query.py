import rsa
import json
import time
import base64
import getpass
import requests
from bs4 import BeautifulSoup

DEBUG = False

def getInfo():
	request = requests.get('https://www.bv2008.cn/app/user/login.php')
	cookies = requests.utils.dict_from_cookiejar(request.cookies)
	soup = BeautifulSoup(request.text, 'html.parser')
	csrfToken = soup.find(name = 'meta', attrs = {'name': 'csrf-token'}, recursive = True)['content']
	seid = soup.find(name = 'input', attrs = {'id': 'seid'}, recursive = True)['value']
	request = requests.get('https://css.zhiyuanyun.com/common/login.js')
	pubkey = ''
	for i in filter(lambda x : 'pubkey' in x and '\'' in x, request.text.split('\n')):
		pubkey += i.split('\'')[1] + '\n'
	request = requests.post(url = 'https://www.bv2008.cn/app/api/view.php?m=get_login_yzm', headers = {
		'Host': 'www.bv2008.cn',
		'User-Agent': 'MicroMessenger'
	})
	soup = BeautifulSoup(request.text, 'html.parser')
	code = soup.find(name = 'p', attrs = {'style': 'font-size:28px;font-weight:bold;letter-spacing:5px;'}
		, recursive = True).string
	if DEBUG:
		print('csrf-token:\n' + csrfToken + '\n')
		print('seid:\n' + seid + '\n')
		print('code:\n' + code + '\n')
		print('pubkey:\n' + pubkey)
	return cookies, csrfToken, seid, code, pubkey

def login(cookies, csrfToken, data):
	request = requests.post(url = 'https://www.bv2008.cn/app/user/login.php?m=login', headers = {
		'X-CSRF-TOKEN': csrfToken
	}, data = data, cookies = cookies)
	if DEBUG:
		print(request.text)
	cookies = requests.utils.dict_from_cookiejar(request.cookies)
	request = requests.get('https://www.bv2008.cn/app/user/hour.php', cookies = cookies)
	return request.text

def analyse(data):
	result = []
	if DEBUG:
		print('\n-------------------------------------------------\n')
	soup = BeautifulSoup(data, 'html.parser')
	table = soup.find(name = 'table', attrs = {'class': 'table1'}, recursive = True)
	lst = ['time', 'text', 'valid', 'from', 'project', 'group', 'date']
	for i in table.contents[2:]:
		cnt = 0
		info = {}
		if type(i) == type(table):
			for j in i.contents:
				if type(j) == type(table):
					for k in j.contents:
						if type(k) == type(table):
							if k.string != None:
								info[lst[cnt]] = k.string
								cnt += 1
						else:
							info[lst[len(lst) - 1]] = time.strptime(str(k), '%Y-%m-%d %X')
			result.append(info)
	sumAll = 0
	for i in result:
		i['date'] = time.strftime('%Y-%m-%d %X', i['date'])
		i['text'] = i['text'].split('【')[1].split('】')[0]
		i['time'] = float(i['time'].split('小时')[0])
		i['valid'] = i['valid'] == '已生效'
		if i['valid']:
			sumAll += i['time']
	final = {}
	final['sum'] = sumAll
	final['result'] = result
	return final

if __name__ == '__main__':
	cookies, csrfToken, seid, code, pubkey = getInfo()
	query = input('verification code detected : ' + code + ', continue query? [Y/n] ')
	if query.lower() == 'y':
		try:
			with open('bv2008_config.txt', 'r') as file:
				print('config file detected, username and password will be obtained here')
				username, password = file.read().split()
		except:
			username = input('please input your username: ')
			password = getpass.getpass('please input your password: ')
		# ---------------------------------------------------------------------
		print('\n--------------------------------------------\n')
		print('getting data from bv2008.cn', end = ' ')
		for i in range(4):
			time.sleep(0.7)
			print('.', end = '')
		print('\n')
		realkey = rsa.PublicKey.load_pkcs1_openssl_pem(pubkey.encode('utf-8'))
		upass = base64.b64encode(rsa.encrypt(password.encode('gbk'), realkey))
		# ---------------------------------------------------------------------
		try:
			data = login(cookies, csrfToken, {
				'seid': seid,
				'uname': username,
				'upass': upass.decode('utf-8'),
				'referer': 'https://www.bv2008.cn/',
				'uyzm': code
			})
			result = analyse(data)
			print(json.dumps(result, indent = 4, ensure_ascii = False))
		except:
			print('^^^ sorry, query failed ^^^')
			print('please ensure network connectivity and check your username, password')
		print()
