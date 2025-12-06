---
title: "Apache Spark - 외부 데이터베이스 연동 (PostgreSQL, MySQL)"
date: "2025-07-12T21:29:06+09:00"
layout: "post"
description: >
  Apache Spark의 외부 데이터 소스 연결과 데이터 읽기/쓰기를 다루며,
  JDBC, RDBMS 등과의 연동을 단계별로 안내합니다. 빅데이터 처리를 위한 실용적인 기법을 배우세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/iafnblb6k95kbw7bwn2xj/spark-00-cover.webp?rlkey=6995tacnu3mvr7s31akl5sca6&dl=0"
categories: ["Data Engineering", "Apache Spark"]
tags: ["Apache Spark", "JDBC", "RDBMS", "Hive", "PostgreSQL", "MySQL", "데이터 엔지니어링", "스파크", "Study"]
---

## Spark SQL CLI

스파크 SQL 쿼리를 실행하는 쉬운 방법은 `spark-sql` CLI이다.
스파크 SQL CLI는 Hive 메타스토어와 서비스와 통신하는 대신 Thrift JDBC 서버와 통신할 수 없다.

### Hive 설치

진행하기 전에 Hive가 설치되어 있지 않아서 설치해야 했다.

설치 과정은 [[Hive] virtual box linux [ubuntu 18.04]에 하이브 설치,다운로드 4.ubuntu 에 Hive(하이브) 다운로드](https://spidyweb.tistory.com/215)
게시글을 참고했다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/0o5512v3i618kk6yrok97/spark-16-hive-tgz.webp?rlkey=1lcorgbp5xngu4w4g4zugvi6b&dl=0"
  alt="/hive/hive-4.0.1/apache-hive-4.0.1-bin.tar.gz"
  max-width="691px"
  align="center"
  href="https://dlcdn.apache.org/hive/hive-4.0.1/" >}}

1. 브라우저 또는 curl, wget 등 명령어를 통해 압축 파일을 내려받는다.

```bash
wget https://dlcdn.apache.org/hive/hive-4.0.1/apache-hive-4.0.1-bin.tar.gz
```

2. 압축 해제 프로그램을 사용하거나, 터미널에서 아래 명령어를 입력하여 압축 해제한다.

```bash
tar zxvf apache-hive-4.0.1-bin.tar.gz
```

3. Hive 경로에 접근하기 위해 `~/.zshrc` 에 환경변수를 설정한다.

```bash
export HIVE_HOME=/Users/{username}/hive-4.0.1
export PATH=$PATH:$HIVE_HOME/bin
```

4. 변경 사항을 적용하기 위해 터미널을 재시작하거나 아래 명령어를 실행한다.

```bash
source ~/.zshrc
````

5. `$HIVE_HOME/bin/hive-config.sh` 파일에 HDFS 경로를 추가한다.

```bash
export HADOOP_HOME=/Users/{username}/hadoop-3.4.0
```

6. HDFS에 Hive 디렉터리를 생성한다.

```bash
$HADOOP_HOME/sbin/start-all.sh
```

```bash
hdfs dfs -mkdir /tmp
hdfs dfs -chmod g+w /tmp
```

```bash
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -chmod g+w /user/hive/warehouse
```

```bash
% hdfs dfs -ls /
drwxrwxr-x   - user supergroup          0 2025-07-12 10:08 /tmp
drwxr-xr-x   - user supergroup          0 2025-07-12 10:08 /user
```

7. `$HIVE_HOME/conf/hive-site.xml` 파일에 아래 속성을 맨 윗부분에 추가한다.
   파일이 없을 경우 동일한 경로의 `hive-default.xml.template` 파일을 `hive-site.xml` 이름의 파일로 복사한다.

```xml
<property>
  <name>system:java.io.tmpdir</name>
  <value>/tmp/hive/java</value>
</property>

<property>
  <name>system:user.name</name>
  <value>${user.name}</value>
</property>
```

8. Derby DB를 시작한다. 오류가 발생할 경우 참고한 [게시글](https://spidyweb.tistory.com/215)을 확인해볼 수 있다.

```bash
$HIVE_HOME/bin/schematool -initSchema -dbType derby
```

```bash
Initializing the schema to: 4.0.0
Metastore connection URL:	 jdbc:derby:;databaseName=metastore_db;create=true
Metastore connection Driver :	 org.apache.derby.jdbc.EmbeddedDriver
Metastore connection User:	 APP
Starting metastore schema initialization to 4.0.0
Initialization script hive-schema-4.0.0.derby.sql
...
Initialization script completed
```

9. Hive CLI를 시작해본다.

```bash
$HIVE_HOME/bin/hive
```

```bash
Beeline version 4.0.1 by Apache Hive
beeline> 
```

10. Hive 메타스토어 서버를 실행한다.

```bash
hive --service metastore &
```

### hive-site.xml 편집하기

[Hive Tables 공식문서](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html)에 따르면,
Spark SQL로 Hive에 저장된 데이터에 액세스하려면
`hive-site.xml`, `core-site.xml`, `hdfs-site.xml` 파일들을 `$SPARK_HOME/conf/` 경로에 배치해야 한다.

그런데 위 파일들을 복사한 후 `spark-sql` 을 실행하니까 `WARN HiveConf` 메시지가 460줄이나 발생했다.

```bash
25/07/12 11:00:36 WARN HiveConf: HiveConf of name hive.repl.dump.metadata.only.for.external.table does not exist
25/07/12 11:00:36 WARN HiveConf: HiveConf of name hive.druid.rollup does not exist
25/07/12 11:00:36 WARN HiveConf: HiveConf of name hive.repl.retain.prev.dump.dir does not exist
...
```

단순히 Hive 경로에서 `$SPARK_HOME/conf/` 경로로 `hive-site.xml` 파일을 복사했는데,
Spark가 사용하지 않는 속성들이 들어있어서 이러한 메시지가 발생했다.

실제 동작에는 영향을 주지 않지만 `spark-sql` 을 실행할 때마다
이런 메시지를 볼 수는 없어서 `hive-site.xml` 파일에서 문제되는 속성들을 전부 삭제했다.

속성을 하나씩 삭제하기에는 너무 많아서 파이썬 코드를 사용해 `hive-site.xml` 파일을 수정했다.
`properties` 변수에 문제되는 속성의 이름에 대한 문자열 리스트를 할당하고 코드를 실행한다.

```python
import xml.etree.ElementTree as ET
import os

SPARK_HOME = os.environ.get("SPARK_HOME")
properties = [] # 제거하고 싶은 속성 이름 리스트

tree = ET.parse(f"{SPARK_HOME}/conf/hive-site.xml")
root = tree.getroot()

targets = [] # 삭제 대상 property 수집
for prop in root.findall("property"):
    name = prop.find("name")
    if (name is not None) and (name.text in properties):
        targets.append(prop)

for prop in targets:
    root.remove(prop) # 속성 삭제

tree.write(f"{SPARK_HOME}/conf/hive-site.cleaned.xml", encoding="utf-8", xml_declaration=True)
```

생성된 `hive-site.cleaned.xml` 내용을 확인하고 `hive-site.xml` 로 바꿔준다.

### spark-sql

`$SPARK_HOME/bin/spark-sql` 스크립트를 실행해 스파크 SQL CLI를 시작한다.

```bash
$SPARK_HOME/bin/spark-sql
```

셸을 시작하면 스파크 SQL 쿼리를 대화 형식으로 수행할 수 있다.
`--help` 옵션을 통해 아래와 같은 CLI 옵션을 확인할 수 있다.

```
CLI options:
 -d,--define <key=value>          Hive 쿼리에서 사용할 변수(key)와 값(value)을 지정
    --database <databasename>     사용할 데이터베이스 지정
 -e <quoted-query-string>         명령어 입력창에서 직접 SQL 쿼리를 실행할 때 사용
 -f <filename>                    SQL 쿼리가 작성된 파일을 실행할 때 사용
 -H,--help                        도움말 제공
    --hiveconf <property=value>   Hive 설정값을 지정할 때 사용
    --hivevar <key=value>         Hive 쿼리에서 사용할 변수(key)와 값(value)을 지정
 -i <filename>                    CLI 실행 시 먼저 실행될 쿼리 파일 제공
 -S,--silent                      대화형 셸에서 결과만 출력하고 기타 정보는 무시
 -v,--verbose                     SQL 쿼리문을 콘솔에 출력
```

스파크 SQL 테이블을 생성하려면 다음 쿼리를 실행한다.

```bash
spark-sql (default)> CREATE TABLE people (name STRING, age INT);
Time taken: 0.685 seconds
```

테이블이 생성되었는지 확인한다.

```bash
spark-sql (default)> SHOW TABLES;
people
Time taken: 0.239 seconds, Fetched 1 row(s)
```

테이블을 생성하고 테이블에 데이터를 삽입한다.

```bash
spark-sql (default)> INSERT INTO people VALUES ("Michael", NULL);
Time taken: 1.728 seconds
spark-sql (default)> INSERT INTO people VALUES ("Andy", 30);
Time taken: 0.601 seconds
spark-sql (default)> INSERT INTO people VALUES ("Samantha", 19);
Time taken: 0.149 seconds
```

테이블에서 20세 미만의 사람들이 몇 명인지 확인해본다.

```bash
spark-sql (default)> SELECT * FROM people WHERE age < 20;
Samantha	19
Time taken: 0.285 seconds, Fetched 1 row(s)
```

### 비라인 작업

비라인은 SQLLine CLI를 기반으로 하는 JDBC 클라이언트다.
동일한 유틸리티를 사용해 스파크 쓰리프트 서버에 대해 스파크 SQL 쿼리를 실행할 수 있다.

스파크 쓰리프트 JDBC/ODBC 서버를 시작하려면
`$SPARK_HOME/sbin/start-thriftserver.sh` 스크립트를 실행한다.

```bash
$SPARK_HOME/sbin/start-thriftserver.sh
```

비라인을 사용하여 쓰리프트 JDBC/ODBC 서버를 테스트한다.

```bash
$SPARK_HOME/bin/beeline
```

비라인을 구성하여 로컬 쓰리프트 서버에 연결한다.
사용자 이름은 로그인 계정을 입력하고 비밀번호는 비어 있다.

```bash
beeline> !connect jdbc:hive2://localhost:10000
Connecting to jdbc:hive2://localhost:10000
Enter username for jdbc:hive2://localhost:10000: user
Enter password for jdbc:hive2://localhost:10000: 

Connected to: Spark SQL (version 4.0.0)
Driver: Hive JDBC (version 2.3.10)
Transaction isolation: TRANSACTION_REPEATABLE_READ
0: jdbc:hive2://localhost:10000> 
```

비라인에서 스파크 SQL 쿼리를 실행할 수 있다.

```bash
0: jdbc:hive2://localhost:10000> SHOW TABLES;
+------------+------------+--------------+
| namespace  | tableName  | isTemporary  |
+------------+------------+--------------+
| default    | people     | false        |
+------------+------------+--------------+
1 row selected (0.297 seconds)
```

```bash
0: jdbc:hive2://localhost:10000> SELECT * FROM people;
+-----------+-------+
|   name    |  age  |
+-----------+-------+
| Samantha  | 19    |
| Andy      | 30    |
| Michael   | NULL  |
+-----------+-------+
3 rows selected (1.44 seconds)
```

쓰리프트 서버를 중지할 때는 `stop-thriftserver.sh` 스크립트를 실행한다.

```bash
$SPARK_HOME/sbin/stop-thriftserver.sh
```

## 외부 데이터 소스

### JDBC

스파크 SQL에는 JDBC를 사용하여 다른 데이터베이스에서 데이터를 읽을 수 있는 데이터 소스 API가 포함되어 있다.
스파크 SQL의 이점을 활용하여 쿼리 결과를 DataFrame으로 반환받을 수 있다.

JDBC 데이터 소스에 연결하려면 JDBC 드라이버를 지정해야 한다.
`spark-shell` 을 실행할 때 클래스 경로를 지정할 수 있다.
클래스 경로에 특정 데이터베이스용 JDBC 드라이버를 포함해야 한다.

```bash
$SPARK_HOME/bin/spark-shell --driver-class-path $database.jar --jars $database.jar
```

### 데이터 소스 옵션

사용자는 데이터 소스 옵션에서 JDBC 연결 속성을 지정할 수 있다.
다음과 같은 일반적인 연결 속성을 제공한다.

- `user`, `password` : 데이터 소스에 로그인하기 위한 계정 정보
- `url` : JDBC 연결 URL, `jdbc:subprotocol:subname` 와 같은 형식
- `dbtable` : 읽거나 쓸 JDBC 테이블, `query` 옵션과 동시에 사용할 수는 없다.
- `query` : 스파크로 데이터를 읽어오는 데 사용되는 쿼리, `dbtable` 옵션과 동시에 사용할 수는 없다.
- `driver` : 지정한 URL에 연결하는 데 사용할 JDBC 드라이버의 클래스 이름

스파크 SQL과 JDBC 외부 소스 간에 많은 양의 데이터를 전송할 때 데이터 소스를 분할할 필요가 있다.
대규모 작업에서 다음과 같은 속성을 사용할 수 있다.

- `numPartitions` : 테이블 읽기 및 쓰기에서 병렬 처리를 위해 사용할 수 있는 최대 파티션 수, 또는 최대 동시 JDBC 연결 수
- `partitionColumn` : 외부 소스를 읽을 때 파티션을 결정하기 위해 사용되는 칼럼 (숫자, 날짜, 또는 타임스탬프)
- `lowerBound` : 파티션 크기에 대한 파티션 열의 최솟값
- `upperBound` : 파티션 크기에 대한 파티션 열의 최댓값

`numPartitions` 는 스파크 워커 수의 배수를 사용하는 것이 좋지만,
소스 시스템이 읽이 요청을 얼마나 잘 처리할 수 있는지 확인해야 한다.

`partitionColumn` 은 데이터 스큐를 방지하기 위해 균일하게 분산될 수 있는 열을 선택해야 한다.   
예를 들어, `{numPartitions : 10, lowerBound : 1000, upperBound : 10000}` 을 선택했지만
대부분이 2000에서 3000 사이의 값을 요청하는 경우 다른 `partitionColumn` 을 사용하거나 새 항목을 생성하는 것이 좋다.

## PostgreSQL

### PostgreSQL 실행

PostgreSQL은 따로 설치하지 않고 Docker 컨테이너로 실행했다.

```bash
% docker run --name postgres13 -d -p 5432:5432 postgres:13
% docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED         STATUS         PORTS                                         NAMES
6d3a827005a6   postgres:13   "docker-entrypoint.s…"   1 seconds ago   Up 2 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres13
```

`postgres13` 컨테이너에 접속하면서 PostgreSQL 프롬프트에 진입한다.

```bash
% docker exec -it postgres13 psql -U postgres
psql (13.21 (Debian 13.21-1.pgdg120+1))
Type "help" for help.

postgres=# 
```

SparkSession에서 접속해보기 위해 임시로 사용자, 스키마, 테이블을 생성했다.

```sql
CREATE USER spark WITH PASSWORD 'spark';
CREATE SCHEMA spark_schema AUTHORIZATION spark;
CREATE TABLE spark_schema.users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT ALL PRIVILEGES ON SCHEMA spark_schema TO spark;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA spark_schema TO spark;
```

3개 행만 추가해보고 내용을 확인해봤다.

```sql
INSERT INTO spark_schema.users (name) VALUES ('김민수');
INSERT INTO spark_schema.users (name) VALUES ('이민수');
INSERT INTO spark_schema.users (name) VALUES ('박민수');
```

```sql
postgres=# SELECT * FROM spark_schema.users;
 id |  name  |         created_at         
----+--------+----------------------------
  1 | 김민수 | 2025-07-12 11:29:42.40485
  2 | 이민수 | 2025-07-12 11:29:47.036362
  3 | 박민수 | 2025-07-12 11:29:50.087099
(3 rows)
```

### PostgreSQL 드라이버 다운로드

PostgreSQL 데이터베이스에 연결하려면 JDBC 드라이버 파일을 클래스 경로에 추가한다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/j2o3uadsj58suc9z81yaw/spark-17-postgres-jdbc-driver.webp?rlkey=qpai41152zlaovp7aoev19p72&dl=0"
  alt="If you are using Java 8 or newer then you should use the JDBC 4.2 version"
  href="https://jdbc.postgresql.org/download/" >}}

이미지 링크로 연결된 위 웹사이트에서 Java 버전에 맞는 파일을 다운로드 받을 수 있는데
Java 8 이상인 경우 아래 URL을 통해 직접 다운로드 받을 수도 있다.

```bash
wget https://jdbc.postgresql.org/download/postgresql-42.7.7.jar
```

### PostgreSQL 데이터 읽기

SparkSession을 생성할 때 앞단계에서 내려받은 JDBC 드라이버 파일의 경로를
`spark.driver.extraClassPath` 설정값으로 전달한다.

```python
from pyspark.sql import SparkSession
import os

SPARK_HOME = os.environ.get("SPARK_HOME")
spark = (SparkSession
    .builder
    .config("spark.driver.extraClassPath", f"{SPARK_HOME}/jars/postgresql-42.7.7.jar") \
    .appName("PostgresExample")
    .getOrCreate())
```

`postgres` 데이터베이스의 `spark_schema.users` 테이블의 데이터를 가져온다.
데이터를 출력해보면 앞에서 추가한 3개 행이 반환되는 것을 볼 수 있다.

```python
df = spark.read.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/postgres") \
    .option("dbtable", "spark_schema.users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .load()
df.show()
```

```sql
+---+------+--------------------+
| id|  name|          created_at|
+---+------+--------------------+
|  1|김민수|2025-07-12 11:29:...|
|  2|이민수|2025-07-12 11:29:...|
|  3|박민수|2025-07-12 11:29:...|
+---+------+--------------------+
```

### PostgreSQL 데이터 쓰기

반대로 DataFrame을 PostgreSQL에 새로운 테이블로 저장할 수도 있다.

```python
df.write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/postgres") \
    .option("dbtable", "spark_schema.new_users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .save()
```

PostgreSQL에서 새로운 테이블을 조회했을 때 동일한 데이터가 저장된 것을 볼 수 있다.

```sql
postgres=# SELECT * FROM spark_schema.new_users;
 id |  name  |          created_at           
----+--------+-------------------------------
  1 | 김민수 | 2025-07-12 02:29:42.40485+00
  2 | 이민수 | 2025-07-12 02:29:47.036362+00
  3 | 박민수 | 2025-07-12 02:29:50.087099+00
(3 rows)
```

또한, 기존 테이블에 새로운 행으로 추가할 수도 있다.

```python
df.select("name").write.format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/postgres") \
    .option("dbtable", "spark_schema.users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .mode("append") \
    .save()
```

`spark_schema.users` 테이블의 `id` 열이 SERIAL 타입인데, 시퀀스에 대한 권한이 없어서
위 명령어를 실행하면 오류가 발생했다. 그래서 PostgreSQL에서 `spark` 사용자에게 권한을 부여했다.

```sql
GRANT USAGE, SELECT ON SEQUENCE spark_schema.users_id_seq TO spark;
```

스파크의 DataFrameWriter를 통해 `spark_schema.users` 테이블에 새로운 행을 추가하고
데이터를 조회하면 아래와 같이 3개의 행이 더 추가된 것을 볼 수 있다.

```sql
postgres=# SELECT * FROM spark_schema.users;
 id |  name  |         created_at         
----+--------+----------------------------
  1 | 김민수 | 2025-07-12 11:29:42.40485
  2 | 이민수 | 2025-07-12 11:29:47.036362
  3 | 박민수 | 2025-07-12 11:29:50.087099
  4 | 김민수 | 2025-07-12 20:42:51.519473
  5 | 이민수 | 2025-07-12 20:42:51.519473
  6 | 박민수 | 2025-07-12 20:42:51.519473
(6 rows)
```

비슷한 시간에 데이터를 추가했는데 컨테이너는 UTC 시간대고 SparkSession은
KST 시간대에 있어서 `created_at` 이 9시간 차이가 나는 것 같다.

## MySQL

### MySQL 실행

마찬가지로 MySQL 컨테이너를 실행한다.

```bash
% docker run --name mysql8 -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql:8
% docker ps
CONTAINER ID   IMAGE         COMMAND                  CREATED             STATUS             PORTS                                         NAMES
48d3c4f28fd6   mysql:8       "docker-entrypoint.s…"   11 seconds ago      Up 10 seconds      0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp   mysql8
6d3a827005a6   postgres:13   "docker-entrypoint.s…"   About an hour ago   Up About an hour   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp   postgres13
```

`mysql8` 컨테이너에 접속하면서 MySQL 프롬프트에 진입한다.

```bash
% docker exec -it mysql8 mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 9
Server version: 8.4.5 MySQL Community Server - GPL
...
mysql> 
```

SparkSession에서 접속해보기 위해 임시로 사용자, 스키마, 테이블을 생성했다.

```sql
CREATE USER 'spark'@'%' IDENTIFIED BY 'spark';
CREATE DATABASE spark_db;
USE spark_db;
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
GRANT ALL PRIVILEGES ON spark_db.* TO 'spark'@'%';
FLUSH PRIVILEGES;
```

3개 행만 추가해보고 내용을 확인해봤다.

```sql
INSERT INTO users (name) VALUES ('kim');
INSERT INTO users (name) VALUES ('lee');
INSERT INTO users (name) VALUES ('park');
```

```sql
mysql> SELECT * FROM users;
+----+------+---------------------+
| id | name | created_at          |
+----+------+---------------------+
|  1 | kim  | 2025-07-12 12:08:41 |
|  2 | lee  | 2025-07-12 12:08:45 |
|  3 | park | 2025-07-12 12:08:48 |
+----+------+---------------------+
3 rows in set (0.01 sec)
```

### MySQL 드라이버 다운로드

MySQL 데이터베이스에 연결하려면 JDBC 드라이버 파일을 클래스 경로에 추가한다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/oyl2a11p3l7jfkzcl5bp3/spark-18-mysql-connector.webp?rlkey=2zsceygess6fl29e1ze5nd9eo&dl=0"
  alt="Platform Independent (Architecture Independent), Compressed TAR Archive"
  href="https://downloads.mysql.com/archives/c-j/" >}}

이미지 링크로 연결된 위 웹사이트 또는 아래와 같은 `curl`, `wget` 명령어 등으로
버전에 맞는 압축 파일을 다운로드 받을 수 있다.

```bash
wget https://downloads.mysql.com/archives/get/p/3/file/mysql-connector-j-8.4.0.tar.gz
```

압축 파일을 해제하면 JDBC 드라이버 파일을 확인할 수 있다.

```bash
% tar zxvf mysql-connector-j-8.4.0.tar.gz
% ls -la mysql-connector-j-8.4.0       
total 5888
drwxr-xr-x@ 10 user  staff      320 Mar 13  2024 .
drwx------@ 49 user  staff     1568 Jul 12 21:12 ..
-rw-r--r--@  1 user  staff   282811 Mar 13  2024 CHANGES
-rw-r--r--@  1 user  staff      188 Mar 13  2024 INFO_BIN
-rw-r--r--@  1 user  staff      134 Mar 13  2024 INFO_SRC
-rw-r--r--@  1 user  staff    82896 Mar 13  2024 LICENSE
-rw-r--r--@  1 user  staff     1624 Mar 13  2024 README
-rw-r--r--@  1 user  staff    91633 Mar 13  2024 build.xml
-rw-r--r--@  1 user  staff  2533399 Mar 13  2024 mysql-connector-j-8.4.0.jar
drwxr-xr-x@  8 user  staff      256 Mar 13  2024 src
```

### MySQL 데이터 읽기

SparkSession을 생성할 때 MySQL JDBC 드라이버 파일의 경로를
`spark.driver.extraClassPath` 설정값으로 전달한다.

```python
from pyspark.sql import SparkSession
import os

SPARK_HOME = os.environ.get("SPARK_HOME")
spark = (SparkSession
    .builder
    .config("spark.driver.extraClassPath", f"{SPARK_HOME}/jars/mysql-connector-j-8.4.0.jar") \
    .appName("MySQLExample")
    .getOrCreate())
```

`spark_db` 데이터베이스의 `users` 테이블의 데이터를 가져온다.
데이터를 출력해보면 앞에서 추가한 3개 행이 반환되는 것을 볼 수 있다.

```python
df = spark.read.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .load()
df.show()
```

```sql
+---+----+-------------------+
| id|name|         created_at|
+---+----+-------------------+
|  1| kim|2025-07-12 12:08:41|
|  2| lee|2025-07-12 12:08:45|
|  3|park|2025-07-12 12:08:48|
+---+----+-------------------+
```

### MySQL 데이터 쓰기

반대로 DataFrame을 MySQL에 새로운 테이블로 저장할 수도 있다.

```python
df.write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "new_users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .save()
```

MySQL에서 새로운 테이블을 조회했을 때 동일한 데이터가 저장된 것을 볼 수 있다.

```sql
mysql> SELECT * FROM new_users;
+------+------+---------------------+
| id   | name | created_at          |
+------+------+---------------------+
|    1 | kim  | 2025-07-12 12:08:41 |
|    2 | lee  | 2025-07-12 12:08:45 |
|    3 | park | 2025-07-12 12:08:48 |
+------+------+---------------------+
3 rows in set (0.00 sec)
```

또한, 기존 테이블에 새로운 행으로 추가할 수도 있다.

```python
df.select("name").write.format("jdbc") \
    .option("url", "jdbc:mysql://localhost:3306/spark_db") \
    .option("dbtable", "users") \
    .option("user", "spark") \
    .option("password", "spark") \
    .mode("append") \
    .save()
```

스파크의 DataFrameWriter를 통해 `users` 테이블에 새로운 행을 추가하고 데이터를 조회하면
아래와 같이 3개의 행이 더 추가된 것을 볼 수 있다.

```sql
mysql> SELECT * FROM users;
+----+------+---------------------+
| id | name | created_at          |
+----+------+---------------------+
|  1 | kim  | 2025-07-12 12:08:41 |
|  2 | lee  | 2025-07-12 12:08:45 |
|  3 | park | 2025-07-12 12:08:48 |
|  4 | kim  | 2025-07-12 12:24:29 |
|  5 | lee  | 2025-07-12 12:24:29 |
|  6 | park | 2025-07-12 12:24:29 |
+----+------+---------------------+
6 rows in set (0.00 sec)
```

## References

- [https://spark.apache.org/docs/latest/sql-distributed-sql-engine-spark-sql-cli.html](https://spark.apache.org/docs/latest/sql-distributed-sql-engine-spark-sql-cli.html)
- [https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html](https://spark.apache.org/docs/latest/sql-data-sources-hive-tables.html)
- [https://spidyweb.tistory.com/215](https://spidyweb.tistory.com/215)
- [https://dlcdn.apache.org/hive/hive-4.0.1/](https://dlcdn.apache.org/hive/hive-4.0.1/)
- [https://kevin717.tistory.com/50](https://kevin717.tistory.com/50)
- [https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)
- [https://jdbc.postgresql.org/download/](https://jdbc.postgresql.org/download/)
- [https://downloads.mysql.com/archives/c-j/](https://downloads.mysql.com/archives/c-j/)
