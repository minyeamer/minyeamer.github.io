---
layout: post
title: "[AI SCHOOL 5기] 웹 크롤링 실습 - 웹 스크래핑 기본"
date: 2022-03-25 18:43:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Web Crawling]
slug: aischool-03-01-web-scraping-basic
---

# BeautifulSoup Library

```python
from bs4 import BeautifulSoup 
from urllib.request import urlopen 
```

---

# 단어의 검색 결과 출력

## 다음 어학사전 URL 불러오기

```python
# 찾는 단어 입력
word = 'happiness'

url = f'https://alldic.daum.net/search.do?q={word}'
web = urlopen(url)
web_page = BeautifulSoup(web, 'html.parser')
```

## 찾는 단어 출력

```python
text_search = web_page.find('span', {'class': 'txt_emph1'})
print(f'찾는 단어: {text_search.get_text()}')
```

## 단어의 뜻 출력

```python
list_search = web_page.find('ul', {'class': 'list_search'})
list_text = list_search.find_all('span', {'class': 'txt_search'})
definitions = [definition.get_text() in list_text]
print(f'단어의 뜻: {definitions}')
```

> **Output**

```vim
찾는 단어: happiness
단어의 뜻: ['행복', '만족', '기쁨', '행운']
```

---

# 영화 정보 출력

## 네이버 영화 URL 불러오기

```python
# 찾는 영화 번호 입력 (향후 영화 제목으로 검색 구현)
movie = 208077

url = f'https://movie.naver.com/movie/search/result.naver?query={movie}'
web = urlopen(url)
web_page = BeautifulSoup(web, 'html.parser')
```

## 영화 제목 출력

```python
title = web_page.find('h3', {'class':'h_movie'}).find('a')
print(f'Movie Title: {title.get_text()}')
```

## 네이버 영화 배우/제작진 URL 불러오기

```python
url = f'https://movie.naver.com/movie/bi/mi/detail.naver?query={movie}'
web = urlopen(url)
web_page = BeautifulSoup(web, 'html.parser')
```

## 감독 이름 출력

```python
director = web_page.find('div', {'class':'dir_product'}).find('a')
print(f'Director: {director.get_text()}')
```

## 출연 배우들 이름 출력

```python
actor_list = web_page.find('ul', {'class':'lst_people'})
actor_names = actor_list.find_all('a', {'class':'k_name'})
actors = [actor.get_text() for actor in actor_names]
print(f'Actors: {actors}')
```

> **Output**

```
Movie Title: 스파이더맨: 노 웨이 홈
Director: 존 왓츠
Actors: ['톰 홀랜드', '젠데이아 콜먼', '베네딕트 컴버배치', '존 파브로', '제이콥 배덜런', '마리사 토메이', '알프리드 몰리나']
```

---

# 티스토리 게시글 출력 및 저장

## 티스토리 게시글 URL 불러오기

```python
# 찾는 글 번호 입력
post_number = 22

url = f'https://minyeamer.tistory.com/{post_number}'
web = urlopen(url)
source = BeautifulSoup(web, 'html.parser')
```

## 티스토리 게시글 출력

```python
all_text = source.find('article',{'class': 'content'})
tags = ['h2', 'h3', 'h4', 'li', 'p', 'blockquote', 'code']
article = all_text.find_all(tags)
print(article)
```

## 티스토리 게시글 저장

```python
from urllib.request import HTTPError

for post_number in range(10):
    try:
        url = f'https://minyeamer.tistory.com/{post_number}'
        web = urlopen(url)
        source = BeautifulSoup(web, 'html.parser')
    except HTTPError:
        print(f'{i}번 글에서 에러가 발생했습니다.')
        pass
    
    with open('tistory_all.txt', 'a', encoding = 'utf-8') as f:        
        all_text = source.find('article',{'class': 'content'})
        tags = ['h2', 'h3', 'h4', 'li', 'p', 'blockquote', 'code']
        article = all_text.find_all(tags)

        for content in article:
            f.write(content.get_text() + '\n')
```