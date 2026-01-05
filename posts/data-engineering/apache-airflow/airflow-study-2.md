---
title: "Apache Airflow - 기본 Operator 이해하기 (Bash, Python)"
date: "2025-05-30T23:36:13+09:00"
layout: "post"
description: >
  Apache Airflow의 Operator 개념을 소개하고, BashOperator와 PythonOperator의 사용법을 단계별로 안내합니다.
  DAG 작성, Plugins 활용, Decorator 패턴, 파라미터 전달 방법까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&raw=1"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "BashOperator", "PythonOperator", "DAG", "Plugins", "Decorator", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
---

## Operator란?
- 특정 행위를 할 수 있는 기능을 모아 놓은 클래스
   - **Task** : Operator를 객체화하여 DAG에서 실행 가능한 오브젝트
- **Bash Operator** : 쉘 스크립트 명령을 수행하는 Operator
- **Python Operator** : 파이썬 함수를 실행하는 Operator

## 개발 환경 설정

### Git & Github

```bash
% git init
% git add .gitignore
% git commit -m "init"
% git remote add origin https://github.com/<username>/<repository>
% git push
```

- Git 설치 및 Github에 리포지토리를 생성
- 로컬 Airflow 설치 경로에서 Git 저장소를 생성하고 원격 저장소와 연결
- Airflow에서 제공하는 `.gitignore` 를 로컬 Airflow 설치 경로에 복제하여 불필요한 `/logs` 경로 등을 Git에서 제외

{{< bookmark "https://github.com/apache/airflow/blob/main/.gitignore" >}}

### 디렉토리 구조

```bash
% tree -a -F .             
./
├── .env
├── .git/
├── .gitignore
├── config/
│   └── airflow.cfg
├── dags/
├── docker-compose.yaml
├── logs/
└── plugins/
```

### Example DAGs 삭제

```yaml
# docker-compose.yaml

AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
```

- 기본 설정으로 Airflow 실행 시 거슬리는 Example DAG를 삭제
- 컨테이너를 재시작해도 여전히 예제가 남아있어 `airflow db reset` 등 여러가지 초기화 방법을 탐색했지만,
  결과적으로 `localhost:8080` 에 대한 크롬 브라우저 캐시를 삭제하니 해결

![빈 DAG 목록](https://dl.dropboxusercontent.com/scl/fi/og5rcgutgrpkxmsa7xs47/airflow-14-empty-dags.webp?rlkey=vcky34swl24vbh53dfw9rr0vq&raw=1)

## BashOperator

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/operators/bash.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

### BashOperator 정의
- `dags/` 경로 아래에 `bash_operator.py` 파일을 생성
- Airflow에서 제공하는 예시 `example_bash_operator` 를 복제 및 일부를 수정하여 DAG 선언

```python
# dags/bash_operator.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "bash"],
) as dag:
    bash_task1 = BashOperator(
        task_id="bash_task1",
        bash_command="echo whoami",
    )

    bash_task2 = BashOperator(
        task_id="bash_task2",
        bash_command="echo $HOSTNAME",
    )

    bash_task1 >> bash_task2
```

### DAG 파라미터
- `dag_id` : UI에서 표시되는 DAG 명칭, 관리의 용이성을 위해 파일 명칭과 동일하게 지정
- `schedule` : 크론탭(Crontab)을 사용하여 스케줄 지정
- `start_date` : 작업 시작일을 지정, 예시에는 시간대가 UTC로 적용되어 Asia/Seoul로 변경
- `catchup` : 시작일(`start_date`)부터 현재까지 실행되지 않은 작업을 일괄로 실행 (`True`)
- `dagrun_timeout` : DAG 실행 시간을 제한
- `tags` : UI에서 DAG를 구별하기 위한 태그 지정

### BashOperator 파라미터
- `BashOperator` 를 사용하여 두 개의 bash 명령어를 실행하는 Task를 정의
- `task_id` : UI에서 표시되는 Task 명칭, 관리의 용이성을 위해 객체명과 동일하게 지정
- `bash_command` : 실행할 bash 명령어
- Task 간 `>>` 기호로 연결하여 종속성을 표시
   - 여러 개의 Task를 묶고 싶을 때는 배열을 사용 (`task1 >> [task2, task3]`)
   - 종속성은 연속해서 표시 가능 (`task1 >> task2 >> task3`)

{{< bookmark "https://github.com/apache/airflow/blob/providers-standard/1.2.0/providers/standard/tests/system/standard/example_bash_operator.py" >}}

### BashOperator 실행
- Airflow 컨테이너를 중지 후 다시 실행해 UI에서 DAG가 올라온 것을 확인

![BashOperator 목록](https://dl.dropboxusercontent.com/scl/fi/vhk1tkfhwy42b3cyffvm8/airflow-15-bash-operator.webp?rlkey=y9ve9t40s4tyiihmb4mmeyibu&raw=1)

- DAG를 실행하여 정상적으로 수행되는지 확인
- DAG를 클릭해서 이동하는 페이지에서 `bash_task` 과 `bash_task2` 의 관계를 그래프로 조회 가능

![BashOperator Task 목록](https://dl.dropboxusercontent.com/scl/fi/zkr4zd86vbadiigpsja2t/airflow-16-bash-tasks.webp?rlkey=meg3x9abfc3leyqsb3pcieko0&raw=1)

- `bash_task1` 과 `bash_task2` 에 대해 각각의 로그를 확인
- `bash_task1` 에는 `echo whoami` 명령어가 전달되어 `whoami` 를 결과로 출력
- `bash_task2` 에는 `echo $HOSTNAME` 명령어가 전달되어 컨테이너의 `HOSTNAME` 을 출력

```bash
# bash_task1

[2025-05-30, 00:16:56] INFO - Running command: ['/usr/bin/bash', '-c', 'echo whoami']: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-05-30, 00:16:56] INFO - Output:: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-05-30, 00:16:56] INFO - whoami: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

```bash
# bash_task2

[2025-05-30, 00:16:57] INFO - Running command: ['/usr/bin/bash', '-c', 'echo $HOSTNAME']: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-05-30, 00:16:57] INFO - Output:: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-05-30, 00:16:57] INFO - wha439072926: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

## PythonOperator

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow-providers-standard/stable/operators/python.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

### PythonOperator 종류
- `PythonOperator` : 파이썬 함수를 실행시키기 위한 Operator
- `PythonVirtualenvOperator` : 파이썬 가상환경 생성 후 작업을 수행하고 마무리되면 가상환경을 삭제하는 Operator
- `ExternalPythonOperator` : 기존에 존재하는 파이썬 가상환경에서 작업을 수행하는 Operator
- `BranchPythonOperator` : 파이썬 함수 실행 결과에 따라 다음 Task를 선택적으로 실행시킬 수 있는 Operator
- `BranchPythonVirtualenvOperator` : 가상환경 생성/삭제 및 브랜치 처리 기능이 있는 Operator
- `BranchExternalPythonOperator` : 기존 가상환경을 사용하면서 브랜치 처리 기능이 있는 Operator

### PythonOperator 정의

```python
# dags/python_operator.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pendulum
import random

with DAG(
    dag_id="python_operator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "python"],
) as dag:
    def select_country():
        COUNTRIES = [
            "Argentina", "Australia", "Brazil", "Canada", "China", "France", "Germany",
            "India", "Indonesia", "Italy", "Japan", "Mexico", "Russia", "Saudi Arabia",
            "South Africa", "South Korea", "Turkey", "United Kingdom", "United States"
        ]
        print(random.choice(COUNTRIES))

    python_task = PythonOperator(
        task_id="python_task",
        python_callable=select_country,
    )
```

- 앞서 `BashOperator` 예제를 가져오고 Task를 `PythonOperator` 로 대체
- G20 국가 중 랜덤한 국가를 선택해 출력하는 함수 `select_country()` 를 정의
- `select_country()` 함수를 실행하는 `python_task` 를 단일 Task로 사용

### PythonOperator 실행
- Airflow UI에서 `python_operator` DAG가 올라온 것을 확인

![PythonOperator 목록](https://dl.dropboxusercontent.com/scl/fi/9kak9x4u6maiyotnvtwgn/airflow-17-python-operator.webp?rlkey=hdijovzk2lngwtytrsldbs8a2&raw=1)

- DAG를 실행하여 정상적으로 수행되는지 확인
- `python_task` 의 첫 번째 실행 로그에서는 "Argentina" 국가가 선택되어 출력
- UI에서 Trigger 버튼을 눌러 `python_task` 를 수동 실행한 로그에서는 "Indonesia" 국가가 선택되어 출력

![PythonOperator Task 목록](https://dl.dropboxusercontent.com/scl/fi/9xyvmxz6108v9a2mxnudn/airflow-18-python-tasks.webp?rlkey=jt7j53z1y7mq1vaqekcyf5dy7&raw=1)


```bash
# scheduled run (first)

[2025-05-31, 11:33:06] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-05-31, 11:33:06] INFO - Filling up the DagBag from /opt/airflow/dags/python_operator.py: source="airflow.models.dagbag.DagBag"
[2025-05-31, 11:33:06] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.operators.python.PythonOperator"
[2025-05-31, 11:33:06] INFO - Argentina: chan="stdout": source="task"
```

```bash
# manual run (second)

[2025-05-31, 11:36:38] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-05-31, 11:36:38] INFO - Filling up the DagBag from /opt/airflow/dags/python_operator.py: source="airflow.models.dagbag.DagBag"
[2025-05-31, 11:36:38] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.operators.python.PythonOperator"
[2025-05-31, 11:36:38] INFO - Indonesia: chan="stdout": source="task"
```

## Plugins

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/plugins.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- `plugins/` 경로에 파이썬 함수를 작성하고 외부에서 활용
- DAG 선언 시 함수를 가져오기만 해도 되어서 깔끔해지고 같은 함수를 재활용할 수 있어서 편리
- 예시로, `plugins/` 경로 아래에 현재 시간을 출력하는 `print_now()` 함수를 정의

```python
# plugins/common/common_func.py

import datetime as dt

def print_now():
    print(dt.datetime.now())
```

### Plugins 활용 예시

```python
# dags/python_plugins.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from common.common_func import print_now
import pendulum

with DAG(
    dag_id="python_plugins",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "python"],
) as dag:
    python_plugins_task = PythonOperator(
        task_id="python_plugins_task",
        python_callable=print_now,
    )
```
- `plugins/` 에 정의한 함수를 import 해서 사용하는 `python_plugins` DAG 및 단일 Task를 생성
- 이 때, VSCode 상에서는 `plugins/` 경로를 생략한 import 문을 인식하지 못하기 때문에 `.env` 파일에 `PYTHONPATH` 를 추가

```bash
# .env

WORKSPACE_FOLDER=/Users/.../airflow
PYTHONPATH=${WORKSPACE_FOLDER}/plugins
```

- 마찬가지로, Airflow 컨테이너를 재시작하면 `python_plugins` DAG가 올라온 것을 확인
- DAG를 실행한 후 `python_plugins_task` 의 실행 로그에서 현재 시간이 출력된 결과를 조회
- 별도로 시간대를 지정하지 않았는데, UTC 시간대를 기준으로 시간이 가져와진 것을 확인

```bash
[2025-05-31, 12:10:35] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-05-31, 12:10:35] INFO - Filling up the DagBag from /opt/airflow/dags/python_plugins.py: source="airflow.models.dagbag.DagBag"
[2025-05-31, 12:10:35] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.operators.python.PythonOperator"
[2025-05-31, 12:10:35] INFO - 2025-05-31 03:10:35.099945: chan="stdout": source="task"
```

## Decorator
- Airflow 공식 문서에서 `PythonOperator` 사용하는 것보다는 코드가 짧고 가독성이 좋은 `@task` 데코레이터를 활용하는 것을 권장

### Decorator 활용

```python
# dags/python_decorator.py

from airflow.sdk import DAG, task
import pendulum

with DAG(
    dag_id="python_decorator",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "python"],
) as dag:
    @task(task_id="python_decorator_task")
    def print_input(__input):
        print(__input)

    python_decorator_task = print_input("@task 데코레이터 실행")
```

- Airflow에서 제공하는 예시 `example_python_decorator` 를 복제 및 일부를 수정하여 DAG 선언
- 단순히 함수에 `@task` 데코레이터를 추가하고 `task_id` 파라미터를 부여

{{< bookmark "https://github.com/apache/airflow/blob/providers-standard/1.2.0/providers/standard/tests/system/standard/example_python_decorator.py" >}}

- DAG를 실행한 후 `python_decorator_task` 의 실행 로그에서 전달한 인수가 출력된 것을 확인

```bash
[2025-05-31, 12:29:22] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-05-31, 12:29:22] INFO - Filling up the DagBag from /opt/airflow/dags/python_decorator.py: source="airflow.models.dagbag.DagBag"
[2025-05-31, 12:29:22] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.decorators.python._PythonDecoratedOperator"
[2025-05-31, 12:29:22] INFO - @task 데코레이터 실행: chan="stdout": source="task"
```

## Parameter
- 파이썬에서는 함수에 순서대로 인자를 전달하거나 키-값의 형태로 파라미터를 전달 가능
- 순서대로 전달되는 인자를 배열로 받을 때는 `*args` 와 같이 `*` 를 붙여서 Tuple 타입의 객체를 받을 수 있음
- 키-값의 형태로 전달되는 파라미터를 받을 때는 `**kwargs` 와 같이 `**` 를 붙여서 딕셔너리 타입의 객체를 받을 수 있음
- 인자와 파라미터를 모두 받아서 출력하는 함수 `regist()` 를 아래와 같이 구현

```python
# plugins/common/common_func.py

def regist(name: str, age: int, *args, **kwargs):
    print(f"이름: {name}")
    print(f"나이: {age}")
    for __key, __value in kwargs.items():
        print(f"{__key}: {__value}")
    if args:
        print(f"기타 정보: {args}")
```

### op_args, op_kwargs
- `PythonOperator` 도 함수를 실행할 때 인자 또는 파라미터를 전달할 수 있는 방법을 제공
- 인자를 전달할 때는 `op_args` 파라미터에 배열 객체를 전달
- 파라미터를 전달할 때는 `op_kwargs` 파라미터에 딕셔너리 객체를 전달

```python
# dags/python_parameter.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from common.common_func import regist
import pendulum

with DAG(
    dag_id="python_parameter",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "python"],
) as dag:
    regist_task = PythonOperator(
        task_id="regist_task",
        python_callable=regist,
        op_args=["김철수", 20, "서울", "대한민국"],
        op_kwargs={"이메일":"su@example.com", "전화번호":"010-1234-5678"},
    )
```

- DAG를 실행한 후 `regist_task` 의 실행 로그에서 전달한 인자와 파라미터가 출력된 것을 확인
- 실제로는 직접 전달한 파라미터 외에 `ds` 또는 `ts` 등 Airflow에서 만들어지는 파라미터가 같이 전달되는 것 같은데
  앞으로 Airflow를 알게되면서 활용할 수 있을 것을 기대

```bash
[2025-05-31, 15:04:22] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-05-31, 15:04:22] INFO - Filling up the DagBag from /opt/airflow/dags/python_parameter.py: source="airflow.models.dagbag.DagBag"
[2025-05-31, 15:04:23] INFO - 이름: 김철수: chan="stdout": source="task"
...
[2025-05-31, 15:04:23] INFO - 나이: 20: chan="stdout": source="task"
...
[2025-05-31, 15:04:23] INFO - 이메일: su@example.com: chan="stdout": source="task"
[2025-05-31, 15:04:23] INFO - 전화번호: 010-1234-5678: chan="stdout": source="task"
...
[2025-05-31, 15:04:23] INFO - 기타 정보: ('서울', '대한민국'): chan="stdout": source="task"
```
