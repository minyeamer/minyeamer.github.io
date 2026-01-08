---
title: "Apache Airflow - DAG 흐름 제어 (Trigger Rule, TriggerDagRun, TaskGroup)"
date: "2025-06-07T11:08:37+09:00"
layout: "post"
description: >
  Apache Airflow의 Trigger Rule과 TriggerDagRunOperator 개념을 소개하고, TaskGroup과 Edge Label 사용법을 단계별로 안내합니다.
  DAG 실행 트리거, 그룹화, 라벨링, Trigger Rule 옵션까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&raw=1"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "TriggerDagRunOperator", "TaskGroup", "Trigger Rule", "Edge Label", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
series: ["Apache Airflow 배우기"]
---

{{< series "Apache Airflow 배우기" "Apache Airflow - " >}}

## Trigger Rule

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#trigger-rules"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- 상위 Task들의 상태에 따라 수행여부를 결정하고 싶을 때 사용
- 기본적으로는 상위 Task가 모두 성공해야 실행

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/dydw147s5pt1s7fg6leop/airflow-31-trigger-rule.webp?rlkey=rg9lo0dungmd863zk8gh76fgj&raw=1"
  alt="Trigger Rule (Failed, Skipped, Success -> Running)"
  max-width="691px"
  align="center"
  href="https://marclamberti.com/blog/airflow-trigger-rules-all-you-need-to-know/" >}}

### Trigger Rule 종류

|옵션|설명|
|---|---|
|`all_success`|기본값, 상위 Task가 모두 성공하면 실행|
|`all_failed`|상위 Task가 모두 `failed` 상태면 실행|
|`all_done`|상위 Task가 모두 수행되면 실행 (성공 또는 실패)|
|`all_skipped`|상위 Task가 모두 `skipped` 상태면 실행|
|`one_failed`|상위 Task 중 하나 이상 실패하면 실행|
|`one_success`|상위 Task 중 하나 이상 성공하면 실행|
|`one_done`|상위 Task 중 하나 이상 수행되면 실행 (성공 또는 실패)|
|`none_failed`|상위 Task 중에 `failed` 상태가 없으면 실행|
|`none_failed_min_one_success`|상위 Task 중에 `failed` 상태가 없고 성공한 Task가 1개 이상이면 실행|
|`none_skipped`|상위 Task 중에 `skipped` 상태가 없으면 실행|
|`always`|항상 실행|

### all_done 예시
- `all_done` 의 동작을 확인하기 위한 예시 DAG 작성
- 3개의 상위 Task 중 2번째 Task에서 의도적으로 예외를 발생시켜서 `failed` 상태를 유발
- 하위 Task `downstream_task` 에 `trigger_rule` 파라미터로 `all_done` 전달

```python
# dags/trigger_rule1.py

from airflow.sdk import DAG, task
from airflow.exceptions import AirflowException
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="trigger_rule1",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    upstream_task1 = BashOperator(
        task_id="upstream_task1",
        bash_command="echo upstream1"
    )

    @task(task_id="upstream_task2")
    def upstream_task2():
        raise AirflowException("upstream2 Exception")

    @task(task_id="upstream_task3")
    def upstream_task3():
        print("정상 처리")

    @task(task_id="downstream_task", trigger_rule="all_done")
    def downstream_task():
        print("정상 처리")

    [upstream_task1, upstream_task2(), upstream_task3()] >> downstream_task()
```

- `all_done` 은 상위 Task가 성공 또는 실패 여부에 관계없이 모두 수행되면 실행하는 옵션으로,
  `upstream_task2` 가 실패 처리되어도 `downstream_task` 가 수행되는 모습을 확인

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/dxr2449t4dkkoomh1qr1u/airflow-32-trigger-all-done.webp?rlkey=9vxn9jjqug6t88csakmh9m87y&raw=1"
  alt="all_done - upstream failed > downstream success"
  max-width="518px"
  align="center" >}}

### none_skipped 예시
- `none_skipped` 의 동작을 확인하기 위한 예시 DAG 작성
- 3개의 상위 Task 중 랜덤한 한 Task만 수행하고 나머지 Task에선 `skipped` 상태를 유발
- 하위 Task `downstream_task` 에 `trigger_rule` 파라미터로 `none_skipped` 전달

```python
# dags/trigger_rule2.py

from airflow.sdk import DAG, task
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="trigger_rule2",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    @task.branch(task_id="branching")
    def random_branch():
        import random

        item_lst = ['A','B','C']
        selected_item = random.choice(item_lst)
        if selected_item == 'A':
            return "upstream_task_a"
        elif selected_item == 'B':
            return "upstream_task_b"
        elif selected_item == 'C':
            return "upstream_task_c"

    upstream_task_a = BashOperator(
        task_id="upstream_task_a",
        bash_command="echo upstream1"
    )

    @task(task_id="upstream_task_b")
    def upstream_task_b():
        print("정상 처리")

    @task(task_id="upstream_task_c")
    def upstream_task_c():
        print("정상 처리")

    @task(task_id="downstream_task", trigger_rule="none_skipped")
    def downstream_task():
        print("정상 처리")

    random_branch() >> [upstream_task_a, upstream_task_b(), upstream_task_c()] >> downstream_task()
```

- `none_skipped` 은 상위 Task가 `skipped` 상태가 아니어야 실행하는 옵션으로, `upstream_task1` 만 성공하고
  나머지는 `skipped` 처리되었기 때문에, `downstream_task` 도 수행되지 못하고 `skipped` 처리

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/3tjf1xjx31kjcufq3fkmp/airflow-33-trigger-none-skipped.webp?rlkey=t89irlnfi2j04e61kh7tie1yz&raw=1"
  alt="none_skipped - upstream failed > downstream success"
  max-width="691px"
  align="center" >}}

## TriggerDagRunOperator

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/2.3.4/_api/airflow/operators/trigger_dagrun/index.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- 다른 DAG을 실행시키는 Operator
- 실행할 다른 DAG의 ID를 지정하여 수행
- 선행 DAG이 하나만 있을 경우 `TriggerDagRunOperator` 를 사용하고, 선행 DAG이 2개 이상인 경우는 `ExternalTaskSensor` 를 사용 권장

{{% columns %}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/vxkt9g7uy44cwfc4vl174/airflow-34-trigger-dagrun-operator.webp?rlkey=t3i8pjpa7l1yfsscggh3d3j8t&raw=1"
  alt="TriggerDagRunOperator" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/o2urlt1hg28y1apeobgom/airflow-35-external-task-sensor.webp?rlkey=rg8l6wgbfja8jw934akg8t5qg&raw=1"
  alt="ExternalTaskSensor" >}}
{{% /columns %}}

### run_id
- DAG의 수행 방식과 시간을 유일하게 식별해주는 키
- 수행 방식(Schedule, manual, Backfill)에 따라 키가 달라짐
- 스케줄에 의해 실행된 경우 scheduled__{{data_interval_start}} 값을 가짐
   - 예시) `scheduled__2025-06-01T00:00:00+00:00`

### TriggerDagRun 활용
- `trigger_run_id` : DAG을 실행시킬 때 어떤 `run_id` 로 실행할지 지정 가능
- `logical_date` : DAG이 트리거된 시간을 지정 가능, `manual__{{logical_date}}`
- `reset_dag_run` : `run_id` 로 수행된 이력이 있어도 실행시키려면 `True` 로 설정
- `wait_for_completion` : 지정한 DAG이 완료되어야 다음 Task를 실행하고 싶을 경우 `True` 로 설정
   - 기본적으로는 DAG의 완료 여부에 관계없이 `success` 로 빠져나가 다음 Task를 실행
- `poke_interval` : 지정한 DAG이 완료되었는지 확인하는 주기
- `allowed_states` : Task가 `success` 상태가 되기 위한 DAG의 처리 상태 목록
- `failed_states` : Task가 `failed` 상태가 되기 위한 DAG의 처리 상태 목록

```python
# dags/trigger_dagrun.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="trigger_dagrun",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "dagrun"],
) as dag:
    start_task = BashOperator(
        task_id="start_task",
        bash_command="echo \"start!\"",
    )

    trigger_dag_task = TriggerDagRunOperator(
        task_id="trigger_dag_task",
        trigger_dag_id="python_operator",
        trigger_run_id=None,
        logical_date="{{data_interval_start}}",
        reset_dag_run=True,
        wait_for_completion=False,
        poke_interval=60,
        allowed_states=["success"],
        failed_states=None
        )

    start_task >> trigger_dag_task
```

### DAG 실행
- `trigger_dag_task` 의 실행 로그에서 `python_operator` 가 호출된 것을 확인

```bash
[2025-06-07, 10:52:54] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-07, 10:52:54] INFO - Filling up the DagBag from /opt/airflow/dags/trigger_dagrun.py: source="airflow.models.dagbag.DagBag"
[2025-06-07, 10:52:54] INFO - Triggering Dag Run.: trigger_dag_id="python_operator": source="task"
[2025-06-07, 10:52:54] INFO - Dag Run triggered successfully.: trigger_dag_id="python_operator": source="task"
```

- 두 번째 이미지인 PythonOperator의 `run_id` 가 첫 번째 이미지인 TriggerDagRunOperator의 실행 시간과 같다는 것을 알 수 있으며,
  `trigger_run_id` 를 지정하지 않았기 때문에 `manual` 로 지정

![Scheduled Dag Run](https://dl.dropboxusercontent.com/scl/fi/6sxhtm8e4yteuivcrjqla/airflow-36-trigger-dagrun-scheduled.webp?rlkey=wvlbjj9imkl733q0ujdi9ot6k&raw=1)

![Manual Dag Run](https://dl.dropboxusercontent.com/scl/fi/76871p6tozn66wxhspgsq/airflow-37-trigger-dagrun-manual.webp?rlkey=3azwukh8qp6syyb8p8u5vgh0d&raw=1)


## TaskGroup

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- 여러 Task들을 그룹화하는 개념
- UI 상에서 Task들을 모아서 편하게 보고 관리하기 쉽게 하기 위한 목적

![TaskGroups - Airflow Documentation](https://dl.dropboxusercontent.com/scl/fi/0ake7j9qyw49ei0nze6n3/airflow-38-task-group.gif?rlkey=eauhbvmxgwh15ybsyx2yh57xn&raw=1)

### TaskGroup 활용
- `@task_group` 데코레이터 또는 `TaskGroup` 클래스를 활용하여 TaskGroup을 구현
- docstring을 추가해 Airflow UI에서 TaskGroup에 대한 Tooltip을 표시
   - 또는, `tooltip` 파라미터로 UI에 표시할 내용을 전달할 수도 있음 (파라미터가 docstring보다 우선)

```python
# dags/task_group.py

from airflow.sdk import DAG, task, task_group, TaskGroup
from airflow.providers.standard.operators.python import PythonOperator
import pendulum

with DAG(
    dag_id="task_group",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    def inner_function2(**kwargs):
        msg = kwargs.get("msg") or str() 
        print(msg)

    @task_group(group_id="first_group")
    def first_group():
        """ 첫 번째 TaskGroup 에 대한 Tooltip 입니다. """

        @task(task_id="inner_function1")
        def inner_function1(**kwargs):
            print("첫 번째 TaskGroup 내 첫 번째 Task 입니다.")

        inner_function2 = PythonOperator(
            task_id="inner_function2",
            python_callable=inner_function2,
            op_kwargs={"msg":"첫 번째 TaskGroup 내 두 번째 Task 입니다."}
        )

        inner_function1() >> inner_function2

    with TaskGroup(group_id="second_group", tooltip="두 번째 TaskGroup 에 대한 Tooltip 입니다.") as second_group:
        """ tooltip 파라미터의 내용이 우선적으로 표시됩니다. """
        @task(task_id="inner_function1")
        def inner_function1(**kwargs):
            print("두 번째 TaskGroup 내 첫 번째 Task 입니다.")

        inner_function2 = PythonOperator(
            task_id="inner_function2",
            python_callable=inner_function2,
            op_kwargs={"msg": "두 번째 TaskGroup 내 두 번째 Task 입니다."}
        )

        inner_function1() >> inner_function2

    first_group() >> second_group
```

### TaskGroup 조회
- DAG 실행 후 Graph View에서 두 개의 TaskGroup을 확인
- 기대와 다르게 지정한 Tooltip이 표시되지 않았는데, Airflow 3.0 버전의 버그인 것으로 추정

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/8eszfqcf35b9trq3n7yzi/airflow-39-task-group-summary.webp?rlkey=87f0vvl76lsxexlqz8i8385mb&raw=1"
  alt="TaskGroup 요약"
  max-width="518px"
  align="center" >}}

- TaskGroup을 클릭하면 펼쳐지면서 내부 Task를 표시

![TaskGroup 상세](https://dl.dropboxusercontent.com/scl/fi/xlxj8po8fb7c79w4kt03x/airflow-40-task-group-detail.webp?rlkey=epggkqvb5m36jsf3bsse28ntb&raw=1)

## Edge Label

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#edge-labels"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&raw=1" >}}

- Task 연결에 대한 설명을 추가하는 개념
- Task 종속성을 나타내는 `>>` 또는 `<<` 연산자 사이에 `Label` 을 추가

### Edge Label 활용
- 첫 번째 Label은 두 개의 단일 Task 사이를 연결
- 두 번째와 세 번째 Label은 Branch의 시작과 끝을 각각 연결

```python
# dags/edge_label.py

from airflow.sdk import DAG, Label
from airflow.providers.standard.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id="edge_label",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    schedule="0 0 * * *",
    catchup=False,
    tags=["example", "branch"],
) as dag:
    empty_1 = EmptyOperator(
        task_id="empty_1"
    )

    empty_2 = EmptyOperator(
        task_id="empty_2"
    )

    empty_1 >> Label("라벨") >> empty_2

    empty_3 = EmptyOperator(
        task_id="empty_3"
    )

    empty_4 = EmptyOperator(
        task_id="empty_4"
    )

    empty_5 = EmptyOperator(
        task_id="empty_5"
    )

    empty_6 = EmptyOperator(
        task_id="empty_6"
    )

    empty_2 >> Label("브랜치 시작") >> [empty_3,empty_4,empty_5] >> Label("브랜치 종료") >> empty_6
```

### Edge Label 조회
- Airflow UI의 Graph View에서 Edge Label을 확인
- Branch 연결에 대해서는 모든 연결에 동일한 내용의 Label을 표시

![Edge Label - 브랜치 시작 > 브랜치 종료](https://dl.dropboxusercontent.com/scl/fi/81h4ymeiwu26fjkdbozxw/airflow-41-edge-label.webp?rlkey=vw8g2kjbmf2kq2q1n988nj4vg&raw=1)
