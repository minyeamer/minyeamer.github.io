---
layout: post
title: "[AI SCHOOL 5기] SQL 프로그래밍 실습 - SQL CRUD"
date: 2022-04-11 20:11:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, DB, SQL]
slug: aischool-05-02-sql-crud
---

# SELECT

```sql
SELECT 10 / 5, 2 * 4;
```

```sql
SELECT trackid, name FROM tracks;
```

```sql
SELECT * FROM tracks;
```

---

# INSERT

```sql
INSERT INTO artists (name) VALUES('Bud Powell');
```

```python
script = """
INSERT INTO artists (name) VALUES ("?");
"""

data = [
    ("Buddy Rich"),
    ("Candido"),
    ("Charlie Byrd")
]

cur.executemany(script, data)
```

```sql
SELECT
    ArtistId,
    Name
FROM
    Artists
ORDER BY
    ArtistId DESC;
```

---

# UPDATE

```sql
UPDATE employees SET lastname = 'Smith' WHERE employeeid = 3;
```

```sql
UPDATE employees
SET city = 'Toronto', 
    state = 'ON',
    postalcode = 'M5P 2N7'
WHERE
    employeeid = 4;
```

```sql
UPDATE employees
SET email = UPPER(firstname || "." || lastname || "@corp.co.kr");
```

---

# Sorting

```sql
SELECT 
    TrackId, 
    Name, 
    Composer 
FROM 
   tracks
ORDER BY 
   Composer;
```

- NULL Data인 `None`은 SQLite3에서 가장 작은 값으로 인식

---

# Filtering

![filter](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/05-sql-programming/02-sql-crud/filter.png?raw=true)

## DISTINCT

```sql
SELECT DISTINCT city FROM customers;
```

- NULL을 포함한 중복값을 하나만 남기고 제외

```sql
SELECT DISTINCT city, country FROM customers;
```

- 2개 열의 값이 모두 동일한 행들을 제외

## WHERE

![where](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/05-sql-programming/02-sql-crud/where.png?raw=true)

```sql
SELECT
   name,
   milliseconds,
   bytes,
   albumid
FROM
   tracks
WHERE
   (albumid = 10) AND (milliseconds > 250000);
```

## WHERE & LIKE

![wildcard](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/05-sql-programming/02-sql-crud/wildcard.png?raw=true)

```sql
SELECT
    trackid,
    name
FROM
    tracks
WHERE
    name LIKE 'Wild%';
```

## WHERE & IN

```sql
SELECT
    TrackId,
    Name,
    MediaTypeId
FROM
    Tracks
WHERE
    MediaTypeId IN (1, 2)
```

## WHERE & LIMIT/OFFSET

```sql
SELECT
    trackId,
    name
FROM
    tracks
LIMIT 10 OFFSET 7;
```
- `LIMIT`: 불러오는 값의 수
- `OFFSET`: OFFSET에 해당하는 수만큼 떼어내 그 이후의 데이터 불러옴

## WHERE & BETWEEN

```sql
SELECT
    InvoiceId,
    BillingAddress,
    Total
FROM
    invoices
WHERE
    Total BETWEEN 14.91 AND 18.86
ORDER BY
    Total; 
```

## WHERE & IS NULL

```sql
SELECT
    Name, 
    Composer
FROM
    tracks
WHERE
    Composer IS NULL
ORDER BY 
    Name; 
```
