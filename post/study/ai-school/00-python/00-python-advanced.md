---
layout: post
title: "[코드라이언] 파이썬 심화"
date: 2022-03-20 17:59:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Python]
slug: aischool-00-02-python-advanced
---

# Crawling
- 크롤러는 웹 페이지의 데이터를 모아주는 소프트웨어
- 크롤링은 크롤러를 사용해 웹 페이지의 데이터를 추출해 내는 행위

## Request
- `request` 모듈의 `get()` 함수는 서버에게 html 정보를 요청
-  `get()` 함수는 url, 파라미터 값을 받고 `request.Response`를 반환
- 정상적인 응답을 받을 경우 `Response [200]` 반환
- 응답값을 reponse 변수에 넣고 `response.text`를 출력하면 html 코드 출력

## BeautifulSoup
- `bs4` 모듈의 `BeautifulSoup` 기능은 입력값을 의미있는 데이터로 변환

```python
soup = BeautifulSoup(response.text, 'html.parser')
soup.title # html 코드에서 title에 해당하는 태그를 반환
soup.title.string # title 태그에서 문자열 값만 뽑아 반환
soup.findAll('span') # 모든 span 태그를 반환
soup.findAll('a', 'link_favorsch') # link_favorsch 클래스만 반환
```

```python
results = soup.findAll('a', 'link_favorsch')
result.get_text() # result에서 태그를 제외하고 텍스트만 반환
```

## File
- `open(file, mode)`: 파일을 생성, 참조, 수정할 때 사용하는 라이브러리
- `mode`에는 `r (read)`, `w (write)`, `a (append)`가 있음

```python
file = open("rankresult.txt", "w")
file.write(result.get_text()+"\n")
```

```python
file = open("rankresult.txt", "a")
file.write(result.get_text()+"\n")
```

# API
- API는 누군가가 만든 프로그램을 가져와서 사용할 때 필요한 인터페이스
- API Key는 API를 누가 사용하는지 알 수 있는 키

## OpenWeatherMap API
- Current Weather Data API 사용    
`https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}`
- f-string을 이용하여 `city name`과 `API Key`를 변수로 설정
- `requests.get(api)`로 API 요청
- API 파라미터에 `lang`을 `kr`로 추가하여 반환값을 한국어로 변경
- API 파라미터에 `units`를 `metric`으로 추가하여 온도 단위르 섭씨로 변경

## JSON
- 자바스크립트의 오브젝트에 따르는 문자 기반 데이터 포맷
- `json.loads(str)`로 문자열을 JSON (딕셔너리 타입)으로 변경

# Translator
- **googletrans**: 언어 감지 및 번역을 도와주는 라이브러리
- `googletrans`의 `Translator`를 import하고 `Translator()`로 Translator 생성

```python
>>> translator.detect(sentence) # 문장에 대한 언어 감지 결과를 반환
>>> Detected(lang=ko, confidence=1.0)

>>> translator.translate(sentence, 'en') # 문장에 대한 변역 결과를 반환
>>> Translated(src=ko, dest=en, text=Hello, ...
```

# Mail

## IMAP
- 다른 메일 서버에서 보낸 메일을 클라이언트에게 보내기 위한 프로토콜

## SMTP
- 간단하게 메일을 보내기 위한 프로토콜

1. SMTP 메일 서버를 연결한다. (smtp.gmail.com:465)

```python
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
```

2. SMTP 메일 서버에 로그인한다.

```python
smtp.login('MAIL_ADDRESS', 'PASSWORD')
```

3. SMTP 메일 서버에 메일을 보내고 연결을 끊는다.

```python
smtp.send_message()
smtp.quit()
```

## MIME
- 전자우편을 위한 인터넷 표준 포맷
- `email.message` 모듈의 `.EmailMessage`기능 사용
- MIME의 Header에는 Subject, To 등이 존재

1. 이메일을 만든다.

```python
message = EmailMessage()
```

1. 이메일에 내용을 담는다.

```python
message.set_content('content')
```

1. 발신자, 수신자를 설정한다.

```python
message['Subject'] = 'subject'
message['from'] = 'user1@gmail.com'
message['To'] = 'user2@gmail.com
```

## Attach Image
- Read Image

```python
with open('codelion.png','rb') as image:
    image_file = image.read()
```

- Attach Image

```python
# 이미지 파일 첨부 (메일 형식이 mixed로 바뀜)
add_attachment(image, maintype='image', subtype='png')
```

- 이미지 파일의 확장자를 판단

```python
imghdr.what('filename', image)
```

## Validation
- 정규표현식   
`^①[a-zA-Z0-9.+_-]+@②[a-zA-Z0-9]+③\.[a-zA-z]{2,3}$`   
① [a부터 z까지, A부터 Z까지, 0부터 9까지, . , + , _ , -] `|` +: 1회 이상 반복   
② @ `|` [a부터 z까지, A부터 Z까지, 0부터 9까지] `|` +: 1회 이상 반복   
③ . (개행문자 \) `|` [a부터 z까지, A부터 Z까지] `|` {2,3}: 최소 2회, 최대 3번 반복

```python
re.match(reg, 'example@gmail.com')
```

- 적합하지 않은 이메일 형식일 경우 `None`을 반환
- if문을 사용해 `None`이 아니면 메일을 보내도록 설정

# Others
- **함수**: 입력한 값을 사용해 결과물을 만들어 반환하는 조립기
- **모듈**: 함수들을 모아놓은 파일
- `type()`: 객체의 타입을 반환
- `datetime.today().strftime("%Y년 %m월 %d일")`: 오늘의 날짜 반환

> 로봇이 아님을 알리는 헤더

```python
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
```