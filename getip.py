import mysql.connector as db
import random, requests, sys

output = sys.stdout
output.write('connect to mysql server\n')
user = "请输入MySQL目标数据库用户名:\n"
password = "请输入MySQL目标数据库用户名{}对应的密码:\n".format(user)
db = db.connect(user=user, passwd=password, db='ip')
output.write('to get the mysql cursor\n')
cur = db.cursor()

https_sql = 'select * from https;'
http_sql = 'select * from http;'
cur.execute(https_sql)
https = cur.fetchall()
cur.execute(http_sql)
http = cur.fetchall()
proxies = {
	'https':random.choice(https)[1],
	'http':random.choice(http)[1]
}
# print(proxies)

# res = requests.get('https://www.baidu.com/', proxies=proxies, timeout=2)
# print(res.status_code)
valideip = {
	'http':set(),
	'https':set()
}
def g(ips,tag,url):
	# if tag = "https"
	sql = 'drop table if exists val{}'.format(tag)
	cur.execute(sql)
	sql = 'create table val{} (id int(11) auto_increment primary key,ip char(88) not null)'.format(tag)
	cur.execute(sql)
	url = url[tag]
	for i in range(len(ips)):
		proxie = {
			tag:ips[i][1]
		}
		try:
			res = requests.get(url,proxies=proxie, timeout=2)
			print(res.status_code)
			print(ips[i])
			print(ips[i][1])
			valideip[tag].add(ips[i][1])
			sql = 'insert into val{} (ip) values ("{}")'.format(tag,ips[i][1])
			print(sql)
			cur.execute(sql)
			db.commit()
			output.write("\r{:<4.2f}% completed".format(i/len(ips)*100))
			# break
		except BaseException as e:
			output.write("\r{:<4.2f}% completed but something is wrong!".format(i/len(ips)*100))
	return valideip
url = {
	"http":"http://www.baidu.com/",
	"https":"https://www.baidu.com/"
}

def getvalip():
	http1 = []
	https1 = []
	url = 'https://www.smzdm.com/'
	http = 'select * from valhttp;'
	output.write('start get http ip...\n')
	cur.execute(http)
	http = cur.fetchall()
	output.write('http ip got successfully\n\n')
	https = 'select * from valhttps;'
	output.write('start get http ip...\n')
	cur.execute(https)
	https = cur.fetchall()
	output.write('http ip got successfully\n')
	output.write('start get all http ip...\n')
	for i in http:
		http1.append(i[1])
	output.write('end get all http ip...\n\n')
	output.write('start get all https ip...\n')
	for i in https:
		https1.append(i[1])
	output.write('end get all https ip...\n')
	proxies = {
		'http':random.choice(http1),
		'https':random.choice(https1)
	}
	output.write('start get html of the url {}'.format(url))
	res = requests.get(url,proxies=proxies, timeout=2)
	output.write('got the html')
	print(res.status_code)


getvalip()
# va = g(https,'https',url)
# print(va)

# vah = g(http,'http',url)
# print(vah)
