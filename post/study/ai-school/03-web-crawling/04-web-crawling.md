---
layout: post
title: "[AI SCHOOL 5기] 웹 크롤링 실습 - 웹 크롤링"
date: 2022-03-29 16:09:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Web Crawling, Selenium]
slug: aischool-03-04-web-crawling
---

# Wadis 마감 상품 재고 체크

## Google 메일 설정

```python
import smtplib
from email.mime.text import MIMEText

def sendMail(sender, receiver, msg):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(sender, 'your google app password')
    
    msg = MIMEText(msg)
    msg['Subject'] = 'Product is available!'
    
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
```

## Wadis 상품 재고 체크

```python
# 라이브러리 선언

check_status = 1
url = 'https://www.wadiz.kr/web/campaign/detail/{item_number}'

# 상품 재고가 확인되어 메일이 발송되면 종료
while check_status:

    webpage = urlopen(url)
    source = BeautifulSoup(webpage, 'html.parser')
    target = source.find_all('button', {'class':'rightinfo-reward-list'})

    for item in target:
        # 가격이 '179,000'원 상품 중
        if '179,000' in item.find('dt').get_text().strip():
            # '블루' 색상인 상품에 대하여
            if '블루' in item.find('p').get_text().strip():
                # 판매 중인 상태가 되면 (마감된 상품엔 "soldout" 클래스가 추가)
                if len(item.attrs['class']) == 2:
                        sendMail(sender, receiver, msg)
                        check_status = 0
```

---

# 서울상권분석서비스

## 웹 스크래핑 시도

```python
url = 'https://golmok.seoul.go.kr/regionAreaAnalysis.do'

response = requests.get(url).content
web_page = BeautifulSoup(response, 'html.parser')
```

- 해당 웹 페이지는 POST 요청으로 데이터를 주고 받기 때문에 GET 방식으로는 접근 불가
- 개발자 도구의 Network 탭을 확인하면 JSON 데이터 확인 가능
- POST 요청할 때 Payload를 변경하여 JSON 파일 종류 변경 가능

## POST 요청

```python
# Payload 설정
data = {'stdrYyCd': '2021', 'stdrQuCd': '4', 'stdrSlctQu': 'sameQu', 'svcIndutyCdL': 'CS000000', 'svcIndutyCdM': 'all'}

response = requests.post('https://golmok.seoul.go.kr/region/selectRentalPrice.json', data=data).content

result = json.loads(response)
```

> **Output**

```json
[{'GBN_CD': '11',
  'NM': '서울시 전체',
  'GUBUN': 'si',
  'BF1_FST_FLOOR': '132504',
  ...
```

---

# 네이버 금융 Top 종목

## TOP 종목 테이블 값 추출

```python
url = 'http://finance.naver.com'
response = requests.get(url).content
web_page = BeautifulSoup(response, 'html.parser')

top_items = web_page.find('tbody', {'id':'_topItems1'})
item_rows = top_items.find_all('tr')
```

## TOP 종목 테이블 값 표시

```python
for item in item_rows:
    item_name = item.find('th').get_text()
    item_price = item.find_all('td')[0].get_text()
    item_delta_price = item.find_all('td')[1].get_text()
    item_delta_percent = item.find_all('td')[2].get_text().strip()
    
    print('{} : 현재가 {}, 어제보다 {} {}, 백분율 변환 시 {}'.format(
        item_name, item_price, 
        item_delta_price[3:], item_delta_price[:2],
        item_delta_percent))
```

---

# 부동산 매매 내역

## 공공데이터포털 API 발급
- https://www.data.go.kr/data/15057267/openapi.do
- 상업업무용 부동산 매매 신고 자료 활용신청
- 상세 정보는 API 기술문서 참조

## Python3 샘플 코드

```python
import requests

url = 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcNrgTrade'
params ={'serviceKey' : '서비스키', 'LAWD_CD' : '11110', 'DEAL_YMD' : '201512' }

response = requests.get(url, params=params)
print(response.content)
```

- `request.get` 요청 시 `params`를 사용해서 파라미터 한번에 입력
- `LAWD_CD`: 법정동코드 10자리 중 앞 5자리 @ https://www.code.go.kr/index.do

## 부동산 매매 신고 자료 XML 요청

```python
response = requests.get(url, params=params).content
web_page = BeautifulSoup(response, 'lxml-xml')
```

## 매매 내역을 DataFrame에 저장

```python
loc_code = []
loc = []
date = []
price = []
building_usage = []

for item in items:
    try:
        loc_code.append(item.find('지역코드').get_text())
        loc.append(item.find('시군구').get_text() + item.find('법정동').get_text())
        date.append(item.find('년').get_text() + item.find('월').get_text() + item.find('일').get_text())
        price.append(item.find('거래금액').get_text())
        building_usage.append(item.find('건물주용도').get_text())
    except:
        pass

import pandas as pd

df = pd.DataFrame({'지역코드':loc_code, 
                   '부동산 위치':loc, 
                   '거래 일자':date, 
                   '거래 금액':price, 
                   '부동산 용도':building_usage})
```