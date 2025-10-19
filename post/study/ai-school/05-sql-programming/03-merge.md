---
layout: post
title: "[AI SCHOOL 5기] SQL 프로그래밍 실습 - Merge"
date: 2022-04-11 20:20:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, DB, SQL]
slug: aischool-05-03-merge
---

# INNER JOIN

```sql
SELECT 
    l.Title,
    r.Name
FROM 
    albums AS l
INNER JOIN
    artists AS r
ON 
    r.ArtistId = l.ArtistId;
```

```sql
SELECT
   Title, 
   Name
FROM
   albums
INNER JOIN artists USING(ArtistId);
```

---

# LEFT JOIN

```sql
SELECT
    Name, 
    Title
FROM
    artists
LEFT JOIN albums ON artists.ArtistId = albums.ArtistId
ORDER BY 
    Name;
```

## SELF JOIN

```sql
SELECT m.firstname || ' ' || m.lastname AS 'Manager',
       e.firstname || ' ' || e.lastname AS 'Receives reports from'
FROM
    employees e
INNER JOIN 
    employees m 
ON 
    m.employeeid = e.reportsto
ORDER BY 
    manager;
```

- 'A 테이블'과 A 테이블의 복사본인 'B 테이블'을 합치기

---

# Grouping Data

![agg-func](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/05-sql-programming/03-merge/agg-func.png?raw=true)

```sql
SELECT
    albumid,
    COUNT(trackid)
FROM
    tracks
GROUP BY
    albumid
ORDER BY 
    COUNT(trackid) DESC;
```

```sql
SELECT
    albumid,
    COUNT(trackid)
FROM
    tracks
GROUP BY
    albumid
HAVING
    albumid = 1;
```

```sql
SELECT
    albumid,
    COUNT(trackid)
FROM
    tracks
WHERE
    COUNT(trackid) BETWEEN 18 AND 20
GROUP BY
    albumid;
```

- **에러발생**: `WHERE`문에는 집계함수 사용 불가   
- `WHERE`가 집계함수보다 우선적으로 실행되기 때문

```sql
SELECT
    tracks.albumid,
    title,
    MIN(tracks.milliseconds),
    MAX(tracks.milliseconds),
    ROUND(AVG(tracks.milliseconds), 2)
FROM
    tracks
INNER JOIN albums ON albums.albumid = tracks.albumid
GROUP BY
    tracks.albumid;
```

- `ROUND`는 n번째 자리까지 나타나도록 반올림

---

# Subquery

```sql
SELECT AVG(SUM(bytes))
FROM tracks
GROUP BY albumid;
```

- SELECT 문에서 집계함수의 결과 값에 바로 중첩하여 집계함수 적용 불가

```sql
SELECT
    AVG(SIZE)
FROM
    (SELECT
         SUM(bytes) AS SIZE
     FROM
         tracks
     GROUP BY
         albumid);
```