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
        title = ' '.join([i for i in search('<title><!\[CDATA\[(.+?)\]\]></title>', item, DOTALL).group(1).split() if i])
        title = unescape(title)
        author = search('<author>(.+?)</author>', item, DOTALL).group(1)
        link = search('<link><!\[CDATA\[(.+?)\]\]></link>', item, DOTALL).group(1)
        desc = search('<description><!\[CDATA\[(.+?)\]\]></description>', item, DOTALL).group(1)
        desc = unescape(desc)
        date = search('<pubDate>(.+?)</pubDate>', item, DOTALL).group(1)
        tag = search('<tag><!\[CDATA\[(.*?)\]\]></tag>', item, DOTALL).group(1)
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

pprint(a[0][1], sort_dicts=False)
pprint(b[0][1], sort_dicts=False)
print()
pprint(a[0][2], sort_dicts=False)
pprint(b[0][2], sort_dicts=False)
print()
print(f'{a[1]=}')
print(f'{b[1]=}')

"""
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

{'title': '[공지] 포스트 종료에 따른 블로그 이전 안내',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223687587849?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요. 네이버 블로그팀입니다. 2025.04.30 (수), 네이버 포스트가 종료됩니다. 포스트 공지 보러 가기 '
         '&gt; 포스트는 아쉽게 종료되지만 포스트에서의 창작과 구독 활동은 블로그에서 계속 이어가실 수 있답니다! '
         '&quot;포스트에 썼던 내 글, 블로그에 그대로 옮겨지나요?&quot; &quot;포스트에서 즐겨 보던 글, 블로그에서 '
         '어떻게 보나요?&quot; 위와 같은 궁금증이 있으시다면! 블로그에서, 포스트 활동을 이어가는 방법에 대해 아래 내용을 '
         '자세히 확인해 주세요. 이전된 게시글은 어떻게 보이나요? 블로그로 게시글 이전을 신청하신 경우, 포스트에서 전체 공개로 '
         '발행된 게시글이 블로그의 최신 에디터 포맷으로 변환됩니다. ※기본형.......',
 'date': 'Mon, 09 Dec 2024 16:34:58 +0900',
 'tag': ' '}
{'title': '[공지] 포스트 종료에 따른 블로그 이전 안내',
 'author': 'blogpeople',
 'link': 'https://blog.naver.com/blogpeople/223687587849?fromRss=true&trackingCode=rss',
 'desc': '안녕하세요. 네이버 블로그팀입니다. 2025.04.30 (수), 네이버 포스트가 종료됩니다. 포스트 공지 보러 가기 > '
         '포스트는 아쉽게 종료되지만 포스트에서의 창작과 구독 활동은 블로그에서 계속 이어가실 수 있답니다! "포스트에 썼던 내 글, '
         '블로그에 그대로 옮겨지나요?" "포스트에서 즐겨 보던 글, 블로그에서 어떻게 보나요?" 위와 같은 궁금증이 있으시다면! '
         '블로그에서, 포스트 활동을 이어가는 방법에 대해 아래 내용을 자세히 확인해 주세요. 이전된 게시글은 어떻게 보이나요? '
         '블로그로 게시글 이전을 신청하신 경우, 포스트에서 전체 공개로 발행된 게시글이 블로그의 최신 에디터 포맷으로 변환됩니다. '
         '※기본형.......',
 'date': 'Mon, 09 Dec 2024 16:34:58 +0900',
 'tag': ''}

a[1]='parse, tt=0.02299976348876953'
b[1]='regex, tt=0.003000974655151367'
"""