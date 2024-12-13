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



url = 'https://search.naver.com/search.naver?where=news&query=%ED%8C%8C%EC%9D%B4%EC%8D%AC&sm=tab_opt&sort=2&photo=3&field=0&pd=3&ds=2020.02.20&de=2022.02.22&nso=so%3Add%2Cp%3Afrom20200220to20220222'

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
{'title': '[단독]4000만 금융빅데이터, 핀테크·스타트업 등 AI 딥러닝에 사용된다 ',
 'author': '전자신문',
 'link': 'http://www.etnews.com/20200226000301',
 'desc': '해당 원석 분석 환경은 △딥러닝 학습을 위한 데이터 제공 △데이터 처리를 위한 하드웨어인 그래픽처리장치(GPU) 구축 '     
         '△파이썬(생산성 높은 프로그래밍 언어) 기반의 라이브러리 제공 등 3단계로 구성된다. 신정원 관계자는 “연내 개별 '       
         '참여자들이 CreDB에서 자체 구축한 AI를 고도화할 수 있는 시스템을... ',
 'date': '2020.02.26.'}
{'title': '[단독]4000만 금융빅데이터, 핀테크·스타트업 등 AI 딥러닝에 사용된다 ',
 'author': '전자신문',
 'link': ['http://www.etnews.com/20200226000301'],
 'desc': '해당 원석 분석 환경은 △딥러닝 학습을 위한 데이터 제공 △데이터 처리를 위한 하드웨어인 그래픽처리장치(GPU) 구축 '     
         '△파이썬(생산성 높은 프로그래밍 언어) 기반의 라이브러리 제공 등 3단계로 구성된다. 신정원 관계자는 “연내 개별 '       
         '참여자들이 CreDB에서 자체 구축한 AI를 고도화할 수 있는 시스템을... ',
 'date': '2020.02.26.'}

{'title': '코인원 개발직군 신입·경력 모집 ',
 'author': '파이낸셜뉴스',
 'link': 'http://www.fnnews.com/news/202003021726171973',
 'desc': '모집분야는 △블록체인 백엔드 엔지니어(지갑개발) △프론트엔드 엔지니어 △백엔드 엔지니어(자바/파이썬) △풀스택 엔지니어 '
         '△프로젝트 매니저(서비스 기획) 등 총 6개 분야다. 채용 절차는 서류전형 및 1차 실무진 면접과 2차 임원 면접 등으로 '    
         '이뤄진다. 차명훈 코인원 대표는 "블록체인의 모든 것을... ',
 'date': '2020.03.02.'}
{'title': '코인원 개발직군 신입·경력 모집 ',
 'author': '파이낸셜뉴스',
 'link': ['http://www.fnnews.com/news/202003021726171973'],
 'desc': '모집분야는 △블록체인 백엔드 엔지니어(지갑개발) △프론트엔드 엔지니어 △백엔드 엔지니어(자바/파이썬) △풀스택 엔지니어 '
         '△프로젝트 매니저(서비스 기획) 등 총 6개 분야다. 채용 절차는 서류전형 및 1차 실무진 면접과 2차 임원 면접 등으로 '    
         '이뤄진다. 차명훈 코인원 대표는 "블록체인의 모든 것을... ',
 'date': '2020.03.02.'}

a[1]='parse, tt=0.039999961853027344'
b[1]='regex, tt=0.002001523971557617'
"""