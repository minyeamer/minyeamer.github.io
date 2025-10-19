---
layout: post
title: "[AI SCHOOL 5기] 웹 크롤링 실습 - 셀레니움"
date: 2022-03-28 21:23:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Web Crawling, Selenium]
slug: aischool-03-03-selenium
---

# Selenium
- 브라우저의 기능을 체크할 때 사용하는 도구
- 브라우저를 조종해야할 때도 사용

## Import Libraries

```python
# 크롬 드라이버 파일 자동 다운로드
from webdriver_manager.chrome import ChromeDriverManager
# 크롬 드라이버를 파일에 연결
from selenium.webdriver.chrome.service import Service

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup 
import time
import pandas as pd

import warnings
warnings.filterwarnings("ignore") # 불필요한 Warning 메시지 무시
```

## Virtual Browser

```python
# 크롬 드라이버 파일을 다운로드 후 세팅
service = Service(executable_path=ChromeDriverManager().install()) 

# 세팅된 크롬 드라이버를 연결해 가상 브라우저 실행
driver = webdriver.Chrome(service=service)
```
- `driver.maximize_window()`: 가상 브라우저 크기 최대화
- 올바른 실행을 위해 가상 브라우저의 내부는 건들지 않아야 함

---

# Google Translation

## Google 번역 페이지 접속

```python
translate_url = 'https://translate.google.co.kr/?sl=auto&tl=en&op=translate&hl=ko'

driver.get(translate_url)
```

- `driver.current_url`: 가상 브라우저가 접속한 페이지의 URL 주소 반환
- `driver.page_source`: 가상 브라우저가 접속한 페이지의 소스코드 반환
- `driver.find_element`: `BeautifulSoup`의 `find`와 같음
- `driver.find_elements`: `BeautifulSoup`의 `find_all`과 같음

## 원본 텍스트 입력
- 클래스나 ID를 통한 접근이 어려울 경우 XPath를 통해 접근
- 개발자 도구에서 full XPath를 복사

```python
origin_xpath = '원본 텍스트 부분에 해당하는 XPath'

driver.find_element_by_xpath(origin_xpath).clear()
driver.find_element_by_xpath(origin_xpath).send_keys('원본 텍스트')
```

- `.click()`: 특정 부분 클릭
- `.clear()`: 특정 부분에 입력된 값 지우기
- `.send_keys()`: 특정 부분에 값 입력

## 번역된 텍스트 가져오기

```python
translation_xpath = '번역된 텍스트 부분에 해당하는 XPath'

translated_contents = driver.find_element_by_xpath(translation_xpath).text
```

- `.text`: 번역된 텍스트

## 가상 브라우저 종료

```python
driver.close()
driver.quit()
```

---

# Translated Word Cloud

## Translated Word Cloud 생성 방법
1. 기사글 전체를 번역하고 단어를 빈도수 순으로 정렬
2. 빈도수를 기반으로 단어를 선정하고 해당 단어들만을 번역 *

## 선정된 단어들을 번역

```python
for key in translation_target:
    
    # key를 원본 텍스트 부분에 입력
    time.sleep(3)

    # translated_contents 변수에 번역된 텍스트를 가져와서 저장
    
    translation_result[translated_contents] = translation_target[key]

driver.close()
driver.quit()
```

## Translated Word Cloud

![translated-word-cloud](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/03-web-crawling/03-selenium/translated-word-cloud.png?raw=true)

---

# 파파고 번역
- 파파고 번역 페이지는 키워드 입력 후 번역된 결과를 보이는 시간 간격이 김
- 딜레이를 지정하고 반복문을 수행할 경우 번역이 끝나지 않아 잘못된 결과를 가져올 가능성
- 번역이 완료될 경우 나타나는 태그를 기준으로 대기 시간 설정
- 파파고에서는 번역된 단어의 발음에 해당하는 `<p>` 태그가 나타날 때를 번역 완료로 판단
- `expected_conditions`를 활용해 특정한 태그의 로딩이 완료될 때까지 대기

## 선정된 단어들을 번역

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# 가상 브라우저 실행
# 파파고 번역 페이지(https://papago.naver.com/?sk=ko&tk=en) 이동

for key in translation_target:    
    driver.find_element_by_id('txtSource').clear()
    driver.find_element_by_id('txtSource').send_keys(key)
    time.sleep(3)

    wait = WebDriverWait(driver, timeout=10)
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#targetEditArea > p")))
    
    translated_contents = driver.find_element_by_id('txtTarget').text
    
    translation_result_papago[translated_contents] = translation_target[key]

# 가상 브라우저 종료
```

- `WebDriverWait()`: 가상 브라우저가 `timeout`을 초과하면 에러 발생
- `wait.until(expected_conditions)`: 지정한 Tag가 포착될 때까지 대기
- `expected_conditions` Documentation @ https://j.mp/3mCnc5G

---

# 인터파크 투어

## 여행지 검색

```python
# 가상 브라우저 실행
# 인터파크 투어 페이지(http://tour.interpark.com/) 이동

driver.find_element_by_id('SearchGNBText').send_keys('보라카이')
driver.find_element_by_class_name('search-btn').click()
```

## 여행지 검색 결과 크롤링

```python
# 더보기 버튼 클릭
driver.find_element_by_class_name('moreBtn').click()

# 2페이지로 변경
driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div[2]/div[4]/div[3]/ul/li[2]').click()
```