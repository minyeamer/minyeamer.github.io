---
title: "Apache Airflow - Operator (Branch, Email)"
date: "2025-06-06T16:36:50+09:00"
layout: "post"
description: >
  Apache Airflow의 BranchOperator와 EmailOperator 개념을 소개하고, Branching 기능과 이메일 전송 방법을 단계별로 안내합니다.
  BranchPythonOperator, @task.branch 데코레이터, BaseBranchOperator 상속, SMTP 설정, Connection 추가, SSLError 해결까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&st=n484uuow&dl=0"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "BranchOperator", "EmailOperator", "Branching", "SMTP", "Email", "데이터 엔지니어링", "Python", "Study"]
---

## BranchOperator

### Branching

{{< bookmark "https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#branching" >}}

- 특정 Task의 결과에 따라 하위 Task를 선별해서 수행시키고 싶을 때 사용

![branch_good - Airflow Documentation](https://dl.dropboxusercontent.com/scl/fi/72b4oq3ksv4r7gs6ykyf2/airflow-25-branch-workflow.webp?rlkey=zm635gumlsypzyjip6ao28j5a&dl=0)

### BranchPythonOperator
- `BranchPythonOperator` 에서 랜덤한 조건에 따라 `task_a` 만 수행하거나, `task_b` 와 `task_c` 를 같이 수행하는 분기 처리

```python
# dags/branch_python.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
import pendulum

with DAG(
    dag_id="branch_python",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    def select_random():
        import random

        item_lst = ['A','B','C']
        selected_item = random.choice(item_lst)
        if selected_item == 'A':
            return "task_a"
        else:
            return ["task_b","task_c"]

    branch_task = BranchPythonOperator(
        task_id="branch_task",
        python_callable=select_random
    )

    def print_selected(**kwargs):
        print(kwargs["selected"])

    task_a = PythonOperator(
        task_id="task_a",
        python_callable=print_selected,
        op_kwargs={"selected":'A'}
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=print_selected,
        op_kwargs={"selected":'B'}
    )

    task_c = PythonOperator(
        task_id="task_c",
        python_callable=print_selected,
        op_kwargs={"selected":'C'}
    )

    branch_task >> [task_a, task_b, task_c]
```

- 여러 번 Trigger하여 실행했는데, 의도대로 `task_a` 만 수행되거나, `task_b` 와 `task_c` 가 같이 수행되는 두 가지 경우를 확인

{{< img-two
  src-left="https://dl.dropboxusercontent.com/scl/fi/zmqrndlh8ei1rlngzxz76/airflow-26-branch-success-a.webp?rlkey=zxsorrt87pao4n0azm8j8378q&dl=0"
  alt-left="branch_task >> task_a 성공"
  src-right="https://dl.dropboxusercontent.com/scl/fi/uu93j7ryw1blnzp5m178z/airflow-27-branch-success-bc.webp?rlkey=kd14bt6phatm40q8mbb56iyoc&dl=0"
  alt-right="branch_task >> task_b, task_c 성공" >}}

- 또한, `task_a` 가 선택되는 작업에서 XCom을 보면 `skipmixin_key` 키로 `{'followed': ['task_a']}` 값이 전달되는데,
  이를 통해 다른 Task에서도 어떤 분기 처리가 되었는지 확인 가능

![skipmixin_key = {'followed': ['task_a']}](https://dl.dropboxusercontent.com/scl/fi/jrraft65v5seeqr3hr21f/airflow-28-branch-skipmixin-key.webp?rlkey=ndgnddwg7dxwruzts4ke8pywa&dl=0)

- 마찬가지로 실행 로그에서도 어떤 Task가 선택되었고, 어떤 Task가 Skip되었는지 조회 가능

```bash
# branch_task

[2025-06-06, 11:19:07] INFO - Done. Returned value was: task_a: source="airflow.task.operators.airflow.providers.standard.operators.python.BranchPythonOperator"
[2025-06-06, 11:19:07] INFO - Branch into task_a: source="airflow.task.operators.airflow.providers.standard.operators.python.BranchPythonOperator"
[2025-06-06, 11:19:07] INFO - Following branch {'task_a'}: source="airflow.task.operators.airflow.providers.standard.operators.python.BranchPythonOperator"
[2025-06-06, 11:19:07] INFO - Skipping tasks [('task_b', -1), ('task_c', -1)]: source="airflow.task.operators.airflow.providers.standard.operators.python.BranchPythonOperator"
[2025-06-06, 11:19:07] INFO - Skipping downstream tasks.: source="task"
```

### @task.branch
- `BranchPythonOperator` 대신에 `@task.branch` 데코레이터를 써서 아래와 같이 표현도 가능
- 함수를 호출하여 종속성 표현 (`select_random() >> [task_a, task_b, task_c]`)

```python
# dags/branch_python_decorator.py

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="branch_python_decorator",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    @task.branch(task_id="branch_task")
    def select_random():
        import random

        item_lst = ['A','B','C']
        selected_item = random.choice(item_lst)
        if selected_item == 'A':
            return "task_a"
        else:
            return ["task_b","task_c"]

    def print_selected(**kwargs):
        print(kwargs["selected"])

    task_a = PythonOperator(
        task_id="task_a",
        python_callable=print_selected,
        op_kwargs={"selected":'A'}
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=print_selected,
        op_kwargs={"selected":'B'}
    )

    task_c = PythonOperator(
        task_id="task_c",
        python_callable=print_selected,
        op_kwargs={"selected":'C'}
    )

    select_random() >> [task_a, task_b, task_c]
```

### BaseBranchOperator

{{< bookmark "https://airflow.apache.org/docs/apache-airflow/2.9.2/_api/airflow/operators/branch/index.html#airflow.operators.branch.BaseBranchOperator" >}}

- Branching 기능을 제공하는 Operator의 기본 클래스
- 해당 클래스를 상속받을 경우 `choose_branch(self, context)` 메서드를 구현해야 하고,
  분기 처리 로직을 통해 선택되어야 할 Task를 한 개(문자열) 또는 여러 개(리스트)로 반환해야 함

```python
# dags/branch_base.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.branch import BaseBranchOperator
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="branch_base",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    class CustomBranchOperator(BaseBranchOperator):
        def choose_branch(self, context):
            import random

            item_lst = ['A','B','C']
            selected_item = random.choice(item_lst)
            if selected_item == 'A':
                return "task_a"
            else:
                return ["task_b","task_c"]

    custom_branch_task = CustomBranchOperator(task_id="custom_branch_task")

    def print_selected(**kwargs):
        print(kwargs["selected"])

    task_a = PythonOperator(
        task_id="task_a",
        python_callable=print_selected,
        op_kwargs={"selected":'A'}
    )

    task_b = PythonOperator(
        task_id="task_b",
        python_callable=print_selected,
        op_kwargs={"selected":'B'}
    )

    task_c = PythonOperator(
        task_id="task_c",
        python_callable=print_selected,
        op_kwargs={"selected":'C'}
    )

    custom_branch_task >> [task_a, task_b, task_c]
```

## EmailOperator

{{< bookmark "https://airflow.apache.org/docs/apache-airflow/1.10.9/_api/airflow/operators/email_operator/index.html" >}}

- 이메일을 전송해주는 Operator
- SMTP 프로토콜을 통해 개인 Gmail에서 다른 주소로 메일을 보내는 기능 구현
- Gmail 옵션에서 [IMAP 사용 설정](https://support.google.com/a/answer/9003945)
  및 [앱 비밀번호 생성](https://support.google.com/accounts/answer/185833)이 선행되어야 함

### docker-compose 수정

{{< bookmark "https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html" >}}

- `docker-compose.yaml` 파일 내에 아래와 같은 항목을 추가
- `AIRFLOW__SMTP__SMTP_USER` 에는 앱 비밀번호를 생성한 구글 계정을 입력
- `AIRFLOW__SMTP__SMTP_PASSWORD` 에는 발급받은 앱 비밀번호를 공백없이 입력
- `AIRFLOW__SMTP__SMTP_MAIL_FROM` 에는 메일을 보내는 계정을 입력

```yaml
# docker-compose.yaml

x-airflow-common:
  environment:
    AIRFLOW__SMTP__SMTP_HOST: smtp.gmail.com
    AIRFLOW__SMTP__SMTP_USER: ${SMTP_USER}
    AIRFLOW__SMTP__SMTP_PASSWORD: ${SMTP_PASSWORD}
    AIRFLOW__SMTP__SMTP_PORT: 587
    AIRFLOW__SMTP__SMTP_MAIL_FROM: ${SMTP_USER}
```

### Connection 추가

{{< bookmark "https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html" >}}

- Airflow 3.0 버전부터는 SMTP 설정을 환경변수나 설정 파일에서 가져오는 것이 아닌, Connection을 활용하도록 권장
- Airflow UI의 사이드바에서 `Admin->Connections` 메뉴로 이동한 후, `Add Connection` 버튼을 클릭하여 Connection 추가
- 아래 이미지와 같이 `Connection Type` 으로 `smtp` 를 선택하고,
  docker-compose 파일에 추가했던 것처럼 구글 계정과 앱 비밀번호를 포함한 메일 연결 설정을 입력
- `Extra Fields` 에서 메일을 보내는 계정 등 추가적인 정보를 입력 가능

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/7tj5wzmg7xo93p8cftpps/airflow-29-smtp-connection.webp?rlkey=sglggl4g8gib7vr4stn0jw1ae&dl=0"
  alt="Edit Connection - SMTP"
  max-width="691px"
  align="center" >}}

### EmailOperator 활용 예시
- 생성한 Connection을 사용하기 위해 `conn_id` 로 지정한 `Connection ID` 를 입력
- 대상 이메일 주소를 `to` 에 입력하고, 제목은 `subject`, 내용은 `html_content` 에 입력
- 참조를 추가할 시 `cc` 파라미터로 추가로 입력 가능

```python
from airflow.sdk import DAG
from airflow.providers.smtp.operators.smtp import EmailOperator
import pendulum

with DAG(
    dag_id="email_operator",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 9 1 * *",
    catchup=False,
    tags=["example", "email"],
) as dag:
    send_email_task = EmailOperator(
        task_id="send_email_task",
        conn_id="gmail",
        to="example@gmail.com",
        subject="Airflow 테스트",
        html_content="Airflow 작업이 완료되었습니다."
    )
```

### SSLError

- 정상적으로 메일이 보내질 것을 기대했지만, 예상치못한 `SSLError` 가 발생

```bash
SSLError: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1010)
...
File "/usr/local/lib/python3.12/smtplib.py", line 1022 in __init__
File "/usr/local/lib/python3.12/smtplib.py", line 255 in __init__
File "/usr/local/lib/python3.12/smtplib.py", line 341 in connect
File "/usr/local/lib/python3.12/smtplib.py", line 1029 in _get_socket
File "/usr/local/lib/python3.12/ssl.py", line 455 in wrap_socket
File "/usr/local/lib/python3.12/ssl.py", line 1041 in _create
File "/usr/local/lib/python3.12/ssl.py", line 1319 in do_handshake
```

- 원인 파악은 못했지만, Connection에서 SSL 비활성화 후 재시도하니 정상적으로 메일 전송

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/jrubhr3qfjs3pv2ll5csk/airflow-30-smtp-disable-ssl.webp?rlkey=fp6yfxpdgry4h7ojyuv77ruel&dl=0"
  alt="Edit Connection - SMTP > Disable SSL"
  max-width="691px"
  align="center" >}}

### 메일 발송 확인
- 정상적으로 메일이 전송되었을 때, 대상 메일에 접속하면 `EmailOperator` 에서 지정한 것과 동일한 제목과 내용의 메일이 전송된 것을 확인 가능

```html
<h2>Airflow 테스트</h2> <!-- 제목 -->
<div>Airflow 작업이 완료되었습니다.</div> <!-- 내용 -->
```

- 실행 로그에서도 메일 전송을 위해 임의로 생성한 Connection `gmail` 을 사용한 것을 확인

```bash
[2025-06-06, 21:10:46] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-06, 21:10:46] INFO - Filling up the DagBag from /opt/airflow/dags/email_operator.py: source="airflow.models.dagbag.DagBag"
[2025-06-06, 21:10:46] INFO - Secrets backends loaded for worker: count=1: backend_classes=["EnvironmentVariablesBackend"]: source="supervisor"
[2025-06-06, 21:10:46] INFO - Connection Retrieved 'gmail': source="airflow.hooks.base"
```
