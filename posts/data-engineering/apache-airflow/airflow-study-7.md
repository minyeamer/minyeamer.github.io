---
title: "Apache Airflow - 외부 시스템 연동 (Connection, Hook, PostgreSQL)"
date: "2025-06-08T16:52:44+09:00"
layout: "post"
description: >
  Apache Airflow의 Connection과 Hook 개념을 소개하고,
  Docker Compose를 활용한 Postgres 컨테이너 생성부터 Connection 설정, Hook 사용, bulk_load 기능까지 단계별로 안내합니다.
  Docker Compose, Postgres, Connection, Hook, bulk_load까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&raw=1"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "Connection", "Hook", "Docker Compose", "Postgres", "Custom Hook", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
series: ["Apache Airflow 배우기"]
---

{{< series "Apache Airflow 배우기" "Apache Airflow - " >}}

## Docker Compose 이해
- 목적 : 1개 이상의 도커 컨테이너 생성 시 컨테이너들의 설정을 관리할 수 있도록 해주는 기능
- 방법 : `docker-compose.yaml` 파일에 컨테이너들의 설정을 입력
- 사용 : `.yaml` 파일이 있는 위치에서 `docker compose up` 명령어를 입력하여 실행
- yaml 파일은 들여쓰기 문법을 사용하며 Airflow의 Docker Compose는 아래와 같이 구분

```yaml
x-airflow-common: # 각 서비스에 공통 적용될 항목들
services: # 컨테이너로 실행할 서비스를 정의
volumns: # 컨테이너에 연결할 볼륨을 정의
networks: # 컨테이너에 연결할 네트워크를 정의
```

`x-airflow-common`
- 공통으로 사용할 항목을 `&` 를 붙여서 지정
- `&` 아래의 모든 영역은 공통 항목으로 묶여 한번에 가져올 수 있음

```yaml
x-airflow-common:
  &airflow-common
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.0.1}
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
```

`services`
- 컨테이너로 올릴 서비스 목록을 지정
- 공통 항목을 `<<: *airflow-common` 과 같은 형식으로 불러오기
- 환경 변수가 있을 경우 `environment` 아래에 입력
- `ports` 는 호스트에서 컨테이너에 접속하기 위해 맵핑할 포트를 명시
   - `expose` 는 `ports` 와 다르게 내부 컨테이너 간에 연결할 때 사용할 포트를 명시
- `depends_on` 은 컨테이너의 실행 순서를 정의
   - `airflow-apiserver` 는 `airflow-init` 에 대한 종속적 관계

```yaml
services:
  airflow-apiserver:
    <<: *airflow-common
    command: api-server
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/api/v2/version"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
```

`volumes`
- 컨테이너 내 데이터를 유지하기 위해 외부와 연결하기 위한 볼륨 정보
- 볼륨 리스트를 보려면 `docker volume ls` 명령어 사용

```yaml
volumes:
  postgres-db-volume:
```

- 서비스를 정의할 때 생성한 볼륨과 컨테이너의 내부 경로를 연결 가능

```yaml
services:
  postgres:
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
```

`networks`
- 컨테이너를 격리된 네트워크로 그룹화하기 위한 네트워크 정보
- 컨테이너는 유동 IP를 가지게 되어 재가동할 때마다 IP 주소가 변경될 수 있는데, 고정 IP를 할당하기 위해 networks 활용 가능
- 네트워크 리스트를 보려면 `docker network ls` 명령어 사용

```yaml
networks:
  network_custom:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

- Airflow에서 기본적으로 사용하는 `airflow_default` 네트워크 대역이 `172.18.0.0/16` 서브넷 범위인데,
  아래에서 새 컨테이너를 만들기 위해 겹치지 않는 대역의 `network_custom` 을 정의

```bash
% docker network inspect {network_id}
[
    {
        "Name": "airflow_default",
        ...
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"
                }
            ]
        },
        ...
    }
]
```

## Postgres 컨테이너 생성

### Docker Compose
- Airflow에서 기본으로 사용하는 Postgres 컨테이너 외에 새로운 Postgres 컨테이너 하나를 추가로 생성
- DB 사용자에 대한 정보는 환경 변수 `environment` 로 입력
- 5432 포트로 접속할 수 있게 포트 맵핑 적용
   - 기존의 `postgres` 컨테이너도 5431 포트로 접속할 수 있게 마찬가지로 포트 맵핑 적용
- `postgres-custom-db-volume` 볼륨을 추가하고 컨테이너 내부 경로와 연결
- 위에서 정의한 `network_custom` 네트워크에 연결하면서 IP 주소는 `172.28.0.3` 으로 고정
   - 다른 컨테이너에도 `network_custom` 및 겹치지 않는 고정 IP 주소를 할당

```yaml
services:
  postgres_custom:
    image: postgres:13
    environment:
      POSTGRES_USER: minyeamer
      POSTGRES_PASSWORD: minyeamer
      POSGRES_DB: minyeamer
      TZ: Asia/Seoul
    volumes:
      - postgres-custom-db-volume:/var/lib/postgresql/data
    ports:
      - 5432:5432
    networks:
      network_custom:
        ipv4_address: 172.28.0.3

  postgres:
    image: postgres:13
    ...
    ports:
      - 5431:5432
    networks:
      network_custom:
        ipv4_address: 172.28.0.4

  ...

volumes:
  postgres-db-volume:
  postgres-custom-db-volume:

networks:
  network_custom:
    ...
```

- 실행 후 컨테이너 목록을 조회하면 `airflow-postgres_custom-1` 명칭의 컨테이너가 같이 올라온 것을 확인

```bash
% docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                    NAMES
72541e89bff4   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   57 seconds ago   Up 20 seconds (healthy)   8080/tcp                 airflow-airflow-worker-1
1735bc475bff   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   57 seconds ago   Up 36 seconds (healthy)   0.0.0.0:8080->8080/tcp   airflow-airflow-apiserver-1
d2b680f273e3   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   57 seconds ago   Up 36 seconds (healthy)   8080/tcp                 airflow-airflow-scheduler-1
f23c6d30d22c   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   57 seconds ago   Up 36 seconds (healthy)   8080/tcp                 airflow-airflow-dag-processor-1
09992f09ac5e   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   57 seconds ago   Up 36 seconds (healthy)   8080/tcp                 airflow-airflow-triggerer-1
5c1b13f33229   postgres:13            "docker-entrypoint.s…"   58 seconds ago   Up 56 seconds             0.0.0.0:5432->5432/tcp   airflow-postgres_custom-1
e23d4eb919fc   postgres:13            "docker-entrypoint.s…"   58 seconds ago   Up 56 seconds (healthy)   0.0.0.0:5431->5432/tcp   airflow-postgres-1
86fc82a16953   redis:7.2-bookworm     "docker-entrypoint.s…"   58 seconds ago   Up 56 seconds (healthy)   6379/tcp                 airflow-redis-1
```

### DBeaver 접속
- [Beaver Community 버전](https://dbeaver.io/download/)을 다운로드 및 설치한 후 실행
- 좌측 상단의 `New Database Connection` 을 클릭해 PostgreSQL 연결을 생성
   - Port는 Docker Compose에서 맵핑한 5432 사용
   - Database, Username, Password 또한 Docker Compose에서 지정한 값을 사용

{{% columns %}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/mdmcowq7snd9kre1nk3er/airflow-47-dbeaver-select-database.webp?rlkey=mqhmcjbk9ffa0cjqb4yib3wkw&raw=1"
  alt="Connect to a database > Select your database" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/fjrzi28evemhofio626rl/airflow-48-dbeaver-connection-settings.webp?rlkey=q4xqe24sguok0arrnn3z8jv2b&raw=1"
  alt="Connect to a database > Connection Settings" >}}
{{% /columns %}}

- 정상적으로 연결되었다면 아래와 같이 Database 명칭을 확인 가능

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/76s6qjohro7qeawziu92c/airflow-49-dbeaver-database-navigator.webp?rlkey=b8ja2rvtsyqjmn6tay2mw8hl4&raw=1"
  alt="Database Navigator"
  max-width="518px"
  align="center" >}}

### Postgres 테이블 생성
- `PythonOperator` 를 사용해 새로 생성한 PostgreSQL 컨테이너에 임의의 값을 INSERT 하는 작업을 구현하기 전에,
  아래와 같이 `public.dag_run` 테이블을 생성

```sql
CREATE TABLE public.dag_run (
	dag_id varchar(100) NULL,
	task_id varchar(100) NULL,
	run_id varchar(100) NULL,
	msg text NULL
);
```

- 테이블이 정상적으로 만들어졌다면 새로고침 후 아래와 같이 테이블 내 컬럼 내역을 확인 가능

![dag_run > Properties > Columns > [dag_id, task_id, run_id, msg]](https://dl.dropboxusercontent.com/scl/fi/7cj3j0xkqa33yk11x4fdq/airflow-50-dbeaver-dagrun-columns.webp?rlkey=vo7evh64owh5o5weotwny3nt9&raw=1)

### PythonOperator

- PostgreSQL에 연결해 현재 실행 정보를 `INSERT INTO` 로 추가하는 함수 `insert_into_postgres()` 를 실행
   - DB 연결 시 `conn` 세션 객체 생성 후 `.close()` 로 종료하는 구문을 `closing` 으로 대체
   - DB 세션에서 쿼리를 실행하는 `cursor` 객체를 만들고 해당 객체를 통해 SQL문을 수행
   - 함수에 인수로 전달하는 DB 연결 정보는 마찬가지로 Docker Compose에서 지정한 값을 사용

```python
# dags/python_with_postgres.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="python_with_postgres",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "hook"],
) as dag:
    def insert_into_postgres(ip: str, port: str, dbname: str, user: str, passwd: str, **kwargs):
        import psycopg2
        from contextlib import closing

        with closing(psycopg2.connect(host=ip, dbname=dbname, user=user, password=passwd, port=int(port))) as conn:
            with closing(conn.cursor()) as cursor:
                dag_id = kwargs.get("ti").dag_id
                task_id = kwargs.get("ti").task_id
                run_id = kwargs.get("ti").run_id
                msg = "INSERT INTO 수행"
                sql = "INSERT INTO dag_run VALUES (%s,%s,%s,%s);"
                cursor.execute(sql,(dag_id,task_id,run_id,msg))
                conn.commit()

    postgres_task = PythonOperator(
        task_id="postgres_task",
        python_callable=insert_into_postgres,
        op_args=["172.28.0.3", "5432", "minyeamer", "minyeamer", "minyeamer"]
    )
```

- DAG을 실행한 후 DBeaver에서 `dag_run` 테이블 조회 시 아래와 같이 하나의 행이 올라온 것을 확인

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/qkhf61bfelnqo014ics1d/airflow-51-dbeaver-dagrun-row.webp?rlkey=nnj98cyd7dn4feedrdoyztee4&raw=1"
  alt="dag_run > Data > manual__2025-06-08T04:11:08.876393+00:00"
  max-width="691px"
  align="center" >}}

#### 문제점 및 해결방법
- 문제점 : DB 접속정보가 노출되고 접속정보가 변경되면 대응하기가 어려움
- 해결방법
   1. Variable 이용
   2. Hook 이용

## Connection & Hook
- Connection : Airflow에서 외부와 연동하기 위해 설정하는 기본 정보
- Hook
   - Airflow에서 외부 솔루션의 기능을 사용할 수 있도록 미리 구현된 메서드를 가진 클래스
   - Connection 정보를 통해 생성되는 객체로, 접속정보가 코드상 노출되지 않음
   - 외부의 특정 솔루션을 다룰 수 있는 메서드가 구현되어 있음
   - Operator와 같이 Task를 만들어내지는 못하기 때문에 Operator 내 함수에서 사용

### Postgres Provider 문서 보기

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/index.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- Providers에 속한 Postgres 문서에서
  [Connection 접속 과정](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.get_conn)을 조회 가능

```python
def get_conn(self) -> connection:
    """Establish a connection to a postgres database."""
    conn = deepcopy(self.connection)

    # check for authentication via AWS IAM
    if conn.extra_dejson.get("iam", False):
        conn.login, conn.password, conn.port = self.get_iam_token(conn)

    conn_args = {
        "host": conn.host,
        "user": conn.login,
        "password": conn.password,
        "dbname": self.database or conn.schema,
        "port": conn.port,
    }
    raw_cursor = conn.extra_dejson.get("cursor", False)
    if raw_cursor:
        conn_args["cursor_factory"] = self._get_cursor(raw_cursor)

    if self.options:
        conn_args["options"] = self.options

    for arg_name, arg_val in conn.extra_dejson.items():
        if arg_name not in self.ignored_extra_options:
            conn_args[arg_name] = arg_val

    self.conn = psycopg2.connect(**conn_args)
    return self.conn
```

- Connection으로부터 `host`, `login`, `password`, `database`, `port`
  정보를 읽어서 DB 연결에 대한 파라미터로 활용하는 것을 확인
- 마지막 줄에는 `psycopg2.connect()` 연결에 대한 `psycopg2.extensions.connection` 세션 객체를 반환

### Connection 추가
- postgres 타입의 Connection을 새로 생성
- 연결 정보로 Docker Compose에서 지정한 값을 입력
- Connection에 입력한 각 항목은 앞서 확인한 `get_conn()` 메서드에서 PostgreSQL 연결 시 사용

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/3q28bhxv5ld52bx3dqaiz/airflow-52-postgres-connection.webp?rlkey=py1x2x3gab8qemhlyw38h188k&raw=1"
  alt="Add Connection - Postgres"
  max-width="691px"
  align="center" >}}

### PostgresHook
- Provider 패키지를 설치하고, 기존에 `psycopg2` 라이브러리로 직접 PostgreSQL에 연결하던 부분을 `PostgresHook` 으로 변경

```bash
pip install apache-airflow-providers-postgres
```

```python
# dags/python_with_postgres_hook.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="python_with_postgres_hook",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "hook"],
) as dag:
    def insert_into_postgres(postgres_conn_id: str, **kwargs):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        from contextlib import closing
        postgres_hook = PostgresHook(postgres_conn_id)
        with closing(postgres_hook.get_conn()) as conn:
            with closing(conn.cursor()) as cursor:
                dag_id = kwargs.get("ti").dag_id
                task_id = kwargs.get("ti").task_id
                run_id = kwargs.get("ti").run_id
                msg = "INSERT INTO 수행"
                sql = "INSERT INTO dag_run VALUES (%s,%s,%s,%s);"
                cursor.execute(sql,(dag_id,task_id,run_id,msg))
                conn.commit()

    postgres_task = PythonOperator(
        task_id="postgres_task",
        python_callable=insert_into_postgres,
        op_kwargs={"postgres_conn_id":"conn-db-postgres-custom"}
    )
```

- DAG을 실행한 후 DBeaver에서 `dag_run` 테이블 조회 시 아래와 같이 두 번째 행이 추가된 것을 확인

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/qgawsskyvb52i0d82sjbs/airflow-53-dbeaver-dagrun-rows.webp?rlkey=l81q9dh7a68q062s0nrnam77v&raw=1"
  alt="dag_run > Data > manual__2025-06-08T06:15:41.672840+00:00"
  max-width="691px"
  align="center" >}}

## bulk_load

### Postgres Provider 문서 보기

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.bulk_load"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- PostgreSQL에 데이터를 업로드하는 `bulk_load()` 메서드에 대해 살펴보기

```python
def bulk_load(self, table: str, tmp_file: str) -> None:
    """Load a tab-delimited file into a database table."""
    self.copy_expert(f"COPY {table} FROM STDIN", tmp_file)
```

- `bulk_load()` 메서드는 내부적으로 `copy_expert()` 메서드를 사용하는데,
  [해당 소스코드](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.copy_expert)를 조회

```python
def copy_expert(self, sql: str, filename: str) -> None:
    self.log.info("Running copy expert: %s, filename: %s", sql, filename)
    if not os.path.isfile(filename):
        with open(filename, "w"):
            pass

    with open(filename, "r+") as file, closing(self.get_conn()) as conn, closing(conn.cursor()) as cur:
        cur.copy_expert(sql, file)
        file.truncate(file.tell())
        conn.commit()
```

- `copy_expert()` 메서드는 `get_conn()` 메서드를 통해 세션 객체를 얻어오고,
  세션 객체로부터 `cursor` 객체를 만들어서 해당 객체가 가지고 있는 `copy_expert()` 메서드를 수행

- [Psycopg 공식 문서](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert)에 따르면,
  `copy_expert()` 메서드는 `file` 객체를 전달받아서 `COPY TO` 문법에 대응되는 SQL문을 실행해 테이블에 업로드 수행

> The _sql_ statement should be in the form _COPY table TO STDOUT_ to
> export _table_ to the file object passed as argument or _COPY table FROM STDIN_ to
> import the content of the file object into _table_.

```python
copy_expert(sql, file, size=8192)
```

```python
>>> cur.copy_expert("COPY test TO STDOUT WITH CSV HEADER", sys.stdout)
id,num,data
1,100,abc'def
2,,dada
...
```

### Postgres 테이블 생성
- 저번에 만든 Custom Operator로 가져온 네이버 쇼핑 검색 결과 [shop.csv](/blog/airflow-study-6/#csv-파일-확인)
  파일을 PostgreSQL에 업로드할 계획을 가지고 테이블 구조를 정의
- CSV 파일과 동일한 열을 `TEXT` 타입으로 가지는 `nshopping.search` 테이블을 생성

```sql
CREATE TABLE nshopping_search(
    rank        text,
    title       text,
    link        text,
    image       text,
    lprice      text,
    hprice      text,
    mallName    text,
    productId   text,
    productType text,
    brand       text,
    maker       text,
    category1   text,
    category2   text,
    category3   text,
    category4   text
);
```

- DBeaver에서 `nshopping` 스키마를 만들고 SQL문을 수행하면 아래와 같이 테이블 열 목록을 확인 가능

![search > Properties > Columns](https://dl.dropboxusercontent.com/scl/fi/fzg4ruvxagiz3vfa5z13e/airflow-54-dbeaver-search-columns.webp?rlkey=o3ovhjjfr7xyktexyjux56el2&raw=1)

### CSV 파일 가공

> Load a tab-delimited file into a database table.

- 앞서 `bulk_load()` 메서드의 주석에 `Tab` 으로 구분된 파일을 업로드한다고 명시되어 있기 때문에, `shop.csv` 파일을 `,` 대신 `Tab` 으로 구분한 `shop_with_tab.csv` 파일을 같은 위치에 생성
   - vi 편집기로 파일을 열었다면 `%s/,/\t/g` 명령어를 입력해 `,` 를 `Tab` 으로 변경 가능

{{< data-table file-name="shop_with_tab.csv" >}}
rank,title,link,image,lprice,hprice,mallName,productId,productType,brand,maker,category1,category2,category3,category4
1,삼성 갤럭시북 인강용 사무용 업무용 가성비 윈도우11 저가 싼 태블릿 <b>노트북</b> 추천 기본팩,https://smartstore.naver.com/main/products/10407884292,https://shopping-phinf.pstatic.net/main_8795238/87952389253.11.jpg,428000,,삼성공식파트너 코인비엠에스,87952389253,2,갤럭시북,삼성전자,디지털/가전,노트북,,
2,LG전자 울트라PC 라이젠5 사무용 인강용 저렴한 8GB NVMe256GB LG<b>노트북</b>,https://smartstore.naver.com/main/products/6174236911,https://shopping-phinf.pstatic.net/main_8371873/83718736488.14.jpg,599000,,제이 씨앤에스,83718736488,2,LG전자,LG전자,디지털/가전,노트북,,
3,LG그램 <b>노트북</b> 14그램 Ultra5 16GB 256GB 인텔Arc GPU 인강용,https://smartstore.naver.com/main/products/9091504708,https://shopping-phinf.pstatic.net/main_8663600/86636005031.7.jpg,1149000,,온라인총판대리점,86636005031,2,LG그램,LG전자,디지털/가전,노트북,,
4,삼성전자 갤럭시북4 NT750XGR-A51A 16GB 256GB,https://search.shopping.naver.com/catalog/52631236642,https://shopping-phinf.pstatic.net/main_5263123/52631236642.20250124094900.jpg,799000,,네이버,52631236642,1,갤럭시북4,삼성전자,디지털/가전,노트북,,
5,2025 LG그램 15 Ai 라이젠5 16GB 256GB AMD 포토샵 대학생 인강용 <b>노트북</b>,https://smartstore.naver.com/main/products/10133562287,https://shopping-phinf.pstatic.net/main_8767806/87678065467.4.jpg,1239000,,창이로운,87678065467,2,LG그램,LG전자,디지털/가전,노트북,	
{{< /data-table >}}

### bulk_load 활용 예시
- `PostgresHook` 을 사용한 Operator에 이어서 `bulk_load()` 메서드를 추가
- DAG 실행 날짜에 대응되는 디렉토리 아래의 `shop_with_tab.csv` 파일을 읽어서 `nshopping.search` 테이블에 업로드될 것을 기대

```python
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="python_with_postgres_load",
    schedule=None,
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "hook"],
) as dag:
    def bulk_load_postgres(postgres_conn_id: str, table_name: str, file_path: str, **kwargs):
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id)
        postgres_hook.bulk_load(table_name, file_path)

    postgres_task = PythonOperator(
        task_id="postgres_task",
        python_callable=bulk_load_postgres,
        op_kwargs={"postgres_conn_id":"conn-db-postgres-custom",
                    "table_name":"nshopping.search",
                    "file_name":"/opt/airflow/files/naverSearch/{{data_interval_end.in_timezone(\"Asia/Seoul\") | ds_nodash }}/shop_with_tab.csv"}
    )
```

- DAG을 실행하고 DBeaver에서 `nshopping.search` 테이블을 조회하면 아래와 같이 CSV 파일이 그대로 올라온 것을 확인
- 하지만, CSV 헤더가 1행으로 들어가는 문제점이 보임

![search > Data > [1] [rank, title, link, ...]](https://dl.dropboxusercontent.com/scl/fi/6lurqjuyz338xpnc8icr3/airflow-55-dbeaver-search-data.webp?rlkey=bjq0qwcguvuh96glzpq2kmy8h&raw=1)

#### 문제점 및 개선방안
- 문제점 : 구분자가 `Tab` 으로 고정되어 있고, 헤더까지 포함해서 업로드 됨
- 개선방안 : Custom Hook을 만들어서 구분자를 입력받고 헤더 포함 여부를 선택받게 함
- Custom Hook은 다음 게시글에서 구현

## Custom Hook

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/hooks/base.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

### BaseHook
- `BaseHook` 클래스를 상속받아 직접 만든 Hook을 사용 가능

**`get_connection()`**
- Connection 객체를 가져오는 메서드
- `classmethod` 로 설정되어 있어 객체화하지 않고도 호출 가능

```python
@classmethod
def get_connection(cls, conn_id: str) -> Connection:
    """
    Get connection, given connection id.

    :param conn_id: connection id
    :return: connection
    """
    from airflow.models.connection import Connection

    conn = Connection.get_connection_from_secrets(conn_id)
    log.info("Connection Retrieved '%s'", conn.conn_id)
    return conn
```

**`get_hook()`**
- Connection 객체로부터 Hook 객체를 반환하는 메서드
- `classmethod` 로 설정되어 있어 객체화하지 않고도 호출 가능


```python
@classmethod
def get_hook(cls, conn_id: str, hook_params: dict | None = None) -> BaseHook:
    """
    Return default hook for this connection id.

    :param conn_id: connection id
    :param hook_params: hook parameters
    :return: default hook for this connection
    """
    connection = cls.get_connection(conn_id)
    return connection.get_hook(hook_params=hook_params)
```

**`get_conn()`**
- Hook 객체에 대한 연결을 구현하는 메서드로, 반드시 재정의해야 함

```python
def get_conn(self) -> Any:
    """Return connection for the hook."""
    raise NotImplementedError()
```

### PostgresHook 개선점 파악

> 이전에 만들었던 네이버 쇼핑 검색 결과에 대한 [CSV 파일을 적재하는 PostgresHook](#bulk_load-활용-예시)의 기능을 개선

1. 구분자가 `Tab` 으로 고정되어 있고, 헤더까지 포함해서 업로드 됨
   - [Psycopg 공식 문서](https://www.psycopg.org/docs/cursor.html#cursor.copy_expert)에 따르면,
     `CSV HEADER` 구문을 뒤에 붙여 헤더를 제외할 수 있음
   - 또한, `COPY` 문 뒤에 `DELIMITER` 구문을 추가해 구분자를 지정할 수도 있음
2. 테이블이 없으면 에러가 발생함, 또한 직접 테이블을 생성하는 것도 불편함
   - CSV 파일의 헤더를 읽어서 `CREATE TABLE` 문을 만들고, 위 `COPY` 문 앞에 붙여서 테이블 생성
   - 또한, 더 정확한 테이블 구성을 위해 모든 열을 `text` 타입으로 지정하지 않고, CSV 파일의 전체 또는 일부를
     읽어서 `int4` 타입의 열을 추측할 수 있을 것이라 판단
3. 기존엔 데이터를 계속해서 추가했는데, 덮어쓰기 옵션을 통해 이전 데이터를 지울 수도 있으면 더 좋을 것이라 생각함

#### Hook 기능 정의

> CSV 파일을 PostgreSQL 테이블에 적재하는데, 테이블이 없으면 생성하고, 덮어쓰기도 허용

## CustomPostgresHook
- `BaseHook` 을 상속받는 `CustomPostgresHook` 를 구현
- 기본적인 구성은 [Postgres Provider 문서](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html)에서
  제공하는 소스코드를 참고
- Hook 재사용을 위해 `plugins/` 경로 아래에 추가

```python
# plugins/hooks/postgres.py

from airflow.hooks.base import BaseHook
from typing import Literal
import psycopg2

class CustomPostgresHook(BaseHook):
    def __init__(self, postgres_conn_id: str, **kwargs):
        self.postgres_conn_id = postgres_conn_id
        self.conn = None
        self.database = kwargs.get("database")

    def get_conn(self) -> psycopg2.extensions.connection:
        conn = BaseHook.get_connection(self.postgres_conn_id)
        conn_args = {
            "host": conn.host,
            "user": conn.login,
            "password": conn.password,
            "dbname": self.database or conn.schema,
            "port": conn.port,
        }
        self.conn = psycopg2.connect(**conn_args)
        return self.conn

    def bulk_load(self, table: str, filename: str, encoding="utf-8",
                if_exists: Literal["append","replace"]="append", sep=',', with_header=True):
        create = self._create_table_sql(table, filename, encoding, sep, with_header)
        replace = "TRUNCATE TABLE {};".format(table) if if_exists == "replace" else str()
        copy = "COPY {} FROM STDIN DELIMITER '{}' {};".format(table, sep, ("CSV HEADER" if with_header else "CSV"))
        sql = ''.join([create, replace, copy])
        self.copy_expert(sql, filename, encoding)

    def _create_table_sql(self, table: str, filename: str, encoding="utf-8", sep=',', with_header=True) -> str:
        if with_header:
            column_list = self._read_csv_column_list(filename, encoding, sep)
            return "CREATE TABLE IF NOT EXISTS {}({});".format(table, column_list)
        else:
            return str()

    def _read_csv_column_list(self, filename: str, encoding="utf-8", sep=',') -> str:
        import csv
        def is_int4_type(value: str) -> bool:
            return (not value) or (value.isdigit() and (-2147483648 <= int(value) <= 2147483647))
        with open(filename, "r+", encoding=encoding) as file:
            reader = csv.reader(file, delimiter=sep)
            header = next(reader)
            dtypes = [all(map(is_int4_type, values)) for values in zip(*[next(reader) for _ in range(5)])]
            return ", ".join(["{} {}".format(col, ("int4" if is_int4 else "text")) for col, is_int4 in zip(header, dtypes)])

    def copy_expert(self, sql: str, filename: str, encoding="utf-8") -> None:
        from contextlib import closing
        self.log.info("Running copy expert: %s, filename: %s", sql, filename)
        with open(filename, "r+", encoding=encoding) as file, closing(self.get_conn()) as conn, closing(conn.cursor()) as cur:
            cur.copy_expert(sql, file)
            file.truncate(file.tell())
            conn.commit()
```

### PostgreSQL 연결 메서드

**`get_conn()`**
- `PostgresHook` 의 [`get_conn()`](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.get_conn)
  메서드와 유사한데, 메서드를 호출할 때마다 `Connection` 객체를 가져와 연결 정보를 읽어오는데 차이가 있음
- `psycopg2` 라이브러리를 사용해 PostgreSQL에 연결하고 `psycopg2.extensions.connection` 객체를 반환

```python
def get_conn(self) -> psycopg2.extensions.connection:
    conn = BaseHook.get_connection(self.postgres_conn_id)
    conn_args = {
        "host": conn.host,
        "user": conn.login,
        "password": conn.password,
        "dbname": self.database or conn.schema,
        "port": conn.port,
    }
    self.conn = psycopg2.connect(**conn_args)
    return self.conn
```

### 쿼리문 생성 메서드

**`bulk_load()`**
- `f"COPY {table} FROM STDIN"` 형식의 단순한 SQL문을 사용하던 기존
  [`bulk_load()`](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.bulk_load) 메서드를 개선
- **`create`** : `_create_table_sql()` 메서드를 통해 `CREATE TABLE` 문 생성
- **`replace`** : `if_exists` 파라미터 값에 따라 테이블 내용을 모두 삭제하는 구문을 선택적으로 추가
- **`copy`** : 구분자 또는 헤더 포함 여부 등을 파라미터로 받고 이를 활용하여 `COPY` 문 생성

```python
def bulk_load(self, table: str, filename: str, encoding="utf-8",
            if_exists: Literal["append","replace"]="append", sep=',', with_header=True):
    create = self._create_table_sql(table, filename, encoding, sep, with_header)
    replace = "TRUNCATE TABLE {};".format(table) if if_exists == "replace" else str()
    copy = "COPY {} FROM STDIN DELIMITER '{}' {};".format(table, sep, ("CSV HEADER" if with_header else "CSV"))
    sql = ''.join([create, replace, copy])
    self.copy_expert(sql, filename, encoding)
```

**`_create_table_sql()`**
- 헤더가 있을 경우에 한정해, `_read_csv_column_list()` 메서드를 통해 열 목록을 가져오고, `CREATE TABLE` 문 안에 열 목록을 포맷팅해 반환
- `IF NOT EXISTS` 구문을 추가해 테이블이 이미 존재할 경우는 테이블 생성 생략
- 헤더가 없을 경우에는 기본적으로 테이블 생성 무시

```python
def _create_table_sql(self, table: str, filename: str, encoding="utf-8", sep=',', with_header=True) -> str:
    if with_header:
        column_list = self._read_csv_column_list(filename, encoding, sep)
        return "CREATE TABLE IF NOT EXISTS {}({});".format(table, column_list)
    else:
        return str()
```

**`_read_csv_column_list()`**
- 헤더와 상위 5개 행을 읽어서 데이터 타입을 추정하고, 이를 바탕으로 테이블의 열 목록을 정의
- 데이터 타입은 `int4` 또는 `text` 두 가지 경우만 판단하며, `int4` 범위에 있는
  숫자형 문자 또는 NULL 값으로만 구성된 열은 `int4` 타입으로 지정하고, 나머지는 `text` 타입으로 지정

```python
def _read_csv_column_list(self, filename: str, encoding="utf-8", sep=',') -> str:
    import csv
    def is_int4_type(value: str) -> bool:
        return (not value) or (value.isdigit() and (-2147483648 <= int(value) <= 2147483647))
    with open(filename, "r+", encoding=encoding) as file:
        reader = csv.reader(file, delimiter=sep)
        header = next(reader)
        dtypes = [all(map(is_int4_type, values)) for values in zip(*[next(reader) for _ in range(5)])]
        return ", ".join(["{} {}".format(col, ("int4" if is_int4 else "text")) for col, is_int4 in zip(header, dtypes)])
```

### 쿼리문 실행 메서드

**`copy_expert()`**
- `PostgresHook` 의 [`copy_expert()`](https://airflow.apache.org/docs/apache-airflow-providers-postgres/6.1.3/_modules/airflow/providers/postgres/hooks/postgres.html#PostgresHook.copy_expert)
  메서드와 동일한데, 한글 CSV 파일은 `EUC-KR` 등 다른 인코딩이 필요할 수 있어 `encoding` 파라미터를 추가

```python
def copy_expert(self, sql: str, filename: str, encoding="utf-8") -> None:
    from contextlib import closing
    self.log.info("Running copy expert: %s, filename: %s", sql, filename)
    with open(filename, "r+", encoding=encoding) as file, closing(self.get_conn()) as conn, closing(conn.cursor()) as cur:
        cur.copy_expert(sql, file)
        file.truncate(file.tell())
        conn.commit()
```

## Custom Hook 활용 예시

### DAG 생성 및 실행
- `plugins/` 에 정의한 `CustomPostgresHook` 을 활용
- 실행 날짜에 생성된 `shop.csv` 파일을 보고 `nshopping.search2` 테이블을 생성 및 적재
- `shop.csv` 파일을 굳이 `shop_with_tab.csv` 파일로 가공할 필요성을 줄여서 편의성 개선

```python
# dags/python_with_postgres_custom.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from hooks.postgres import CustomPostgresHook
import pendulum

with DAG(
        dag_id="python_with_postgres_custom",
        schedule=None,
        start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
        catchup=False,
        tags=["example", "hook"],
) as dag:
    def bulk_load_postgres(postgres_conn_id: str, table: str, filename: str, **kwargs):
        custom_postgres_hook = CustomPostgresHook(postgres_conn_id=postgres_conn_id)
        custom_postgres_hook.bulk_load(table=table, filename=filename, if_exists="replace", sep=",", with_header=True)

    bulk_load_postgres = PythonOperator(
        task_id="bulk_load_postgres",
        python_callable=bulk_load_postgres,
        op_kwargs={"postgres_conn_id": "conn-db-postgres-custom",
                    "table":"nshopping.search2",
                    "filename":"/opt/airflow/files/naverSearch/{{data_interval_end.in_timezone(\"Asia/Seoul\") | ds_nodash }}/shop.csv"}
    )
```

- 실행 로그 중에서 `CustomPostgresHook` 이 생성한 SQL문을 확인 가능
- `if_exists="replace"` 파라미터를 추가했기 때문에, 중간에 `TRUNCATE TABLE` 구문이 추가
   - 따라서, 여러 번 DAG을 실행해도 매번 테이블이 초기화되어 중복된 데이터가 업로드되지 않음

```bash
[2025-06-11, 01:24:16] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-11, 01:24:16] INFO - Filling up the DagBag from /opt/airflow/dags/python_with_postgres_custom.py: source="airflow.models.dagbag.DagBag"
[2025-06-11, 01:24:16] INFO - Running copy expert: CREATE TABLE IF NOT EXISTS nshopping.search2(rank int4, title text, link text, image text, lprice int4, hprice int4, mallName text, productId text, productType int4, brand text, maker text, category1 text, category2 text, category3 int4, category4 int4);TRUNCATE TABLE nshopping.search2;COPY nshopping.search2 FROM STDIN DELIMITER ',' CSV HEADER;, filename: /opt/airflow/files/naverSearch/20250611/shop.csv: source="hooks.postgres.CustomPostgresHook"
[2025-06-11, 01:24:16] INFO - Secrets backends loaded for worker: count=1: backend_classes=["EnvironmentVariablesBackend"]: source="supervisor"
[2025-06-11, 01:24:16] INFO - Connection Retrieved 'conn-db-postgres-custom': source="airflow.hooks.base"
[2025-06-11, 01:24:16] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.operators.python.PythonOperator"
```

### 테이블 조회
- DBeaver에서 `nshopping.search2` 테이블이 생성되었고, 의도대로 정수형 열을 추측하여 데이터 타입을 구분해서 지정된 것을 확인

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/7wxi8iful4mscw6hrbk4b/airflow-56-dbeaver-search2-columns.webp?rlkey=21gcfnuz4969c25nzmocd9kmc&raw=1"
  alt="search2 > Properties > Columns"
  max-width="691px"
  align="center" >}}

- 테이블 내용을 보면, 기존의 문제였던 헤더가 1행으로 들어갔던게 해결됨이 확인
- 또한, 추측한 데이터 타입에 맞춰서 값이 정상적으로 들어갔음을 확인
- 참조한 강의에서는 CSV 파일을 `pd.DataFrame` 객체로 읽고, SQLAlchemy의 엔진을 사용해 `to_sql()` 기능으로 PostgreSQL 테이블에 데이터를 적재하는 방식으로 접근
   - 개인적으로는 `PostgresHook` 을 이해하고자, `PostgresHook` 의 원형을 최대한 유지하면서 필요한 기능만 추가하기 위해 외부 라이브러리의 사용을 제한함

![search2 > Data](https://dl.dropboxusercontent.com/scl/fi/p2tb7a2tcjq69pfixzf6p/airflow-57-dbeaver-search2-data.webp?rlkey=0t6eb81t9ullwkfowhocrjrhx&raw=1)
