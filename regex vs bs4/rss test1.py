from html import unescape
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
        desc = item.find('description').text
        date = item.find('pubDate').text
        tag = item.find('tag').text
        i = {
            'title': title,
            'author': author,
            'link': link,
            'desc': desc,
            'date': date,
            'tag': tag
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
        title = ' '.join([i for i in search(r'<title><!\[CDATA\[(.+?)\]\]></title>', item, DOTALL).group(1).split() if i])
        title = unescape(title)
        author = search('<author>(.+?)</author>', item, DOTALL).group(1)
        link = search(r'<link><!\[CDATA\[(.+?)\]\]></link>', item, DOTALL).group(1)
        desc = search(r'<description><!\[CDATA\[(.+?)\]\]></description>', item, DOTALL).group(1)
        desc = unescape(desc)
        date = search('<pubDate>(.+?)</pubDate>', item, DOTALL).group(1)
        tag = search(r'<tag><!\[CDATA\[(.*?)\]\]></tag>', item, DOTALL).group(1)
        i = {
            'title': title,
            'author': author,
            'link': link,
            'desc': desc,
            'date': date,
            'tag': tag
        }
        result.append(i)

    tt = time() - t
    text = f'regex, {tt=}'
    return (result, text)


url = 'https://rss.blog.naver.com/blogpeople.xml'

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
{'title': '이달의 블로그 연말결산, 2024년도 고마웠어요!',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223691101885?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요, 네이버 블로그팀입니다! 다사다난했던 2024년, 어느새 올해도 마지막을 향해 달려가고 있습니다. 모두들 올 '     
         '겨울을 무사히 보내고 계신가요? 2024년에도 블로그에 꾸준히 소중한 노하우와 기록을 남겨주신 덕분에 저희 블로그팀은 '     
         '기쁘고 뿌듯한 한 해를 보냈습니다. 특히, 이달의 블로그 여러분이 블로그에 남겨주신 다양한 주제의 값진 글들은 블로그라는 '
         '공간을 한층 더 풍성하고 가치있는 공간으로 거듭나게 만들어주었답니다! 감사의 눈물.. 이번 연말에도 블로그팀은 감사의 '   
         '마음을 담아 이달의 블로그분들께 드릴 블로그 굿즈 패키지를 준비했습니다. 그 전에 잠시, 재밌는 데이터로 뽑아낸 이달의 '  
         '블로거 5분을 소개해 드리.......',
 'date': 'Thu, 12 Dec 2024 14:47:17 +0900',
 'tag': '이달의블로그,2024이달의블로그,블로그연말결산'}
{'title': '이달의 블로그 연말결산, 2024년도 고마웠어요!',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223691101885?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요, 네이버 블로그팀입니다! 다사다난했던 2024년, 어느새 올해도 마지막을 향해 달려가고 있습니다. 모두들 올 '     
         '겨울을 무사히 보내고 계신가요? 2024년에도 블로그에 꾸준히 소중한 노하우와 기록을 남겨주신 덕분에 저희 블로그팀은 '     
         '기쁘고 뿌듯한 한 해를 보냈습니다. 특히, 이달의 블로그 여러분이 블로그에 남겨주신 다양한 주제의 값진 글들은 블로그라는 '
         '공간을 한층 더 풍성하고 가치있는 공간으로 거듭나게 만들어주었답니다! 감사의 눈물.. 이번 연말에도 블로그팀은 감사의 '
         '마음을 담아 이달의 블로그분들께 드릴 블로그 굿즈 패키지를 준비했습니다. 그 전에 잠시, 재밌는 데이터로 뽑아낸 이달의 '
         '블로거 5분을 소개해 드리.......',
 'date': 'Thu, 12 Dec 2024 14:47:17 +0900',
 'tag': '이달의블로그,2024이달의블로그,블로그연말결산'}

{'title': '[2024 블로그 리포트 OPEN] 풍성한 데이터가 가득한 블로그 마을로 초대합니다  ️',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223690028011?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요, 네이버 블로그팀입니다! 2024년에도 블로그와 함께해 주신 여러분들을 위해 올해도 어김없이 찾아온 블로그 연말 '
         '결산입니다. 매해 블로그를 찾아주시고, 아껴주시고, 애정해 주시는 여러분들의 사랑에 보답하기 위해 이번 블로그 연말 결산은 '
         '더욱 알차게 구성하였는데요! 블로그 곳곳에 숨겨진 의미 있는 기록들을 살펴보는 네이버 블로그 리포트 그리고 나의 블로그홈 '
         '데이터를 기반으로 그려진 내 블로그 마을을 확인해 보는 마이 블로그 리포트를 공개합니다. (개봉 박두) 올해도 기록 맛집 '
         '/ 블로그가 핫플일 수밖에 없는 이유 2024 네이버 블로그 리포트 벌써 막바지를 향해 달려가고 있는 2024년, 블로그와 '
         '함께한 올해는 여.......',
 'date': 'Wed, 11 Dec 2024 17:42:44 +0900',
 'tag': '2024마이블로그리포트,2024네이버블로그리포트,2024블로그연말결산,올해도많관부'}
{'title': '[2024 블로그 리포트 OPEN] 풍성한 데이터가 가득한 블로그 마을로 초대합니다 ️',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223690028011?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요, 네이버 블로그팀입니다! 2024년에도 블로그와 함께해 주신 여러분들을 위해 올해도 어김없이 찾아온 블로그 연말 '
         '결산입니다. 매해 블로그를 찾아주시고, 아껴주시고, 애정해 주시는 여러분들의 사랑에 보답하기 위해 이번 블로그 연말 결산은 '
         '더욱 알차게 구성하였는데요! 블로그 곳곳에 숨겨진 의미 있는 기록들을 살펴보는 네이버 블로그 리포트 그리고 나의 블로그홈 '
         '데이터를 기반으로 그려진 내 블로그 마을을 확인해 보는 마이 블로그 리포트를 공개합니다. (개봉 박두) 올해도 기록 맛집 '
         '/ 블로그가 핫플일 수밖에 없는 이유 2024 네이버 블로그 리포트 벌써 막바지를 향해 달려가고 있는 2024년, 블로그와 '
         '함께한 올해는 여.......',
 'date': 'Wed, 11 Dec 2024 17:42:44 +0900',
 'tag': '2024마이블로그리포트,2024네이버블로그리포트,2024블로그연말결산,올해도많관부'}

a[1]='parse, tt=0.026998043060302734'
b[1]='regex, tt=0.0050008296966552734'
"""