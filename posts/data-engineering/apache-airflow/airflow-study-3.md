---
title: "Apache Airflow - 데이터 전달과 템플릿 활용 (Jinja, XCom, Variable)"
date: "2025-06-01T23:46:09+09:00"
layout: "post"
description: >
  Apache Airflow의 Jinja 템플릿과 XCom을 소개하고, 템플릿 변수 활용과 Task 간 데이터 공유 방법을 단계별로 안내합니다.
  Variable 사용법과 Airflow 3.0 업데이트 내용까지 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&dl=0"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "Jinja 템플릿", "XCom", "Variable", "템플릿 변수", "BashOperator", "PythonOperator", "데이터 엔지니어링", "에어플로우", "Python", "Study"]
---

## Jinja 템플릿

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- 파이썬 기반 웹 프레임워크 Flask, Django에서 주로 사용
- HTML 템플릿을 만들고 화면에 보여질 때 값을 렌더링해서 출력
- Airflow에서는 파라미터 입력 시 중괄호 2개 `{{ }}` 를 이용해 변수를 치환된 값으로 입력

#### 변수 목록 (중괄호 생략)
- **`data_interval_start`** : 스케줄의 시작 날짜이며,`pendulum.DateTime` 타입
- **`data_interval_end`** : 스케줄의 종료 날짜(= 배치일)이며,`pendulum.DateTime` 타입
- **`logical_date`** : DAG가 실행 중인 시점의 날짜이며,`pendulum.DateTime` 타입
- **`ds`** : `logical_date` 를 `YYYY-MM-DD` 형태의 문자열로 변환한 값
   - `ds` 에서 `-` 을 제거한 `YYYYMMDD` 형태의 문자열 `ds_nodash` 변수도 제공
- **`ts`** : `logical_date` 를 `2018-01-01T00:00:00+00:00` 형태의 문자열로 변환한 값
   - `ts_nodash_with_tz` 또는 `ts_nodash` 등의 변형된 변수도 지원
- `ds` 또는 `ts` 등은 `{{ logical_date | ds }}` 의 형태로도 표현 가능

#### 적용 대상
- BashOperator에서는 `bash_command`, `env` 파라미터에 템플릿 적용 가능
- PythonOperator에서는 `templates_dict`, `op_args`, `op_kwargs` 파라미터에 템플릿 적용 가능
- Airflow의 각 Operator 문서에서 **Templating** 부분 참고

## Jinja 템플릿 변수 활용

### BashOperator
- Jinja 템플릿 변수를 그대로 출력하는 명령어를 실행하는 DAG 구성
- 첫 번째 Task는 변수를 그대로 출력하고, 두 번째 Task는 `env`로 파라미터를 전달해서 출력

```python
# dags/bash_template.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_template",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    bash_task1 = BashOperator(
        task_id="bash_task1",
        bash_command="echo \"End date is {{ data_interval_end }}\"",
    )

    bash_task2 = BashOperator(
        task_id="bash_task2",
        env={
            "START_DATE": "{{ data_interval_start | ds }}",
            "END_DATE": "{{ data_interval_end | ds }}"
        },
        bash_command="echo \"Start date is $START_DATE \" && echo \"End date is $END_DATE\"",
    )

    bash_task1 >> bash_task2
```

- DAG 실행 후 `bash_task1` 의 실행 로그에서 `data_interval_end` 가 시간대를 포함하여 전체 출력된 것을 확인
- `bash_task2` 의 실행 로그에서는 `data_interval_start` 와 `data_interval_end` 이 YYYY-MM-DD 형태의 문자열로 출력된 것을 확인

```bash
# bash_task1

[2025-06-01, 19:59:27] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-01, 19:59:27] INFO - Filling up the DagBag from /opt/airflow/dags/bash_template.py: source="airflow.models.dagbag.DagBag"
[2025-06-01, 19:59:27] INFO - Running command: ['/usr/bin/bash', '-c', 'echo "End date is 2025-05-31 15:00:00+00:00"']: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:27] INFO - Output:: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:27] INFO - End date is 2025-05-31 15:00:00+00:00: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:27] INFO - Command exited with return code 0: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:27] INFO - Pushing 
```

```bash
[2025-06-01, 19:59:28] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-01, 19:59:28] INFO - Filling up the DagBag from /opt/airflow/dags/bash_template.py: source="airflow.models.dagbag.DagBag"
[2025-06-01, 19:59:28] INFO - Running command: ['/usr/bin/bash', '-c', 'echo "Start date is $START_DATE " && echo "End date is $END_DATE"']: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:28] INFO - Output:: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:28] INFO - Start date is 2025-05-31: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:28] INFO - End date is 2025-05-31: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:28] INFO - Command exited with return code 0: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-01, 19:59:28] INFO - Pushing 
```

### PythonOperator (1)
- keyword argument로 전달되는 Jinja 템플릿 변수를 출력하는 명령어를 실행하는 DAG 구성
- 이전에 한번 `**kwargs` 내용을 출력한적이 있었는데, 직접 전달하지 않았음에도 출력되었던 값들이 바로 Jinja 템플릿 변수에 해당

```python
# dags/python_template1.py

from airflow.sdk import DAG, task
import pendulum

with DAG(
    dag_id="python_template1",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    @task(task_id="python_task")
    def show_templates(**kwargs):
        from pprint import pprint
        pprint(kwargs)

    show_templates()
```

- DAG 실행 후 `python_task` 의 실행 로그에서 `data_interval_end`, `data_interval_start` 등 Jinja 템플릿 변수가 출력된 것을 확인

```bash
[2025-06-01, 20:18:19] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-01, 20:18:19] INFO - Filling up the DagBag from /opt/airflow/dags/python_template.py: source="airflow.models.dagbag.DagBag"
[2025-06-01, 20:18:19] INFO - {'conn': <ConnectionAccessor (dynamic access)>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'dag': <DAG: python_template>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'dag_run': DagRun(dag_id='python_template', run_id='scheduled__2025-05-31T15:00:00+00:00', logical_date=datetime.datetime(2025, 5, 31, 15, 0, tzinfo=TzInfo(UTC)), data_interval_start=datetime.datetime(2025, 5, 31, 15, 0, tzinfo=TzInfo(UTC)), data_interval_end=datetime.datetime(2025, 5, 31, 15, 0, tzinfo=TzInfo(UTC)), run_after=datetime.datetime(2025, 5, 31, 15, 0, tzinfo=TzInfo(UTC)), start_date=datetime.datetime(2025, 6, 1, 11, 18, 19, 250768, tzinfo=TzInfo(UTC)), end_date=None, clear_number=0, run_type=<DagRunType.SCHEDULED: 'scheduled'>, conf={}, consumed_asset_events=[]),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'data_interval_end': DateTime(2025, 5, 31, 15, 0, 0, tzinfo=Timezone('UTC')),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'data_interval_start': DateTime(2025, 5, 31, 15, 0, 0, tzinfo=Timezone('UTC')),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ds': '2025-05-31',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ds_nodash': '20250531',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'inlet_events': InletEventsAccessors(_inlets=[], _assets={}, _asset_aliases={}),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'inlets': [],: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'logical_date': DateTime(2025, 5, 31, 15, 0, 0, tzinfo=Timezone('UTC')),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'macros': <MacrosAccessor (dynamic access to macros)>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'map_index_template': None,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'outlet_events': <airflow.sdk.execution_time.context.OutletEventAccessors object at 0xffffaacaa810>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'outlets': [],: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'params': {},: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'prev_data_interval_end_success': <Proxy at 0xffffaad2b140 with factory <function RuntimeTaskInstance.get_template_context.<locals>.<lambda> at 0xffffaad3cfe0>>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.decorators.python._PythonDecoratedOperator"
[2025-06-01, 20:18:19] INFO -  'prev_data_interval_start_success': <Proxy at 0xffffaad2b0b0 with factory <function RuntimeTaskInstance.get_template_context.<locals>.<lambda> at 0xffffaad3cea0>>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'prev_end_date_success': <Proxy at 0xffffaacde870 with factory <function RuntimeTaskInstance.get_template_context.<locals>.<lambda> at 0xffffaad0c7c0>>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'prev_start_date_success': <Proxy at 0xffffaacde8d0 with factory <function RuntimeTaskInstance.get_template_context.<locals>.<lambda> at 0xffffaad0c720>>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'run_id': 'scheduled__2025-05-31T15:00:00+00:00',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'task': <Task(_PythonDecoratedOperator): python_task>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'task_instance': RuntimeTaskInstance(id=UUID('01972b36-c56a-7d54-b52e-45bb8feb6594'), task_id='python_task', dag_id='python_template', run_id='scheduled__2025-05-31T15:00:00+00:00', try_number=1, map_index=-1, hostname='f6f932b48199', context_carrier={}, task=<Task(_PythonDecoratedOperator): python_task>, bundle_instance=LocalDagBundle(name=dags-folder), max_tries=0, start_date=datetime.datetime(2025, 6, 1, 11, 18, 19, 315990, tzinfo=TzInfo(UTC)), end_date=None, state=<TaskInstanceState.RUNNING: 'running'>, is_mapped=False, rendered_map_index=None),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'task_instance_key_str': 'python_template__python_task__20250531',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'task_reschedule_count': 0,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'templates_dict': None,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ti': RuntimeTaskInstance(id=UUID('01972b36-c56a-7d54-b52e-45bb8feb6594'), task_id='python_task', dag_id='python_template', run_id='scheduled__2025-05-31T15:00:00+00:00', try_number=1, map_index=-1, hostname='f6f932b48199', context_carrier={}, task=<Task(_PythonDecoratedOperator): python_task>, bundle_instance=LocalDagBundle(name=dags-folder), max_tries=0, start_date=datetime.datetime(2025, 6, 1, 11, 18, 19, 315990, tzinfo=TzInfo(UTC)), end_date=None, state=<TaskInstanceState.RUNNING: 'running'>, is_mapped=False, rendered_map_index=None),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'triggering_asset_events': TriggeringAssetEventsAccessor(_events=defaultdict(<class 'list'>, {})),: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ts': '2025-05-31T15:00:00+00:00',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ts_nodash': '20250531T150000',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'ts_nodash_with_tz': '20250531T150000+0000',: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -  'var': {'json': <VariableAccessor (dynamic access)>,: chan="stdout": source="task"
[2025-06-01, 20:18:19] INFO -          'value': <VariableAccessor (dynamic access)>}}: chan="stdout": source="task"
```

### PythonOperator (2)
- 이번에는 PythonOperator에 Jinja 템플릿 변수를 전달하여 출력하는 `python_task1` 정의
- keyword argument로 전달되는 Jinja 템플릿 변수 중 일부 항목만 선택해서 출력하는 `python_task2` 정의

```python
# dags/python_template2.py

from airflow.sdk import DAG, task
import pendulum

with DAG(
    dag_id="python_template2",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    def print_period(start_date, end_date, **kwargs):
        print(start_date)
        print(end_date)

    python_task1 = PythonOperator(
        task_id="python_task1",
        python_callable=print_period,
        op_kwargs={
            "start_date": "{{ data_interval_start | ds }}",
            "end_date": "{{ data_interval_end | ds }}"
        },
    )

    @task(task_id="python_task2")
    def python_task2(**kwargs):
        for __key in ["ds", "ts", "data_interval_start", "data_interval_end"]:
            if __key in kwargs:
                print(f"{__key}: {kwargs[__key]}")

    python_task1 >> python_task2()
```

- DAG 실행 후 `python_task1` 의 실행 로그에서 전달한 `data_interval_start`, `data_interval_end` 값이 YYYY-MM-DD 형태의 문자열로 출력된 것을 확인
- `python_task2` 의 실행 로그에서는 `ds`, `ts`, `data_interval_start`, `data_interval_end` 값을 keyword argument로부터 꺼내서 그대로 출력

```bash
# python_task1

[2025-06-02, 00:12:27] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-02, 00:12:27] INFO - Filling up the DagBag from /opt/airflow/dags/python_template2.py: source="airflow.models.dagbag.DagBag"
[2025-06-02, 00:12:27] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.operators.python.PythonOperator"
[2025-06-02, 00:12:27] INFO - 2025-06-01: chan="stdout": source="task"
[2025-06-02, 00:12:27] INFO - 2025-06-01: chan="stdout": source="task"
```

```bash
# python_task2

[2025-06-02, 00:12:27] INFO - DAG bundles loaded: dags-folder: source="airflow.dag_processing.bundles.manager.DagBundlesManager"
[2025-06-02, 00:12:27] INFO - Filling up the DagBag from /opt/airflow/dags/python_template2.py: source="airflow.models.dagbag.DagBag"
[2025-06-02, 00:12:27] INFO - Done. Returned value was: None: source="airflow.task.operators.airflow.providers.standard.decorators.python._PythonDecoratedOperator"
[2025-06-02, 00:12:27] INFO - ds: 2025-06-01: chan="stdout": source="task"
[2025-06-02, 00:12:27] INFO - ts: 2025-06-01T15:00:00+00:00: chan="stdout": source="task"
[2025-06-02, 00:12:27] INFO - data_interval_start: 2025-06-01 15:00:00+00:00: chan="stdout": source="task"
[2025-06-02, 00:12:27] INFO - data_interval_end: 2025-06-01 15:00:00+00:00: chan="stdout": source="task"
```

## Macro 변수

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html#macros"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- Jinja 템플릿 변수 기반으로 다양한 날짜 연산이 가능하도록 연산 모듈을 제공

### Macro 변수 목록
- **`macros.datetime`** : `datetime.datetime` 라이브러리 기반 연산 제공
- **`macros.timedelta`** : `datetime.timedelta` 라이브러리 기반 연산 제공
- **`macros.dateutil`** : `dateutil` 라이브러리 기반 연산 제공

```python
import datetime as dt
from dateutil.relativedelta import relativedelta

today = dt.date.today()

# 1일로 변경
first_date = today.replace(day=1) # datetime 연산
first_date = today + relativedelta(day=1) # dateutil 연산

# 1일 빼기
yesterday = today - dt.timedela(days=1) # timedela 연산
yesterday = today - relativedelta(days=1) # dateutil 연산
```

### Macro 변수 활용 예시
- 첫 번째 DAG `bash_macros1` 은 매월 말에 실행되도록 스케줄을 지정하고,
- 직전 배치일에서 1일을 추가한 날짜를 `START_DATE`, 배치일을 `END_DATE` 로 설정하여 1일부터 말일이 출력되기를 기대

```python
# dags/bash_macros1.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_macros1",
    schedule="0 0 L * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    bash_task1 = BashOperator(
        task_id="bash_task1",
        env={
            "START_DATE": "{{ (data_interval_start.in_timezone(\"Asia/Seoul\") + macros.dateutil.relativedelta.relativedelta(days=1)) | ds }}",
            "END_DATE": "{{ data_interval_end.in_timezone(\"Asia/Seoul\") | ds }}"
        },
        bash_command="echo \"Start date is $START_DATE \" && echo \"End date is $END_DATE\"",
    )

    bash_task1
```

- 두 번째 DAG `bash_macros2` 는 매월 둘째주 토요일에 실행되도록 스케줄을 지정하고,
  직전 배치일과 배치일을 1일로 변경해서 전월 1일과 당월 1일이 출력되기를 기대

```python
# dags/bash_macros2.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_macros2",
    schedule="0 0 * * 6#2",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    bash_task2 = BashOperator(
        task_id="bash_task2",
        env={
            "START_DATE": "{{ (data_interval_end.in_timezone(\"Asia/Seoul\") + macros.dateutil.relativedelta.relativedelta(day=1)) | ds }}",
            "END_DATE": "{{ (data_interval_end.in_timezone(\"Asia/Seoul\") + macros.dateutil.relativedelta.relativedelta(day=1)) | ds }}"
        },
        bash_command="echo \"Start date is $START_DATE \" && echo \"End date is $END_DATE\"",
    )

    bash_task2
```

- 하지만 실행 로그를 확인했을 때 기대와 다른 결과가 확인되었는데, 마치 `data_interval_start`, `data_interval_end` 가 동일한 값을 가지고 있다고 생각됨

```bash
# bash_task1 (bash_macros1)

[2025-06-03, 10:54:43] INFO - Start date is 2025-06-01: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-03, 10:54:43] INFO - End date is 2025-05-31: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

```bash
# bash_task2 (bash_macros2)

[2025-06-03, 10:57:23] INFO - Start date is 2025-05-01: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-03, 10:57:23] INFO - End date is 2025-05-01: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

- 실제로 `bash_macros1` 의 마지막 실행 내역에 대해 Details 탭에서 실행 정보를 조회했을 때,
  `data_interval_start`, `data_interval_end` 값이 모두 동일한 배치일로 나타나는 것을 확인
- 참고 자료로 활용한 강의에서 사용했던 Airflow 2.x 버전과, 현재 사용하는 Airflow 3.x 버전에서
  `data_interval_start`, `data_interval_end` 를 결정하는 기준이 변경된 것을 인지

![Macro 변수 목록](https://dl.dropboxusercontent.com/scl/fi/wcfx74annpqby7h9qmc73/airflow-19-bash-macros.webp?rlkey=5ec769twafb9d2m9ldfnfc3rc&dl=0)

## Airflow 3.0 업데이트
- 2.9 버전에서 `data_interval` 계산 알고리즘에 영향을 주는 `create_cron_data_intervals` 파라미터가 도입되었는데,
  3.0 버전부터 기본값이 기존 `False` 에서 `True` 로 변경되면서,
  기존 `CronDataIntervalTimetable` 대신 `CronTriggerTimetable` 알고리즘이 사용되도록 변경됨
- **즉, 3.0 버전부터 기본적으로 `data_interval` 을 고려하지 않도록 변경되어 `data_interval_start` 와 `data_interval_end` 값이 모두 실제 DAG이 실행된 날짜로 표현**

> The `create_cron_data_intervals` configuration is now `False` by default.
> This means that the `CronTriggerTimetable` will be used by default instead of the `CronDataIntervalTimetable`

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html#breaking-changes"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

### CronDataIntervalTimetable
- 이전 버전의 알고리즘인 `CronDataIntervalTimetable` 의 경로를 파악해서 `bash_macros1` DAG의 스케줄을 재설정
- 실행 로그를 조회했을 때, 초기 의도대로 `START_DATE` 는 배치일 기준 1일, `END_DATE` 는 배치일인 말일이 출력되는 것을 확인

```python
# dags/bash_macros1.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.timetables.interval import CronDataIntervalTimetable
import pendulum

with DAG(
    dag_id="bash_macros1",
    schedule=CronDataIntervalTimetable("0 0 L * *", timezone="Asia/Seoul"),
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    bash_task1 = BashOperator(
        task_id="bash_task1",
        env={
            "START_DATE": "{{ (data_interval_start.in_timezone(\"Asia/Seoul\") + macros.dateutil.relativedelta.relativedelta(days=1)) | ds }}",
            "END_DATE": "{{ data_interval_end.in_timezone(\"Asia/Seoul\") | ds }}"
        },
        bash_command="echo \"Start date is $START_DATE \" && echo \"End date is $END_DATE\"",
    )

    bash_task1
```

```bash
# bash_task1 (bash_macros1)

[2025-06-03, 12:10:27] INFO - Start date is 2025-05-01: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-03, 12:10:27] INFO - End date is 2025-05-31: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

### CronTriggerTimetable
- 3.0 버전 이후에서 사용되는 `CronTriggerTimetable` 알고리즘으로도 `data_interval` 을 적용할 수 있는 방법이 있는데, `interval` 파라미터로 `timedelta` 를 전달하면 가능
- `bash_macros2` DAG의 스케줄에 `CronTriggerTimetable` 알고리즘을 적용하면서, `interval` 파라미터로 1주의 간격을 지정 (초기 의도인 매월 둘째주 토요일과는 다르게 매주 토요일로 변경)
- 실행 로그를 조회했을 때, `END_DATE` 는 배치일인 5월 31일, `START_DATE` 는 직전 배치일인 5월 24일이 출력되는 것을 확인

```python
# dags/bash_macros2.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.timetables.trigger import CronTriggerTimetable
import datetime as dt
import pendulum

with DAG(
    dag_id="bash_macros2",
    schedule=CronTriggerTimetable(
        "0 0 * * 6",
        timezone="Asia/Seoul",
        interval=dt.timedelta(weeks=1),
    ),
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "template"],
) as dag:
    bash_task2 = BashOperator(
        task_id="bash_task2",
        env={
            "START_DATE": "{{ data_interval_start.in_timezone(\"Asia/Seoul\") | ds }}",
            "END_DATE": "{{ data_interval_end.in_timezone(\"Asia/Seoul\") | ds }}"
        },
        bash_command="echo \"Start date is $START_DATE \" && echo \"End date is $END_DATE\"",
    )

    bash_task2
```

```bash
# bash_task2 (bash_macros2)

[2025-06-03, 12:20:03] INFO - Start date is 2025-05-24: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-03, 12:20:03] INFO - End date is 2025-05-31: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

## XCom

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- Cross Communication이란 의미로, Airflow DAG 내 Task 간 데이터 공유를 위해 사용되는 기술
- 주로 작은 규모의 데이터 공유를 위해 사용 (XCom 내용은 메타 DB의 xcom 테이블에 값이 저장)
   - 1GB 이상의 대용량 데이터 공유를 위해서는 외부 솔루션 사용 필요

### XCom 사용법

- keyword arguments로 전달되는 `ti` (task_instance) 객체를 활용

```python
@task(task_id="task1")
def task1(**kwargs):
	ti = kwargs["ti"]
	ti.xcom_push(key="key1", value="value1")

@task(task_id="task2")
def task2(**kwargs):
	ti = kwargs["ti"]
	value1 = ti.xcom_pull(key="key1")
    print(value1)
```

- 만약 서로 다른 Task 에서 동일한 키값을 push 한 후, 단순히 해당 키값을 pull로 꺼낼 때, 가장 마지막에 push된 키값이 반환
- 안전하게 키값을 꺼내오기 위해서는 대상 Task를 가리키는 `task_ids` 파라미터를 명시할 수 있음

> 주의) Airflow 3.0 버전에서는 `task_ids` 가 반드시 명시되어야 함

```python
@task(task_id="task2")
def task2(**kwargs):
	ti = kwargs["ti"]
	value1 = ti.xcom_pull(key="key1", task_ids="task1")
    print(value1)
```

### return 값 활용
- `@task` 데코레이터 사용 시 return 값은 자동으로 XCom에 `return_value` 키로 저장
- 다음 단계의 Task에서 이전 단계의 return 값을 꺼낼 수 있음

```python
@task(task_id="task1")
def task1(**kwargs):
	return "value1"

@task(task_id="task2")
def task2(**kwargs):
	ti = kwargs["ti"]
	value1 = ti.xcom_pull(key="return_value", task_ids="task1")
    print(value1)

task1() >> task2()
```

- 또는, 데코레이터 사용 시 함수의 출력값을 다음 함수의 입력값으로 직접 전달하는 표현을 통해 return 값을 인수로 전달할 수도 있음

```python
@task(task_id="task1")
def task1(**kwargs):
	return "value1"

@task(task_id="task2")
def task2(value1, **kwargs):
	print(value1)

task2(task1())
```

## Xcom 활용

### PythonOperator (1)
- 앞서 서술한 코드를 DAG 안에서 Task로 구현
- 두 개의 `xcom_push_task` 에서 동일한 키값을 XCom에 push하고, `xcom_pull_task` 에서 Xcom으로부터 키값을 pull하여 출력

```python
# dags/python_xcom1.py

from airflow.sdk import DAG, task
from airflow.models.taskinstance import TaskInstance
import pendulum

with DAG(
    dag_id="python_xcom1",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "xcom"],
) as dag:
    @task(task_id="xcom_push_task1")
    def xcom_push_task1(ti: TaskInstance, **kwargs):
        ti.xcom_push(key="key1", value="value1")
        ti.xcom_push(key="key2", value=[1,2,3])

    @task(task_id="xcom_push_task2")
    def xcom_push_task2(ti: TaskInstance, **kwargs):
        ti.xcom_push(key="key1", value="value2")
        ti.xcom_push(key="key2", value=[4,5,6])

    @task(task_id="xcom_pull_task")
    def xcom_pull_task(ti: TaskInstance, **kwargs):
        value1 = ti.xcom_pull(key="key1")
        value2 = ti.xcom_pull(key="key2", task_ids="xcom_push_task1")
        print(value1)
        print(value2)

    xcom_push_task1() >> xcom_push_task2() >> xcom_pull_task()
```

- 두 개의 `xcom_push_task` 실행 내역의 XCom 탭에서 `key1` 과 `key2` 에 대한 값이 지정됨을 확인
- `xcom_pull_task` 에서는 `task_ids` 를 지정하지 않았을 때 마지막으로 push된 "value2"가 출력될 것을 기대했지만, Airflow 3.0에서 발생한 업데이트로 인해 None 값이 출력

![xcom_push_task1 > XCom 목록](https://dl.dropboxusercontent.com/scl/fi/j0vd8nzylw6qanmygqxhb/airflow-20-xcom-push-task1.webp?rlkey=x6e0oqpuaf8lxltfy6v91fx7u&dl=0)

![xcom_push_task2 > XCom 목록](https://dl.dropboxusercontent.com/scl/fi/20rcijufdw87qw9xw3cxv/airflow-21-xcom-push-task2.webp?rlkey=47xl0no6t7wdemtgiwdnn3srd&dl=0)

```bash
# xcom_pull_task

[2025-06-03, 15:27:41] INFO - None: chan="stdout": source="task"
[2025-06-03, 15:27:41] INFO - [1, 2, 3]: chan="stdout": source="task"
```

#### Airflow 3.0 업데이트
- Airflow 3.0부터는 `task_ids` 를 반드시 명시하도록 변경됨
   - `kwargs["ti"].xcom_pull(key="key")` 와 같은 구문은 더 이상 작동하지 않음

> In Airflow 2, the `xcom_pull()` method allowed pulling XComs by key without specifying task_ids, ..., leading to unpredictable behavior.
> Airflow 3 resolves this inconsistency by requiring `task_ids` when pulling by key.

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/release_notes.html#behaviour-change-in-xcom-pull"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

### PythonOperator (2)
- `xcom_return_task` 에서 문자열 "Success"를 반환하고, 두 개의 `xcom_pull_task` 에서 서로 다른 방식으로 return 값을 받아 출력

```python
# dags/python_xcom2

from airflow.sdk import DAG, task
from airflow.models.taskinstance import TaskInstance
import pendulum

with DAG(
    dag_id="python_xcom2",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "xcom"],
) as dag:
    @task(task_id="xcom_return_task")
    def xcom_return_task(**kwargs) -> str:
        return "Success"

    @task(task_id="xcom_pull_task1")
    def xcom_pull_task1(ti: TaskInstance, **kwargs):
        status = ti.xcom_pull(key="return_value", task_ids="xcom_return_task")
        print(f"\"xcom_return_task\" 함수의 리턴 값: {status}")

    @task(task_id="xcom_pull_task2")
    def xcom_pull_task2(status: str, **kwargs):
        print(f"\"xcom_return_task\" 함수로부터 전달받은 값: {status}")

    return_value = xcom_return_task()
    return_value >> xcom_pull_task1()
    xcom_pull_task2(return_value)
```

- 두 개의 `xcom_pull_task` 에서 모두 정상적으로 return 값을 받아서 동일한 결과가 출력됨을 확인

```bash
# xcom_pull_task1

[2025-06-03, 15:36:10] INFO - "xcom_return_task" 함수의 리턴 값: "Success": chan="stdout": source="task"
```

```bash
# xcom_pull_task2

[2025-06-03, 15:36:10] INFO - "xcom_return_task" 함수로부터 전달받은 값: "Success": chan="stdout": source="task"
```

### BashOperator
- Jinja 템플릿 문법을 통해 `ti.xcom_push` 또는 `ti.xcom_pull` 사용이 가능
- 마지막 출력문은 자동으로 `return_value` 로 전달

```python
# dags/bash_xcom.py

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_xcom",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "xcom"],
) as dag:
    bash_push_task = BashOperator(
        task_id="bash_push_task",
        bash_command="echo START && echo XCOM PUSHED {{ ti.xcom_push(key='bash_pushed', value='bash_message') }} && echo COMPLETE",
    )

    bash_pull_task = BashOperator(
        task_id="bash_pull_task",
        env={
            "PUSHED_VALUE": "{{ ti.xcom_pull(key='bash_pushed', task_ids='bash_push_task') }}",
            "RETURN_VALUE": "{{ ti.xcom_pull(key='return_value', task_ids='bash_push_task') }}"
        },
        bash_command="echo $PUSHED_VALUE && echo $RETURN_VALUE",
    )

    bash_push_task >> bash_pull_task
```

- `bash_push_task` 의 실행 내역에서 직접 push한 `bash_pushed` 가 XCom에 들어있고, 마지막 출력문도 `return_value` 로 저장되어 있음을 조회
- `bash_pull_task` 에서 첫 번째로는 XCom에서 `bash_pushed` 키를 가지고 꺼낸 PUSHED_VALUE 값을 출력하여, 실행 로그에 "bash_message" 가 출력됨을 확인
- 두 번째로는 Xcom에서 `return_value` 키를 가지고 꺼낸 RETURN_VALUE 값을 출력하여, 실행 로그에 `bash_push_task` 의 마지막 출력문 "COMPLETE" 가 출력됨을 확인

![bash_push_task1 > XCom 목록](https://dl.dropboxusercontent.com/scl/fi/4qwkzxfg4atptcz3djxs4/airflow-22-bash-push-task.webp?rlkey=lr5wsqb82ititdv0f0jp1ic82&dl=0)

```bash
# bash_pull_task

[2025-06-03, 16:05:09] INFO - bash_message: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
[2025-06-03, 16:05:09] INFO - COMPLETE: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

### Python → Bash 전달
- PythonOperator에서 딕셔너리 객체를 반환했을 경우, BashOperator에서 XCom을 통해 딕셔너리 내 특정 값을 꺼낼 수 있음
- 반대로, BashOperator에서 push한 값 또는 마지막 출력문을 PythonOperator에서 XCom을 통해 꺼낼 수도 있음

```python
@task(task_id="python_push")
def python_push_xcom():
	return {"status":"Success", "data":[1,2,3]}

bash_pull = BashOperator(
	task_id="bash_pull",
    env={
    	"STATUS": "{{ ti.xcom_pull(key=\"return_value\", task_ids=\"python_push\")[\"status\"] }}",
    	"DATA": "{{ ti.xcom_pull(key=\"return_value\", task_ids=\"python_push\")[\"data\"] }}"
	},
    bash_command="echo $STATUS && echo $DATA"
)
```

## Variable

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}

- 모든 DAG에서 공유하는 전역 변수
- Airflow UI에서 Admin 메뉴를 통해 접근 및 생성 가능

![Variable 페이지](https://dl.dropboxusercontent.com/scl/fi/n02tx2fag1ngmoo34c2ar/airflow-23-variable.webp?rlkey=lks97xtcwoplxjhx6tg3rxjga&dl=0)

![Variable 추가](https://dl.dropboxusercontent.com/scl/fi/of4scht6bxg0avu0t69m0/airflow-24-add-variable.webp?rlkey=k0lij755upimzylzcxk4bnhhj&dl=0)

### Variable 가져오기
- Variable 라이브러리를 통해 전역 변수를 꺼내는 방법
- 해당 방법은 DAG를 파싱할 때마다 DB 연결을 발생시켜 불필요한 부하가 발생 (스케줄러 과부하 원인)

```python
from airflow.models import Variable

var = Variable.get("key")
```

- Jinja 템플릿을 이용해 Operator 내부에서 가져오는 방법
- 실제 실행할때만 DB에 접근하기 때문에 상대적으로 부하가 적음 (Airflow에서 권장하는 방법)

```python
from airflow.operators.bash import BashOperator

bash_task = BashOperator(
	task_id="bash_task",
    bash_command=f"echo {{var.value.key}}"
)
```

### Variable 활용
- 앞서 서술한 코드를 DAG 안에서 Task로 구현
- 첫 번째 Task에서는 Variable 라이브러리로 꺼낸 전역 변수를 출력하고, 두 번째 Task에서는 Jinja 템플릿을 이용해 전역 변수를 출력

```python
# dags/bash_variable.py

from airflow.sdk import DAG, Variable
from airflow.providers.standard.operators.bash import BashOperator
import pendulum

with DAG(
    dag_id="bash_variable",
    schedule="0 0 * * *",
    start_date=pendulum.datetime(2025, 1, 1, tz="Asia/Seoul"),
    catchup=False,
    tags=["example", "xcom"],
) as dag:
    var = Variable.get("sample_key")

    bash_var_task1 = BashOperator(
        task_id="bash_var_task1",
        bash_command=f"echo variable: \"{var}\"",
    )

    bash_var_task2 = BashOperator(
        task_id="bash_var_task2",
        bash_command="echo variable: \"{{ var.value.sample_key }}\"",
    )
```

- 기대했던 것과 달리, 실행 로그에서는 전역 변수가 마스킹 처리되어 출력
- `airflow.cfg` 설정에서 `sensitive_var_conn_names` 항목을 확인해보고, Web UI 컨테이너에 들어가서 `airflow variables get` 명령어로 전역 변수가 마스킹된 채로 저장되어 있는지도 확인해보고, BashOperator 안에서 비교 연산자로 설정한 것과 동일한 값이 가져와지는지도 출력해서 확인해봤는데, 모두 정상적이고 실행 로그에서 전역 변수를 직접 출력할 때만 마스킹 처리됨
- 어떻게든 출력해보려고 했지만, 모든 사람이 접근할 수 있는 환경 변수를 평문으로 출력시키지 않으려는 의도가 있다고 짐작하고 추가적인 시도를 중지함

```bash
# bash_var_task1

[2025-06-03, 16:52:07] INFO - variable: ***: source="airflow.task.hooks.airflow.providers.standard.hooks.subprocess.SubprocessHook"
```

{{< bookmark
  url="https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/mask-sensitive-values.html"
  image="https://dl.dropboxusercontent.com/scl/fi/jaltieh1sb4r7ozm6ju3e/airflow-00-cover-bg.webp?rlkey=s10wwm9o11zy79dwm1vje30sb&dl=0" >}}
