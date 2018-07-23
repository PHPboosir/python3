# coding=utf-8
import urllib.request
import ssl
from bs4 import BeautifulSoup
save_path = 'D:\\klcExcel.xls'
str_s = '<table><tr><th>项目名称</th><th>历史收益率</th><th>项目期限</th><th>项目金额</th><th>进度比</th><th>进度</th><th>项目状态</th></tr>'
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    html = html.decode('utf-8')
    return html


def getList(html):
    lists = BeautifulSoup(html, 'html.parser').select('div.klc-invest-item')
    strs = ''
    for i in lists:
    	strs+='<tr><td>'+i.find('div',class_='project-title').get('title')+'</td>'
    	strs+='<td>'+ i.find('div',class_='year-money').find_all('p')[1].get_text().replace(' ','')+'</td>'
    	strs+='<td>'+i.find('div',class_='project-day').find_all('div')[0].find_all('span')[0].get_text().replace(' ','')+'</td>'
    	strs+='<td>'+i.find('div',class_='project-day').find_all('div')[1].find_all('span')[0].get_text().replace(' ','')+'</td>'
    	strs+='<td>'+i.find('a').find_all('span',recursive=False)[1].get_text().replace(' ','')+'</td>'
    	strs+='<td>'+i.find('a').find_all('span',recursive=False)[0].get_text().replace(' ','')+'</td>'
    	strs+='<td>'+i.find('div',class_='buy-button').find('a').get_text().replace(' ','')+'</td>'
    	strs+='</tr>'
    return strs

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://www.58klc.com/"
html = getHtml(url)
str_s += getList(html)
str_s += '</table>'
with open(save_path,'w') as fw:
	fw.write(str_s)