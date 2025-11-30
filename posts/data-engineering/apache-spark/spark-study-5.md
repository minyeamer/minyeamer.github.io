---
title: "Apache Spark - 스파크 SQL"
date: "2025-07-05T23:03:04+09:00"
layout: "post"
description: >
  Apache Spark의 Spark SQL을 다루며,
  SQL 쿼리 실행부터 테이블/뷰 관리, 메타데이터 캐싱까지 단계별로 안내합니다.
  빅데이터 분석과 데이터 엔지니어링을 위한 강력한 도구를 습득하고 실무에 적용하세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/iafnblb6k95kbw7bwn2xj/spark-00-cover.webp?rlkey=6995tacnu3mvr7s31akl5sca6&dl=0"
categories: ["Data Engineering", "Apache Spark"]
tags: ["Apache Spark", "Spark SQL", "SQL", "View", "PySpark", "데이터 엔지니어링", "스파크", "Study"]
---

## Spark SQL

스파크 SQL은 다음과 같은 특징을 갖는다.

- 정형화 API가 엔진으로 제공한다.
- 다양한 정형 데이터(Parquet 등)를 읽거나 쓸 수 있다.
- 외부 BI 툴(태블로 등)의 데이터 소스나 RDBMS(MySQL 등)의 데이터를 쿼리할 수 있다.
- 정형 데이터에 대해 SQL 쿼리를 실행할 수 있는 대화형 쉘을 제공한다.

### Spark SQL 사용법

```python
spark.sql("SELECT * FROM table")
```

`SparkSession` 객체에 `sql()` 함수를 사용한다. 쿼리 결과로는 `DataFrame` 객체가 반환된다.

### Spark SQL 활용 (Python)

[databricks/LearningSparkV2](https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights)의
`databricks-datasets/learning-spark-v2/flights` 경로에서 미국 항공편 운항 지연 데이터세트
`departuredelays.csv` 를 가져온다. 해당 데이터를 활용해 아래와 같이 임시뷰를 생성한다.

```python
from pyspark.sql import SparkSession

spark = (SparkSession
    .builder
    .appName("SparkSQLExampleApp")
    .getOrCreate())

# 데이터 경로
csv_file = "data/flights/departuredelays.csv"

# 스키마를 추론하여 데이터를 읽기
df = (spark.read.format("csv")
    .option("inferSchema", "true")
    .option("header", "true")
    .load(csv_file))

# 데이터로부터 임시뷰를 생성
df.createOrReplaceTempView("delay_flights")
```

스파크 SQL을 사용해 임시뷰에 대해 SQL 쿼리를 실행할 수 있다.
스파크 SQL은 ANSI:2003과 호환되는 SQl 인터페이스를 제공한다.

```python
spark.sql("""
SELECT distance, origin, destination
FROM delay_flights
WHERE distance > 1000
ORDER BY distance DESC;""").show(10)
```

```bash
+--------+------+-----------+
|distance|origin|destination|
+--------+------+-----------+
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
|    4330|   HNL|        JFK|
+--------+------+-----------+
only showing top 10 rows
```

위의 쿼리는 아래 파이썬 예제와 같이 동등한 DataFrame API로 표현할 수 있다.

```python
from pyspark.sql.functions import col, desc
(df.select("distance", "origin", "destination")
    .where(col("distance") > 1000)
    .orderBy(desc("distance"))).show(10)
```

SQL 쿼리로 단순 `SELECT` 조회뿐 아니라 현재 생성된 임시뷰 목록을 조회할 수도 있다.

```python
spark.sql("SHOW TABLES;").show()
```

```bash
+---------+-------------+-----------+
|namespace|    tableName|isTemporary|
+---------+-------------+-----------+
|         |delay_flights|       true|
+---------+-------------+-----------+
```

앞에서 스키마를 추론하여 DataFrame을 읽었는데, SQL 쿼리로 어떤 스키마로 인식되었는지 확인해 보았다.
DataFrame 객체의 스키마 `df.schema` 의 출력 결과와 동일하다.

```python
spark.sql("DESC delay_flights;").show()
```

```bash
+-----------+---------+-------+
|   col_name|data_type|comment|
+-----------+---------+-------+
|       date|      int|   NULL|
|      delay|      int|   NULL|
|   distance|      int|   NULL|
|     origin|   string|   NULL|
|destination|   string|   NULL|
+-----------+---------+-------+
```

## Table & View

스파크는 테이블을 위한 별도 메타스토어를 생성하지 않고 기본적으로 `/user/hive/warehouse` 경로에 있는
아파치 하이브 메타스토어를 사용해 테이블에 대한 모든 메타데이터를 유지한다.

스파크는 관리형과 비관리형이라는 두 가지 유형의 테이블로 만들 수 있다.

**관리형 테이블**은 스파크가 메타데이터와 파일 저장소의 데이터를 모두 관리한다.
따라서, `DROP TABLE` 과 같은 SQL 명령에 대해 메타데이터와 실제 데이터를 모두 삭제한다.

반면에 **비관리형 테이블**은 스파크가 메타데이터만 관리하고 외부 데이터 소스에서 데이터를 직접 관리한다.
그래서, `DROP TABLE` 명령에도 실제 데이터는 그대로 두고 메타데이터만 삭제한다.

### 테이블 생성하기

스파크는 기본적으로 `default` 데이터베이스 안에 테이블을 생성한다.
SparkSession을 열고 현재 접속한 데이터베이스를 조회하면 알 수 있다.

```python
spark.sql("SELECT current_database();").show()
```

```bash
+----------------+
|current_schema()|
+----------------+
|         default|
+----------------+

```

우선, SQL 명령어를 실행하여 새로운 데이터베이스 `learn_spark_db` 를 생성할 수 있다.
생성한 데이터베이스를 사용하고 다시 현재 접속한 데이터베이스를 확인해 보았다.

```python
spark.sql("CREATE DATABASE learn_spark_db;")
spark.sql("USE learn_spark_db;")
spark.sql("SELECT current_database();").show()
```

```bash
+----------------+
|current_schema()|
+----------------+
|  learn_spark_db|
+----------------+
```

### 관리형 테이블 생성하기

`CREATE` 문을 사용하여 현재 데이터베이스 안에 관리형 테이블을 생성할 수 있다.

```python
table = "managed_delay_flights"
schema = "date STRING, delay INT, distaince INT, origin STRING, destination STRING"
spark.sql("CREATE TABLE {} ({});".format(table, schema))
```

위 SQL 쿼리는 마찬가지로 아래처럼 DataFrame API로 표현할 수도 있다.
이미 테이블을 만들었을 경우, 아래 파이썬 예제를 그대로 실행하면 `TABLE_OR_VIEW_ALREADY_EXISTS` 에러가
발생하므로 `mode="overwrite"` 옵션을 넣어주어 기존 테이블을 덮어쓴다.

```python
csv_file = "data/flights/departuredelays.csv"
flights_df = spark.read.csv(csv_file, schema=schema)
flights_df.write.saveAsTable(table, mode="overwrite")
```

테이블을 생성하게 되면 현재 위치 아래의 `spark-warehouse/{{DB명}}.db/{{테이블명}}` 경로에
`.parquet` 파일들이 생성된다. 스파크 공식문서 중
[Hive Table](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html)을 참고하면,
기본 디렉토리인 `spark-warehouse` 는 SparkSession을 실행할 때 `spark.sql.warehouse.dir` 설정을 통해 변경할 수 있다. 

```python
warehouse_location = abspath('spark-warehouse')

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL Hive integration example") \
    .config("spark.sql.warehouse.dir", warehouse_location) \
    .enableHiveSupport() \
    .getOrCreate()
```

정적 설정이라 세션 실행 중에는 변경할 수 없어서 세션을 종료하고 다시 실행했다.
`saved` 경로로 변경하고 다시 관리형 테이블을 생성해보니 해당 위치에 Parquet 파일들이 만들어졌다.

```python
from pyspark.sql import SparkSession
from pathlib import Path

warehouse_location = Path("saved")
warehouse_location.mkdir(exist_ok=True)

spark = (SparkSession
    .builder
    .appName("SparkSQLExampleApp")
    .config("spark.sql.warehouse.dir", str(warehouse_location.absolute()))
    .getOrCreate())
```

### 비관리형 테이블 생성하기

기존 `CREATE` 문을 사용하는 SQL 쿼리에서 뒤에 `USING` 키워드로 시작하는
CSV 파일 경로를 붙여주어 외부 데이터 소스로부터 비관리형 테이블을 생성할 수 있다.

```python
import os

table = "unmanaged_delay_flights"
schema = "date STRING, delay INT, distaince INT, origin STRING, destination STRING"
csv_file = os.path.join(os.getcwd(), "data/flights/departuredelays.csv")

spark.sql("CREATE TABLE {} ({}) USING csv OPTIONS (PATH '{}');".format(table, schema, csv_file))
```

CSV 파일의 상대경로로 SQL 쿼리를 실행해보니까 `FileStreamSink: Assume no metadata directory.`
경고 메시지가 발생했는데 절대경로로 바꿔주니까 해결되었다.

SQL 쿼리를 DataFrame API로 표현하면 아래와 같다. 관리형 테이블을 만드는 구문이랑 거의 비슷한데,
`path` 옵션으로 `/tmp` 경로를 지정하는데 차이가 있다.

```python
(flights_df
	.write
    .option("path", "/tmp/data/delay_flights")
    .saveAsTable(table, mode="overwrite"))
```

### 뷰 생성하기

기존 테이블을 토대로 뷰를 만들 수 있다. 전역(모든 SparkSession) 또는 세션 범위에서 생성할 수 있고,
Spark Application이 종료되면 뷰는 사라진다.

전역 임시 뷰는 SQL 쿼리에서는 `GLOBAL TEMP VIEW` 키워드를 추가하고,
파이썬에서는 `createOrReplaceGlobalTempView()` 함수를 호출하여 생성할 수 있다.

```python
table = "us_origin_airport_SFO"
spark.sql("""
CREATE OR REPLACE GLOBAL TEMP VIEW {} AS
SELECT date, delay, origin, destination FROM delay_flights
WHERE origin = 'SFO';
""".format(table))
```

```python
from pyspark.sql.functions import col
table = "us_origin_airport_SFO"
(df.select("date", "delay", "origin", "destination")
    .where(col("origin") == "SFO")
    .createOrReplaceGlobalTempView(table))
```

전역 임시 뷰는 `global_temp` 라는 전역 임시 데이터베이스에 생성되며,
`global_temp.<view_name>` 처럼 명시하여 뷰 테이블에 접근할 수 있다.
일반 임시 뷰는 현재 데이터베이스에 생성되므로 `global_temp` 접두사를 붙일 필요가 없다.

```python
spark.sql("SELECT * FROM global_temp.{};".format(table)).show(5)
```

### 메타데이터 보기

스파크는 관리형 및 비관리형 테이블에 대한 메타데이터를 관리한다.
메타데이터는 스파크 SQL의 상위 추상화 모듈인 카탈로그에 저장된다.
카탈로그에서 아래와 같이 데이터베이스, 테이블, 칼럼 목록을 조회할 수 있다.

```python
>>> spark.catalog.listDatabases()
[Database(name='default', catalog='spark_catalog', description='default database', locationUri='file:/Users/cuz/Documents/Github/study/spark/saved')]
```

```python
>>> spark.catalog.listTables()
[Table(name='delay_flights', catalog=None, namespace=[], description=None, tableType='TEMPORARY', isTemporary=True)]
```

```python
>>> spark.catalog.listColumns("delay_flights")
[Column(name='date', description=None, dataType='int', nullable=True, isPartition=False, isBucket=False, isCluster=False),
 Column(name='delay', description=None, dataType='int', nullable=True, isPartition=False, isBucket=False, isCluster=False),
 Column(name='distance', description=None, dataType='int', nullable=True, isPartition=False, isBucket=False, isCluster=False),
 Column(name='origin', description=None, dataType='string', nullable=True, isPartition=False, isBucket=False, isCluster=False),
 Column(name='destination', description=None, dataType='string', nullable=True, isPartition=False, isBucket=False, isCluster=False)]
```

### SQL 테이블 캐싱하기

스파크 공식문서 중 [CACHE TABLE](https://spark.apache.org/docs/latest/sql-ref-syntax-aux-cache-cache-table.html)을 참고하면,
`CACHE TABLE` 쿼리를 사용하여 임시 뷰를 캐싱할 수 있다.
`CACHE LAZY TABLE` 과 같이 `LAZY` 파라미터를 추가하면 테이블이 사용되는 시점까지 캐싱을 미룰 수 있다.

```python
spark.sql("CACHE TABLE delay_flights;")
```

테이블 캐시가 활성화 상태인지 보려면 카탈로그가 가진 `isCached` 함수를 참고할 수 있다.
캐시가 활성화되었다면 `True`, 아니면 `False` 를 반환한다.

```python
>>> spark.catalog.isCached("delay_flights")
True
```

```python
>>> spark.catalog.isCached("global_temp.us_origin_airport_sfo")
False
```

테이블 캐시를 삭제하고 싶다면 `UNCACHE TABLE` 쿼리를 사용한다.

```python
>>> spark.sql("UNCACHE TABLE delay_flights;")
>>> spark.catalog.isCached("delay_flights")
False
```

### 테이블을 DataFrame으로 변환하기

SQL 쿼리로 테이블 전체를 읽을 수도 있지만, `table()` 함수를 사용할 수도 있다.

```python
spark.sql("SELECT * FROM delay_flights;")
```

```python
spark.table("delay_flights")
```

`sql()` 과 `table()` 모두 `DataFrame` 객체를 반환한다.

## References

- [https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/)
- [https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights](https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights)
- [https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html)
- [https://spark.apache.org/docs/latest/sql-ref-syntax-aux-cache-cache-table.html](https://spark.apache.org/docs/latest/sql-ref-syntax-aux-cache-cache-table.html)
- [https://spark.apache.org/docs/latest/sql-ref-syntax-aux-cache-uncache-table.html](https://spark.apache.org/docs/latest/sql-ref-syntax-aux-cache-uncache-table.html)
