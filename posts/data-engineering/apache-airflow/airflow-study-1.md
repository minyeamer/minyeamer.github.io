---
title: "Apache Airflow - 설치하기 (Docker Compose)"
date: "2025-05-27T22:05:51+09:00"
layout: "post"
description: >
  Apache Airflow의 개념과 장단점을 소개하고, Docker를 이용한 Airflow 설치 과정을 단계별로 안내합니다.
  DAG 구조와 워크플로우 이해, Docker Compose를 활용한 로컬 환경 구축, 웹 UI를 통한 Example DAG 실행까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&dl=0"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "Airflow 설치", "Docker", "Docker Compose", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
---

## Airflow란?
- 워크플로우를 만들고 관리하기 위한 목적의 파이썬 기반 오픈소스 플랫폼
- 워크플로우는 DAG(Directed Acyclic Graph) 구조를 가짐
- Cron 기반으로 작업 스케줄링
- 웹 UI를 통해 작업을 모니터링하고 실패 시 재실행이 가능

### Airflow 장점
- 파이썬에서 지원되는 다양한 라이브러리를 활용 가능
- 대규모 환경에서 부하 증가 시 수평적 확장이 가능한 Kubenetes 등 아키텍처 지원
- 오픈소스 플랫폼의 이점을 살려 원하는 기능을 커스터마이징 가능

### Airflow 단점
- 실시간 워크플로우 관리에 적합하지 않음 (최소 분 단위 실행)
- 워크플로우가 많아질수록 모니터링이 어려움

### DAG(Directed Acyclic Graph)
- DAG는 Task 간의 종속성과 순서를 지정
   - **Task** : DAG 내에서 어떠한 행위를 할 수 있는 객체
- DAG는 1개 이상의 Task로 구성
- Task 간에 순한되지 않고 방향성을 가짐
- Task에 대한 종속성은 `>>` 또는 `<<` 연산자를 사용해 선언
   - 예시) `first_task >> second_task`

![DAGs - Airflow Documentation](https://dl.dropboxusercontent.com/scl/fi/ngxutq3ok3w4zin85ftt9/airflow-01-dag-example.webp?rlkey=5u21auwiiqf32ziksstmeu16r&dl=0)

### Airflow Workflow
- **Scheduler** : 예약된 일정에 워크플로우를 Executor에게 넘겨 Task를 실행
- **Executor** : Scheduler 내부의 모든 작업을 실행하며, 모든 Task가 순차적으로 실행되게 관리
- **Worker** : 실제 Task를 실행하는 주체
- **Metadata Database** : Scheduler, Executor, Webserver가 상태를 저장하는데 사용
- **DAG Directory** : 파이썬으로 작성한 DAG 파일을 저장하는 공간
- **Webserver** : User Interface를 통해 Scheduler와 DAG 실행 과정을 시각화해 표시

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/f3l1sntgvfm9h82c1utod/airflow-02-workflow.webp?rlkey=l6qafh8nbfricv588tsdk1qye&dl=0"
  alt="Architecture Overview - Airflow Documentation"
  max-width="691px"
  align="center" >}}

### User Interface
- DAG와 각각의 작업이 수행되는 내용을 시각적으로 확인
- DAG 실행을 직접 트리거
- DAG 실행 로그를 확인하고 제한적인 디버깅 수행

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/2.6.0/core-concepts/overview.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

![UI / Screenshots - Airflow Documentation](https://dl.dropboxusercontent.com/scl/fi/r15u5f5worgn1qmt8dfga/airflow-03-user-interface.webp?rlkey=weeolbcg3a9e363nunxmj21ux&dl=0)

## Airflow 설치 환경
- macOS Sequoia 15.5
- Docker Desktop 4.41.2
- Airflow 3.0.1

### Docker란?
- 애플리케이션을 독립적인 환경에서 실행시키는 기술
- 가상화 서버(VM)와 비교했을 때, Guest OS를 요구하지 않아 더 효율적인 자원 활용이 가능
- `docker-compose` 를 이용해 Airflow를 운영하는데 필요한 여러 서비스(컨테이너)를 실행

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/wrp3yqqd8l9llzk5jfjb2/airflow-04-docker.webp?rlkey=p5u5yu9bbs0hu6clbu9azubbt&dl=0"
  alt="Docker vs VM"
  max-width="691px"
  align="center" >}}

### Docker Descktop 설치

{{< bookmark "https://docs.docker.com/desktop/setup/install/mac-install/" >}}

- 운영체제에 맞는 Docker Descktop 파일을 내려받아 설치
- 설치 후 실행하면 아래와 같은 초기 화면을 확인

![Docker Descktop UI](https://dl.dropboxusercontent.com/scl/fi/3pl7bbucirxxzozqfgawb/airflow-05-docker-home.webp?rlkey=stzfnx8s35sa6zpkyw818nol8&dl=0)

## Airflow 설치하기

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

### 1. docker-compose.yaml

```bash
% curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.1/docker-compose.yaml'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 12766  100 12766    0     0  38365      0 --:--:-- --:--:-- --:--:-- 38336
```

- Airflow 문서로부터 `docker-compose.yaml` 경로를 복사해 터미널에서 요청
- 내려받은 `docker-compose.yaml` 파일을 보면 아래와 같은 컨테이너가 설치될 것임을 짐작 가능

```yaml
services:
  postgres:
    image: postgres:13

  redis:
    image: redis:7.2-bookworm

  airflow-apiserver: ...
  airflow-scheduler: ...
  airflow-dag-processor: ...
  airflow-worker: ...
  airflow-triggerer: ...
  airflow-init: ...
  airflow-cli: ...
  flower: ...
```

### 2. 환경 설정

```bash
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

- Airflow 문서에 따라 필요한 디렉토리를 생성
- AIRFLOW_UID가 설정되지 않았다는 경고를 피하기 위해 `.env` 파일을 생성

### 3. Airflow 초기화

```bash
docker compose up airflow-init
```

- `exited with code 0` 가 출력되면 정상적으로 초기화되어 다음 단계로 진행

### 4. Airflow 실행

```
docker compose up
```

- Docker Desktop 상에서 아래 이미지와 같이 모든 컨테이너들이 실행되고 있는지 확인 가능

![Docker Descktop에서 Airflow 서비스 조회](https://dl.dropboxusercontent.com/scl/fi/8e2btqsfjeapzv1k6924j/airflow-06-docker-container.webp?rlkey=2zz6vga8bfhtqgjrng0ir6j20&dl=0)

- 또는 터미널에서 `docker ps` 명령어를 입력해 컨테이너 실행 상태를 조회 가능

```bash
% docker ps
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                    NAMES
a0431bfa0d1f   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   1 minutes ago   Up 1 minutes (healthy)    8080/tcp                 airflow-airflow-worker-1
4d32f0c45d4a   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   1 minutes ago   Up 1 minutes (healthy)    8080/tcp                 airflow-airflow-triggerer-1
f4cd1b0887de   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   1 minutes ago   Up 1 minutes (healthy)    8080/tcp                 airflow-airflow-dag-processor-1
3213192935b6   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   1 minutes ago   Up 1 minutes (healthy)    8080/tcp                 airflow-airflow-scheduler-1
e933dc415a73   apache/airflow:3.0.1   "/usr/bin/dumb-init …"   1 minutes ago   Up 1 minutes (healthy)    0.0.0.0:8080->8080/tcp   airflow-airflow-apiserver-1
94f88f2e5507   postgres:13            "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   5432/tcp                 airflow-postgres-1
3f82ba15433e   redis:7.2-bookworm     "docker-entrypoint.s…"   6 minutes ago   Up 6 minutes (healthy)   6379/tcp                 airflow-redis-1
```

## Airflow 둘러보기

### Airflow 로그인

- 컨테이너가 정상적으로 실행 중인 경우 브라우저에서 `localhost:8080` 주소로 접속하면 Airflow UI에 접근 가능
- 초기 계정은 Username 과 Password 모두 `airflow` 입력

![Airflow 로그인 페이지](https://dl.dropboxusercontent.com/scl/fi/fijme1clvmdqlt46roizs/airflow-07-airflow-signin.webp?rlkey=6dc4nuq3td9h673unb7vo2bi5&dl=0)

- 정상적으로 로그인 시 아래와 같은 홈페이지로 이동

![Airflow 홈페이지](https://dl.dropboxusercontent.com/scl/fi/8ugkzw79rcae4gnf1ix9l/airflow-08-airflow-home.webp?rlkey=ksnnjlbiobl6sn9n21s5lhvg3&dl=0)

### Example DAG 실행

- 사이드바에서 Dags 메뉴를 클릭하면 DAG 목록이 있는 페이지로 이동
- 첫 번째에 있는 `tutorial_taskflow_templates` DAG를 클릭하여 상세 페이지 조회

![/dags 페이지](https://dl.dropboxusercontent.com/scl/fi/qssvefcj7yqz86yauf5vu/airflow-09-dags.webp?rlkey=zubkjhref7wyy8evao33b8ooh&dl=0)

- 상단의 DAG 제목 옆에 토글 스위치를 클릭하면 DAG 활성화
- 좌측에서 DAG 내 Task 간 종속성을 그래프로 확인 (해당 DAG는 단일 Task로 구성)

![Dag 페이지 > Overview 탭](https://dl.dropboxusercontent.com/scl/fi/gwo3af2ws3slm9lg52c50/airflow-10-dag-overview.webp?rlkey=d6g317x96hq6fl45u5fd8uoqt&dl=0)

- 내비게이션 메뉴 중에서 Runs 메뉴를 클릭하면 실행 이력을 조회

![Dag 페이지 > Runs 탭](https://dl.dropboxusercontent.com/scl/fi/1z3pcjj7soidh5ii2rb3i/airflow-11-dag-runs.webp?rlkey=084k611n5p59r94jdeyzfq9j3&dl=0)

- 실행된 결과를 하나 클릭하면 하위 Task 목록을 조회 가능
- State 항목을 통해 처리 상태를 알 수 있는데, `success` 상태는 Task가 성공적으로 처리됨을 의미

![Dag Run 페이지 > Task Instances 탭](https://dl.dropboxusercontent.com/scl/fi/opw1v6yekhji2677pa64t/airflow-12-dag-run-tasks.webp?rlkey=g5kohv8yzorz9hb5sdno2ynsl&dl=0)

- Task 하나를 클릭해서 Logs 메뉴에 들어가면 아래와 같이 `context` 라는 객체를 출력하는 구문이 확인됨
- 앞서 DAG 페이지의 내비게이션 메뉴 중 Code 메뉴에서 이미 코드를 확인했는데,
  `get_current_context()` 라는 함수를 통해 `context` 라는 딕셔너리 객체를 가져와 출력하는 작업으로 추측

```
[2025-05-27, 23:31:26] INFO - context: {'dag': <DAG: tutorial_taskflow_templates>, ...}: chan="stdout": source="task"
```

![Task 페이지 > Logs 탭](https://dl.dropboxusercontent.com/scl/fi/sktawkrc89dzg7bu9v7ih/airflow-13-dag-run-logs.webp?rlkey=ib50ujf423m0664xpi72v8kcf&dl=0)

## Airflow 중지

```bash
% docker compose stop 
[+] Stopping 8/8
 ✔ Container airflow-airflow-dag-processor-1  Stopped                      1.1s 
 ✔ Container airflow-airflow-triggerer-1      Stopped                      0.9s 
 ✔ Container airflow-airflow-worker-1         Stopped                      2.8s 
 ✔ Container airflow-airflow-scheduler-1      Stopped                      0.8s 
 ✔ Container airflow-airflow-apiserver-1      Stopped                      0.6s 
 ✔ Container airflow-airflow-init-1           Stopped                      0.0s 
 ✔ Container airflow-postgres-1               Stopped                      0.1s 
 ✔ Container airflow-redis-1                  Stopped                      0.2s 
```

- `docker-compose.yaml` 파일이 있는 경로에서 서비스를 명시하지 않고 명령어를 실행하면 모든 Airflow 컨테이너를 중지

### Airflow 컨테이너 삭제

```bash
% docker compose down --volumes --rmi all
[+] Running 13/13
 ✔ Container airflow-airflow-dag-processor-1  Removed                                                                                                                   1.5s 
 ✔ Container airflow-airflow-triggerer-1      Removed                                                                                                                   1.2s 
 ✔ Container airflow-airflow-worker-1         Removed                                                                                                                   3.4s 
 ✔ Container airflow-airflow-scheduler-1      Removed                                                                                                                   1.0s 
 ✔ Container airflow-airflow-apiserver-1      Removed                                                                                                                   0.9s 
 ✔ Container airflow-airflow-init-1           Removed                                                                                                                   0.1s 
 ✔ Container airflow-postgres-1               Removed                                                                                                                   0.2s 
 ✔ Container airflow-redis-1                  Removed                                                                                                                   0.2s 
 ✔ Image apache/airflow:3.0.1                 Removed                                                                                                                   0.9s 
 ✔ Image postgres:13                          Removed                                                                                                                   0.9s 
 ✔ Image redis:7.2-bookworm                   Removed                                                                                                                   0.9s 
 ✔ Volume airflow_postgres-db-volume          Removed                                                                                                                   0.0s 
 ✔ Network airflow_default                    Removed                                                                                                                   0.5s 
```

- `docker-compose.yaml` 파일이 있는 경로에서 서비스를 명시하지 않고 명령어를 실행하면 모든 Airflow 컨테이너를 삭제
   - `--rmi` 옵션을 추가하여 관련 이미지까지 모두 삭제
