---
layout: post
title: "[Python] requests로 네이버 스마트스토어센터 로그인 구현하기 (3)"
date: 2022-12-04 10:22:03 +0900
categories: [Data, Crawling]
tags: [Crawling, Python, requests, Naver, 네이버, 스마트스토어, 스마트스토어센터, 로그인, 크롤링]
---

앞선 네이버 로그인 구현 과정을 통해 네이버 로그인에 대해 이해하고   
스마트스토어센터 로그인 결과로 얻을 수 있는 쿠키 값의 일부를 획득했습니다.

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

하지만, 스마트스토어센터에서 데이터를 가져오기 위해 필요한 쿠키 값은   
`CBI_SES`, `CBI_CHK`, `NSI` 세 가지 값이기 때문에   
지금까지는 준비 과정에 불과했다고 할 수 있습니다.

이번 게시글에서는 스마트스토어센터 로그인 과정을 이해하고   
직접 구현해보면서 `SmartstoreLogin` 클래스를 완성해보겠습니다.

---

# 스마트스토어센터 로그인 이해

지금까지 스마트스토어센터의 두 가지 로그인 방식 중   
네이버 로그인 방식으로 로그인을 수행하기 위해,   
실제 네이버 로그인에 대한 이해 및 구현을 진행했습니다.

## 요청 내역 탐색 시 주의사항

새 창에서 띄워지는 네이버 로그인 페이지는   
로그인이 완료되면 닫혀버리기 때문에 네트워크 요청 내역을 확인하기 어렵습니다.

이 경우 개발자 도구 Sources 탭에서 Event Listener Breakpoints 메뉴 아래   
Window > window.close 부분을 선택하면 창이 닫히는 순간에 중단시킬 수 있습니다.

![breakpoints](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/breakpoints.png?raw=true)

## 네이버 로그인과의 차이점

스마트스토어센터 로그인에서의 네이버 로그인은 기존 방식과 다소의 차이점이 존재합니다.

아래는 스마트스토어센터 로그인 POST 요청에서 확인할 수 있는 데이터입니다.

```json
{
    "localechange": "",
    "dynamicKey": "...",
    "logintp": "oauth2",
    "encpw": "...",
    "enctp": 1,
    "svctype": 64,
    "smart_LEVEL": 1,
    "bvsd": {
        "uuid":"...",
        "encData":"..."
    },
    "encnm": "...",
    "locale": "ko_KR",
    "client_id": "...",
    "url": "https://nid.naver.com/oauth2.0/authorize?response_type=code&state=...&client_id=...&redirect_uri=https%3A%2F%2Faccounts.commerce.naver.com%2Foauth%2Fcallback&locale=ko_KR&inapp_view=&oauth_os=",
    "id": "",
    "pw": ""
}
```

기존의 네이버 로그인 데이터와 비교했을 때 3개의 값이 추가되었음을 알 수 있습니다.

`logintp`의 경우 `"oauth2"`로 고정된 값으로 보이지만,   
`url` 내 `state`와 `client_id`는 지금까지의 과정에서는 얻을 수 없었던   
새로운 값으로 로그인을 위해 추가적인 동작이 필요해 보입니다.

## OAuth URL 가져오기

`state`와 `client_id`의 경우 네이버 로그인 페이지를 불러오는 과정에서   
이미 전달되는 값이기 때문에 해당 페이지 안에서는 출처를 찾을 수 없었습니다.

따라서 네이버 로그인 페이지로 이동하기 위해 거치는 스마트스토어센터 로그인 페이지에서   
네이버 로그인 페이지를 띄우는 과정에 집중하여 두 값이 발생하는 지점을 찾아보았고,   
graphql 주소로 보낸 POST 요청에 대한 응답으로 `url`에 해당하는 `authUrl` 값을 받는 것을 확인했습니다.

![auth-url](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/auth-url.png?raw=true)

이렇게 구한 `client_id` 및 `url` 값을 로그인 데이터에 담아 요청을 보낼 경우   
일반적인 네이버 로그인 결과로 얻을 수 있는 `NID_AUT` 등의 쿠키 값을 획득할 수 있습니다.

## GraphQL 로그인 분석

스마트스토어센터 로그인은 네이버 로그인에서 그치지 않고   
`CBI_SES`, `CBI_CHK`, `NSI` 쿠키 값을 추가로 얻어야 합니다.

이 중에서 `CBI_SES`를 응답 파일 내에서 검색했을 때 graphql 주소에 대한 응답으로   
`CBI_SES`와 `CBI_CHK` 값을 반환하는 것을 알 수 있었습니다.

해당 주소는 앞서 인증 주소를 가져오는 과정에서 보았던 것인데   
당시 `snsLoginBegin`라는 명칭의 쿼리와는 다른 `snsLoginCallback` 쿼리를 사용하여   
추가적인 로그인을 수행하는 것임을 짐작할 수 있습니다.

![graphql](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/graphql.png?raw=true)

변수로 전달되는 `state`의 경우 앞에서 구한 것과 동일한 값이지만,   
`code`는 아직까지 본 적 없는 값입니다.

하지만, `code`는 어떠한 응답 파일 내에서도 출처를 찾아볼 수 없고,   
`code`의 값 자체를 검색했을 때 `oauth_token`이라는 키와 동일한 값을 사용한다는 것 말고는   
별다른 단서를 찾을 수 없었습니다.

이 경우 네이버 로그인 후에 연속적으로 진행되는 다른 요청 내역을 직접 들여다봐야 했고,   
다행히 바로 아래의 주소에 대한 응답 내역에서 `oauth_token` 값을 받아볼 수 있었습니다.

![oauth-token](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/oauth-token.png?raw=true)

```html
<html>
<script language=javascript nonce="4SzeR1mCGzDbnzr3s5rjQ1Li">
location.replace("https://nid.naver.com/login/noauth/allow_oauth.nhn?oauth_token=...&with_pin&step=agree_term&inapp_view=&oauth_os=");
</script>
</html>
```

`oauth_token`의 값을 `code`에 넣어서 `state`와 함께 graphql 주소에 요청할 경우   
응답 헤더의 `Set-Cookie`에서 볼 수 있는 `CBI_SES`와 `CBI_CHK`를 받게 됩니다.

## 2단계 인증 분석

스마트스토어센터는 최초 로그인 시 반드시 2단계 인증을 거쳐야 합니다.

![two-login](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/two-login.png?raw=true)

마지막 남은 `NSI` 값 또한 해당 2단계 인증을 거쳐야 얻을 수 있을 것이라 걱정했지만,   
다행히 2단계 인증을 거치지 않아도 네트워크 응답 내역에서 `NSI`를 확인할 수 있었습니다.

![two-factor](https://github.com/minyeamer/til/blob/main/.media/data/crawling/smartstore-login/two-factor.png?raw=true)

POST 요청이지만 전달되는 데이터는 아래와 같이 단순했기에   
추가적인 분석 없이 마지막 `NSI` 값을 획득했습니다.

```json
{"url": "https://sell.smartstore.naver.com/#/home/dashboard"}
```

---

# 스마트스토어센터 로그인 구현

지금까지의 과정을 통해 스마트스토어센터에서 데이터를 가져오기 위해 필요한
`CBI_SES`, `CBI_CHK`, `NSI` 값을 획득하는 방법을 파악했습니다.

이를 `SmartstoreLogin` 클래스의 메소드로 구현해보겠습니다.

## 네이버 로그인 구현

기존의 네이버 로그인 기능에 OAuth URL을 가져오는 부분을 추가시킨   
`nid_login()` 및 `fetch_oauth_url()` 메소드를 정의합니다.

```python
SMARTSTORE_URL = "https://sell.smartstore.naver.com/"
SLOGIN_URL = "https://accounts.commerce.naver.com"

GRAPHQL_DATA = str({
    "operationName": "snsLoginBegin",
    "variables": {
        "mode": "login",
        "snsCd": "naver",
        "svcUrl": "https://sell.smartstore.naver.com/#/login-callback"},
    "query": "mutation snsLoginBegin($mode: String!, $snsCd: String!, $svcUrl: String!, \
$oneTimeLoginSessionKey: String, $userInfos: [UserInfoEntry!]) {\n  snsBegin(\n    \
snsLoginBeginRequest: {mode: $mode, snsCd: $snsCd, svcUrl: $svcUrl, oneTimeLoginSessionKey: \
$oneTimeLoginSessionKey, userInfos: $userInfos}\n  ) {\n    authUrl\n    __typename\n  }\n}\n"
}).replace('\'','\"')

class SmartstoreLogin(NaverLogin):
    def fetch_oauth_url(self):
        referer = f"{SLOGIN_URL}/login?url={SMARTSTORE_URL}#/login-callback"
        headers = self.get_headers(host=SLOGIN_URL, referer=referer)
        response = self.post(urljoin(SLOGIN_URL, "graphql"), data=GRAPHQL_DATA, headers=headers)
        self.oauth_url = json.loads(response.text)["data"]["snsBegin"]["authUrl"]
        self.oauth_params = {k:v.pop() for k,v in parse_qs(urlparse(self.oauth_url).query).items()}
        if "auth_type" in self.oauth_params: self.oauth_params.pop("auth_type")
        self.oauth_params = dict(self.oauth_params, **{"locale":"ko_KR","inapp_view":'',"oauth_os":''})
```

graphql 주소에 대한 요청 데이터를 그대로 구현한 것이 GRAPHQL_DATA이며,   
그 결과로 OAuth URL을 얻을 수 있습니다.

OAuth URL의 파라미터는 향후 GraphQL 인증 과정에서 재활용되기 때문에   
`oauth_params` 변수에 저장해둡니다.

```python
LOGIN_URL = "https://nid.naver.com/nidlogin.login"

SLOGIN_DATA = lambda dynamicKey, encpw, bvsd, encnm, client_id: \
    dict(LOGIN_DATA(dynamicKey, encpw, bvsd, encnm),
        **{"logintp":"oauth2","svctype":"64","client_id":client_id})

class SmartstoreLogin(NaverLogin):
    def nid_login(self):
        self.fetch_keys()
        self.set_encpw()
        self.set_bvsd()
        self.fetch_oauth_url()
        data = SLOGIN_DATA(self.dynamicKey, self.encpw, self.bvsd, self.encnm, self.oauth_params.get("client_id"))
        headers = self.get_headers(LOGIN_URL, referer=self.oauth_url)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Upgrade-Insecure-Requests"] = "1"
        response = self.post(LOGIN_URL, data=data, headers=headers)
```

네이버 로그인 과정에서는 `bvsd`를 생성한 후 OAuth URL을 추가로 가져오고   
`client_id`를 기존의 로그인 데이터 내에 포함시켜 POST 요청을 보냅니다.

해당 메소드의 결과로 `NID_AUT`, `NID_JKL`, `NID_SES`를 부여받을 수 있습니다.

## OAuth 로그인 구현

OAuth 로그인은 네이버 로그인과 GraphQL 인증으로 구성됩니다.

현시점에서 GraphQL 인증에 필요한 것은 `oauth_token` 뿐이기 때문에   
앞선 네이버 로그인 과정에서 획득한 주소로부터 `oauth_token`을 가져오는 메소드 `fetch_oauth_token()`과   
전체적인 OAuth 로그인 과정을 구현한 `oauth_login()` 메소드를 정의합니다.

```python
OAUTH_URL = "https://nid.naver.com/oauth2.0/authorize"

class SmartstoreLogin(NaverLogin):
    def fetch_oauth_token(self):
        headers = self.get_headers(LOGIN_URL, referer=LOGIN_URL, cookies=self.get_cookies())
        response = self.get(OAUTH_URL, headers=headers, params=self.oauth_params)
        if re.search("(?<=oauth_token\=)(.*?)(?=&)", response.text):
            self.oauth_token = re.search("(?<=oauth_token\=)(.*?)(?=&)", response.text).group()
```

```python
OAUTH_DATA = lambda code, state: str({
    "operationName":"snsLoginCallback",
    "variables": {
        "code": code,
        "state": state},
    "query":"mutation snsLoginCallback($code: String!, $state: String!) \
{\n  snsCallback(snsLoginCallbackRequest: {code: $code, state: $state}) \
{\n    statCd\n    loginStatus\n    nextUrl\n    sessionKey\n    snsCd\n    \
idNo\n    realnm\n    age\n    email\n    __typename\n  }\n}\n"
}).replace('\'','\"')

class SmartstoreLogin(NaverLogin):
    def oauth_login(self):
        self.nid_login()
        self.fetch_oauth_token()
        code, state = self.oauth_token, self.oauth_params.get("state")
        referer = SLOGIN_URL+f"/oauth/callback?code={code}&state={state}"
        headers = self.get_headers(host=SLOGIN_URL, referer=referer, cookies=self.get_cookies())
        response = self.post(urljoin(SLOGIN_URL, "graphql"), data=OAUTH_DATA(code, state), headers=headers)
```

## 2단계 인증 구현

2단계 인증을 직접 수행할 필요는 없습니다.

`NSI` 쿠키 값을 할당받을 수 있는 주소로 POST 요청을 보내는   
`two_factor_login()` 메소드를 정의합니다.

```python
TWOLOGIN_URL = SMARTSTORE_URL+"api/login?url=https%3A%2F%2Fsell.smartstore.naver.com%2F%23%2Fhome%2Fdashboard"

TWOLOGIN_DATA = {"url": "https://sell.smartstore.naver.com/#/home/dashboard"}

class SmartstoreLogin(NaverLogin):
    def two_factor_login(self):
        headers = self.get_headers(SMARTSTORE_URL, referer=SMARTSTORE_URL, cookies=self.get_cookies())
        headers["Content-Type"] = "application/json;charset=UTF-8"
        headers["x-current-state"] = "https://sell.smartstore.naver.com/#/login-callback"
        headers["x-current-statename"] = "login-callback"
        headers["x-to-statename"] = "login-callback"
        response = self.post(TWOLOGIN_URL, data=TWOLOGIN_DATA, headers=headers)
```

## 로그인 메소드 구현

`SmartstoreLogin` 객체를 사용할 때는 `login()` 메소드를 활용합니다.

```python
class SmartstoreLogin(NaverLogin):
    def login(self):
        email_pattern = re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self.seller_login() if email_pattern.search(self.userid) else self.oauth_login()
        self.two_factor_login()
```

향후 판매자 계정으로 로그인 하는 경우를 고려해   
`userid`가 이메일인 경우 `seller_login()` 이라는 미구현된 메소드를 실행하도록 정의했습니다.

일반적인 네이버 아이디를 사용할 경우엔 OAuth 로그인과 2단계 인증을 거쳐   
처음 목적으로 했던 아래의 모든 쿠키 값을 획득하게 됩니다.

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

해당 쿠키를 가진 `SmartstoreLogin` 객체를 세션 객체로 활용한다면   
스마트스토어센터 내 어떤 데이터라도 파이썬 `requests` 모듈로 가져올 수 있게 됩니다.
