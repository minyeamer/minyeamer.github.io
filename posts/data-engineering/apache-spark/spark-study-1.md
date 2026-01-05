---
title: "Apache Spark - 스파크의 기본 개념과 아키텍처"
date: "2025-06-22T18:42:10+09:00"
layout: "post"
description: >
  Apache Spark의 기본 개념과 아키텍처를 다루며,
  스파크의 시작부터 컴포넌트, Spark Driver, SparkSession, Cluster Manager, 배포 모드까지 단계별로 안내합니다.
  데이터 엔지니어링과 빅데이터 처리를 위한 필수 지식을 습득하고 실무에 적용하세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/iafnblb6k95kbw7bwn2xj/spark-00-cover.webp?rlkey=6995tacnu3mvr7s31akl5sca6&raw=1"
categories: ["Data Engineering", "Apache Spark"]
tags: ["Apache Spark", "Spark Architecture", "SparkSession", "Cluster Manager", "PySpark", "데이터 엔지니어링", "스파크", "Study"]
---

## Study Overview

[러닝 스파크 2nd 개정판](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=296379664) 과정을 따릅니다.

### 목적
- 대용량 데이터 처리를 위한 아파치 스파크를 이론적으로 학습
- 책에서 대상으로 하는 스파크 3.x 버전과 25년 5월 출시된 Spark 4.0 버전을 비교
- 각 챕터에서 배운 것으로 실습할만한 것이 있다면 추가로 시도하기
- 실습은 PySpark API를 사용하며, 최신화된
  [PySpark 4.0.0 문서](https://spark.apache.org/docs/4.0.0/api/python/index.html)를 참조

### 챕터
> 1. 아파치 스파크 소개: 통합 분석 엔진
> 2. 아파치 스파크 다운로드 및 시작
> 3. 아파치 스파크의 정형화 API
> 4. 스파크 SQL과 데이터 프레임: 내장 데이터 소스 소개
> 5. 스파크 SQL과 데이터 프레임: 외부 데이터 소스와 소통하기
> 6. 스파크 SQL과 데이터세트
> 7. 스파크 애플리케이션의 최적화 및 튜닝
> 8. 정형화 스트리밍
> 9. 아파치 스파크를 통한 안정적인 데이터 레이크 구축
> 10. MLlib을 사용한 머신러닝
> 11. 아파치 스파크로 머신러닝 파이프라인 관리, 배포 및 확장
> 12. 에필로그: 아파치 스파크 3.0

## Spark Overview

### 스파크의 시작
RDBMS 같은 전통적인 저장 시스템으로는 구글이 방대한 규모의 인터넷 문서를 다룰 수 없어
구글 파일 시스템(GFS), 맵리듀스(MapReduce), 빅테이블(BigTable) 등을 만들어 냈다.
GFS는 클러스터 환경에서 분산 파일시스템을 제공하고, 빅테이블은 GFS를 기반으로 대규모 데이터 저장 수단을 제공한다.
맵리듀스는 함수형 프로그래밍 기반으로 대규모 데이터 분산 처리를 구현했다. 클러스터의 워커 노드들이
분산된 데이터에 연산을 하고(Map), 그 결과를 하나로 합쳐(Reduce) 최종 결과를 생성해낸다.
이러한 접근 방식은 네트워크 트래픽을 크게 감소시키면서 로컬 디스크에 대한 I/O를 극대화한다.

GFS는 하둡 파일 시스템과 맵리듀스 구현에 영향을 주었다. HDFS의 맵리듀스에는 몇 가지 단점이 있었다.
첫째, 운영이 복잡해 관리가 쉽지 않았다. 둘째, 배치 처리를 위한 맵리듀스 API의 기본 설정 코드가 너무 많이 필요했다.
셋째, 맵리듀스 태스크가 필요해질 때마다 중간 과정의 데이터를 로컬 디스크에 써야 했다.
반복적인 I/O 작업에 의해 거대한 맵리듀스 작업에 며칠이 걸리기도 했다.

![Big Data -> Split -> Map -> Reduce -> Output](https://dl.dropboxusercontent.com/scl/fi/pg3qcymue8h7z8h8n8cau/spark-01-map-reduce.webp?rlkey=6bnfs4bxy1haa8e52335qv24a&raw=1)

UC 버클리 연구원들은 동적이고 반복적인 작업에서 비효율적인 맵리듀스를 개선하여 단순하고 빠르고 쉬운 스파크를 만들기로 했다.
구체적으로는 더 높은 장애 내구성을 갖고, 병렬성을 높이면서, 맵리듀스 연산을 위한 중간 결과를 메모리에 저장하고,
간편한 API를 다양한 언어로 제공하고자 했다.

### 아파치 스파크란?
아파치 스파크는 데이터 센터나 클라우드에서 대규모 분산 데이터 처리를 위한 통합형 엔진이다.
중간 연산을 메모리에 저장하고 머신러닝, SQL, 스트리밍 처리, 그래프 처리 등을 간편하게 API로 지원한다.

스파크의 설계 철학에는 속도, 사용 편리성, 모듈성, 확장성이 있다.

1. 속도
스파크는 하드웨어 산업의 발전으로 메모리 성능 향상에 많은 이득을 얻었는데, 모든 중간 결과를 메모리에 저장해
I/O 작업을 제한하고 속도를 향상시켰다. 또한, 질의 연산을 DAG로 구성해 효율적인 연산 그래프를 만들고 병렬 수행을 지원한다.

2. 사용 편리성
데이터프레임이나 데이터세트 같이 고수준으로 추상화된 자료 구조를 사용해 단순성을 실현시켰다.
다양한 언어로 연산을 지원하여 사용자들이 편한 언어로 빅데이터를 처리할 수 있다.

3. 모듈성
문서화가 잘된 API를 제공하며, 스파크 SQL이나 정형화 스트리밍 등의
핵심 컴포넌트를 하나의 엔진 안에서 연동된 상태로 사용할 수 있다.

4. 확장성
스파크는 저장보다는 빠른 병렬 연산 엔진에 초점을 맞춰, 수많은 데이터 소스에서 데이터를 읽어 들여
메모리에서 처리하는 것이 가능하다. 서드파티 패키지 목록에는 다양한 외부 데이터 소스가 포함되어 있다.

### 아파치 컴포넌트
다양한 워크로드를 위해 스파크 SQL, 스파크 MLlib, 스파크 정형화 스트리밍, GraphX를 제공한다.
자바, R, 스칼라, SQL, 파이썬 중 어느 것으로 스파크 코드를 작성해도 바이트 코드로 변환되어 워커 노드의 JVM에서 실행된다.

1. 스파크 SQL
RDBMS 테이블이나 CSV와 같은 구조화된 데이터 파일 포맷에서 데이터를 읽어 들여 영구적이거나
임시적인 테이블을 생성한다. SQL 계통의 질의를 써서 데이터를 데이터프레임으로 읽어 들일 수 있다.

2. 스파크 MLlib
범용 머신러닝 알고리즘들이 들어 있다. 특성을 추출 및 가공하고 학습/검증 파이프라인을 구축하는 기능을
지원하며, 경사 하강법 최적화를 포함한 저수준 ML 기능을 포함한다.

3. 스파크 정형화 스트리밍
실시간으로 연결하고 반응하기 위한 데이터 모델은 스트림을 연속적으로 증가하는 테이블이자,
끝에 새로운 레코드가 추가되는 형태이다. 단순히 정형화 테이블로 보고 쿼리를 날리면 된다.
정형화 스트리밍 모델의 하부에는 스파크 SQL 엔진이 장애 복구와 지연 데이터의 모든 측면을 관리한다.

4. GraphX
그래프를 조작하고 그래프 병렬 연산을 수행하기 위한 라이브러리다. 분석, 연결 탐색 등
표준적인 그래프 알고리즘과 커뮤니티 사용자들이 기여한 알고리즘을 포함한다.

## Spark Architecture

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/hhpp6o2d6m6grww5vz6t8/spark-02-architecture.webp?rlkey=mzdwo2l947nuead3shu2xeodz&raw=1"
  alt="The Architecture of Apache Spark"
  max-width="691px"
  align="center" >}}

### Spark Driver
SparkSession 객체를 초기화하는 책임을 가진 Spark Application의 일부이다.
Spark Driver는 여러 가지 역할을 한다.

1. Cluster Manager와 통신하며 Spark Executor들을 위해 필요한 자원을 요청한다.
2. 모든 스파크 작업을 DAG 연산 형태로 변환해 스케줄링한다.
3. 각 실행 단위를 태스크로 나누어 Spark Executor들에게 분배한다.
4. 자원이 한번 할당되면 그 다음부터는 Driver가 Executor와 직접 통신한다.

### SparkSession
스파크 2.0에서 모든 스파크 연산과 데이터에 대한 통합 연결 채널이 만들어졌다.

1. SparkContext, SQLContext, HiveContext, SparkConf, StreamingContext 등이 합쳐졌다.
2. 일원화된 연결 채널을 통해 JVM 실행 파라미터들을 만들고 데이터프레임이나 데이터세트를 정의한다.
3. 데이터 소스에서 데이터를 읽고 메타데이터에 접근해 스파크 SQL 질의를 실행할 수 있다.

SparkSession은 모든 스파크 기능을 한 군데에서 접근할 수 있는 시작점을 제공한다.

> [pyspark.sql.SparkSession](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html)
> 문서를 참조해 SparkSession 생성

```python
spark = (
    SparkSession.builder
        .master("local") # 원격 접속의 경우 .remote("sc://localhost")
        .appName("LearnSpark")
        .config("spark.sql.shuffle.partitions", 6)
        .getOrCreate()
)
```

### Cluster Manager
Spark Application이 실행되는 클러스터에서 자원을 관리 및 할당하는 책임을 가진다.
Standalone, Hadoop YARN, Apache Mesos, Kubernetes 네 종류의 Cluster Manager를 지원한다.

### Spark Executor
클러스터의 각 워커 노드에서 동작하며, Driver와 통신하며 Task를 실행하는 역할을 한다.
대부분의 배포 모드에서 노드당 하나의 Executor만 실행한다.

### 배포 모드
스파크가 여러 환경에서 돌아갈 수 있도록 다양한 배포 모드를 지원한다. 추상화되어 있어 Cluster Manager는 실행 환경에 대한 정보가 필요없고, YARN이나 Kubernetes 같은 인기 있는 환경에 배포가 가능하다.

|Mode|Spark Driver|Spark Executor|Cluster Manager|
|---|---|---|---|
|Local|단일 서버 같은 머신에서 단일 JVM 위에서 실행|Driver와 동일한 JVM 위에서 동작|동일한 호스트에서 실행|
|Standalone|Cluster의 아무 노드에서나 실행|Cluster의 각 노드가 자체적인 Executor를 실행|Cluster의 아무 호스트에나 할당|
|YARN(Client)|Cluster 외부의 Client에서 동작|YARM의 노드 매니저의 컨테이너|YARN의 리소스 매니저가 노드 매니저에 컨테이너 할당|
|YARN(Cluster)|YARN 애플리케이션 마스터에서 동작|YARN(Client)와 동일|YARN(Client)와 동일|
|Kubernetes|Kubernetes Pod에서 동작|각 워커가 자신의 Pod 내에서 실행|Kubernetes 마스터|

### 분산 데이터
물리적인 데이터는 HDFS나 클라우드 저장소에 존재한다. 데이터는 파티션으로 물리적인 수준에서 분산되고, 스파크는 파티션을 추상화하여 메모리의 데이터프레임 객체를 바라본다.

파티셔닝은 효과적인 병렬 처리를 가능하게 해준다. 데이터를 조각내 청크나 파티션 단위로 분산해 Spark Executor가 네트워크 사용을 최소화하고 가까이 있는 데이터만 처리한다.

## 스파크 활용사례

### 데이터 사이언스
데이터 사이언티스트들은 데이터를 정제하고 패턴을 발견하기 위해 데이터를 살펴본다. 대부분은 SQL에 능하고, NumPy나 pandas 같은 라이브러리를 편하게 사용한다. 모델 구축을 위해 분류, 회귀, 클러스터링 알고리즘을 어떻게 사용할지도 알아야 한다.

스파크는 MLlib은 모델 파이프라인을 구축할 수 있는 일반적인 머신러닝 알고리즘들을 제공한다. 또한, 스파크 SQL로 일회성 데이터 탐색을 가능하게 해준다.

### 데이터 엔지니어링
클러스터링 모델은 독립적으로 존재하지 않고 아파치 카프카 같은 스트리밍 엔진과 연계해 동작한다. 데이터 파이프라인은 다양한 소스에서 오는 원본 데이터를 최종 단계로까지 변형해주며, 그런 데이터는 NoSQL이나 RDBMS 등에 저장된다.

스파크의 정형화 스트리밍 API를 써서 실시간 또는 정적인 데이터 소스에 대한 ETL 파이프라인을 구축할 수 있게 해준다. 또한, 스파크가 연산을 쉽게 병렬화 해주어 고수준 언어에만 집중해 ETL을 수행할 수 있게 지원한다.

### 스파크 사용 사례
1. 클러스터 전체에 걸쳐 분산된 대규모 데이터세트의 병렬 처리
2. 데이터 탐색이나 시각화를 위한 일회성이나 대화형 질의 수행
3. MLlib을 이용해 머신러닝 모델을 구축, 훈련, 평가
