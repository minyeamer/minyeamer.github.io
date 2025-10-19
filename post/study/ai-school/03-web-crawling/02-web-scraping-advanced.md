---
layout: post
title: "[AI SCHOOL 5기] 웹 크롤링 실습 - 웹 스크래핑 심화"
date: 2022-03-28 20:31:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Web Crawling]
slug: aischool-03-02-web-scraping-advanced
---

# Import Libraries

```python
import requests
from bs4 import BeautifulSoup

import pandas as pd
from datetime import datetime
import time # time.sleep()
import re
```

---

# 뉴스 검색 결과에서 네이버 뉴스 추출

## 네이버 뉴스 검색 결과 URL 분석

```html
https://search.naver.com/search.naver?
    where=news&
    sm=tab_jum& <!-- 불필요 -->
    query=데이터분석
```

## 네이버 뉴스 검색 URL 불러오기

```python
query = input() # 데이터분석

url = f'https://search.naver.com/search.naver?where=news&query={query}'
web = requests.get(url).content
source = BeautifulSoup(web, 'html.parser')
```

## 네이버 뉴스 기사 주제 가져오기

```python
news_subjects = source.find_all('a', {'class' : 'news_tit'})

subject_list = []

for subject in news_subjects:
    subject_list.append(subject.get_text())
```

## 네이버 뉴스 기사 링크 가져오기

```python
urls_list = []

for urls in source.find_all('a', {'class' : 'info'}):
    if urls.attrs['href'].startswith('https://news.naver.com'):
        urls_list.append(urls.attrs['href'])
```

---

# 단일 뉴스 페이지 분석

## ConnectionError

```python
web_news = requests.get(urls_list[0]).content
source_news = BeautifulSoup(web_news, 'html.parser')
```

```bash
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```

- 브라우저를 거치지 않고 HTML 코드를 요청하면 `ConnectionError` 발생
- 사용자임을 알리는 헤더 추가

```python
headers = {'User-Agent':'Mozilla/5.0
           (Windows NT 6.3; Win64; x64) 
           AppleWebKit/537.36 (KHTML, like Gecko)
           Chrome/63.0.3239.132 Safari/537.36'}

web_news = requests.get(urls_list[0], headers=headers).content
source_news = BeautifulSoup(web_news, 'html.parser')
```

## 기사 제목 / 발행 날짜 추출

```python
title = source_news.find('h3', {'id' : 'articleTitle'}).get_text()
date = source_news.find('span', {'class' : 't11'}).get_text()
```

## Pandas Timestamp

```python
# 2022.03.25. 오전 10:18
date = source_news.find('span', {'class' : 't11'}).get_text()

# 2022.03.25.10:18am
pd_date = pd.Timestamp(reformatted_date)
```

## 기사 본문 추출

```python
article = source_news.find('div', {'id' : 'articleBodyContents'}).get_text()

article = article.replace("\n", "")
article = article.replace("// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}", "")
article = article.replace("동영상 뉴스       ", "")
article = article.replace("동영상 뉴스", "")
article = article.strip()
```

## 기사 발행 언론사 추출

```python
press_company = source_news.find('address', {'class' : 'address_cp'}).find('a').get_text()
print(press_company)
```

---

# 여러 뉴스 데이터 수집

## 각 기사들의 데이터를 수집해 리스트에 추가

```python
for url in urls_list:
    ...

    titles.append(title)
    dates.append(date)
    articles.append(article)
    article_urls.append(url)
    press_companies.append(press_company)
```

## 데이터에 대한 DataFrame 생성

```python
article_df = pd.DataFrame({'Title':titles, 
                           'Date':dates, 
                           'Article':articles, 
                           'URL':article_urls, 
                           'PressCompany':press_companies})
```

![article-df](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/03-web-crawling/02-web-scraping-advanced/article-df.png?raw=true)

---

# 여러 페이지의 뉴스 데이터 수집

## 각각의 페이지에 해당하는 쿼리 리스트 생성

```python
max_page = int(input()) # 5
query = input()         # 데이터분석
start_points = []

for point in range(1, max_page*10+1, 10):
    start_points.append(str(point))
```

## 각각의 페이지에 대한 반복문 실행

```python
current_call = 1
last_call = (max_page - 1) * 10 + 1

while current_call <= last_call:
    url = "https://search.naver.com/search.naver?where=news&query=" + query + \
          "&start=" + str(current_call)
    web = requests.get(url).content
    source = BeautifulSoup(web, 'html.parser')

    ...

    # 대량의 데이터를 크롤링할 때는 요청 사이에 딜레이 생성
    time.sleep(5)
    current_call += 10
```

---

# 날짜 지정하여 크롤링

## 네이버 뉴스 날짜 지정 검색 결과 URL 분석

```html
https://search.naver.com/search.naver?where=news
    &query=데이터분석
    &sm=tab_opt
    &sort=0
    &photo=0
    &field=0
    &pd=4
    &ds=
    &de=
    &docid=
    &related=0
    &mynews=0
    &office_type=0
    &office_section_code=0
    &news_office_checked=
    <!-- 날짜 지정 (from{YYYYMMDD}to{YYYYMMDD}) -->
    &nso=so%3Ar%2Cp%3Afrom20220101to20220301
    &is_sug_officeid=0
```

## 날짜에 해당하는 쿼리 생성

```python
start_date = input() # 2022.01.01
end_date = input()   # 2022.03.01

start_date = start_date.replace(".", "")
end_date = end_date.replace(".", "")

...

while current_call <= last_call:
    url = "https://search.naver.com/search.naver?where=news&query=" + query \
          + "&nso=so%3Ar%2Cp%3Afrom" + start_date \
          + "to" + end_date \
          + "%2Ca%3A&start=" + str(current_call)
    web = requests.get(url).content
    source = BeautifulSoup(web, 'html.parser')

    ...
```

---

# 기사 정렬 순서 지정하여 크롤링

## 네이버 뉴스 기사 정렬 순서 검색 결과 URL 분석

```html
https://search.naver.com/search.naver?where=news
    &query=데이터분석
    &sm=tab_opt
    <!-- 관련도순: 0, 최신순: 1, 오래된순: 2 -->
    &sort=0
    ...
```

## 정렬 순서에 해당하는 쿼리 생성

```python
query = input()             # "데이터분석" < 정확한 검색
sort_type = int(input())    # 1
```

---

# 데이터를 엑셀 파일로 저장

```python
article_df.to_excel('result_{}.xlsx'.format(datetime.now().strftime('%y%m%d_%H%M')), index=False, encoding='utf-8')
```