#-*- coding:utf-8 -*-
'''Zheng 's BUG'''
from urllib.parse import urlencode
import json
# import re
# from hashlib import  md5
# import os
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
# from multiprocessing import Pool
import time
import datetime
import calendar

def get_page_index(start_time,end_time,pageNo=''):
	#构造请求参数
    data = {
        'name': 'ssq',
        'dayStart': start_time,
        'dayEnd': end_time,
        'pageNo':pageNo
    }
    url = 'http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?' + urlencode(data)
    header_selfdefine={
		'Host':'www.cwl.gov.cn',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': 'http://www.cwl.gov.cn/kjxx/ssq/kjgg/',
		'Cookie':'UniqueID=FJrLT5kyzFbr3sXX1532071893820; _ga=GA1.3.1457036941.1532071895; _gid=GA1.3.356619425.1532071895; 21_vq=9; _gat_gtag_UA_113065506_1=1'
	}
    try:
        response = requests.get(url,headers=header_selfdefine)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引出错")
        return None

def get_json_index(html):
	json_str = json.loads(html)
	if json_str['state'] == 0:
		return json_str
	else:
		return None

def save_in_file(jsonObj,savePath):
	lastStr = '<table><tr><th>期号</th><th>开奖日期</th><th>红球号码</th><th>蓝球号码</th><th>总销售额</th><th>一等奖注数</th><th>一等奖金额</th><th>奖池</th></tr>';
	for i in jsonObj:
		lastStr += '<tr><td>'+i['code']+'</td><td>'+i['date']+'</td><td>'+i['red']+'</td><td>'+i['blue']+'</td><td>'+i['sales']+'</td><td>'+i['prizegrades'][0]['typenum']+'</td><td>'+i['prizegrades'][0]['typemoney']+'</td><td>'+i['poolmoney']+'</td></tr>'
	lastStr += '</table>'
	with open(savePath,'w') as fw:
		fw.write(lastStr)


def main(start,end,savePath):
    #获得的是json形式返回的数据
    html = get_page_index(start,end)
    json_object = get_json_index(html)
    if json_object == None:
    	print('未获取到数据')
    else:
    	page = json_object['pageCount']
    	json_list = json_object['result']
    	if page > 1:
    		for m in range(2,page):
    			htmls = get_page_index(start,end,m)
    			json_res = get_json_index(htmls)
    			if json_res != None:
    				json_list += json_res['result']
    	save_in_file(json_list,savePath)

if __name__ == '__main__':
	prev_time = str(datetime.datetime.now() - datetime.timedelta(days=365*2))
	end = time.strftime('%Y-%m-%d', time.localtime())
	start=prev_time[0:10]
	savePath = 'D:\\ball.xls'
	main(start,end,savePath)