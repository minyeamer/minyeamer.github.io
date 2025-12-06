---
title: "Apache Airflow - REST API 연동과 Custom Operator 구현"
date: "2025-06-07T12:50:14+09:00"
layout: "post"
description: >
  Apache Airflow의 HttpOperator와 Custom Operator 개념을 소개하고, 네이버 Open API 연동과 BaseOperator 상속을 단계별로 안내합니다.
  REST API 호출, Connection 설정, Variable 활용, CSV 파일 저장, NaverSearchToCsvOperator 구현까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&dl=0"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "HttpOperator", "BaseOperator", "REST API", "네이버 Open API", "Custom Operator", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
---

## HttpOperator

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-http/stable/index.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- HTTP 요청을 하고 응답 결과를 반환받는 Operator (반환값은 XCom에 저장)
- HTTP를 이용하여 API를 처리하는 RestAPI 호출 시 사용 가능

### Provider 패키지 설치
- `HttpOperator` 는 Provider 패키지로 별도의 설치가 필요
- 5.3.0 버전을 기준으로 `apache-airflow>=2.10.0` 버전을 요구

```bash
pip install apache-airflow-providers-http
```

### HttpOperator 파라미터

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/operators/http/index.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- `http_conn_id` : http Connection을 생성해야 하는데 해당 Connection의 ID
- `endpoint` : Connection에 등록한 Host 뒤에 붙는 경로
- `method` : HTTP 메서드 (GET, POST, PUT, DELETE 등)
- `data` : POST 요청 시 전달할 데이터 또는 GET 요청 시 전달할 파라미터
- `headers` : HTTP 요청 헤더
- `response_check` : HTTP 응답 결과가 정상인지 확인하는 함수 (`True` 반환)
- `response_filter` : HTTP 응답 결과에 대한 전처리 함수

## 네이버 쇼핑 검색 API

{{< bookmark
  url="https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md"
  image="https://dl.dropboxusercontent.com/scl/fi/x4x2s1wylgkwatfygk09z/naver-developers.webp?rlkey=z10lqzacm268bma2enhqbej0g&dl=0" >}}

- `HttpOperator` 활용을 위해 간단한 API를 예제로 사용
- 네이버 쇼핑 검색 API는 네이버에서 제공하는 Open API 중 하나로 네이버 쇼핑 페이지에서 검색한 결과를 XML 형식 또는 JSON 형식으로 반환하는 RestAPI
- 하나의 키워드를 전달하여 정확도순으로 1위에 노출되는 상품 정보를 출력하는 기능을 구현

### API 키 생성
- [네이버 개발자 센터](https://developers.naver.com/main/)에서 로그인 후 상단의 메뉴 중 `Application->애플리케이션 등록` 으로 이동
- 아래 이미지와 같이 사용 API로 "검색"을 선택하고, 임의로 애플리케이션 이름과 서비스 환경을 입력하여 애플리케이션 등록

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/077ryedn6nmsmd7xnb1xy/airflow-42-naver-openapi-register.webp?rlkey=8e0iylgt9z8ze8snge38nbaky&dl=0"
  alt="애플리케이션 등록 (API 이용신청)"
  max-width="691px"
  align="center" >}}

- 생성한 애플리케이션 정보에서 `Client ID` 와 `Client Secret` 을 조회 가능

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/yxvxn3o30wvxip6cyy40b/airflow-43-naver-openapi-info.webp?rlkey=skjpbqiydx1e4if1octvkef4a&dl=0"
  alt="애플리케이션 정보 - Client ID, Client Secret"
  max-width="691px"
  align="center" >}}

### Connection 추가
- [문서에 명시된 요청 URL](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md#%EC%9A%94%EC%B2%AD-url)을
  참고하여 `Host` 를 입력
- API가 별도로 알려지지 않은 포트를 사용할 경우 `Port` 에 포트 번호를 입력하지만, 네이버 Open API는 표준 HTTPS 포트를 사용하기 때문에 미표기

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/yk6vu7a970ulpe7m1fog5/airflow-44-http-connection.webp?rlkey=5l6wya7grf6757xubjmcfid2w&dl=0"
  alt="Edit Connection - HTTP"
  max-width="691px"
  align="center" >}}

### Variable 추가
- API키는 Variable로 추가하는데, `Client ID` 와 `Client Secret` 을 각각의 Variable로 등록
- `Client Secret` 의 키 명칭에는 "secret" 이 포함되어 UI에서 자동으로 마스킹 처리되는 것을 확인

![Variables - 애플리케이션 정보](https://dl.dropboxusercontent.com/scl/fi/t27j9mfzzmve67j5oflj1/airflow-45-naver-openapi-variables.webp?rlkey=3tj9lslxgqltobx9yuesp1xe1&dl=0)

### HttpOperator 활용 예시
- 앞서 등록한 Connection의 ID를 `http_conn_id` 에 입력하고, `endpoint` 에 Host를 제외한 나머지 경로를 입력
- `data` 에는 GET 요청에 대한 파라미터를 전달하는데, `query` 로 원하는 키워드를 입력
- `headers` 에는 Jinja 템플릿을 활용하여 `Client ID` 와 `Client Secret` 에 대한 Variable 값을 추가
- HTTPS 요청 후 반환되는 `Response` 객체를 JSON 파싱하여 `items` 배열 내 첫 번째 항목, 즉 "노트북" 키워드로 검색한 결과에서 1위로 노출되는 상품을 딕셔너리 타입으로 반환
- 다음 단계의 Task `print_product_task` 에서는 XCom에서 반환된 값을 꺼내 단순 출력

```python
# dags/http_operator.py

from airflow.sdk import DAG, task
from airflow.providers.http.operators.http import HttpOperator
from airflow.models.taskinstance import TaskInstance
import pendulum

with DAG(
    dag_id="http_operator",
    start_date=pendulum.datetime(2025, 6, 1, tz="Asia/Seoul"),
    schedule=None,
    catchup=False,
    tags=["example", "http"],
) as dag:
    def parse(response):
        return response.json()["items"][0]

    nshopping_search_task = HttpOperator(
        task_id="nshopping_search_task",
        http_conn_id="openapi.naver.com",
        endpoint="/v1/search/shop.json",
        method="GET",
        data={
            "query": "노트북",
            "display": 10,
            "start": 1,
            "sort": "sim"
        },
        headers={
            "Content-Type": "application/json",
            "X-Naver-Client-Id": "{{var.value.client_id_openapi_naver_com}}",
            "X-Naver-Client-Secret": "{{var.value.client_secret_openapi_naver_com}}"
        },
        response_filter=parse
    )

    @task(task_id="print_product_task")
    def print_product_task(ti: TaskInstance, **kwargs):
        result = ti.xcom_pull(task_ids="nshopping_search_task")
        from pprint import pprint
        pprint(result)

    nshopping_search_task >> print_product_task()
```

- DAG 실행 후 `print_product_task` 의 실행 로그를 확인했을 때, 아래와 같이 `nshopping_search_task` 에서 반환된 상품에 대한 정보를 조회 가능

```bash
# print_product_task

[2025-06-07, 12:33:35] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-07, 12:33:35] INFO - Filling up the DagBag from /opt/airflow/dags/http_operator.py: source="airflow.models.dagbag.DagBag"
[2025-06-07, 12:33:35] INFO - {'brand': '갤럭시북',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'category1': '디지털/가전',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'category2': '노트북',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'category3': '',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'category4': '',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'hprice': '',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'image': 'https://shopping-phinf.pstatic.net/main_8795238/87952389253.11.jpg',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'link': 'https://smartstore.naver.com/main/products/10407884292',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'lprice': '428000',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'maker': '삼성전자',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'mallName': '삼성공식파트너 코인비엠에스',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'productId': '87952389253',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'productType': '2',: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO -  'title': '삼성 갤럭시북 인강용 사무용 업무용 가성비 윈도우11 저가 싼 태블릿 <b>노트북</b> 추천 기본팩'}: chan="stdout": source="task"
[2025-06-07, 12:33:35] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.decorators.python._PythonDecoratedOperator"
```

## Custom Operator

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/howto/custom-operator.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

### BaseOperator
- `BaseOperator` 클래스를 상속받아 직접 만든 Operator를 사용 가능
- `BaseOperator` 상속 시 두 가지 메서드를 재정의(Overriding)해야 함
   1. `def __int__(self, *args, **kwargs)`
      - 객체 생성 시 초기화하는 과정을 구현 (명시하지 않은 파라미터는 `kwargs`에 포함)
   2. `def execute(self, context)`
      - Operator 실행 시 호출되는 메서드로 비즈니스 로직을 구현
   3. `template_fields: Sequence[str] = ("name",)`
      - Jinja template을 적용할 파라미터를 지정

```python
class HelloOperator(BaseOperator):
    template_fields: Sequence[str] = ("name",)

    def __init__(self, name: str, world: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.world = world

    def execute(self, context):
        message = f"Hello {self.world} it's {self.name}!"
        print(message)
        return message
```

### HttpOperator 개선점 파악

1. 주요 문제점은 네이버 쇼핑 검색 API의 표시 결과가 최대 100개로 제한되는 것으로, 더 많은 결과를 보려면 파라미터의 `start` 값을 다르게 한 여러 개의 HttpOperator를 만들어야 함
   - `execute()` 메서드 안에서 전체 요청을 100개 단위로 나누고, 반복문을 통해 여러 번 요청 및 응답 결과를 합칠 수 있게 로직을 작성
2. 기존엔 `endpoint` 를 전부 입력해야 했는데, API 종류를 구분할 수 있는 문자열만 전달해서 `endpoint` 를 자동으로 만들어주면 더 편리할 것이라 생각함
   - `endpoint` 변경이 용이하기 때문에 쇼핑 검색 뿐 아니라 블로그 검색도 같이 수행할 것을 고려
3. 기존엔 JSON 파싱한 결과를 그대로 반환했는데, 로컬 경로에 CSV 파일로 저장하면 결과를 확인하기 더 쉬울 것이라 생각함

### Operator 기능 정의

> 네이버 쇼핑 및 블로그 검색 API를 호출하여 전체 데이터를 받은 후 CSV 파일로 저장하기

## NaverSearchToCsvOperator

- `BaseOperator` 를 상속받는 `NaverSearchToCsvOperator` 를 구현
- Operator 재사용을 위해 `plugins/` 경로 아래에 추가

```python
# plugins/operators/nshopping.py

from airflow.models import BaseOperator
from airflow.hooks.base import BaseHook
from typing import Dict, List

class NaverSearchToCsvOperator(BaseOperator):
    template_fields = ("file_path", "client_id", "client_secret")

    def __init__(self,
            search_type: str,
            file_path: str,
            client_id: str,
            client_secret: str,
            keyword: str,
            display: int = 10,
            start: int = 1,
            sort = "sim",
            **kwargs):
        super().__init__(**kwargs)
        self.http_conn_id = "openapi.naver.com"
        self.endpoint = f"/v1/search/{search_type}.json"
        self.method = "GET"
        self.file_path = file_path if file_path.startswith("/") else ("/opt/airflow/files/"+file_path)
        self.client_id = client_id
        self.client_secret = client_secret
        self.keyword = keyword
        self.display = min(display, 1000)
        self.start = min(start, 1000)
        self.sort = sort

    def execute(self, context):
        connection = BaseHook.get_connection(self.http_conn_id)
        url = connection.host + self.endpoint
        rows = list()
        for i, start in enumerate(range(self.start, self.display, 100)):
            display = min(self.display + self.start - start, 100)
            self.log.info(f"시작: {start}")
            self.log.info(f"끝: {start+display-1}")
            kwargs = dict(keyword=self.keyword, display=display, start=start, sort=self.sort)
            rows = rows + self._request_api(url, show_header=(i == 0), **kwargs)
        self._mkdir(self.file_path)
        self._to_csv(rows, self.file_path, encoding="utf-8", sep=',')

    def _request_api(self, url: str, keyword: str, display: int=10, start: int=1, sort="sim", show_header=True) -> List[List]:
        import requests
        params = self._get_params(keyword, display, start, sort)
        headers = self._get_headers(self.client_id, self.client_secret)
        with requests.request(self.method, url, params=params, headers=headers) as response:
            return self._parse_api(response, start, show_header)

    def _get_params(self, keyword: str, display: int=10, start: int=1, sort="sim") -> Dict:
        return {"query": keyword, "display": min(display, 100), "start": min(start, 1000), "sort": sort}

    def _get_headers(self, client_id: str, client_secret: str) -> Dict[str,str]:
        return {
            "Content-Type": "application/json",
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    def _parse_api(self, response, start: int=1, show_header=True) -> List[List]:
        contents = response.json()["items"]
        if contents:
            header = ([["rank"] + list(contents[0].keys())]) if show_header else []
            return header + [[start+i]+list(content.values()) for i, content in enumerate(contents)]
        else: return list()

    def _mkdir(self, file_path: str):
        import os
        dir_path = os.path.split(file_path)[0]
        if not os.path.exists(dir_path):
            os.system(f"mkdir -p {dir_path}")

    def _to_csv(self, rows: List[List], file_path: str, encoding="utf-8", sep=','):
        def clean(value: str) -> str:
            return str(value).replace(sep, '')
        with open(file_path, 'w', encoding=encoding) as file:
            for row in rows:
                file.write(sep.join(map(clean, row))+'\n')
```

### 초기화 파라미터

**`search_type: str`**
- 네이버 쇼핑 검색 API의 `endpoint` 는 `/v1/search/shop.json` 인데, 블로그 검색 또는 뉴스 검색과 같은 다른 API를 확인했을 때, URL에서 `{{host}}/v1/search/{{search_type}}.json` 와 같은 패턴이 있음을 확인 가능
- 따라서, `endpoint` 대신에 `search_type` 을 입력으로 받고 `endpoint` 를 자동으로 생성

**`file_path: str`**
- `naverSearch/` 경로 아래 실행 날짜별로 폴더를 만들어서 아래에 CSV 파일을 저장할 계획인데, `data_interval_end` 변수를 사용하기 위해 `template_fields` 에 해당 파라미터를 등록
- Root(`/`) 경로를 지정하지 않았을 경우 `/opt/airflow/files` 경로를 Root 경로로 사용하도록 지정
- 이 때, Airflow 웹서버 컨테이너에 파일을 저장해도 로컬 컴퓨터에서 확인할 수 없기 때문에 `docker-compose.yaml` 파일에 컨테이너와 로컬 컴퓨터 경로를 연결짓는 구문을 입력
   ```yaml
   # docker-compose.yaml
   
   x-airflow-common:
     volumes:
       - ${AIRFLOW_PROJ_DIR:-.}/files:/opt/airflow/files
   ```

**`client_id: str`, `client_secret: str`**
- 두 개의 API 계정 정보 또한 Variable에서 값을 꺼내오기 때문에 `template_fields` 에 등록
- 요청 헤더에 게정 정보를 추가하기 위해 사용

**`keyword: str`, `display: int`, `start: int`, `sort: str`**
- API 요청 파라미터를 구성하는 대표적인 키값을 입력 받음
- `display` 는 최대 100까지 허용되지만, 반복문을 통해 나눠서 요청할 수 있기 때문에 1000까지 확장
- `start` 는 API 문서에 명세된 것과 같이 최대 1000까지의 값으로 제한
- `sort` 는 API 종류에 따라 허용되는 값이 다르지만, 공통적으로 정확도순 정렬(`sim`)을 사용할 것이기에 별도로 검증하지 않음

```python
template_fields = ("file_path", "client_id", "client_secret")

def __init__(self,
        search_type: str,
        file_path: str,
        client_id: str,
        client_secret: str,
        keyword: str,
        display: int = 10,
        start: int = 1,
        sort = "sim",
        **kwargs):
    super().__init__(**kwargs)
    self.http_conn_id = "openapi.naver.com"
    self.endpoint = f"/v1/search/{search_type}.json"
    self.method = "GET"
    self.file_path = file_path if file_path.startswith("/") else ("/opt/airflow/files/"+file_path)
    self.client_id = client_id
    self.client_secret = client_secret
    self.keyword = keyword
    self.display = min(display, 1000)
    self.start = min(start, 1000)
    self.sort = sort
```

### API 요청 메서드

**`execute()`**
- 고정된 Connection ID를 가지고 Connection에 등록된 Host를 조회
- Host와 `endpoint` 를 조합하여 API 요청 URL을 생성
- `start` 부터 `display` 까지의 범위를 100개 단위로 구분하여 반복문을 구성하고, 반복문마다 파라미터를 다르게 하여 API 요청 메서드 `_request_api()` 에 전달

```python
def execute(self, context):
    connection = BaseHook.get_connection(self.http_conn_id)
    url = connection.host + self.endpoint
    rows = list()
    for i, start in enumerate(range(self.start, self.display, 100)):
        display = min(self.display + self.start - start, 100)
        self.log.info(f"시작: {start}")
        self.log.info(f"끝: {start+display-1}")
        kwargs = dict(keyword=self.keyword, display=display, start=start, sort=self.sort)
        rows = rows + self._request_api(url, show_header=(i == 0), **kwargs)
        ...
```

**`_request_api()`**
- 직접적으로 API에 요청을 보내는 메서드
- 다른 메서드를 통해 파라미터와 헤더를 만들고, 전달받은 URL에 대해 GET 요청을 보냄
- 응답 결과인 `requests.Response` 객체를 그대로 파싱 메서드 `_parse_api()` 로 전달

```python
def _request_api(self, url: str, keyword: str, display: int=10, start: int=1, sort="sim", show_header=True) -> List[List]:
    import requests
    params = self._get_params(keyword, display, start, sort)
    headers = self._get_headers(self.client_id, self.client_secret)
    with requests.request(self.method, url, params=params, headers=headers) as response:
        return self._parse_api(response, start, show_header)
```

**`_get_params()`**
- 전달받은 파라미터를 딕셔너리 객체로 맵핑하여 반환하는 메서드

```python
def _get_params(self, keyword: str, display: int=10, start: int=1, sort="sim") -> Dict:
    return {"query": keyword, "display": min(display, 100), "start": min(start, 1000), "sort": sort}
```

**`_get_headers()`**
- API 계정 정보를 추가한 요청 헤더를 딕셔너리 객체로 반환하는 메서드

```python
def _get_headers(self, client_id: str, client_secret: str) -> Dict[str,str]:
    return {
        "Content-Type": "application/json",
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
```

### API 응답 결과 파싱 메서드

**`execute()`**
- 반복문 밖에서 리스트 객체 `rows` 를 만들고, 반복문마다 `_request_api()` 메서드가 반환하는 각각의 리스트 객체를 하나로 결합
- 첫 번째 반복문에서만 CSV의 헤더를 표시하기 위해 `show_header` 파라미터를 활용

```python
def execute(self, context):
    ...
    rows = list()
    for start in range(self.start, self.display, 100):
        ...
        rows = rows + self._request_api(url, show_header=(i == 0), **kwargs)
    ...
```

**`_parse_api()`**
- `requests.Response` 객체를 인수로 전달받아 JSON 파싱한 후 `items` 키에서 배열을 꺼냄
- CSV 파일로 저장하기 편한 구조로 가공하기 위해 딕셔너리에서 값만 꺼내 배열로 구성
- `execute()` 에서 전달한 `show_header` 파라미터를 통해 첫 번째 반복문에서만 CSV 헤더를 추가해 반환
- `pd.DataFrame` 을 활용할 수도 있지만, 단순하게 배열 타입으로 파싱

```python
def _parse_api(self, response, start: int=1, show_header=True) -> List[List]:
    contents = response.json()["items"]
    if contents:
        header = ([["rank"] + list(contents[0].keys())]) if show_header else []
        return header + [[start+i]+list(content.values()) for i, content in enumerate(contents)]
    else: return list()
```

### CSV 파일 저장 메서드

**`execute()`**
- CSV 파일을 저장하기 전에 `_mkdir()` 메서드를 통해 `file_path` 검증
- API 응답 결과를 가진 `rows` 객체를 `_to_csv()` 메서드에 전달해 CSV 파일로 저장

```python
def execute(self, context):
    ...
    self._mkdir(self.file_path)
    self._to_csv(rows, self.file_path, encoding="utf-8", sep=',')
```

**`_mkdir()`**
- `file_path` 가 있는지 확인하고, 없으면 해당 경로를 생성하는 메서드

```python
def _mkdir(self, file_path: str):
    import os
    dir_path = os.path.split(file_path)[0]
    if not os.path.exists(dir_path):
        os.system(f"mkdir -p {dir_path}")
```

**`_to_csv()`**
- `file_path` 를 열고, 전달받은 `rows` 객체를 한 줄씩 기록하는 메서드
- 구분자 `,` 가 있을 경우 쌍따옴표 `" "` 로 감싸는 것과 같은 조치가 필요하지만, 내용이 중요한건 아니기 때문에 단순히 값에서 구분자 `,` 를 모두 제거하는 방식으로 가공하여 저장

```python
def _to_csv(self, rows: List[List], file_path: str, encoding="utf-8", sep=','):
    def clean(value: str) -> str:
        return str(value).replace(sep, '')
    with open(file_path, 'w', encoding=encoding) as file:
        for row in rows:
            file.write(sep.join(map(clean, row))+'\n')
```

## Custom Operator 활용 예시

### DAG 생성 및 실행
- `plugins/` 에 정의한 `NaverSearchToCsvOperator` 를 가져와서 두 개의 Task를 생성
- 하나는 네이버 쇼핑 검색 API를 사용하는 `search_shopping_task`, 다른 하나는 네이버 블로그 검색 API를 사용하는 `search_blog_task`
- `HttpOperator` 를 사용했으면 길어졌을 내용을 `NaverSearchToCsvOperator` 로 구조화하여 DAG 선언을 단순화

```python
# dags/nsearch_operator.py

from airflow.sdk import DAG
from operators.nshopping import NaverSearchToCsvOperator
import pendulum

with DAG(
    dag_id="nsearch_operator",
    schedule="0 9 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "http"],
) as dag:
    api_keys = dict(
        client_id="{{var.value.client_id_openapi_naver_com}}",
        client_secret="{{var.value.client_secret_openapi_naver_com}}")
    common_params = dict(keyword="노트북", display=1000, start=1, sort="sim")

    """네이버 쇼핑 검색"""
    search_shopping_task = NaverSearchToCsvOperator(
        task_id="search_shopping_task",
        search_type="shop",
        file_path="naverSearch/{{data_interval_end.in_timezone(\"Asia/Seoul\") | ds_nodash }}/shop.csv",
        **api_keys,
        **common_params
    )

    """네이버 블로그 검색"""
    search_blog_task = NaverSearchToCsvOperator(
        task_id="search_blog_task",
        search_type="blog",
        file_path="naverSearch/{{data_interval_end.in_timezone(\"Asia/Seoul\") | ds_nodash }}/blog.csv",
        **api_keys,
        **common_params
    )

    search_shopping_task >> search_blog_task
```

- `start` 1부터 `display` 1000까지 총 1000개의 검색 결과를 100개 단위로 나눠서 요청하는 과정을 로그로 남겨서 조회

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/3hty0k935z7ae0y3u0y2y/airflow-46-naver-search-task.webp?rlkey=k2diw9fntl9qaud4pxvgl6akv&dl=0"
  alt="search_shopping_task >> search_blog_task"
  max-width="518px"
  align="center" >}}

```bash
[2025-06-07, 19:44:00] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-07, 19:44:00] INFO - Filling up the DagBag from /opt/airflow/dags/nsearch_operator.py: source="airflow.models.dagbag.DagBag"
[2025-06-07, 19:44:00] INFO - Secrets backends loaded for worker: count=1: backend_classes=["EnvironmentVariablesBackend"]: source="supervisor"
[2025-06-07, 19:44:00] INFO - Secrets backends loaded for worker: count=1: backend_classes=["EnvironmentVariablesBackend"]: source="supervisor"
[2025-06-07, 19:44:00] INFO - Secrets backends loaded for worker: count=1: backend_classes=["EnvironmentVariablesBackend"]: source="supervisor"
[2025-06-07, 19:44:00] INFO - Connection Retrieved 'openapi.naver.com': source="airflow.hooks.base"
[2025-06-07, 19:44:00] INFO - 시작: 1: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:00] INFO - 끝: 100: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:00] INFO - 시작: 101: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:00] INFO - 끝: 200: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 시작: 201: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 끝: 300: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 시작: 301: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 끝: 400: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 시작: 401: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:01] INFO - 끝: 500: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 시작: 501: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 끝: 600: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 시작: 601: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 끝: 700: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 시작: 701: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 끝: 800: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 시작: 801: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:02] INFO - 끝: 900: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:03] INFO - 시작: 901: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
[2025-06-07, 19:44:03] INFO - 끝: 1000: source="airflow.task.operators.operators.nshopping.NaverSearchToCsvOperator"
```

### CSV 파일 확인

- 모든 Task가 `success` 로 처리된 후, 로컬 컴퓨터의 `files/` 경로에 두 개의 CSV 파일이 생성됨을 확인

```bash
% tree files -F
files/
└── naverSearch/
    └── 20250607/
        ├── blog.csv
        └── shop.csv
```

#### `shop.csv`

{{< data-table >}}
rank,title,link,image,lprice,hprice,mallName,productId,productType,brand,maker,category1,category2,category3,category4
1,삼성 갤럭시북...,https://...,https://...,428000,,삼성공식파트너 코인비엠에스,87952389253,2,갤럭시북,삼성전자,디지털/가전,노트북,,
2,삼성전자 갤럭시북4...,https://...,https://...,799000,,네이버,52631236642,1,갤럭시북4,삼성전자,디지털/가전,노트북,,
3,LG전자 울트라PC...,https://...,https://...,599000,,제이 씨앤에스,83718736488,2,LG전자,LG전자,디지털/가전,노트북,,
4,삼성전자 갤럭시북4...,https://...,https://...,728000,,네이버,52647794278,1,갤럭시북4,삼성전자,디지털/가전,노트북,,
5,LG그램 <b>노트북</b>...,https://...,https://...,1149000,,온라인총판대리점,86636005031,2,LG그램,LG전자,디지털/가전,노트북,,
{{< /data-table >}}

#### `blog.csv`

{{< data-table >}}
rank,title,link,description,bloggername,bloggerlink,postdate
1,<b>노트북</b>에서...,https://...,버리고 <b>노트북</b>으로...,란디의 하늘색 꿈,blog.naver.com/fksel33,20250601
2,고비넘긴 삼성<b>노트북</b>...,https://...,노원구 공릉동에 위치한...,하드웨어수리닷컴(엘존),blog.naver.com/yzenn,20250603
3,MSI 사무용<b>노트북</b>...,https://...,MSI<b>노트북</b>중에서...,Modulestudio,blog.naver.com/modulestudio,20250602
4,아직 이걸 안 써?...,https://...,아직 이걸 안 써?...,짜루의 이것저것 리뷰,blog.naver.com/skdaksdptn,20250520
5,가성비 초경량 <b>노트북</b>...,https://...,그런 <b>노트북</b>을...,삼성Mall 한사랑씨앤씨 공식 블로그,blog.naver.com/hansarangcnc,20250527
{{< /data-table >}}
