import requests
import re
import os
import random
import sys
from bs4 import BeautifulSoup
import redis
import mysql.connector


class redis_():
    def __init__(self, host=None, pw=None, db=0):
        self.host = host
        self.pw = pw
        self.db = db
        self.redis_connection = self.redis_con()
        print("redis连接成功")
        # output.write("初始化函数")

    def __new__(cls, *args, **kwargs):
        _instance = ''
        print("这个会先被调用么")
        instance = object.__new__(cls, *args, **kwargs)
        cls.instance = super()
        return instance

    def set_(self, key, value):

        self.redis_connection.set(key, value)

    def redis_con(self):
        redis_connection = redis.Redis(host=self.host, db=self.db)
        return redis_connection

    def get_(self, key=None):
        if key == None:
            key = input('please input your keyword:\n')
        self.redis_connection[key]
"""
urls变量为一个字典，集合要爬取的网页的首页地址
"""
urls = {
    "zdm": "https://www.smzdm.com/",
    "baidu": "https://www.baidu.com/",
    "douban": "https://www.baidu.com/",
    "anjuke": "https://www.anjuke.com/",
    "xhip": "https://ip.ihuan.me/",
    "xlip": "http://www.xiladaili.com/",
    "kip": "https://www.kuaidaili.com/free/",
    # 获取本地IP地址的url
    "getip":"http://icanhazip.com/",
}
output = sys.stdout
ipss = {'http':[],'https':[]}
red = redis_()
red = red.redis_connection


class sql_mysql():
    def __init__(self, filepath=None):
        self.count = 0
        self.filepath = filepath
        self.user, self.password = self.getMysqlinfo(self.filepath)
        self.host = 'localhost'
        self.database = ''
        output.write('初始化sql_mysql成功！')

    # 获取MySQL用户名和密码
    def getMysqlinfo(self, filepath):
        self.count += 1
        print("第{}次调用getmysqlinfo函数".format(self.count))
        if self.filepath == None:
            # output.write("请输入sql信息文件路径:\n")
            self.filepath = input("请输入sql信息文件路径:\n")
        inf = []
        with open(self.filepath, 'r', encoding='utf-8') as fr:
            info = fr.read()
            ig = info.split(';')
            for i in ig:
                if len(i) > 0:
                    # print("i.split(':')"+str(i.split(':')))
                    inf.append(i.split(':')[1])
        print("inf***"+str(inf))
        print("已获得信息")
        return inf[0], inf[1]

    # 连接数据库，返回MySQL连接器和cursor
    def mysqlConnect(self, user, password, host='localhost', database=''):
        con = mysql.connector.connect(
            user=user, password=password, host=host, database=database)
        cur = con.cursor()
        if cur.execute('show databases;'):
            print('连接成功!')
        return con, cur
        # return 1,2

    def mysqlOperation(self, cur, statement):
        try:
            r1 = cur.fetchall()
            print(r1)
        except BaseException as e:
            print('以下是错误信息')
            print(e)
            print('以上是错误信息')
        cur.execute(statement)
        try:
            ru = cur.fetchall()
            print('rururururur')
            print(ru)
        except BaseException as e:
            print('以下是错误信息')
            print(e)
            print('以上是错误信息')

    def mysqlClose(self, con, cur):
        self.cur.close()
        self.con.close()


class htmlInfo():
    def __new__(cls,*args, **kwargs):
        instance_ = None
        if instance_ == None:
            instance_ = super().__new__(cls,*args,**kwargs)
        return instance_

    def __init__(self):
        self.pg_ = 0 
        pass

    def getHeaders(self):
        headers = []
        with open('f:/迅雷下载/userAgent.txt', 'r+', encoding='utf-8') as hs:
            h = hs.readlines()    # h: type:list;len:38
            s = ''
            for i in h:  # i  type:str;
                i = i.replace('\n', '')
                s += i
            s.encode('utf-8')
            # print(s)
            rs = re.findall(r'"(.+?)"', s)
            # print(len(rs))
            for i in rs:
                headers.append(i)
            return headers


    def getIP(self, ippath):
        pass

    def getHTML(self,url, proxies=None, headers=None,pagenum=0):
        # proxies = getIP()
        # headers = {'user-agent':getHeaders()}
        print(headers)

        html = requests.get(url, headers=headers, proxies=proxies)
        html.encoding = 'utf-8'
        self.savePage(pagenum=pagenum,html=html)
        self.parseHTML(html)
        self.getPageNum(url=url,html=html)


        # return self.htext

    def savePage(self,html,pagenum=None):
        # self.pagenum = self.getPageNum()

        filepath = "f:/迅雷下载/ip" + str(pagenum) + ".html"
        with open(filepath, 'w+', encoding='utf-8') as fi:
            fi.write(html.text)

    def parseHTML(self,html):
    # 本正则匹配只针对小幻ip网站网页
        ress = {
            'ip':'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',
            'port':">(\d{1,5})<",
            'https_post':'>支持',
        }
        html = html.text

        tr = re.compile('<tr>(.*?)</tr>', re.S)
        td = re.compile('<td>(.+?)</td>')
        trs = tr.findall(html)  #trs list,
        # print(len(trs))
        for i in trs:
            ishttps = ''
            ip_ = ''
            port = ''
            ispost = ''
            tds = td.findall(i)

            for i in range(len(tds)):
                ip = re.findall(ress['ip'],tds[i])
                if len(ip) != 0 and i==0:
                	ip_ = ip[0]
                if i == 1:
                	port = tds[i]
                if i == 4:
                	ishttps = tds[i]
                if i == 5:
                        ispost = tds[i]
            # print((ishttps,ip_,port,ispost))
            if not "不" in ishttps and bool(ip_)==True:
                ishttps = 'http'
                ipss['http'].append((ishttps,ip_,port,ispost))
                ipn = str(ishttps)+ "://" + str(ip_) + ":" + str(port)
                red.sadd('http',ipn)
            elif bool(ip_)==True:
                ishttps = 'https'
                ipss['https'].append((ishttps,ip_,port,ispost))
                ipn = str(ishttps)+ "://" + str(ip_) + ":" + str(port)
                red.sadd('https',ipn)
        print(ipss)

        
        
        return ipss

    def getPageNum(self,url,html):
        print(self)
        pagenum = 0
        htext = html.text
        ul = re.findall('\?page=(.+)',url)
        if len(ul) != 0 :
            nu = re.findall('\?page={}".*?>(.*?)<'.format(ul[0]),htext)
            if len(nu) > 0 and nu[0]:
                print(nu[0])
                print(nu)
                pagenum = int(nu[0]) + 1
                print(pagenum)
        nul = re.findall('\?page=([\d\w]+)"*.*?>{}<'.format(pagenum),htext)
        if len(nul) > 0:
            nul = nul[0]
            print(nul)
            url = "https://ip.ihuan.me/?page={}".format(nul)
            if pagenum <10:
                self.getHTML(url=url,pagenum=pagenum)
        # re.findall()
        # return self.pagenum

    def getNext(self):
        print('getNext')

    def saveIP(filepath):
        pass




def main():
    url = urls['xhip']
    url = "https://ip.ihuan.me/?page=ce1d45977"
    hf = htmlInfo()
    html = hf.getHTML(url)


if __name__ == '__main__':
    main()
