from html import unescape
from pprint import pprint
from re import DOTALL, findall, search, sub
from time import time

import requests
from bs4 import BeautifulSoup


def parse(text):
    t = time()

    soup = BeautifulSoup(text, 'html.parser')
    list_item = soup.select('ul.list_news > li')
    result = []
    for item in list_item:
        a = item.select_one('a.news_tit')
        title = a.text
        author = item.select_one('a.info.press').text
        link = a['href']
        desc = item.select_one('a.dsc_txt_wrap').text
        date = item.select_one('span.info:not(:has(i))').text
        i = {
            'title': title,
            'author': author,
            'link': link,
            'desc': desc,
            'date': date,
        }
        result.append(i)

    tt = time() - t
    text = f'parse, {tt=}'
    return (result, text)

def regex(text):
    t = time()

    list_item = findall('<li class="bx".+?>(.+?)</li>', text, DOTALL)
    result = []
    for item in list_item:
        title = search('<a.+class="news_tit.+?>(.+?)</a>', item, DOTALL).group(1)
        title = sub('<.+?>', '', title)
        title = unescape(title)
        author = search('</span>(.+?)</a>', item, DOTALL).group(1)
        author = sub('<.+?>', '', author)
        link = findall('<a href="([^"]+?)" class="news_tit', item, DOTALL)
        # a = findall('<a.+?>', item)
        # for i in a:
        #     link = search('href="(.+?)" class="news_tit', i, DOTALL)
        #     if link:
        #         link = link.group(1)
        #         break
        desc = search('<a.+class="api_txt_lines.+?>(.+?)</a>', item, DOTALL).group(1)
        desc = sub('<.+?>', '', desc)
        desc = unescape(desc)
        date = search('<span class="info">([^<]+?)</span>', item, DOTALL).group(1)
        i = {
            'title': title,
            'author': author,
            'link': link,
            'desc': desc,
            'date': date,
        }
        result.append(i)

    tt = time() - t
    text = f'regex, {tt=}'
    return (result, text)



url = 'https://search.naver.com/search.naver?where=news&query=%EB%84%A4%EC%9D%B4%EB%B2%84&sm=tab_opt&sort=1&photo=3&field=0&pd=3&ds=2020.02.20&de=2022.02.22&nso=so%3Add%2Cp%3Afrom20200220to20220222'

r = requests.get(url)
t = r.text
# print(t)

a = parse(t)
b = regex(t)

pprint(a[0][1], sort_dicts=False)
pprint(b[0][1], sort_dicts=False)
print()
pprint(a[0][2], sort_dicts=False)
pprint(b[0][2], sort_dicts=False)
print()
print(f'{a[1]=}')
print(f'{b[1]=}')


"""
{'title': '우크라이나 긴장 고조에 깜짝 놀란 코스피…외국인 3200억 매도 ',
 'author': '한겨레언론사 선정',
 'link': 'https://www.hani.co.kr/arti/economy/economy_general/1032169.html',
 'desc': '시가총액 상위 10개 종목 중 외국인 보유 비중이 50%가 넘는 삼성전자·에스케이(SK)하이닉스·네이버 모두 1%대 '
         '하락률을 보였다. 외국인은 이날 유가증권시장에서만 3200억원 남짓 주식을 팔아치웠다. 코스닥지수는 전날보다 '
         '1.83%(16.14) 내린 868.11에 마감했다. 닛케이지수(일본) 등 아시아 주요 지수들도 1%대... ',
 'date': '2022.02.22.'}
{'title': '우크라이나 긴장 고조에 깜짝 놀란 코스피…외국인 3200억 매도 ',
 'author': '한겨레언론사 선정',
 'link': ['https://www.hani.co.kr/arti/economy/economy_general/1032169.html'],
 'desc': '시가총액 상위 10개 종목 중 외국인 보유 비중이 50%가 넘는 삼성전자·에스케이(SK)하이닉스·네이버 모두 1%대 '
         '하락률을 보였다. 외국인은 이날 유가증권시장에서만 3200억원 남짓 주식을 팔아치웠다. 코스닥지수는 전날보다 '
         '1.83%(16.14) 내린 868.11에 마감했다. 닛케이지수(일본) 등 아시아 주요 지수들도 1%대... ',
 'date': '2022.02.22.'}

{'title': '크래프톤도 NFT 사업 진출… "새 성장동력 확보" ',
 'author': '디지털타임스',
 'link': 'http://www.dt.co.kr/contents.html?article_no=2022022302101231820001&ref=naver',
 'desc': '크래프톤은 이미 네이버제트와 이용자 창작 콘텐츠(User Generated Contents·UGC) 오픈 메타버스 '
         '프로젝트를 추진 중이다. 다수의 온라인 게임을 개발하며... 네이버와 카카오는 연내 NFT 사업을 본격화한다. 네이버의 '
         "경우 최근 자회사 스노우와 AI(인공지능) 기업 알체라가 함께 만든 조인트벤처 '팔라'를... ",
 'date': '2022.02.22.'}
{'title': '크래프톤도 NFT 사업 진출… "새 성장동력 확보" ',
 'author': '디지털타임스',
 'link': ['http://www.dt.co.kr/contents.html?article_no=2022022302101231820001&ref=naver'],
 'desc': '크래프톤은 이미 네이버제트와 이용자 창작 콘텐츠(User Generated Contents·UGC) 오픈 메타버스 '
         '프로젝트를 추진 중이다. 다수의 온라인 게임을 개발하며... 네이버와 카카오는 연내 NFT 사업을 본격화한다. 네이버의 '
         "경우 최근 자회사 스노우와 AI(인공지능) 기업 알체라가 함께 만든 조인트벤처 '팔라'를... ",
 'date': '2022.02.22.'}

a[1]='parse, tt=0.04700040817260742'
b[1]='regex, tt=0.0019998550415039062'
"""