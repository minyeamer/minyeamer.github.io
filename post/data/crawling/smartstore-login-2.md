---
layout: post
title: "[Python] requests로 네이버 스마트스토어센터 로그인 구현하기 (2)"
date: 2022-12-03 16:11:42 +0900
categories: [Data, Crawling]
tags: [Crawling, Python, requests, Naver, 네이버, 스마트스토어, 스마트스토어센터, 로그인, 크롤링]
---

이번 게시글에서는 스마트스토어센터 페이지에서 데이터를 수집하는 자동화 프로그램을 제작하기 위한   
첫 번째 과정으로 네이버 로그인을 구현할 것입니다.

앞선 게시글에서 데이터를 수집하는 방식에 대해 알아보면서   
로그인이 필요한 페이지에 접근하기 다음과 같은 쿠키 값이 필요함을 확인했습니다.

```python
cookies = {
    "NNB": "...",
    "nid_inf": "...",
    "NID_AUT": "...",
    "NID_SES": "...",
    "NID_JKL": "...",
    "CBI_SES": "...",
    "CBI_CHK": "...",
    "NSI": "...",
}
```

위 키값들은 앞으로 로그인 프로세스를 파악하는 과정에서 중요하게 활용됩니다.

---

# 네이버 로그인 이해

네이버 스마트스토어센터 로그인 과정에서 진행되는 네이버 로그인은   
일반적인 네이버 로그인과는 다른 과정으로 진행됩니다.

따라서 우선 일반적인 네이버 로그인 과정을 알아보겠습니다.

해당 파트는 아래 게시글을 참고해 작성되었습니다.

> [파이썬#76 - 파이썬 크롤링 requests 로 네이버 로그인 하기](https://blog.naver.com/PostView.naver?blogId=nkj2001&logNo=222722322802)

## 네이버 로그인 요청 분석

네이버 로그인 과정을 분석하기 위해서는 우선 네이버 로그인을 요청을 시도하여   
전달되는 값을 확인해야 합니다.

네이버 로그인 페이지에서 로그인을 수행하는 과정에서   
발견할 수 있는 POST 요청을 살펴보면 다음과 같은 데이터가 전달됨을 발견할 수 있습니다.

![nid-login](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/nid-login.png?raw=true)

암호화된 값을 생략하고 키로 전달되는 내용을 확인하면 다음과 같습니다.

```json
{
    "localechange": "",
    "dynamicKey": "...",
    "encpw": "...",
    "enctp": 1,
    "svctype": 1,
    "smart_LEVEL": 1,
    "bvsd": {
        "uuid": "...",
        "encData": "..."
    },
    "encnm": "...",
    "locale": "ko_KR",
    "url": "https://www.naver.com",
    "id": "",
    "pw": ""
}
```

공백이나 고정된 값을 가진 키를 제외하면 결과적으로   
`dynamicKey`, `encpw`, `bvsd`, `encnm`를 밝혀내는 것이 중요할 것이라 판단됩니다.

## 네이버 로그인 폼 분석

키의 명칭만으로는 무엇을 의미하는지 알 수 없기 때문에   
로그인 페이지 소스에서 키명칭을 검색하였고 네이버 로그인 폼에서 하나의 단서를 찾을 수 있었습니다.

![nid-form](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/nid-form.png?raw=true)

`dynamicKey`의 경우 로그인 폼에 동적으로 부여되는 값임을 알 수 있습니다.   
하지만 나머지 `encpw`, `bvsd`, `encnm`의 값은 비어있기 때문에   
다른 자바스크립트 응답을 분석해야 합니다.

## 네이버 로그인 RSA 암호화

`encpw` 값에 대한 단서를 찾기 위해 전체 검색을 수행했을 때   
`common_202201.js` 내부에서 RSA 암호화 처리를 통해 값을 생성함을 알 수 있습니다.   
그 중에서 가장 처음 단계로 실행될 것이라 추측되는 것이 아래 `confirmSubmit()` 함수입니다.

![encpw](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/encpw.png?raw=true)

해당 함수는 아이디와 비밀번호의 여부를 체크하고 `encryptIdPw()` 함수의 결과를 반환합니다.   
바로 밑에서 확인할 수 있는 `encryptIdPw()` 함수의 내용은 다음과 같습니다.

```js
function encryptIdPw() {
	var id = $("id");
	var pw = $("pw");
	var encpw = $("encpw");
	var rsa = new RSAKey;

	if (keySplit(session_keys)) {
		rsa.setPublic(evalue, nvalue);
		try{
			encpw.value = rsa.encrypt(
				getLenChar(sessionkey) + sessionkey +
				getLenChar(id.value) + id.value +
				getLenChar(pw.value) + pw.value);
		} catch(e) {
			return false;
		}
		$('enctp').value = 1;
		id.value = "";
		pw.value = "";
		return true;
	}
	else
	{
		getKeyByRuntimeInclude();
		return false;
	}

	return false;
}
```

해당 함수는 `session_keys`라는 값을 처리하고 RSA 암호화한 결과를   
`encpw`의 값으로 대체하는 것을 알 수 있습니다.

마찬가지로 해당 명칭을 검색했을 때   
`session_keys`는 Ajax 통신의 응답 결과를 받아오는 것을 확인할 수 있습니다.

![session-keys](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/session-keys.png?raw=true)

하지만 네이버 로그인 페이지에서 `svctype=262144`를 추가적인 파라미터로 입력할 경우   
접근할 수 있는 모바일 로그인 페이지에서 해당 값을 확인할 수 있었습니다.

![nid-mlogin](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/nid-mlogin.png?raw=true)

다시 `encryptIdPw()` 함수로 돌아가서 `session_keys`를 처리하기 위해   
`keySplit()` 함수를 찾아보았습니다.

```js
function keySplit(a) {
	keys = a.split(",");
	if (!a || !keys[0] || !keys[1] || !keys[2] || !keys[3]) {
		return false;
	}
	sessionkey = keys[0];
	keyname = keys[1];
	evalue = keys[2];
	nvalue = keys[3];
	$("encnm").value = keyname;
	return true
}
```

모바일 페이지에서 볼 수 있는 `session_keys` 값은 콤마를 기준으로   
4개의 값으로 구분되어 있었는데 해당 함수에서는 각각을   
`sessionKey`, `encnm`, `evalue`, `nvalue`으로 분리했습니다.

여기서 `encnm` 값을 우선적으로 가져올 수 있었고,   
다음으로 `encpw` 값을 찾기 위해 RSA 암호화 부분을 탐색해봅니다.

```js
rsa.setPublic(evalue, nvalue);
encpw.value = rsa.encrypt(
    getLenChar(sessionkey) + sessionkey +
    getLenChar(id.value) + id.value +
    getLenChar(pw.value) + pw.value);
```

`session_keys`에서 분리된 `evalue`와 `nvalue`로 RSA 공개키를 생성하고   
마찬가지로 `session_keys`에 포함된 `sessionKey` 및 아이디, 비밀번호의 조합을   
암호화한 결과가 `encpw`임을 확인할 수 있습니다.

파이썬에서는 공개키 생성을 `rsa.PublicKey()` 함수로 수행할 수 있으며   
`rsa.encrypt()` 함수로 RSA 암호화를 진행할 수 있습니다.   
해당 과정은 아래와 같이 구현됩니다.

```python
publicKey = rsa.PublicKey(int(nvalue,16), int(evalue,16))
value = ''.join([chr(len(key))+key for key in [sessionKey, id, pw]])
encpw = rsa.encrypt(value.encode(), publicKey).hex()
```

여기까지의 과정으로 `dynamicKey`, `encpw`, `encnm`의 값을 얻을 수 있습니다.

## bvsd 값 생성하기

마지막으로 필요한 `bvsd` 값에 대한 단서는 응답 문서 내에서   
`bvsd.1.3.8.min.js`란 명칭으로 알기 쉽게 확인할 수 있지만   
그 내용은 가독성 면에서 쉽게 해석하기 어려웠습니다.

다른 자료를 참고했을 때 `bvsd`는 브라우저가 정상적인지 여부를 파악하기 위한 값으로   
해당 값이 없을 경우 로그인 과정에서 캡차를 발생시킨다는 것을 알 수 있었습니다.

`bvsd.1.3.8.min.js`에서 주목할 부분은 `uuid` 및 `encData`를 생성하는 부분인데   
아래 코드에서 `encData`는 `o`라는 값을 인코딩하는 것으로 추측됩니다.

![bvsd](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/bvsd.png?raw=true)

`o` 값을 코드 내에서 찾아보니 아래와 같이 디바이스의 마우스 상태 등을   
기록한 값임을 확인할 수 있었습니다.

```js
o = {
    a: n,
    b: "1.3.8",
    c: (0, m["default"])(),
    d: r,
    e: this._deviceOrientation.get(),
    f: this._deviceMotion.get(),
    g: this._mouse.get(),
    j: this._fpDuration || y.NOT_YET,
    h: this._fpHash || "",
    i: this._fpComponent || []
};
```

하지만 각각의 값을 해석하고 생성하는 것은 쉽지 않았기에   
이미 완성된 코드를 참고하여 `set_bvsd()` 메소드를 정의했습니다.

`encData`의 인코딩에는 `lzstring` 모듈의   
`LZString.compressToEncodedURIComponent()` 함수를 활용했습니다.

```python
from lzstring import LZString
import uuid

ENC_DATA = lambda uuid, userid, passwd: str({
    "a": f"{uuid}-4",
    "b": "1.3.4",
    "d": [{
        "i": "id",
        "b": {"a": ["0", userid]},
        "d": userid,
        "e": "false",
        "f": "false"
    },
    {
        "i": passwd,
        "e": "true",
        "f": "false"
    }],
    "h": "1f",
    "i": {"a": "Mozilla/5.0"}
}).replace('\'','\"')

class NaverLogin(LoginSpider):
    def set_bvsd(self):
        uuid4 = str(uuid.uuid4())
        encData = LZString.compressToEncodedURIComponent(ENC_DATA(uuid4, self.userid, self.passwd))
        self.bvsd = str({"uuid":uuid4, "encData":encData}).replace('\'','\"')
```

---

# 네이버 로그인 구현

지금까지의 과정을 통해 네이버 로그인에 필요한   
`dynamicKey`, `encpw`, `bvsd`, `encnm` 값을 생성하는 법을 파악했습니다.

이를 `NaverLogin` 클래스의 메소드로 구현해보겠습니다.

## RSA 암호화 구현

먼저 `dynamicKey`와 함께 `encpw`, `encmn` 생성에 필요한   
`session_keys`를 가져오기 위한 메소드 `fetch_keys()`와,   
RSA 암호화를 통해 encpw 값을 구하는 `set_encpw()` 메소드를 정의합니다.

```python
from bs4 import BeautifulSoup
import rsa

LOGIN_URL = "https://nid.naver.com/nidlogin.login"

class NaverLogin(LoginSpider):
    def fetch_keys(self):
        response = self.get(LOGIN_URL, headers=self.get_headers(host=LOGIN_URL), params={"svctype":"262144"})
        source = BeautifulSoup(response.text, 'lxml')
        keys = source.find("input", {"id":"session_keys"}).attrs.get("value")
        self.sessionKey, self.encnm, n, e = keys.split(",")
        self.dynamicKey = source.find("input", {"id":"dynamicKey"}).attrs.get("value")
        self.publicKey = rsa.PublicKey(int(n,16), int(e,16))
```

`session_keys`의 경우 모바일 로그인 페이지에서만 가져올 수 있기 때문에   
`svctype=262144`를 GET 요청의 파라미터로 전달해 모바일 로그인 페이지를 가져옵니다.

`nvalue`와 `evalue`는 별도의 변수로 저장하지 않고   
`publicKey`를 생성해 클래스 변수로 저장합니다.

```python
class NaverLogin(LoginSpider):
    def set_encpw(self):
        value = "".join([chr(len(key))+key for key in [self.sessionKey, self.userid, self.passwd]])
        self.encpw = rsa.encrypt(value.encode(), self.publicKey).hex()
```

앞에서 가져온 `sessionKey`와 함께 미리 초기화된 네이버 아이디 및 비밀번호를   
조합 및 암호화하여 `encpw`를 생성합니다.

## POST 요청 구현

미리 정의한 `set_bvsd()` 메소드를 포함해 모든 준비 과정이 마무리되었습니다.

클래스 변수로 저장된 암호화된 값들을 데이터에 담아 POST 로그인 요청을 보내는   
`login()` 메소드는 다음과 같이 정의할 수 있습니다.

```python
NAVER_URL = "https://www.naver.com"

LOGIN_DATA = lambda dynamicKey, encpw, bvsd, encnm: {
    "localechange": "",
    "dynamicKey": dynamicKey,
    "encpw": encpw,
    "enctp": "1",
    "svctype": "1",
    "smart_LEVEL": "1",
    "bvsd": bvsd,
    "encnm": encnm,
    "locale": "ko_KR",
    "url": quote_plus(NAVER_URL),
    "id": "",
    "pw": "",
}

class NaverLogin(LoginSpider):
    def login(self):
        self.fetch_keys()
        self.set_encpw()
        self.set_bvsd()
        data = LOGIN_DATA(self.dynamicKey, self.encpw, self.bvsd, self.encnm)
        headers = self.get_headers(LOGIN_URL, referer=LOGIN_URL)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Upgrade-Insecure-Requests"] = "1"
        self.post(LOGIN_URL, data=data, headers=headers)
```

POST 요청 시 전달되었던 데이터와 동일한 값을 반환하는 `LOGIN_DATA` 함수를 생성하고   
암호화된 값을 전달해 최종적인 POST 데이터를 만들었습니다.

해당 데이터로 요청을 보낼 경우 정상적인 응답을 받게 되고   
`NaverLogin` 세션 객체의 쿠키 값을 확인하면 아래와 같은 결과를 확인할 수 있습니다.

```python
naver = NaverLogin("userid", "passwd")
naver.login()
naver.get_cookies()
======================================
'NID_AUT=...; NID_JKL=...; NID_SES=...; nid_inf=1228467713'
```

또한 해당 결과는 개발자 도구에서도 응답 헤더의 `set-cookie` 값에서 찾아볼 수 있습니다.   

![nid-cookies](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/nid-cookies.png?raw=true)

지금까지의 과정으로 네이버 로그인 과정을 거쳤을 때,   
게시글의 서두에서 언급한 쿠키 값의 목록 중에서 일부 값을 획득할 수 있습니다.

```python
cookies = {
    "NNB": "...",
    "nid_inf": "...",
    "NID_AUT": "...",
    "NID_SES": "...",
    "NID_JKL": "...",
    "CBI_SES": "...",
    "CBI_CHK": "...",
    "NSI": "...",
}
```

이 중에서 `NNB`의 경우 네이버 페이지 접속 시 기본적으로 부여되는 값이기 때문에 무시하고   
`NID_AUT`, `NID_JKL`, `NID_SES`가 채워졌습니다.

나머지 값들은 스마트스토어센터 로그인 과정에서 얻을 수 있기 때문에   
다음 게시글에서 다뤄보도록 하겠습니다.
