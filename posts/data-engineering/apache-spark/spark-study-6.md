---
title: "Apache Spark - 데이터 소스"
date: "2025-07-10T23:56:54+09:00"
layout: "post"
description: >
  Apache Spark의 다양한 데이터 소스를 다루며,
  Parquet, JSON, CSV, Avro 등 형식의 데이터 읽기/쓰기를 단계별로 안내합니다.
  빅데이터 처리를 위한 실용적인 기법을 배우세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/iafnblb6k95kbw7bwn2xj/spark-00-cover.webp?rlkey=6995tacnu3mvr7s31akl5sca6&dl=0"
categories: ["Data Engineering", "Apache Spark"]
tags: ["Apache Spark", "Data Sources", "Parquet", "JSON", "CSV", "Avro", "Spark SQL", "PySpark", "데이터 엔지니어링", "스파크", "Study"]
---

## Data Source API

### DataFrameReader

DataFrameReader는 데이터 소스에서 DataFrame으로 데이터를 읽는 방식이다. 아래와 같이 권장되는 사용 패턴이 있다.

```python
DataFrameReader
	.format(args) # 데이터 소스 형식
    .option("key", "value") # 키/값 쌍으로 연결되는 옵션
    .schema(args) # DDL 문자열 또는 StructType
    .load() # 데이터 소스의 경로
```

데이터 소스 형식에는 인수로 "parquet", "csv", "txt", "json", "jdbc", "orc", "avro" 등이 전달된다.
기본값은 "parquet" 또는 `spark.sql.sources.default` 에 지정된 항목이 설정된다.

JSON이나 CSV 형식은 `option()` 함수에서 스키마를 유추하는 `inferSchema` 옵션을 적용할 수 있지만,
스키마를 제공하면 로드 속도가 빨라진다.

SparkSession 인스턴스를 통해서 DataFrame에 액세스할 경우 `read()` 또는 `readStream()` 을 사용할 수 있다.
`read()` 는 정적 데이터 소스에서 DataFrame을 읽어 오며, `readStream()` 은 스트리밍 소스에서 인스턴스를 반환한다.

### DataFrameWriter

DataFrameWriter는 데이터 소스에 데이터를 저장하거나 쓰는 작업을 수행한다. 권장되는 사용 형식은 다음과 같다.

```python
DataFrameWriter
	.format(args) # 데이터 소스 형식
    .option(args) # 키/값 쌍으로 연결되는 옵션
    .bucketBy(args) # 버킷 개수 및 버킷 기준 칼럼 이름
    .partitionBy(args) # 데이터 소스의 경로
    .save(path) # 저장할 테이블
```

DataFrame에서 인스턴스에 액세스할 경우 `write()` 또는 `writeStream()` 을 사용할 수 있다.

## Data Sources

### Parquet

스파크의 기본 데이터 소스인 Parquet는 다양한 I/O 최적화를 제공하는 오픈소스 칼럼 기반 파일 형식이다.
압축을 통해 저장 공간을 절약하고 데이터 칼럼에 대한 빠른 액세스를 허용한다.

Parquet 파일은 데이터 파일, 메타데이터, 여러 압축 파일 및 일부 상태 파일이 포함된 디렉터리 구조가 저장된다.
메타데이터에는 파일 형식의 버전, 스키마, 경로 등의 칼럼 데이터가 포함된다.

[databricks/LearningSparkV2](https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights/summary-data)의
`databricks-datasets/learning-spark-v2/flights/summary-data/parquet` 경로에서
`2010-summary.parquet/` 디렉터리를 가져온다.

Parquet 파일의 디렉터리에는 다음과 같은 파일 집합이 포함된다.

```bash
% ls -la data/flights/summary-data/parquet/2010-summary.parquet/
-rwxr-xr-x@ ...     0 ... _SUCCESS
-rwxr-xr-x@ ...  3921 ... part-r-00000-1a9822ba-b8fb-4d8e-844a-ea30d0801b9e.gz.parquet
```

Parquet 파일을 DataFrame으로 읽으려면 형식과 경로를 지정하기만 하면 된다.
`spark.sql.sources.default` 설정을 하지 않았다면 `.format("parquet")` 함수는 생략해도 된다.

```python
file = "data/flights/summary-data/parquet/2010-summary.parquet"
df = spark.read.format("parquet").load(file)
df.show(5)
```

```bash
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|    1|
|    United States|            Ireland|  264|
|    United States|              India|   69|
|            Egypt|      United States|   24|
|Equatorial Guinea|      United States|    1|
+-----------------+-------------------+-----+
```

Parquet 파일을 Spark SQL 테이블로 읽으려면 아래와 같은 스파크 SQL을 사용할 수 있다.

```sql
CREATE OR REPLACE TEMPORARY VIEW delay_flights
	USING parquet
    OPTIONS (
    	path "data/flights/summary-data/parquet/2010-summary.parquet")
```

메타데이터가 궁금해서 `parquet-tools` 라이브러리를 설치하고,
`inspect` 명령어로 `part-XXXX` 압축 파일을 조회했다. 아래와 같이 출력되었는데,
3개의 칼럼 `DEST_COUNTRY_NAME`, `ORIGIN_COUNTRY_NAME`, `count` 에 대한
데이터 타입 등의 정보가 상세히 적혀 있다. 스파크는 해당 데이터 타입을 읽기 때문에,
위 DataFrame에 `printSchema()` 출력한 결과는 아래 칼럼별 데이터 타입과 같다.

```bash
% parquet-tools inspect data/flights/summary-data/parquet/2010-summary.parquet/part-r-00000-1a9822ba-b8fb-4d8e-844a-ea30d0801b9e.gz.parquet

############ file meta data ############
created_by: parquet-mr (build 32c46643845ea8a705c35d4ec8fc654cc8ff816d)
num_columns: 3
num_rows: 255
num_row_groups: 1
format_version: 1.0
serialized_size: 658


############ Columns ############
DEST_COUNTRY_NAME
ORIGIN_COUNTRY_NAME
count

############ Column(DEST_COUNTRY_NAME) ############
name: DEST_COUNTRY_NAME
path: DEST_COUNTRY_NAME
max_definition_level: 1
max_repetition_level: 0
physical_type: BYTE_ARRAY
logical_type: String
converted_type (legacy): UTF8
compression: GZIP (space_saved: 37%)

############ Column(ORIGIN_COUNTRY_NAME) ############
name: ORIGIN_COUNTRY_NAME
path: ORIGIN_COUNTRY_NAME
max_definition_level: 1
max_repetition_level: 0
physical_type: BYTE_ARRAY
logical_type: String
converted_type (legacy): UTF8
compression: GZIP (space_saved: 39%)

############ Column(count) ############
name: count
path: count
max_definition_level: 1
max_repetition_level: 0
physical_type: INT64
logical_type: None
converted_type (legacy): NONE
compression: GZIP (space_saved: 53%)
```

DataFrame을 DataFrameWriter를 사용해 Parquet 파일로 저장할 때는 아래와 같은 함수를 사용할 수 있다.

```python
(df.write.format("parquet")
	.mode("overwrite")
    .option("compression", "snappy")
    .save("/tmp/data/parquet/df_parquet"))
```

압축 방식으로 `snappy` 를 사용하여 `snappy` 압축 파일이 생성된다.
DataFrame을 직접 저장하면 아래와 같은 파일이 생성된다.

```bash
% ls -la /tmp/data/parquet/df_parquet/
-rw-r--r--@ ...     8 ... ._SUCCESS.crc
-rw-r--r--@ ...    52 ... .part-00000-9828b287-9956-40cb-9c33-d59bea52e5be-c000.snappy.parquet.crc
-rw-r--r--@ ...     0 ... _SUCCESS
-rw-r--r--@ ...  5442 ... part-00000-9828b287-9956-40cb-9c33-d59bea52e5be-c000.snappy.parquet
```

### JSON

JSON 데이터 형식은 XML에 비해 읽기 쉽고, 구문을 분석하기 쉬운 형식이다.
단일 라인 모드와 다중 라인 모드를 모두 지원한다. 단일 라인 모드에서는 각 라인이 단일 JSON 개체를 나타내지만,
다중 라인 모드에서는 전체 라인 객체가 단일 JSON 개체를 구성한다. `option()` 함수에서
`multiLine` 옵션에 `ture` 또는 `false` 를 설정할 수 있다.

단일 라인 모드의 JSON 데이터는 아래와 같이 구성된다.

```bash
% head -n 5 data/flights/summary-data/json/2010-summary.json
{"ORIGIN_COUNTRY_NAME":"Romania","DEST_COUNTRY_NAME":"United States","count":1}
{"ORIGIN_COUNTRY_NAME":"Ireland","DEST_COUNTRY_NAME":"United States","count":264}
{"ORIGIN_COUNTRY_NAME":"India","DEST_COUNTRY_NAME":"United States","count":69}
{"ORIGIN_COUNTRY_NAME":"United States","DEST_COUNTRY_NAME":"Egypt","count":24}
{"ORIGIN_COUNTRY_NAME":"United States","DEST_COUNTRY_NAME":"Equatorial Guinea","count":1}
```

JSON 파일을 DataFrame으로 읽으려면 아래처럼 `.format("json")` 을 지정한다.

```python
file = "data/flights/summary-data/json/*"
df = spark.read.format("json").load(file)
df.show(5)
```

```bash
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|   15|
|    United States|            Croatia|    1|
|    United States|            Ireland|  344|
|            Egypt|      United States|   15|
|    United States|              India|   62|
+-----------------+-------------------+-----+
```

JSON 데이터 소스에 대해 DataFrameReader 및 DataFrameWriter 에 대한 일반적인 옵션은 아래와 같다.

- `compression` : 압축 코덱을 쓰기 시에 사용할 수 있다. `bzip2`, `gzip`, `snappy` 등이 값으로 전달된다.
- `dateFormat` : Java의 DateTimeFormatter에서 제공하는 모든 형식을 사용할 수 있다. (yyyy-MM-dd 등)
- `multiLine` : `true` 를 지정하면 다중 라인 모드를 사용한다. 기본값은 `false` 이다.
- `allowUnquotedFileNames` : 따옴표로 묶이지 않은 JSON 필드 이름을 허용한다. 기본값은 `false` 이다.

### CSV

쉼표로 각 데이터 또는 필드를 구분하며, 쉼표로 구분된 각 줄은 레코드를 나타낸다.
쉼표가 데이터의 일부인 경우, 값을 쌍따옴표로 감싸주거나, 다른 구분 기호를 사용하여 필드를 분리할 수 있다.

일반적인 CSV 데이터는 아래와 같이 구성된다.

```bash
% head -n 5 data/flights/summary-data/csv/2010-summary.csv          
DEST_COUNTRY_NAME,ORIGIN_COUNTRY_NAME,count
United States,Romania,1
United States,Ireland,264
United States,India,69
Egypt,United States,24
```

CSV 파일을 DataFrame으로 읽으려면 아래처럼 `.format("csv")` 을 지정한다.
위 파일과 같이 헤더가 있는 경우 `header` 옵션에 `true` 를 설정한다.
`nullValue` 옵션을 사용해 `null` 데이터를 특정 값으로 교체할 수 있다.

```python
file = "data/flights/summary-data/csv/*"
df = spark.read.format("csv").option("header", "true").load(file)
df.show(5)
```

```bash
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|    1|
|    United States|            Ireland|  264|
|    United States|              India|   69|
|            Egypt|      United States|   24|
|Equatorial Guinea|      United States|    1|
+-----------------+-------------------+-----+
```

CSV 데이터 소스에 대해 DataFrameReader 및 DataFrameWriter 에 대한 일반적인 옵션은 아래와 같다.

- `compression` : 압축 코덱을 쓰기 시에 사용할 수 있다. `bzip2`, `gzip`, `snappy` 등이 값으로 전달된다.
- `dateFormat` : Java의 DateTimeFormatter에서 제공하는 모든 형식을 사용할 수 있다. (yyyy-MM-dd 등)
- `multiLine` : `true` 를 지정하면 다중 라인 모드를 사용한다. 기본값은 `false` 이다.
- `interSchema` : `true` 를 지정하면 스파크가 칼럼 데이터 유형을 결정한다. 기본값은 `false` 이다.
- `sep` : 칼럼을 구분하기 위한 문자이며, 기본 구분 기호는 쉼표(,)다.
- `escape` : 따옴표를 이스케이프할 때 사용하는 문자이며, 기본값은 / 다.
- `header` : 첫 번째 줄이 칼럼명을 나타내는 헤더일 경우 `true` 를 지정하고, 기본값은 `false` 이다.

### Avro

스파크 2.4에 내장된 데이터 소스인 Avro 형식은 특히 아파치 카프카에서
메시지를 직렬화 및 역직렬화할 때 사용된다. JSON에 대한 직접 매핑, 속도와 효율성 등 많은 이점을 제공한다.

스파크 공식 문서의 [Apache Avro Data Source Guide](https://spark.apache.org/docs/latest/sql-data-sources-avro.html)에 따르면,
`spark-avro` 모듈은 외부 모듈로 `spark-submit` 또는 `spark-shell` 에 포함되어 있지 않다.
따라서, 아래와 같이 `--packages` 를 사용하여 종속성을 추가할 수 있다.

```bash
./bin/spark-shell --packages org.apache.spark:spark-avro_2.13:4.0.0 ...
```

SparkSession 인스턴스를 사용할 경우, `spark.jars.packages` 설정에 `spark-avro_2.13` 종속성을 추가한다.

```python
from pyspark.sql import SparkSession

spark = (SparkSession
    .builder
    .appName("SparkAvroExampleApp")
    .config("spark.jars.packages", "org.apache.spark:spark-avro_2.13:4.0.0")
    .getOrCreate())
```

Avro 파일을 DataFrame으로 읽으려면 아래처럼 `.format("avro")` 을 지정한다.

```python
file = "data/flights/summary-data/avro/*"
df = spark.read.format("avro").load(file)
df.show(5)
```

```bash
+-----------------+-------------------+-----+
|DEST_COUNTRY_NAME|ORIGIN_COUNTRY_NAME|count|
+-----------------+-------------------+-----+
|    United States|            Romania|    1|
|    United States|            Ireland|  264|
|    United States|              India|   69|
|            Egypt|      United States|   24|
|Equatorial Guinea|      United States|    1|
+-----------------+-------------------+-----+
```

Avro 데이터 소스에 대해 DataFrameReader 및 DataFrameWriter 에 대한 일반적인 옵션은 아래와 같다.

- `avroSchema` : JSON 형식으로 제공할 수 있는 Avro 스키마이다. Avro 데이터나 카탈리스트 데이터와 일치하지 않으면 읽기/쓰기 작업이 실패한다.
- `recordName` : Avro 사양에 필요한 쓰기 결과의 최상위 레코드명이다.
- `recrodNamespace` : 쓰기 결과에 네임스페이스를 기록한다.
- `ignoreExtension` : 확장자가 `.avro` 인지 여부에 관계없이 모든 파일을 읽어들인다.
- `compression` : 쓰기에 사용할 압축 코덱을 지정할 수 있다.

### Image

스파크 2.4에서 머신러닝 프레임워크를 지원하기 위해 새로운 데이터 소스인 이미지 파일을 도입했다.

[databricks/LearningSparkV2](https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2)의
`databricks-datasets/learning-spark-v2` 경로에서 `cctvVideos/` 디렉터리를 가져온다.
해당 디렉터리의 구조는 다음과 같다.

```
cctvVideos/
├── README.md
└── train_images/
    ├── label=0/
    │   ├── Browse2frame0000.jpg
    │   ├── Browse2frame0001.jpg
    │   ├── Browse2frame0002.jpg
    │   ├── ...
    |   └── Walk2frame0042.jpg
    └── label=1/
        ├── Fight_Chaseframe0012.jpg
        ├── Fight_Chaseframe0013.jpg
        ├── Fight_Chaseframe0014.jpg
        ├── ...
        └── Rest_WiggleOnFloorframe0050.jpg
```

이미지 파일은 아래와 같이 DataFrameReader 함수로 읽을 수 있다.
이미지 파일을 읽을 때 `numpy` 라이브러리가 필요하다.

```python
from pyspark.ml import image

image_dir = "data/cctvVideos/train_images"
images_df = spark.read.format("image").load(image_dir)
images_df.printSchema()
```

```bash
root
 |-- image: struct (nullable = true)
 |    |-- origin: string (nullable = true)
 |    |-- height: integer (nullable = true)
 |    |-- width: integer (nullable = true)
 |    |-- nChannels: integer (nullable = true)
 |    |-- mode: integer (nullable = true)
 |    |-- data: binary (nullable = true)
 |-- label: integer (nullable = true)
```

이미지의 높이 및 너비와 같은 정보는 아래와 같이 조회할 수 있다.

```python
images_df.select("image.height", "image.width", "image.nChannels", "image.mode", "label").show(5)
```

```bash
+------+-----+---------+----+-----+
|height|width|nChannels|mode|label|
+------+-----+---------+----+-----+
|   288|  384|        3|  16|    0|
|   288|  384|        3|  16|    1|
|   288|  384|        3|  16|    0|
|   288|  384|        3|  16|    0|
|   288|  384|        3|  16|    0|
+------+-----+---------+----+-----+
```

### Binary File

이진 파일을 읽으려면 데이터 소스 형식을 `binaryFile` 로 지정해야 한다.
DataFrameReader는 이진 파일을 원본 내용과 메타데이터를 포함하는 단일 DataFrame 행으로 변환한다.

`pathGlobFilter` 를 사용하면 지정된 전역 패턴과 일치하는 경로로 파일을 로드할 수 있다.
아래 코드는 디렉터리에서 모든 `.jpg` 파일을 읽는다.

```python
path = "data/cctvVideos/train_images"
binary_files_df = spark.read.format("binaryFile").option("pathGlobFilter", "*.jpg").load(path)
binary_files_df.show(5)
```

```bash
+--------------------+-------------------+------+--------------------+-----+
|                path|   modificationTime|length|             content|label|
+--------------------+-------------------+------+--------------------+-----+
|file:/Users/cuz/D...|2025-01-28 13:30:40| 55037|[FF D8 FF E0 00 1...|    0|
|file:/Users/cuz/D...|2025-01-28 13:30:40| 54634|[FF D8 FF E0 00 1...|    1|
|file:/Users/cuz/D...|2025-01-28 13:30:40| 54624|[FF D8 FF E0 00 1...|    0|
|file:/Users/cuz/D...|2025-01-28 13:30:40| 54505|[FF D8 FF E0 00 1...|    0|
|file:/Users/cuz/D...|2025-01-28 13:30:40| 54475|[FF D8 FF E0 00 1...|    0|
+--------------------+-------------------+------+--------------------+-----+
```

## References

- [https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/)
- [https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights/summary-data](https://github.com/databricks/LearningSparkV2/tree/master/databricks-datasets/learning-spark-v2/flights/summary-data)
- [https://spark.apache.org/docs/latest/api/python/tutorial/sql/python_data_source.html](https://spark.apache.org/docs/latest/api/python/tutorial/sql/python_data_source.html)
- [https://spark.apache.org/docs/latest/sql-data-sources.html](https://spark.apache.org/docs/latest/sql-data-sources.html)
- [https://spark.apache.org/docs/latest/sql-data-sources-avro.html](https://spark.apache.org/docs/latest/sql-data-sources-avro.html)
