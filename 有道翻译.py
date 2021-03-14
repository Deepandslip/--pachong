import time 
import math
import random
import hashlib
import requests
"""
		var t = n.md5(navigator.appVersion)
		  , r = "" + (new Date).getTime()
		  , i = r + parseInt(10 * Math.random(), 10);
		return {
			ts: r,
			bv: t,
			salt: i,
			sign: n.md5("fanyideskweb" + e + i + "Nw(nmmbP%A-r6U3EUn]Aj")
"""
# 1586414252304
# 1586414773994



def getTran():
	data={
	'i': keyword,
	'from': 'AUTO',
	'to': 'AUTO',
	'smartresult': 'dict',
	'client': 'fanyideskweb',
	'salt': salt,
	'sign': sign,
	'ts': ts,
	'bv': bv,
	'doctype': 'json',
	'version': '2.1',
	'keyfrom': 'fanyi.web',
	'action':' FY_BY_CLICKBUTTION'
	}
	url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
	headers={
		
		'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=1145050017.7216291; OUTFOX_SEARCH_USER_ID="-885817080@10.169.0.82"; UM_distinctid=170bf0b58c75b3-0a8bdaf8fa3364-4313f6a-13c680-170bf0b58c8698; P_INFO=deepll123; _ntes_nnid=6a654fe584638c644fcb8afb1983c5a5,1585562407152; JSESSIONID=aaa2fElW_b-TOfafADDfx; YOUDAO_MOBILE_ACCESS_TYPE=0; ___rl__test__cookies=1586413371044',
		'Referer': 'http://fanyi.youdao.com/',
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36'}
	html=requests.post(url,data=data,headers=headers)
	print('有道翻译：')
	print('翻译的词为：',html.json()['translateResult'][0][0]['src'])
	print('翻译结果：',html.json()['translateResult'][0][0]['tgt'])

if __name__ == '__main__':
	r=math.floor(time.time()*1000)
	i=r+int(random.random()*10)
	print('r',r)
	print('i',i)
	salt=i
	ts=r
	keyword=input('请输入翻译内容：')
	sign=hashlib.md5(("fanyideskweb" + keyword + str(i) + "Nw(nmmbP%A-r6U3EUn]Aj").encode('utf-8')).hexdigest()
	print('sign:',sign)
	bv=hashlib.md5("5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36".encode('utf-8')).hexdigest()
	print('bv:',bv)
	getTran()