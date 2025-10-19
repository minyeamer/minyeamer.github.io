---
layout: post
title: "[AI SCHOOL 5기] SQL 프로그래밍 실습 - SQLite3"
date: 2022-04-11 19:52:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, DB, SQL]
slug: aischool-05-01-sqlite3
---

# Connect SQLite3

```python
import sqlite3

dbpath = "maindb.db"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()
```

- `connnect()`: DBMS와 연결
- `conn.commit()`: 현재 변경사항 저장
- `conn.rollback()`: 마지막 commit 시점으로 되돌리기
- `cursor()`: DB에서 SQL문을 실행하는 객체

---

# Execute Scripts

## Datatypes
- **NULL**: 결측치
- **INTEGER (or INT)**: 정수 (양수 또는 음수), int 값
- **REAL**: 실수, float 값
- **TEXT (or VARCHAR)**: 텍스트, string 값
- **BLOB**: 모든 종류의 파일을 저장하는 바이너리 객체

## Scripts
- DROP TABLE IF EXISTS: 테이블이 이미 있으면 제거
- CREATE TABLE: 테이블 생성
- AUTOINCREMENT: 값을 따로 입력하지 않으면 자동 증가 숫자 부여
- NOT NULL: 빈 값이 저장되는 것을 허용하지 않음
- INSERT INTO TABLE(FIELD, ...) VALUES(VALUE, ...):   
  테이블에 데이터 추가, 전체 필드에 값 추가 시 필드명 생략 가능
- `--`: 한 줄 주석, `/* ... */`: 여러 줄 주석

## Excecute
- `conn.executescript()`: 스크립트 구문 실행
- `cur.executemany()`: 많은 데이터를 한번에 INSERT/UPDATE/DELETE   
  `("INSERT INTO ... VALUES(?, ?, ?, ?, ?);", date)`
- `cur.execute()`: 하나의 SQL문 실행
- `cur.fetchall()`: SQL문 실행 결과를 모두 반환 (튜플 형태)
- `cur.description`: 테이블 정보
- `conn.close()`: DB 연결 해제

## To Dataframe
- `pd.read_sql_query(query, conn)`

---

# CREATE Table

```sql
CREATE TABLE devices (
   name TEXT NOT NULL,
   model TEXT NOT NULL,
   Serial INTEGER NOT NULL UNIQUE
```

```sql
CREATE TABLE contact_groups(
   contact_id INTEGER,
   group_id INTEGER,
   PRIMARY KEY (contact_id, group_id), 
   FOREIGN KEY (contact_id) 
      REFERENCES contacts(contact_id)
         ON DELETE CASCADE,
   FOREIGN KEY (group_id) 
      REFERENCES groups(group_id)
         ON DELETE CASCADE
);
```

- CASCADE: css cascade와 동일

---

# ALTER Table

```sql
ALTER TABLE devices RENAME TO equipment;
```

```sql
ALTER TABLE equipment 
ADD COLUMN location text;
```

```sql
ALTER TABLE equipment 
RENAME COLUMN location TO loc;
```

---

# DROP Table

```sql
DROP TABLE equipment ;
```

- Pandas로 삭제된 테이블 요청 시 `no such table` 에러 발생

---

# DB 내 테이블 목록/구조 확인

```sql
SELECT 
    name
FROM 
    sqlite_master 
WHERE
    type ='table' AND 
    name NOT LIKE 'sqlite_%'; 
```

- sqlite_master는 기본적으로 생성되는 테이블
- sqlite_master 테이블에서 생성된 모든 테이블 목록/구조 확인 가능

![sqllite-master](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/05-sql-programming/01-sqlite3/sqllite-master.png?raw=true)