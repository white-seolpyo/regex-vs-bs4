from pprint import pprint
from re import DOTALL, findall, search
from time import time

import requests
from bs4 import BeautifulSoup



def parse(text):
    t = time()

    soup = BeautifulSoup(text, 'xml')
    list_item = soup.select('item')
    result = []
    for item in list_item:
        title = item.find('title').text
        author = item.find('author').text
        link = item.find('link').text
        date = item.find('lastBuildDate').text
        i = {
            'title': title,
            'author': author,
            'link': link,
            'date': date,
        }
        result.append(i)

    tt = time() - t
    text = f'parse, {tt=}'
    return (result, text)

def regex(text):
    t = time()

    list_item = findall('<item>(.+?)</item>', text, DOTALL)
    result = []
    for item in list_item:
        title = search(r'<title><!\[CDATA\[(.+?)\]\]></title>', item, DOTALL).group(1)
        author = search(r'<author><!\[CDATA\[(.+?)\]\]></author>', item, DOTALL).group(1)
        link = search(r'<link><!\[CDATA\[(.+?)\]\]></link>', item, DOTALL).group(1)
        date = search('<lastBuildDate>(.+?)</lastBuildDate>', item, DOTALL).group(1)
        i = {
            'title': title,
            'author': author,
            'link': link,
            'date': date,
        }
        result.append(i)

    tt = time() - t
    text = f'regex, {tt=}'
    return (result, text)


url = 'https://kind.krx.co.kr/disclosure/rsstodaydistribute.do?method=searchRssTodayDistribute&repIsuSrtCd=&mktTpCd=0&searchCorpName=&currentPageSize=100'

r = requests.get(url)
t = r.text
# print(t)

a = parse(t)
b = regex(t)

pprint(a[0][0], sort_dicts=False)
pprint(b[0][0], sort_dicts=False)
print()
pprint(a[0][1], sort_dicts=False)
pprint(b[0][1], sort_dicts=False)
print()
print(f'{a[1]=}')
print(f'{b[1]=}')

"""
{'title': '[유]영보화학 [정정]현금ㆍ현물배당을 위한 주주명부폐쇄(기준일) 결정',
 'author': '[유]영보화학',
 'link': 'http://kind.krx.co.kr:80/common/disclsviewer.do?method=searchInitInfo&acptNo=20241213000524&docno=',
 'date': 'Fri, 13 Dec 2024 11:15:00 +0900'}
{'title': '[유]영보화학 [정정]현금ㆍ현물배당을 위한 주주명부폐쇄(기준일) 결정',
 'author': '[유]영보화학',
 'link': 'http://kind.krx.co.kr:80/common/disclsviewer.do?method=searchInitInfo&acptNo=20241213000524&docno=',
 'date': 'Fri, 13 Dec 2024 11:15:00 +0900'}

{'title': '[코]엠케이전자 임원ㆍ주요주주특정증권등소유상황보고서',
 'author': '[코]엠케이전자',
 'link': 'http://kind.krx.co.kr:80/common/disclsviewer.do?method=searchInitInfo&acptNo=20241213000522&docno=',
 'date': 'Fri, 13 Dec 2024 11:14:00 +0900'}
{'title': '[코]엠케이전자 임원ㆍ주요주주특정증권등소유상황보고서',
 'author': '[코]엠케이전자',
 'link': 'http://kind.krx.co.kr:80/common/disclsviewer.do?method=searchInitInfo&acptNo=20241213000522&docno=',
 'date': 'Fri, 13 Dec 2024 11:14:00 +0900'}

a[1]='parse, tt=0.02499866485595703'
b[1]='regex, tt=0.002000093460083008'
"""