---
layout: post
title: "[Python] requests로 네이버 스마트스토어센터 로그인 구현하기 (1)"
date: 2022-12-03 13:56:14 +0900
categories: [Data, Crawling]
tags: [Crawling, Python, requests, Naver, 네이버, 스마트스토어, 스마트스토어센터, 로그인, 크롤링]
---

네이버 스마트스토어센터에서는 매출 향상에 도움을 주는 유용한 통계 데이터를 제공해줍니다.   
쇼핑몰 데이터를 분석하는 입장에서 무료로 제공되는 이런 데이터는 큰 도움이 되지만,   
대부분이 엑셀 파일 다운로드를 지원하지 않고 빈번하게 수치가 바뀌는 데이터를 각각의 메뉴에서 매번 확인하기도 어렵습니다.   
이런 데이터를 자동화 프로그램으로 수집 및 적재할 수 있다면 업무 효율을 크게 향상시킬 수 있을 것입니다.

이번 게시글에서는 실제 네이버 스마트스토어 로그인 구현에 앞서   
데이터 수집에 대한 간단한 설명을 진행하고 네이버 로그인 구현의 바탕이 되는 클래스와 메소드를 정의합니다.

---

# 데이터 수집 개요

네이버 웹사이트에서 데이터를 수집할 때 활용할 수 있는 방안은 2가지가 있습니다.   
첫 번째는 CSS Selector 또는 XPath를 활용해 웹사이트 특정 위치의 값을 가져오는 것,   
두 번째는 API에 요청을 보내 JSON 형태의 데이터를 가져오는 것입니다.

특정 위치의 값을 가져오는 첫 번째 방식은 UI에 의존적이어서 코드의 지속성을 보장하기 어렵고   
원하는 데이터와 관련없는 웹 소스 전체를 불러오기 때문에 속도 면에서도 단점이 있습니다.   
따라서, API를 제공하는 경우 두 번째 방식을 이용하는 것이 효율적입니다.

## 데이터 수집 시나리오

네이버 쇼핑에서 표시되는 상품의 순위는 검색인기도를 기준으로 결정됩니다.   
키워드별 상위권 상품의 검색인기도를 가져오는 것을 예시로 데이터 수집을 진행해보겠습니다.

![popularity-ui](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/popularity-ui.png?raw=true)

위 이미지에서 왼쪽 부분은 실제 UI, 오른쪽 부분은 HTML 소스 입니다.   
해당 소스에서 데이터를 가져온다면 `div.popularity-product > div.box-border` 위치에서   
`dd` 태그를 순서대로 지정해서 각각의 종합, 적합도, 인기도 값을 가져올 수 있습니다.

해당 데이터를 분석에 활용하기 위해서는 인기도 수치를 구성하는 클릭수, 판매실적 등도 필요하기 때문에   
상세보기 페이지를 확인해야하고 결과적으로 하나의 상품에 대한 데이터를 보기 위해 두 개의 페이지를 방문해야 합니다.

하지만 네이버의 대부분의 웹페이지는 API를 기반으로 가져온 데이터로 구성되기 때문에   
해당 API를 활용할 수 있다면 더욱 효율적인 데이터 수집이 가능합니다.

![popularity-json](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/popularity-json.png?raw=true)

서버에서 가져오는 데이터를 확인할 때는 주로 개발자 도구의 네트워크 탭을 활용합니다.   
웹페이지 로드 시 가져오는 문서를 확인하다보면 위 이미지와 같이 목표로 하는 데이터를 보내주는 API를 발견할 수 있습니다.

새 탭에서 해당 API 주소를 요청하면 위 이미지 내 오른쪽 부분과 같은 JSON 형식의 데이터를 받을 수 있습니다.   
실제 UI에서 가져오고자 하는 종합, 적합도, 인기도 수치도 해당 데이터에서 확인할 수 있습니다.   
여기에는 추가로 클릭수, 판매실적 등에 대한 수치 데이터도 포함되어 있기 때문에   
해당 API를 활용하면 다수의 페이지에 요청을 보낼 수고도 줄어들게 됩니다.

## 로그인이 필요한 페이지의 데이터 가져오기

여기까지는 간단해보이지만 네이버 스마트스토어센터 데이터를 `requests` 모듈로 가져오는데는   
하나의 추가적인 문제가 존재합니다.   
단순한 GET 요청일지라도 로그인 정보를 갖고 있지 않다면 데이터를 받을 수 없습니다.   
스마트스토어센터에 로그인하지 않은 상태에서 위 API 주소로 요청을 보내게 된다면   
아래와 같은 에러 메시지를 받아볼 수 있습니다.

```json
{ "error": "Full authentication is required to access this resource" }
```

이 문제에 대한 해결방법은 헤더에 있습니다.   
개발자 도구 네트워크 탭에서 하나의 문서를 클릭하고 Headers 탭에서 스크롤을 내리면   
아래와 같은 Request Headers 정보를 확인할 수 있습니다.

![headers](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/headers.png?raw=true)

서버와 클라이언트 간 네트워크 요청 시 서버는 클라이언트의 정보를 확인할 목적으로   
클라이언트에 쿠키라는 암호화된 인증 정보를 남깁니다.   
클라이언트가 해당 정보를 헤더에 담아 요청을 보내는 경우에만 서버가 올바른 응답을 전달합니다.

`requests` 모듈에서는 이러한 과정을 다음과 같이 구현할 수 있습니다.

```python
headers = {"cookie": "..."}
response = requests.get(url, headers=headers)
```

하지만 일반적인 쿠키 값은 30분의 유통기한이 있기 때문에, 매번 쿠키 값을 갱신해야 하는데   
자동화 프로그램을 돌리기 전에 직접 로그인해서 쿠키 값을 갱신하는 것은 바람직하지 못합니다.

결과적으로 로그인이 필요한 스마트스토어 페이지의 데이터를 가져오기 위해서는   
자동화된 로그인 과정을 거쳐서 쿠키 값을 갱신할 필요가 있습니다.

## 쿠키 확인하기

클라이언트에서 요청하는 헤더 내역에서 확인할 수 있는 정보는 표현하면 다음과 같습니다.

```json
{
    "NNB": "...",
    "nid_inf": "...",
    "NID_AUT": "...",
    "NID_SES": "...",
    "NID_JKL": "...",
    "CBI_SES": "...",
    "CBI_CHK": "...",
    "NSI": "..."
}
```

이는 앞으로 스마트스토어센터 로그인을 구현하는데서 반드시 확인해야할 목록입니다.   
지금은 이 값들이 어떤 의미를 가지고 어디서 발생하는 값인지 알 수는 없지만,   
서버로부터 해당 값들을 받아오는 것에 집중하여 로그인 프로세스를 파악하고   
로그인 진행 과정을 쿠키 값을 통해 시각적으로 점검할 것입니다.

---

# 스마트스토어센터 로그인 개요

스마트스토어센터 로그인을 구현하기 위해 로그인 페이지를 탐색할 필요가 있습니다.

|||
|:-:|:-:|
|![smartstore-ui](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/smartstore-ui.png?raw=true)|![login-ui](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/login-ui.png?raw=true)|

메인 페이지에서 로그인하기 버튼을 클릭했을 때 이동하는 로그인 페이지에서 실제 로그인이 이루어집니다.   
스마트스토어센터 로그인에는 판매자 아이디로 로그인하는 방식과   
네이버 아이디로 로그인하는 방식이 있습니다.

우선적으로 네이버 아이디로 로그인하는 방식을 알아보겠습니다.

네이버 로그인을 구현하는 것에 관해선 좋은 선례가 있어 많은 부분을 참고했습니다.   
해당 내용은 아래 링크를 참고할 수 있습니다.

> [파이썬#76 - 파이썬 크롤링 requests 로 네이버 로그인 하기](https://blog.naver.com/PostView.naver?blogId=nkj2001&logNo=222722322802)

## 클래스 정의

네이버 로그인 기능은 자동화 프로그램에서 지속적으로 활용될 것이기 때문에   
별도의 클래스에서 메소드로 구현할 필요가 있습니다.

먼저 `requests` 모듈의 `Session` 클래스를 상속받는 `NaverLogin` 클래스를 정의합니다.

`NaverLogin`은 네이버 ID와 비밀번호를 초기화하는 단순한 기능만을 구현했지만   
`requests.Session` 클래스를 상속받았기 때문에   
웹페이지 요청과 관련된 다양한 기능을 가지고 있습니다.

```python
class NaverLogin(requests.Session):
    def __init__(self, userid: str, passwd: str, **kwargs):
        super().__init__(**kwargs)
        self.userid = userid
        self.passwd = passwd
```

그리고 `NaverLogin`을 상속받는 `SmartstoreLogin` 클래스를 정의합니다.   
일반적인 네이버 로그인과 스마트스토어센터에서 진행되는 네이버 로그인이 다르기 때문에   
`NaverLogin` 메소드의 일부를 변경할 필요가 있을 것입니다.

```python
class SmartstoreLogin(NaverLogin):
    def __init__(self, userid=str(), passwd=str(), **kwargs):
        super().__init__(userid, passwd, **kwargs)
```

추가적으로 로그인 페이지 요청 과정에서 빈번하게 정의해야 하는 매개변수 생성을   
간단하게 할 수 있는 메소드를 정의하겠습니다.

## 헤더 생성 메소드 정의

`requests` 모듈은 기본적으로 헤더를 갖고 있지 않는데   
이 상태로 다수의 웹페이지에 요청을 보낸다면 로봇으로 간주당해 차단당할 것입니다.

임의의 웹페이지에 요청을 보낼 때 확인할 수 있는 요청 헤더 `HEADERS`를 기본 바탕으로,   
웹페이지 별로 최적화된 헤더를 생성하는 `get_headers()` 메소드를 정의합니다.

```python
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}
```

```python
from urllib.parse import urlparse

class NaverLogin(requests.Session):
    def get_headers(self, authority=str(), referer=str(), cookies=str(),
                    host=str(), **kwargs) -> Dict[str,Any]:
        headers = HEADERS.copy()
        if authority: headers["Authority"] = urlparse(authority).hostname
        if host: headers["Host"] = urlparse(host).hostname
        if referer: headers["Referer"] = referer
        if cookies: headers["Cookie"] = cookies
        return dict(headers, **kwargs)
```

호스트명을 의미하는 `Authority` 또는 `Host`, 리다이렉트 전 경로를 의미하는 `Referer`,   
그리고 쿠키를 의미하는 `Cookie` 등의 값은 수시로 변하기 때문에 별도의 입력으로 지정합니다.

## 쿠키 생성 메소드 정의

헤더와 함께 활용되는 쿠키는 헤더와 마찬가지로 웹페이지 요청 시 빈번히 활용되는데   
`requests` 모듈의 쿠키 자료형인 `RequestsCookieJar`를 헤더에 직접 포함시킬 수 없기 때문에,   
쿠키를 적절한 형태의 문자열로 변환하는 `get_cookies()` 메소드를 정의합니다.

```python
from requests.cookies import RequestsCookieJar

class NaverLogin(requests.Session):
    def get_cookies(self, **kwargs) -> str:
        return self.parse_cookies(dict(self.cookies, **kwargs))

    def parse_cookies(self, cookies: RequestsCookieJar) -> str:
        return "; ".join([str(key)+"="+str(value) for key,value in cookies.items()])
```

---

# 마치며

이번 게시글에서는 두 가지 데이터 수집 방식을 예시를 통해 알아보았고   
스마트스토어센터 로그인의 바탕이 되는 클래스와 메소드를 정의했습니다.

다음 게시글에서는 네이버 로그인을 본격적으로 구현해보겠습니다.
