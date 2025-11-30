---
title: "Apache Spark - 고차함수(Higher-Order Functions)"
date: "2025-07-19T23:53:45+09:00"
layout: "post"
description: >
  Apache Spark의 고차함수와 사용자 정의 함수를 다루며,
  UDF 생성부터 Pandas UDF, transform, filter 등 고차 함수 활용까지 단계별로 안내합니다.
  빅데이터 분석과 데이터 엔지니어링을 위한 강력한 도구를 습득하고 실무에 적용하세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/iafnblb6k95kbw7bwn2xj/spark-00-cover.webp?rlkey=6995tacnu3mvr7s31akl5sca6&dl=0"
categories: ["Data Engineering", "Apache Spark"]
tags: ["Apache Spark", "고차함수", "UDF", "Pandas UDF", "Spark SQL", "PySpark", "데이터 엔지니어링", "스파크", "Study"]
---

## User-Defined Functions

스파크는 자신의 기능을 정의할 수 있는 유연성을 제공한다.
이를 사용자 정의 함수(User-Defined Function, UDF)라고 한다.

UDF를 생성하는 이점은 스파크 SQL 안에서 이를 사용할 수 있다는 것이다.

### Spark SQL UDF 활용

다음은 스파크 SQL UDF를 만드는 예시로, 인수를 세제곱하는 함수 `cubed()` 를 생성한다.

```python
from pyspark.sql.types import LongType

# 큐브 함수 생성
def cubed(s):
    return s * s * s

# UDF로 등록
spark.udf.register("cubed", cubed, LongType())
```

스파크 SQL을 사용하여 `cubed()` 함수를 실행할 수 있다.

```python
# 임시 뷰 생성
spark.range(1, 9).createOrReplaceTempView("udf_test")

# 큐브 UDF를 사용하여 쿼리
spark.sql("SELECT id, cubed(id) AS id_cubed FROM udf_test").show()
```

```bash
+---+--------+
| id|id_cubed|
+---+--------+
|  1|       1|
|  2|       8|
|  3|      27|
|  4|      64|
|  5|     125|
|  6|     216|
|  7|     343|
|  8|     512|
+---+--------+
```

### 스파크 SQL 평가 순서

스파크 SQL은 하위 표현식의 평가 순서를 보장하지 않는다.
예를 들어, 다음 쿼리에서 `s IS NOT NULL` 절이 `strlen(s) > 1` 절 이전에 실행된다는 것을 보장할 수 없다.

```python
spark.sql("SELECT s FROM test1 WHERE s IS NOT NULL AND strlen(s) > 1")
```

따라서, 다음 두 가지 `null` 검사 방식을 수행하는 것이 좋다.
1. UDF 안에서 `null` 을 인식하고 `null` 검사를 수행할 필요가 있다.
2. SQL문에서 `IF` 또는 `CASE WHEN` 식을 사용하여 `null` 검사를 수행하고 조건에 맞으면 UDF를 호출한다.

### Pandas UDF

PySpark UDF는 JVM과 파이썬 사이의 데이터 이동을 필요로 해서 Scala UDF보다 성능이 느렸다.

이 문제를 해결하기 위해 Pandas UDF가 스파크 2.3 버전부터 도입되었다.
Pandas UDF는 Apache Arrow를 사용하여 Pandas UDF를 정의하거나 함수 자체를 래핑할 수 있다.
Apache Arrow 형식에 포함된 데이터라면 더이상 JVM으로 데이터를 전달하기 위해 직렬화나 피클할 필요가 없다.

Pandas UDF는 `pandas.Series`, `pandas.DataFrame` 과 같은 파이썬 유형 힌트로 유추한다.
예시로, 앞에서 정의한 큐브 함수를 Pandas UDF로 만들면 아래와 같다.

```python
import pandas as pd

from pyspark.sql.functions import col, pandas_udf
from pyspark.sql.types import LongType

# 큐브 함수 생성
def cubed(a: pd.Series) -> pd.Series:
    return a * a * a

# 큐브 함수에 대한 Pandas UDF 생성
cubed_udf = pandas_udf(cubed, returnType=LongType())
```

Pandas UDF는 아래와 같이 실행할 수 있다.

```python
# 스파크 데이터프레임 생성
df = spark.range(1, 4)

# Pandas UDF를 실행
df.select("id", cubed_udf(col("id"))).show()
```

```bash
+---+---------+
| id|cubed(id)|
+---+---------+
|  1|        1|
|  2|        8|
|  3|       27|
+---+---------+
```

스파크 UI에서 시각화된 `pandas_udf` 함수의 실행 단계에 대한 DAG을 조회할 수 있다.
Stage 0에서 `ArrowEvalPython` 연산이 Pandas UDF를 평가하는 단계이다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/kn9ih42tqsbxfskwq5vj4/spark-19-pandas-udf.webp?rlkey=f1yvfjog5fvxjyhcvjugsd1id&dl=0"
  alt="WholeStageCodegen (1) -> ArrowEvalPython -> WholeStageCodeGen (2) -> mapPartitionsInternal"
  max-width="432px"
  align="center" >}}

## 고차 함수

복잡한 데이터 유형은 단순한 데이터 유형의 결합이기 때문에 다음과 같이 조작할 수 있다.

1. 중첩된 구조를 개별 행으로 분해하고 각각에 함수를 적용한 후 중첩된 구조를 다시 만드는 방법
2. 사용자 정의 함수를 사용하는 방법

하지만 배열과 같은 중첩된 구조를 분해하고 다시 만든다고 가정할 때, 셔플 작업이 발생해 결과 배열의 순서가 원래 배열의 순서와 동일하지 않을 수 있다.

사용자 정의 함수를 사용할 경우에는 정렬 문제는 해결할 수 있지만, 직렬화 및 역직렬화 과정을 거치면서 발생하는 비용이 크다는 문제가 있다.

### 내장 함수

복잡한 데이터 유형에 대해 스파크 2.4 이상 버전에 포함된 내장 함수를 사용할 수 있다.
자세한 건 [공식 문서](https://spark.apache.org/docs/latest/api/sql/index.html)를 참고해볼 수 있는데,
그 중에서 배열과 맵에 대해서 일부를 알아본다.

배열과 관련된 함수는 공식 문서에서
[array 문단](https://spark.apache.org/docs/latest/api/sql/index.html#array)부터 시작하는 함수들을 참고하면 된다.
대표적으로 `array_distinct` 함수는 배열 내 중복을 제거하고, `array_sort` 함수는 배열을 오름차순으로 정렬한다.
array로 시작하지 않는 함수 중에서도 `concat` 함수는 복수 개의 배열을 받아 하나의 배열로 합쳐주고,
`flatten` 함수는 2차원 이상 중첩된 배열을 단일 배열로 플랫화한다. `sequence` 함수로
시작과 끝에 대한 배열을 생성할 수 있고, `slice` 함수로 배열의 특정 부분만 잘라낼 수도 있다.

맵과 관련된 함수는 공식 문서에서
[map 문단](https://spark.apache.org/docs/latest/api/sql/index.html#map)부터
시작하는 함수들을 참고하면 된다.
대표적으로 `map_concat` 함수는 복수 개의 맵을 하나의 맵으로 합쳐주고,
`map_keys` 함수로 맵에서 키 배열만 추출할 수도 있다. map으로 시작하지 않는 함수 중에서도
`element_at` 함수는 주어진 키에 대한 값을 반환하고, `cardinality` 함수는 맵의 크기를 반환한다.

### transform()

내장 함수 외에도 익명 람다 함수를 인수로 사용하는 고차 함수 `transform()` 이 있다.

고차 함수를 실행해보기 위해 아래와 같이 샘플 데이터 `tC` 를 만들어본다.

```python
from pyspark.sql.types import *

schema = StructType([StructField("celsius", ArrayType(IntegerType()))])

t_list = [[35, 36, 32, 30, 40, 42, 38]], [[31, 32, 34, 55, 56]]
t_c = spark.createDataFrame(t_list, schema)
t_c.createOrReplaceTempView("tC")

t_c.show()
```

```bash
+--------------------+
|             celsius|
+--------------------+
|[35, 36, 32, 30, ...|
|[31, 32, 34, 55, 56]|
+--------------------+
```

Celsius 단위를 Fahrenheit 단위로 바꾸는 `transform()` 함수를 사용해,
`celsius` 열로부터 `fahrenheit` 열을 계산했다. 출력 결과는 아래와 같다.

```python
spark.sql("""
SELECT
  celsius,
  transform(celsius, t -> ((t * 9) div 5) + 32) AS fahrenheit
FROM tc
""").show()
```

```bash
+--------------------+--------------------+
|             celsius|          fahrenheit|
+--------------------+--------------------+
|[35, 36, 32, 30, ...|[95, 96, 89, 86, ...|
|[31, 32, 34, 55, 56]|[87, 89, 93, 131,...|
+--------------------+--------------------+
```

### filter()

`filter()`  함수는 입력한 배열의 요소 중 부울 함수가 참인 요소만으로 구성된 배열을 생성한다.

```python
spark.sql("""
SELECT
  celsius,
  filter(celsius, t -> t > 38) AS high
FROM tc
""").show()
```

```bash
+--------------------+--------+
|             celsius|    high|
+--------------------+--------+
|[35, 36, 32, 30, ...|[40, 42]|
|[31, 32, 34, 55, 56]|[55, 56]|
+--------------------+--------+
```

### exists()

`exists()` 함수는 입력한 배열의 요소 중 불린 함수를 만족시키는 것이 존재할 때 참을 반환한다.

```python
spark.sql("""
SELECT
  celsius,
  exists(celsius, t -> t = 38) AS threshold
FROM tc
""").show()
```

```bash
+--------------------+---------+
|             celsius|threshold|
+--------------------+---------+
|[35, 36, 32, 30, ...|     true|
|[31, 32, 34, 55, 56]|    false|
+--------------------+---------+
```

## 스파크 SQL 작업

스파크 SQL의 기능 중 일부는 DataFrame의 다양한 기능에서 유래된다.
이용가능한 작업에는 집계 함수, 수집 함수, 날짜 함수, 수학 함수, 정렬 함수,
문자열 함수, 윈도우 함수 등 매우 광범위하다.

### Union

Union은 동일한 스키마를 가진 두 개의 서로 다른 DataFrame을 하나로 합치는 작업이다.

SQL문으로 다음과 같이 표현할 수 있다.

```sql
(SELECT * FROM first_half)
UNION ALL
(SELECT * FROM second_half);
```

파이썬으로는 다음과 같이 표현할 수 있다.

```python
result = first_half.union(second_half)
```

### Join

Join은 두 개 이상의 DataFrame을 특정 조건을 기준으로 결합하여 하나로 합치는 작업이다.

SQL문으로 다음과 같이 표현할 수 있다.

```sql
SELECT
  p.id AS productId,
  p.storeId,
  s.name AS storeName,
  p.name AS productName
FROM product AS p
  LEFT JOIN store AS s
    ON p.storeId = s.id;
```

파이썬으로는 다음과 같이 표현할 수 있다.

```python
from pyspark.sql.functions import col

product.join(
    store,
    product.storeId == store.id,
    how = "left"
).select(
    col("p.id").alias("productId"),
    "p.storeId",
    col("s.name").alias("storeName"),
    col("p.name").alias("productName")
).show()
```

### 윈도우

윈도우 함수를 사용하면 모든 입력 행에 대해 단일값을 반환하면서 행 그룹에 대해 작업할 수 있다.

순위를 매기는 작업과 관련해서는 `RANK`, `DENSE_RANK`, `PERCENT_RANK`, `NTILE`, `ROW_NUMBER`
함수가 있고, 집계와 관련해서는 `MAX`, `MIN`, `COUNT`, `SUM`, `AVG` 등의 함수가 있다.

SQL문으로 다음과 같이 표현할 수 있다.

```sql
SELECT
  name,
  dept,
  salary,
  RANK() OVER (PARTITION BY dept ORDER BY salary) AS rank
FROM employees;
```

파이썬으로는 다음과 같이 표현할 수 있다.

```python
from pyspark.sql.functions import rank
from pyspark.sql import Window

window = rank().over(Window.partitionBy("dept").orderBy("salary")).alias("rank")
employees.select("name", "dept", "salary", window).show()
```

### 수정

DataFrame 자체는 변경할 수 없지만, 열을 가공하여 새로운 DataFrame을 만드는 것과 같은 작업을 통해 수정할 수 있다.

파이썬으로 활용 가능한 다음과 같은 예시가 있다.

```python
from pyspark.sql.functions import expr

# 열 추가
foo2 = foo.withColumn(
  "status",
  expr("CASE WHEN delay <= 10 THEN 'On-time' ELSE 'Delayed' END"))

# 열 삭제
foo3 = foo2.drop("delay")

# 칼럼명 바꾸기
foo4 = foo3.withColumnRenamed("status", "flight_status")
```

### 피벗

로우와 칼럼을 바꿔야 하는 경우가 있다. 이 경우에 `pivot` 함수를 지원한다.

피벗을 실행해보기 위해 아래와 같이 샘플 데이터를 만들어본다.

```python
from pyspark.sql import Row

df1 = spark.createDataFrame([
    Row(course="dotNET", year=2012, earnings=10000),
    Row(course="Java", year=2012, earnings=20000),
    Row(course="dotNET", year=2012, earnings=5000),
    Row(course="dotNET", year=2013, earnings=48000),
    Row(course="Java", year=2013, earnings=30000),])
df1.show()
```

```bash
+------+----+--------+
|course|year|earnings|
+------+----+--------+
|dotNET|2012|   10000|
|  Java|2012|   20000|
|dotNET|2012|    5000|
|dotNET|2013|   48000|
|  Java|2013|   30000|
+------+----+--------+
```

위 데이터에서 `course` 를 열로, `year` 를 행으로, `earnings` 를 값으로
`sum` 집계해 구성한 피벗 테이블을 아래와 같이 만들 수 있다.

```python
df1.groupBy("year").pivot(
    "course", ["dotNET", "Java"]).sum("earnings").sort("year").show()
```

```bash
+----+------+-----+
|year|dotNET| Java|
+----+------+-----+
|2012| 15000|20000|
|2013| 48000|30000|
+----+------+-----+
```

## References

- [https://spark.apache.org/docs/latest/sql-ref-functions-udf-scalar.html](https://spark.apache.org/docs/latest/sql-ref-functions-udf-scalar.html)
- [https://books.japila.pl/pyspark-internals/sql/ArrowEvalPython/#evalType](https://books.japila.pl/pyspark-internals/sql/ArrowEvalPython/#evalType)
- [https://spark.apache.org/docs/latest/api/sql/index.html](https://spark.apache.org/docs/latest/api/sql/index.html)
- [https://docs.databricks.com/aws/en/semi-structured/higher-order-functions](https://docs.databricks.com/aws/en/semi-structured/higher-order-functions)
- [https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.rank.html](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.rank.html)
- [https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.pivot.html](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.pivot.html)
