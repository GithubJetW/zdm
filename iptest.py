import re, os, re, requests


def fileParse(file:str):
	# print(file)
	proxies = {
		'http':[],
		'https':[]
	}
	f1 = re.findall(r'\'.+?\'',file)
	s = f1[1].split(',')[0]
	if s[1:5].lower() != "http":
		print('it is not rghit!')
	for i in f1:
		i1 = i.split(',')[0]
		if i1[1:6].lower() == "https":
			proxies["https"].append(i1.replace("\'",'').lower())
		elif i1[1:6].lower() == "http:":
			proxies["http"].append(i1.replace("\'",'').lower())
	return proxies

def openFile(filepath,encoding='utf-8'):
	with open(filepath,'r+', encoding=encoding) as r:
		rn = r.readlines()
		rn = str(rn)
		proxies = fileParse(rn)
		print(proxies['http'])

def getIp():
	
	pass

def main():
	filepath = 'f:/迅雷下载/tao.json'
	openFile(filepath)

if __name__ == "__main__":
	main()