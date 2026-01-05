---
title: "프로그래머스 SQL Lv.4, 5 완전 정복 - 20문제 상세 풀이 (JOIN, GROUP BY, 윈도우 함수)"
date: "2025-07-03T23:15:02+09:00"
layout: "post"
description: >
  이직 준비를 하면서 오랜만에 코딩테스트를 보게되었는데,
  SQL 코딩테스트는 어떻게 나오나 궁금해서 프로그래머스 Lv.4, 5 수준의 문제를 모두 풀어보았습니다.
  표에서 제목을 클릭하면 프로그래머스 문제 풀이로 이동합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/3090p904jp5tkidn1l398/programmers-cover.webp?rlkey=yvpp7t47lzzxm8lgsjfdgdeby&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/nrqqo3iyw68si0zamyqey/programmers-logo.webp?rlkey=emibt2grzxs1ra3bla48pe6r8&raw=1"
categories: ["Algorithm", "SQL"]
tags: ["프로그래머스", "알고리즘", "코딩테스트", "SQL", "JOIN", "GROUP BY", "SELECT", "프로그래머스 Lv4", "프로그래머스 Lv5", "알고리즘 문제풀이"]
---

이직 준비를 하면서 오랜만에 코딩테스트를 보게되었는데,
SQL 코딩테스트는 어떻게 나오나 궁금해서 프로그래머스 Lv.4, 5 수준의 문제를 모두 풀어보았습니다.

## 모든 문제

표에서 ID를 클릭하면 프로그래머스 문제 풀이로 이동합니다.
문제는 최신순으로 정렬되어 있는데 풀이 순서는 표에서 역순으로, 즉 오래된순으로 나열합니다.

문제를 순서대로 풀어보면 유사한 데이터를 사용하는 경우가 있어 비슷한건 큰 제목으로 묶었습니다.
테이블 구조는 생략하고 `문제 요약 > 문제 해석 + 풀이 > SQL문` 순서로 구성합니다.

{{% data-table delimiter="|" align-center="1,4,5,6,7" %}}
ID|제목|유형|난이도|정답률|문제풀기|풀이보기
301651|멸종위기의 대장균 찾기|SELECT|Lv.5|21%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/301651)|[링크](#멸종위기의-대장균-찾기)
301650|특정 세대의 대장균 찾기|SELECT|Lv.4|61%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/301650)|[링크](#특정-세대의-대장균-찾기)
284528|연간 평가점수에 해당하는 평가 등급 및 성과금 조회하기|GROUP BY|Lv.4|72%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/284528)|[링크](#연간-평가점수에-해당하는-평가-등급-및-성과금-조회하기)
276036|언어별 개발자 분류하기|GROUP BY|Lv.4|41%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/276036)|[링크](#언어별-개발자-분류하기)
276035|FrontEnd 개발자 찾기|JOIN|Lv.4|51%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/276035)|[링크](#frontend-개발자-찾기)
157339|특정 기간동안 대여 가능한 자동차들의 대여비용 구하기|JOIN|Lv.4|49%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/157339)|[링크](#특정-기간동안-대여-가능한-자동차들의-대여비용-구하기)
151141|자동차 대여 기록 별 대여 금액 구하기|String, Date|Lv.4|51%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/151141)|[링크](#자동차-대여-기록-별-대여-금액-구하기)
144856|저자 별 카테고리 별 매출액 집계하기|GROUP BY|Lv.4|76%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/144856)|[링크](#저자-별-카테고리-별-매출액-집계하기)
133027|주문량이 많은 아이스크림들 조회하기|JOIN|Lv.4|74%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/133027)|[링크](#주문량이-많은-아이스크림들-조회하기)
132204|취소되지 않은 진료 예약 조회하기|String, Date|Lv.4|79%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/132204)|[링크](#취소되지-않은-진료-예약-조회하기)
131537|오프라인/온라인 판매 데이터 통합하기|SELECT|Lv.4|67%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131537)|[링크](#오프라인/온라인-판매-데이터-통합하기)
131534|상품을 구매한 회원 비율 구하기|JOIN|Lv.5|46%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131534)|[링크](#상품을-구매한-회원-비율-구하기)
131532|년, 월, 성별 별 상품 구매 회원 수 구하기|GROUP BY|Lv.4|75%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131532)|[링크](#년,-월,-성별-별-상품-구매-회원-수-구하기)
131124|그룹별 조건에 맞는 식당 목록 출력하기|JOIN|Lv.4|71%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131124)|[링크](#그룹별-조건에-맞는-식당-목록-출력하기)
131118|서울에 위치한 식당 목록 출력하기|SELECT|Lv.4|75%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131118)|[링크](#서울에-위치한-식당-목록-출력하기)
131117|5월 식품들의 총매출 조회하기|JOIN|Lv.4|84%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131117)|[링크](#5월-식품들의-총매출-조회하기)
131116|식품분류별 가장 비싼 식품의 정보 조회하기|GROUP BY|Lv.4|85%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/131116)|[링크](#식품분류별-가장-비싼-식품의-정보-조회하기)
62284|우유와 요거트가 담긴 장바구니|GROUP BY|Lv.4|74%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/62284)|[링크](#우유와-요거트가-담긴-장바구니)
59413|입양 시각 구하기(2)|GROUP BY|Lv.4|61%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/59413)|[링크](#입양-시각-구하기(2))
59045|보호소에서 중성화한 동물|JOIN|Lv.4|85%|[링크](https://school.programmers.co.kr/learn/courses/30/lessons/59045)|[링크](#보호소에서-중성화한-동물)
{{% /data-table %}}

## 동물 입양 테이블

### [보호소에서 중성화한 동물](https://school.programmers.co.kr/learn/courses/30/lessons/59045)

> `ANIMAL_INS` 테이블은 동물 보호소에 들어온 동물의 정보를 담은 테이블입니다.
> `ANIMAL_OUTS` 테이블은 동물 보호소에서 입양 보낸 동물의 정보를 담은 테이블입니다.
>
> 보호소에서 중성화 수술을 거친 동물 정보를 알아보려 합니다. 보호소에 들어올 당시에는 중성화되지 않았지만,
> 보호소를 나갈 당시에는 중성화된 동물의 아이디와 생물 종, 이름을 조회하는 아이디 순으로 조회하는 SQL 문을 작성해주세요.

보호소에 들어올 당시에 대한 테이블 `ANIMAL_INS` 에서 특정 조건만 선택하고,
보호소를 나갈 당시에 대한 테이블 `ANIMAL_OUTS` 에서 특정 조건만 선택해서,
두 테이블을 `INNER JOIN` 하여 두 조건을 만족하는 경우만 선택하는 문제입니다.

`ANIMAL_INS` 테이블에서는 중성화되지 않은 조건인, 성별 및 중성화 여부(`SEX_UPON_INTAKE`)에
"Intact" 단어가 포함된 경우를 선택하면 됩니다.
중성화 여부를 나타내는 단어는 앞에 있기 때문에 `LIKE 'Intact%'` 조건식을 사용했습니다.

`ANIMAL_OUTS` 테이블에서는 중성화된 조건인, 성별 및 중성화 여부(`SEX_UPON_INTAKE`)에
"Spayed" 또는 "Neutered" 단어가 포함된 경우를 선택하면 됩니다.
너무 길게 쓰는건 좋아하지 않아서 정규표현식을 활용하여 `REGEXP '^Spayed|Neutered'` 로 표현했습니다.

```sql
SELECT INS.ANIMAL_ID, INS.ANIMAL_TYPE, INS.NAME
FROM ANIMAL_INS AS INS
    INNER JOIN ANIMAL_OUTS AS OUTS
        ON INS.ANIMAL_ID = OUTS.ANIMAL_ID
WHERE INS.SEX_UPON_INTAKE LIKE 'Intact%'
    AND OUTS.SEX_UPON_OUTCOME REGEXP '^Spayed|Neutered'
ORDER BY ANIMAL_ID;
```

### [입양 시각 구하기(2)](https://school.programmers.co.kr/learn/courses/30/lessons/59413)

> `ANIMAL_OUTS` 테이블은 동물 보호소에서 입양 보낸 동물의 정보를 담은 테이블입니다.
>
> 보호소에서는 몇 시에 입양이 가장 활발하게 일어나는지 알아보려 합니다. 0시부터 23시까지,
> 각 시간대별로 입양이 몇 건이나 발생했는지 조회하는 SQL문을 작성해주세요. 이때 결과는 시간대 순으로 정렬해야 합니다.

입양일(`DATETIME`)에서 시간만 추출하고, 추출한 값을 기준으로 COUNT 집계하는 문제입니다.

주의할 점은, 0시부터 23시까지 모든 행이 존재해야 합니다. `ANIMAL_OUTS` 테이블에
모든 시간대가 있지 않기 때문에 0시부터 23시까지 값을 가지는 테이블을 만들어야 합니다.

잘 안써본 구문이라 찾아봤는데 `RECURSIVE` 라는 재귀적 쿼리를 활용하면 간단하게 해결될 것 같았습니다.
재귀적 쿼리를 사용한 `HOURS` 임시 테이블을 생성하고, 여기에 `ANIMAL_OUTS` 테이블을 COUNT 집계한
`COUNTS` 임시 테이블을 `LEFT JOIN` 으로 붙여서 모든 시간대를 표시했습니다.

```sql
WITH RECURSIVE HOURS AS (
    SELECT 0 AS HOUR
    UNION ALL
    SELECT HOUR + 1 FROM HOURS WHERE HOUR < 23
),

COUNTS AS (
    SELECT HOUR(DATETIME) AS HOUR, COUNT(ANIMAL_ID) AS COUNT
    FROM ANIMAL_OUTS
    GROUP BY HOUR
)

SELECT HR.HOUR, COALESCE(CNT.COUNT, 0) AS COUNT
FROM HOURS AS HR
    LEFT JOIN COUNTS AS CNT
        ON HR.HOUR = CNT.HOUR
ORDER BY HOUR;
```

## 식품 테이블

### [우유와 요거트가 담긴 장바구니](https://school.programmers.co.kr/learn/courses/30/lessons/62284)

> `CART_PRODUCTS` 테이블은 장바구니에 담긴 상품 정보를 담은 테이블입니다.
>
> 데이터 분석 팀에서는 우유(Milk)와 요거트(Yogurt)를 동시에 구입한 장바구니가 있는지 알아보려 합니다.
> 우유와 요거트를 동시에 구입한 장바구니의 아이디를 조회하는 SQL 문을 작성해주세요.
> 이때 결과는 장바구니의 아이디 순으로 나와야 합니다.

장바구니의 아이디(`CART_ID`) 그룹으로 집계하면서, 상품 종류(`NAME`) 에
"Milk"가 있는 경우와 "Yogurt"가 있는 경우를 모두 만족하는 아이디만 선택하는 문제입니다.

자주 쓰는 Python에서는 Boolean 타입의 `True` / `False` 를 각각 정수 1과 0으로 인식할 수 있는데,
SQL도 그렇지 않을까 싶어서 SUM 집계해봤습니다.
두 가지 조건에 대해 SUM 집계 결과가 1 이상인 경우만 선택해서 아이디만 조회했습니다.

```sql
WITH COUNTS AS (
    SELECT CART_ID, SUM(NAME = "Milk") AS MILK_COUNT, SUM(NAME = "Yogurt") AS YOG_COUNT
    FROM CART_PRODUCTS
    GROUP BY CART_ID
)

SELECT CART_ID
FROM COUNTS
WHERE MILK_COUNT > 0 AND YOG_COUNT > 0
ORDER BY CART_ID;
```

### [식품분류별 가장 비싼 식품의 정보 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/131116)

> `FOOD_PRODUCT` 테이블은 식품의 정보를 담은 테이블입니다.
>
> `FOOD_PRODUCT` 테이블에서 식품분류별로 가격이 제일 비싼 식품의 분류, 가격,
> 이름을 조회하는 SQL문을 작성해주세요. 이때 식품분류가 '과자', '국', '김치', '식용유'인 경우만
> 출력시켜 주시고 결과는 식품 가격을 기준으로 내림차순 정렬해주세요.

식품분류(`CATEGORY`) 그룹에서 가격(`PRICE`)이 가장 큰 항목만 선택하는 문제입니다.

가격(`PRICE`)이 MAX 집계 결과와 동일한 항목만 선택하는 경우도 있지만, 더 간단하게 WINDOW 함수를 사용했습니다.
식품분류(`CATEGORY`) 파티션에 대해 가격(`PRICE`)을 내림차순으로 정렬한
순번(`ROW_NUMBER`)이 1인 경우만 선택하면 동일한 결과를 조회할 수 있습니다.

```sql
WITH HIGHEST AS (
    SELECT PRODUCT_ID,
            ROW_NUMBER() OVER (PARTITION BY CATEGORY ORDER BY PRICE DESC) AS SEQ
    FROM FOOD_PRODUCT
    WHERE CATEGORY IN ("과자","국","김치","식용유")
)

SELECT PRD.CATEGORY, PRD.PRICE AS MAX_PRICE, PRD.PRODUCT_NAME
FROM FOOD_PRODUCT AS PRD
    INNER JOIN (SELECT * FROM HIGHEST WHERE SEQ = 1) AS HGT
        ON PRD.PRODUCT_ID = HGT.PRODUCT_ID
ORDER BY MAX_PRICE DESC;
```

### [5월 식품들의 총매출 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/131117)

> `FOOD_PRODUCT` 테이블은 식품의 정보를 담은 테이블입니다.
> `FOOD_ORDER` 테이블은 식품의 주문 정보를 담은 테이블입니다.
>
> `FOOD_PRODUCT` 와 `FOOD_ORDER` 테이블에서 생산일자가 2022년 5월인 식품들의
> 식품 ID, 식품 이름, 총매출을 조회하는 SQL문을 작성해주세요. 이때 결과는 총매출을 기준으로
> 내림차순 정렬해주시고 총매출이 같다면 식품 ID를 기준으로 오름차순 정렬해주세요.

식품 ID(`PRODUCT_ID`) 그룹에 대해 총매출(`SUM(AMOUNT * PRICE)`)을 계산하는 문제입니다.

`JOIN` 을 먼저해서 매출(`AMOUNT * PRICE`)을 계산하고 SUM 집계하는 경우도 가능한데,
개인적으로는 `GROUP BY` 시에 식품 이름(`PRODUCT_NAME`)과 같은 긴 문자열을 포함하는 것을 선호하지 않습니다.

입고일(`PRODUCE_DATE`)에 따라 가격(`PRICE`)이 바뀌는 것도 아니기 때문에 `JOIN` 과 `GROUP BY` 의
순서를 신경쓸 필요도 없습니다. 물론, `FOOD_PRODUCT` 테이블에서 식품 ID(`PRODUCT_ID`)에 중복이 없음을 전제로 합니다.

따라서, 식품 ID(`PRODUCT_ID`)에 대해서 먼저 `GROUP BY` 하여 총주문량(`SUM(AMOUNT)`)을 계산하고,
가격(`PRICE`)을 나중에 곱해 총매출(`SUM(AMOUNT) * PRICE`)을 만들었습니다.

```sql
WITH AMOUNTS AS (
    SELECT PRODUCT_ID, SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM FOOD_ORDER
    WHERE PRODUCE_DATE BETWEEN '2022-05-01' AND '2022-05-31'
    GROUP BY PRODUCT_ID
)

SELECT AMT.PRODUCT_ID, PRD.PRODUCT_NAME,
        (AMT.TOTAL_AMOUNT * PRD.PRICE) AS TOTAL_SALES
FROM AMOUNTS AS AMT
    INNER JOIN FOOD_PRODUCT AS PRD
        ON AMT.PRODUCT_ID = PRD.PRODUCT_ID
ORDER BY TOTAL_SALES DESC, PRODUCT_ID ASC;
```

## 식당 테이블

### [서울에 위치한 식당 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131118)

> `REST_INFO` 테이블은 식당의 정보를 담은 테이블입니다.
> `REST_REVIEW` 테이블은 식당의 리뷰 정보를 담은 테이블입니다.
>
> `REST_INFO` 와 `REST_REVIEW` 테이블에서 서울에 위치한 식당들의
> 식당 ID, 식당 이름, 음식 종류, 즐겨찾기수, 주소, 리뷰 평균 점수를 조회하는 SQL문을 작성해주세요.
> 이때 리뷰 평균점수는 소수점 세 번째 자리에서 반올림 해주시고 결과는 평균점수를 기준으로 내림차순 정렬해주시고,
> 평균점수가 같다면 즐겨찾기수를 기준으로 내림차순 정렬해주세요.

`REST_REVIEW` 테이블에서 식당 ID(`REST_ID`) 그룹에 대해 리뷰 평균 점수(`AVG(REVIEW_SCORE)`)를 계산하고,
`REST_INFO` 테이블에 계산 결과를 결합하는 문제입니다.

`REST_INFO` 테이블을 조회하면 서울에 있는 식당은 전부 주소(`ADDRESS`)가 "서울"로 시작합니다.
정렬 기준만 맞춰서 조회하면 정답을 도출할 수 있습니다.

```sql
WITH REVIEWS AS (
    SELECT REST_ID, ROUND(AVG(REVIEW_SCORE),2) AS SCORE
    FROM REST_REVIEW
    GROUP BY REST_ID
)

SELECT INFO.REST_ID, INFO.REST_NAME, INFO.FOOD_TYPE, INFO.FAVORITES, INFO.ADDRESS, RVW.SCORE
FROM REST_INFO AS INFO
    INNER JOIN REVIEWS AS RVW
        ON INFO.REST_ID = RVW.REST_ID
WHERE INFO.ADDRESS LIKE "서울%"
ORDER BY SCORE DESC, FAVORITES DESC;
```

### [그룹별 조건에 맞는 식당 목록 출력하기](https://school.programmers.co.kr/learn/courses/30/lessons/131124)

> `MEMBER_PROFILE` 테이블은 고객의 정보를 담은 테이블입니다.
> `REST_REVIEW` 테이블은 식당의 리뷰 정보를 담은 테이블입니다.
>
> `MEMBER_PROFILE` 와 `REST_REVIEW` 테이블에서 리뷰를 가장 많이 작성한 회원의 리뷰들을 조회하는 SQL문을 작성해주세요.
> 회원 이름, 리뷰 텍스트, 리뷰 작성일이 출력되도록 작성해주시고, 결과는 리뷰 작성일을 기준으로
> 오름차순, 리뷰 작성일이 같다면 리뷰 텍스트를 기준으로 오름차순 정렬해주세요.

`REST_REVIEW` 테이블에서 리뷰 수(`COUNT(REVIEW_ID)`)가 가장 큰 회원 ID(`MEMBER_ID`)에 대한 리뷰 목록을 조회하는 문제입니다.

회원 ID(`MEMBER_ID`) 그룹별 리뷰 수(`COUNT(REVIEW_ID)`)를 계산하고,
내림차순 정렬하여 첫 번째 항목만 조회하여 리뷰를 가장 많이 작성한 회원을 구합니다.

해당 회원 ID(`MEMBER_ID`)에 대한 `REST_REVIEW` 항목을 모두 조회하면서,
`MEMBER_PROFILE` 테이블을 결합해 회원 이름(`MEMBER_NAME`)을 같이 표시합니다.
DATE 타입의 리뷰 작성일(`REVIEW_DATE`)은 그대로 출력하면 안되고 `%Y-%m-%d` 날짜 포맷팅을 해야합니다.

```sql
WITH BEST_MEMBER AS (
    SELECT MEMBER_ID, COUNT(REVIEW_ID) AS REVIEW_COUNT
    FROM REST_REVIEW
    GROUP BY MEMBER_ID
    ORDER BY REVIEW_COUNT DESC LIMIT 1
)

SELECT MEM.MEMBER_NAME, RVW.REVIEW_TEXT,
        DATE_FORMAT(RVW.REVIEW_DATE, '%Y-%m-%d') AS REVIEW_DATE
FROM REST_REVIEW AS RVW
    INNER JOIN BEST_MEMBER AS BST
        ON RVW.MEMBER_ID = BST.MEMBER_ID
    INNER JOIN MEMBER_PROFILE AS MEM
        ON RVW.MEMBER_ID = MEM.MEMBER_ID
ORDER BY REVIEW_DATE;
```

## 쇼핑몰 테이블

### [년, 월, 성별 별 상품 구매 회원 수 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131532)

> `USER_INFO` 테이블은 의류 쇼핑몰에 가입한 회원 정보를 담은 테이블입니다.
> `ONLINE_SALE` 테이블은 온라인 상품 판매 정보를 담은 테이블입니다.
>
> `USER_INFO` 테이블과 `ONLINE_SALE` 테이블에서 년, 월, 성별 별로 상품을 구매한 회원수를
> 집계하는 SQL문을 작성해주세요. 결과는 년, 월, 성별을 기준으로 오름차순 정렬해주세요.
> 이때, 성별 정보가 없는 경우 결과에서 제외해주세요.

두 테이블을 `INNER JOIN` 하면서 성별(`GENDER`)이 있는(`IS NOT NULL`) 경우만 선택합니다.

판매일(`SALES_DATE`)에서 각각 연도(`YEAR`), 월(`MONTH`)을 추출하고,
성별(`GENDER`)과 함께 세 가지 기준에 대해 `GROUP BY` 합니다.
그룹 내에서 중복 없는 회원 ID(`DISTINCT USER_ID`)를 COUNT 집계해 회원수를 계산합니다.

```sql
SELECT EXTRACT(YEAR FROM SALES.SALES_DATE) AS YEAR,
        EXTRACT(MONTH FROM SALES.SALES_DATE) AS MONTH,
        USR.GENDER,
        COUNT(DISTINCT SALES.USER_ID) AS USERS
FROM ONLINE_SALE AS SALES
    INNER JOIN USER_INFO AS USR
        ON SALES.USER_ID = USR.USER_ID
WHERE USR.GENDER IS NOT NULL
GROUP BY YEAR, MONTH, GENDER
ORDER BY YEAR, MONTH, GENDER;
```

### [상품을 구매한 회원 비율 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/131534)

> `USER_INFO` 테이블은 의류 쇼핑몰에 가입한 회원 정보를 담은 테이블입니다.
> `ONLINE_SALE` 테이블은 온라인 상품 판매 정보를 담은 테이블입니다.
>
> `USER_INFO` 테이블과 `ONLINE_SALE` 테이블에서 2021년에 가입한 전체 회원들 중 상품을 구매한 회원수와
> 상품을 구매한 회원의 비율(=2021년에 가입한 회원 중 상품을 구매한 회원수 / 2021년에 가입한 전체 회원 수)을
> 년, 월 별로 출력하는 SQL문을 작성해주세요. 상품을 구매한 회원의 비율은 소수점 두번째자리에서 반올림하고,
> 전체 결과는 년을 기준으로 오름차순 정렬해주시고 년이 같다면 월을 기준으로 오름차순 정렬해주세요.

2021년에 가입한 회원수와, 그중에서 상품을 구매한 회원수를 집계해 그 비율을 계산하는 문제입니다.

우선, 대상을 2021년에 가입한 회원으로 좁히기 위해 `USER_INFO` 에서 가입일(`JOINED`)의 연도가
2021인 항목만 선택한 `TARGET_USERS` 임시 테이블 결과를 `ONLINE_SALE` 에 `INNER JOIN` 으로 연결합니다.

가입일(`JOINED`)에서 연도(`YEAR`) 와 월(`MONTH`)을 추출하고, 두 가지 기준에 대해 `GROUP BY` 합니다.
그룹 내에서 중복 없는 회원 ID(`DISTINCT USER_ID`)를 COUNT 집계해 회원수를 계산하는데,
이때 판매량(`SALES_AMOUNT`)이 1 이상인, 즉 상품을 구매한 회원 ID만 고려합니다.
조건에 맞지 않는 회원 ID는 `NULL` 로 바꿔서 COUNT 집계에서 제외했습니다.

이렇게 계산한 `PURCHASED_USERS` 값을 분자로, 회원 ID(`USER_ID`)를 COUNT 집계한 값을
분모로 하여 상품을 구매한 회원의 비율(`PURCHASED_RATIO`)을 계산합니다.

```sql
WITH TARGET_USERS AS (
    SELECT DISTINCT USER_ID
    FROM USER_INFO
    WHERE EXTRACT(YEAR FROM JOINED) = 2021
),

PURCHASED AS (
    SELECT EXTRACT(YEAR FROM SALES.SALES_DATE) AS YEAR,
            EXTRACT(MONTH FROM SALES.SALES_DATE) AS MONTH,
            COUNT(DISTINCT IF(SALES.SALES_AMOUNT > 0, USERS.USER_ID, NULL)) AS PURCHASED_USERS
    FROM ONLINE_SALE AS SALES
        INNER JOIN TARGET_USERS AS USERS
            ON SALES.USER_ID = USERS.USER_ID
    GROUP BY YEAR, MONTH
)

SELECT YEAR, MONTH, PURCHASED_USERS,
    ROUND(PURCHASED_USERS / (SELECT COUNT(USER_ID) FROM TARGET_USERS), 1) AS PUCHASED_RATIO
FROM PURCHASED
ORDER BY YEAR, MONTH;
```

### [오프라인/온라인 판매 데이터 통합하기](https://school.programmers.co.kr/learn/courses/30/lessons/131537)

> `ONLINE_SALE` 테이블은 온라인 상품 판매 정보를 담은 테이블입니다.
> `ONLINE_SALE` 테이블은 온라인 상품 판매 정보를 담은 테이블입니다.
>
> `ONLINE_SALE` 테이블과 `OFFLINE_SALE` 테이블에서 2022년 3월의 오프라인/온라인
> 상품 판매 데이터의 판매 날짜, 상품ID, 유저ID, 판매량을 출력하는 SQL문을 작성해주세요.
> `OFFLINE_SALE` 테이블의 판매 데이터의 `USER_ID` 값은 NULL 로 표시해주세요.
> 결과는 판매일을 기준으로 오름차순 정렬해주시고 판매일이 같다면 상품 ID를 기준으로
> 오름차순, 상품ID까지 같다면 유저 ID를 기준으로 오름차순 정렬해주세요.

두 테이블을 결과를 세로로 결합하고 정렬하는 문제입니다.

`ONLINE_SALE` 테이블은 판매일(`SALES_DATE`), 상품 ID(`PRODUCT_ID`), 회원 ID(`USER_ID`)
그룹별로 판매량(`SALES_AMOUNT`)을 SUM 집계했습니다. `GROUP BY` 하라는 지문이 없어 안해도 되었던 것 같은데
개인적으로 판매 데이터를 보면 버릇처럼 `GROUP BY` 하게 됩니다.

`OFFLINE_SALE` 테이블은 회원 ID(`USER_ID`)가 없지만, `UNION ALL` 연산을 위해 `ONLINE_SALE` 테이블과
구성을 맞춰줄 목적으로 `NULL` 값을 가지는 `USER_ID` 열을 추가합니다.

DATE 타입의 판매일(`REVIEW_DATE`)은 그대로 출력하면 안되고 `%Y-%m-%d` 날짜 포맷팅을 해야합니다.

```sql
SELECT DATE_FORMAT(TOTAL.SALES_DATE, '%Y-%m-%d') AS SALES_DATE,
    TOTAL.PRODUCT_ID,
    TOTAL.USER_ID,
    TOTAL.SALES_AMOUNT
FROM
(
    SELECT SALES_DATE, PRODUCT_ID, USER_ID, SUM(SALES_AMOUNT) AS SALES_AMOUNT
    FROM ONLINE_SALE
    WHERE SALES_DATE BETWEEN '2022-03-01' AND '2022-03-31'
    GROUP BY SALES_DATE, PRODUCT_ID, USER_ID
    
    UNION ALL
    
    SELECT SALES_DATE, PRODUCT_ID, NULL AS USER_ID, SUM(SALES_AMOUNT) AS SALES_AMOUNT
    FROM OFFLINE_SALE
    WHERE SALES_DATE BETWEEN '2022-03-01' AND '2022-03-31'
    GROUP BY SALES_DATE, PRODUCT_ID
) AS TOTAL
ORDER BY SALES_DATE, PRODUCT_ID, USER_ID;
```

## 진료 테이블

### [취소되지 않은 진료 예약 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/132204)

> `PATIENT` 테이블은 환자 정보를 담은 테이블입니다.
> `DOCTOR` 테이블은 의사 정보를 담은 테이블입니다.
> `APPOINTMENT` 테이블은 진료 예약목록을 담은 테이블입니다.
>
> `PATIENT`, `DOCTOR` 그리고 `APPOINTMENT` 테이블에서 2022년 4월 13일 취소되지 않은 흉부외과(CS)
> 진료 예약 내역을 조회하는 SQL문을 작성해주세요. 진료예약번호, 환자이름, 환자번호, 진료과코드, 의사이름, 진료예약일시 항목이
> 출력되도록 작성해주세요. 결과는 진료예약일시를 기준으로 오름차순 정렬해주세요.

세 개의 테이블에서 조건에 맞는 항목들만 선택해 결합하는 문제입니다.

`APPOINTMENT` 테이블에서는 진료 예약일시(`APNT_YMD`)가 '2022-04-13' 과 동일하고
예약취소여부(`APNT_CNCL_YN`)가 'N'에 해당하는 경우만 선택합니다.

`DOCTOR` 테이블에서는 진료과코드(`MCDP_CD`)가 'CS'에 해당하는 경우만 선택합니다.

`PATIENT` 테이블은 환자이름(`PT_NAME`)을 가져오기 위한 목적이며 따로 조건은 없습니다.

세 개의 테이블을 `INNER JOIN` 하여 조건을 결합하고 필요한 항목들을 출력합니다.

```sql
SELECT APP.APNT_NO,
        PAT.PT_NAME,
        APP.PT_NO,
        APP.MCDP_CD,
        DOC.DR_NAME,
        APP.APNT_YMD
FROM APPOINTMENT AS APP
    INNER JOIN DOCTOR AS DOC
        ON APP.MDDR_ID = DOC.DR_ID
    INNER JOIN PATIENT AS PAT
        ON APP.PT_NO = PAT.PT_NO
WHERE DATE_FORMAT(APP.APNT_YMD, '%Y-%m-%d') = '2022-04-13'
    AND APP.APNT_CNCL_YN = 'N'
    AND DOC.MCDP_CD = 'CS'
ORDER BY APNT_YMD
```

## 판매 테이블

### [주문량이 많은 아이스크림들 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/133027)

> `FIRST_HALF` 테이블은 아이스크림 가게의 상반기 주문 정보를 담은 테이블입니다.
> `JULY` 테이블은 7월의 아이스크림 주문 정보를 담은 테이블입니다.
>
> 7월 아이스크림 총 주문량과 상반기의 아이스크림 총 주문량을 더한 값이
> 큰 순서대로 상위 3개의 맛을 조회하는 SQL 문을 작성해주세요.

아이스크림 총주문량(`TOTAL_ORDER`)을 내림차순 정렬하여 상위 3개 항목만 조회하는 문제입니다.

구성이 동일한 `FIRST_HALF` 테이블과 `JULY` 테이블을 `UNION ALL` 결합하고
아이스크림 맛(`FLAVOR`) 그룹별로 아이스크림 총주문량(`TOTAL_ORDER`)을 SUM 집계합니다.

이때, 집계한 값을 출력할 필요는 없기 때문에 굳이 `SELECT` 하지는 않고 `ORDER BY` 구문에서
직접적으로 사용합니다. 집계한 값을 내림차순 정렬한 후 `LIMIT 3` 으로 상위 3개 항목만 조회합니다.

```sql
SELECT FLAVOR
FROM (
    SELECT * FROM FIRST_HALF
    UNION ALL
    SELECT * FROM JULY
) AS TOTAL
GROUP BY FLAVOR
ORDER BY SUM(TOTAL_ORDER) DESC
LIMIT 3
```

### [저자 별 카테고리 별 매출액 집계하기](https://school.programmers.co.kr/learn/courses/30/lessons/144856)

> `BOOK` 테이블은 각 도서의 정보를 담은 테이블입니다.
> `AUTHOR` 테이블은 도서의 저자의 정보를 담은 테이블입니다.
> `BOOK_SALES` 테이블은 각 도서의 날짜 별 판매량 정보를 담은 테이블입니다.
>
> `2022년 1월`의 도서 판매 데이터를 기준으로 저자 별, 카테고리 별
> 매출액(`TOTAL_SALES = 판매량 * 판매가`) 을 구하여, 저자 ID(`AUTHOR_ID`),
> 저자명(`AUTHOR_NAME`), 카테고리(`CATEGORY`), 매출액(`SALES`) 리스트를 출력하는 SQL문을 작성해주세요.
> 결과는 저자 ID를 오름차순으로, 저자 ID가 같다면 카테고리를 내림차순 정렬해주세요.

세 개의 테이블을 결합하고 제시된 그룹별 매출액을 계산하는 문제입니다.

`BOOK_SALES` 테이블에서 `BOOK_ID`, `AUTHOR_ID` 를 기준으로 각각 `BOOK`, `AUTHOR`
테이블과 `INNER JOIN` 합니다. `BOOK_SALES` 테이블의 판매량(`SALES`)과 `BOOK` 테이블의
판매가(`PRICE`)를 곱한 매출액을 SUM 집계하여 총매출액(`TOTAL_SALES`)을 계산합니다.

```sql
SELECT BK.AUTHOR_ID, AU.AUTHOR_NAME, BK.CATEGORY,
        SUM(SALES.SALES * BK.PRICE) AS TOTAL_SALES
FROM BOOK_SALES AS SALES
    INNER JOIN BOOK AS BK ON SALES.BOOK_ID = BK.BOOK_ID
    INNER JOIN AUTHOR AS AU ON BK.AUTHOR_ID = AU.AUTHOR_ID
WHERE SALES.SALES_DATE BETWEEN '2022-01-01' AND '2022-01-31'
GROUP BY AUTHOR_ID, AUTHOR_NAME, CATEGORY
ORDER BY AUTHOR_ID, CATEGORY DESC;
```

## 자동차 대여 테이블

### [자동차 대여 기록 별 대여 금액 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/151141)

> `CAR_RENTAL_COMPANY_CAR` 테이블은 대여 중인 자동차들의 정보를 담은 테이블입니다.
> `CAR_RENTAL_COMPANY_RENTAL_HISTORY` 테이블은 자동차 대여 기록 정보를 담은 테이블입니다.
> `CAR_RENTAL_COMPANY_DISCOUNT_PLAN` 테이블은 자동차 종류 별 대여 기간 종류 별 할인 정책 정보를 담은 테이블 입니다.
>
> `CAR_RENTAL_COMPANY_CAR` 테이블과 `CAR_RENTAL_COMPANY_RENTAL_HISTORY` 테이블과
> `CAR_RENTAL_COMPANY_DISCOUNT_PLAN` 테이블에서 자동차 종류가 '트럭'인 자동차의 대여 기록에 대해서
> 대여 기록 별로 대여 금액(컬럼명: `FEE`)을 구하여 대여 기록 ID와 대여 금액 리스트를 출력하는 SQL문을 작성해주세요.
> 결과는 대여 금액을 기준으로 내림차순 정렬하고, 대여 금액이 같은 경우 대여 기록 ID를 기준으로 내림차순 정렬해주세요.

세 개의 테이블을 결합하는데, 우선 대여 시작일(`START_DATE`)과 대여 종료일(`END_DATE`) 기간에 대한
날짜수를 기준으로 할인율 적용 기준을 분류합니다. 할인율 적용 기준을 통해 할인율(`DISCOUNT_RATE`)
수치를 도출하여 대여 금액(`FEE`)에 할인 적용을 하는 문제입니다. 

일수(`DAYS`)를 계산하는 방법으로 `DATEDIFF` 함수를 사용합니다. 시작일과 종료일도 기간에 포함되기 때문에
함수의 결과에 `+1` 을 더합니다. 일수(`DAYS`)에 대해 CASE 조건문을 통해 대여 기간 종류(`DURATION_TYPE`)에
해당하는 4가지 분류로 구분합니다. 대여 기간 종류(`DURATION_TYPE`)는 그대로 `LEFT JOIN` 의 기준으로써,
`CAR_RENTAL_COMPANY_DISCOUNT_PLAN` 테이블로부터 할인율(`DISCOUNT_RATE`)을 도출하는데 사용됩니다.

대여 금액(`FEE`)은 일일 대여 요금(`DAILY_FEE`)에 앞에서 구한 일수(`DAYS`)와
할인율(`DISCOUNT_RATE`)을 곱한 결과입니다. 이때, 정수 타입인 할인율(`DISCOUNT_RATE`)은
그대로 사용하지 않고, `1.0 - (할인율 / 100)` 계산식에 넣어 배율로 변환합니다.

```sql
WITH HISTORY AS (
    SELECT *, (DATEDIFF(END_DATE, START_DATE) + 1) AS DAYS
    FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
)

SELECT HIST.HISTORY_ID,
        ROUND(CAR.DAILY_FEE * HIST.DAYS * (1.0 - (IFNULL(DIS.DISCOUNT_RATE, 0) / 100))) AS FEE
FROM HISTORY AS HIST
    INNER JOIN CAR_RENTAL_COMPANY_CAR AS CAR
        ON HIST.CAR_ID = CAR.CAR_ID
    LEFT JOIN CAR_RENTAL_COMPANY_DISCOUNT_PLAN AS DIS
        ON DIS.CAR_TYPE = CAR.CAR_TYPE
            AND DIS.DURATION_TYPE = (
                CASE WHEN HIST.DAYS >= 90 THEN '90일 이상'
                    WHEN HIST.DAYS >= 30 THEN '30일 이상'
                    WHEN HIST.DAYS >= 7 THEN '7일 이상'
                    ELSE '7일 미만' END)
WHERE CAR.CAR_TYPE = '트럭'
ORDER BY FEE DESC, HISTORY_ID DESC
```

### [특정 기간동안 대여 가능한 자동차들의 대여비용 구하기](https://school.programmers.co.kr/learn/courses/30/lessons/157339)

> `CAR_RENTAL_COMPANY_CAR` 테이블은 대여 중인 자동차들의 정보를 담은 테이블입니다.
> `CAR_RENTAL_COMPANY_RENTAL_HISTORY` 테이블은 자동차 대여 기록 정보를 담은 테이블입니다.
> `CAR_RENTAL_COMPANY_DISCOUNT_PLAN` 테이블은 자동차 종류 별 대여 기간 종류 별 할인 정책 정보를 담은 테이블 입니다.
>
> `CAR_RENTAL_COMPANY_CAR` 테이블과 `CAR_RENTAL_COMPANY_RENTAL_HISTORY` 테이블과
> `CAR_RENTAL_COMPANY_DISCOUNT_PLAN` 테이블에서 자동차 종류가 '세단' 또는 'SUV' 인 자동차 중
> 2022년 11월 1일부터 2022년 11월 30일까지 대여 가능하고 30일간의 대여 금액이 50만원 이상 200만원 미만인
> 자동차에 대해서 자동차 ID, 자동차 종류, 대여 금액(컬럼명: `FEE`) 리스트를 출력하는 SQL문을 작성해주세요.
> 결과는 대여 금액을 기준으로 내림차순 정렬하고, 대여 금액이 같은 경우 자동차 종류를 기준으로 오름차순 정렬,
> 자동차 종류까지 같은 경우 자동차 ID를 기준으로 내림차순 정렬해주세요.

앞선 문제와 테이블 및 대여 금액(`FEE`) 계산 방법이 동일한데, 세부적인 조건이 늘어났습니다.

첫 번째 조건인 자동차 종류를 선택하는 것은 `CAR_RENTAL_COMPANY_CAR` 테이블에서
WHERE 절을 통해 자동차 종류(`CAR_TYPE`)가 '세단' 또는 'SUV'인 것만 선택하면 됩니다.

두 번째 조건인 2022년 11월 1일부터 2022년 11월 30일까지 대여 가능한 경우는
`CAR_RENTAL_COMPANY_RENTAL_HISTORY` 테이블에서 대여 시작일(`START_DATE`)과 대여 종료일(`END_DATE`)이
해당 기간에 걸치는 경우를 파악하고 대상 자동차 ID(`CAR_ID`)를 WHERE 절의 AND 조건으로 추가해 제외합니다.

세 번째 조건은 대여 금액(`FEE`)을 계산한 후, WHERE 절을 통해 50만원 이상 200만원 미만인 경우를 선택합니다.
`FEE >= (50 * 10000) AND FEE < (200 * 10000)` 조건을 적용할 수도 있지만,
상대적으로 길이가 짧은 `BETWEEN` 절로 표현했습니다. 대여 금액(`FEE`)은 소수점까지 떨어지지는
않기 때문에 `-1` 하여 미만(`<`)과 동일하게 표현할 수 있습니다.

```sql
WITH HISTORY AS (
    SELECT *, (DATEDIFF(END_DATE, START_DATE) + 1) AS DAYS
    FROM CAR_RENTAL_COMPANY_RENTAL_HISTORY
),

DISCOUNT_PLAN AS (
    SELECT CAR_TYPE, DURATION_TYPE,
            (1.0 - (DISCOUNT_RATE / 100)) AS DISCOUNT_RATE
    FROM CAR_RENTAL_COMPANY_DISCOUNT_PLAN
),

CAR_IN_USE AS (
    SELECT DISTINCT CAR_ID
    FROM HISTORY
    WHERE START_DATE <= '2022-11-30' AND END_DATE >= '2022-11-01'
),

CAR AS (
    SELECT CAR.CAR_ID, CAR.CAR_TYPE,
            ROUND(CAR.DAILY_FEE * 30 * IFNULL(DIS.DISCOUNT_RATE, 1.0)) AS FEE
    FROM CAR_RENTAL_COMPANY_CAR AS CAR
        LEFT JOIN DISCOUNT_PLAN AS DIS
            ON CAR.CAR_TYPE = DIS.CAR_TYPE
                AND DIS.DURATION_TYPE = '30일 이상'
    WHERE CAR.CAR_TYPE IN ('세단','SUV')
        AND CAR.CAR_ID NOT IN (SELECT CAR_ID FROM CAR_IN_USE)
)

SELECT CAR_ID, CAR_TYPE, FEE
FROM CAR
WHERE FEE BETWEEN (50 * 10000) AND (200 * 10000 - 1)
ORDER BY FEE DESC, CAR_TYPE ASC, CAR_ID DESC
```

## 개발자 스킬 테이블

### [FrontEnd 개발자 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/276035)

> `SKILLCODES` 테이블은 개발자들이 사용하는 프로그래밍 언어에 대한 정보를 담은 테이블입니다.
> `DEVELOPERS` 테이블은 개발자들의 프로그래밍 스킬 정보를 담은 테이블입니다.
>
> `DEVELOPERS` 테이블에서 Front End 스킬을 가진 개발자의 정보를 조회하려 합니다.
> 조건에 맞는 개발자의 ID, 이메일, 이름, 성을 조회하는 SQL 문을 작성해 주세요.
> 결과는 ID를 기준으로 오름차순 정렬해 주세요.

두 개의 테이블에서 정수 타입인 스킬 코드 열을 비트 연산하여 공통된 경우를 `JOIN` 하는 문제입니다.

`SKILLCODES` 테이블에서 스킬의 범주(`CATEGORY`)가 'Front End'에 해당하는 항목만 선택합니다.
해당 테이블의 스킬의 코드(`CODE`)는 2진수로 표현했을 때 각 비트마다 하나의 스킬에 대응됩니다.

`DEVELOPERS` 테이블에도 마찬가지로 개발자에 대한 스킬 코드(`SKILL_CODE`)가 있습니다.
두 개 테이블의 스킬 코드를 `&` 연산자를 활용해 비트 연산하면 공통된 비트만 얻을 수 있습니다.
이것이 `SKILLCODES` 테이블의 스킬의 코드(`CODE`)와 같다면 해당 스킬을 보유하고 있다고 판단할 수 있습니다.

'Front End' 스킬을 가진 개발자의 ID(`ID`)만 따로 추출하고,
`DEVELOPERS` 테이블에서 해당 `ID` 에 해당하는 항목들만 선택하여 조회합니다.

```sql
WITH TARGET AS (
    SELECT DISTINCT DEV.ID
    FROM DEVELOPERS AS DEV
        INNER JOIN SKILLCODES AS SKL
            ON (DEV.SKILL_CODE & SKL.CODE) = SKL.CODE
    WHERE SKL.CATEGORY = 'Front End'
)

SELECT ID, EMAIL, FIRST_NAME, LAST_NAME
FROM DEVELOPERS
    WHERE ID IN (SELECT ID FROM TARGET)
ORDER BY ID;
```

### [언어별 개발자 분류하기](https://school.programmers.co.kr/learn/courses/30/lessons/276036)

> `SKILLCODES` 테이블은 개발자들이 사용하는 프로그래밍 언어에 대한 정보를 담은 테이블입니다.
> `DEVELOPERS` 테이블은 개발자들의 프로그래밍 스킬 정보를 담은 테이블입니다.
>
> `DEVELOPERS` 테이블에서 GRADE별 개발자의 정보를 조회하려 합니다. GRADE는 다음과 같이 정해집니다.
>
> - A : Front End 스킬과 Python 스킬을 함께 가지고 있는 개발자
> - B : C# 스킬을 가진 개발자
> - C : 그 외의 Front End 개발자
>
> GRADE가 존재하는 개발자의 GRADE, ID, EMAIL을 조회하는 SQL 문을 작성해 주세요.
> 결과는 GRADE와 ID를 기준으로 오름차순 정렬해 주세요.

앞선 문제와, 테이블 및 스킬 코드를 비트 연산하여 개발자가 스킬을 가졌는지 판단하는 방법이 동일한데,
세부적인 조건이 늘어났습니다.

CASE 조건문을 통해 'A', 'B', 'C' 세 가지 등급으로 개발자를 나누는데,
CASE 안에서 직접적으로 조건을 표현하면 길어질 수도 있습니다.
또한, 'Front End' 스킬을 보유한 경우에 대해서는 'A', 'C' 두 가지 등급에서 참조하기 때문에 중복 선언도 피하고 싶습니다.

따라서, 원하는 스킬을 보유한 경우를 `HAS_SKILLS` 라는 임시 테이블로 구성하고,
해당 테이블을 `DEVELOPERS` 테이블에 `INNER JOIN` 하여 미리 계산한 조건에 대한
Boolean 값을 CASE 안에서 가져다 사용합니다. 조건에 해당되지 않는 나머지 개발자에 대한 등급은
`NULL` 로 분류하고, 등급이 `NULL` 인 경우만 제외하여 조회합니다.

```sql
WITH HAS_SKILLS AS (
    SELECT DEV.ID, (SUM(SKL.CATEGORY = 'Front End') > 0) AS HAS_FRONT,
            (SUM(SKL.NAME = 'Python') > 0) AS HAS_PYTHON,
            (SUM(SKL.NAME = 'C#') > 0) AS HAS_CSHARP
    FROM DEVELOPERS AS DEV
        LEFT JOIN SKILLCODES AS SKL
            ON (DEV.SKILL_CODE & SKL.CODE) = SKL.CODE
    GROUP BY ID
),

WITH_GRADE AS (
    SELECT (CASE WHEN SKL.HAS_FRONT AND SKL.HAS_PYTHON THEN 'A'
                WHEN SKL.HAS_CSHARP THEN 'B'
                WHEN SKL.HAS_FRONT THEN 'C'
                ELSE NULL END) AS GRADE,
            DEV.ID, DEV.EMAIL
    FROM DEVELOPERS AS DEV
        INNER JOIN HAS_SKILLS AS SKL
            ON DEV.ID = SKL.ID
)

SELECT *
FROM WITH_GRADE
WHERE GRADE IS NOT NULL
ORDER BY GRADE, ID;
```

## 인사 테이블

### [연간 평가점수에 해당하는 평가 등급 및 성과금 조회하기](https://school.programmers.co.kr/learn/courses/30/lessons/284528)

> `HR_DEPARTMENT` 테이블은 회사의 부서 정보를 담은 테이블입니다.
> `HR_EMPLOYEES` 테이블은 회사의 사원 정보를 담은 테이블입니다.
> `HR_GRADE` 테이블은 2022년 사원의 평가 정보를 담은 테이블입니다.
>
> `HR_DEPARTMENT`, `HR_EMPLOYEES`, `HR_GRADE` 테이블을 이용해 사원별 성과금 정보를 조회하려합니다.
> 평가 점수별 등급과 등급에 따른 성과금 정보가 아래와 같을 때, 사번, 성명, 평가 등급, 성과금을 조회하는 SQL문을 작성해주세요.
>
> 평가등급의 컬럼명은 `GRADE` 로, 성과금의 컬럼명은 `BONUS` 로 해주세요.
> 결과는 사번 기준으로 오름차순 정렬해주세요.

`HR_GRADE` 테이블의 평가 점수(`SCORE`)를 기준으로 평가등급(`GRADE`)과 성과금(`BONUS`)을 도출하는 문제입니다.

사원 평가는 반기마다 발생하는데 2022년 내에 두 차례 발생했기 때문에, 사번(`EMP_NO`) 그룹별로
평가 점수(`SCORE`)를 AVG 집계합니다. 평균 평가 점수(`AVG(SCORE)`)를
CASE 조건문에 넣어 평가등급(`GRADE`)과 성과금(`BONUS`)을 분류합니다.

분류한 성과금은 연봉에 대한 배율이기 때문에, 최종 답안을 낼 때는 `HR_EMPLOYEES` 테이블의
연봉(`SAL`)에 배율을 곱해서 실제 성과금(`BONUS`)을 계산합니다.

```sql
WITH SCORE AS (
    SELECT EMP_NO, AVG(SCORE) AS SCORE
    FROM HR_GRADE
    GROUP BY EMP_NO
),

GRADE AS (
    SELECT EMP_NO,
        (CASE WHEN SCORE >= 96 THEN 'S'
            WHEN SCORE >= 90 THEN 'A'
            WHEN SCORE >= 80 THEN 'B'
            ELSE 'C' END) AS GRADE,
        (CASE WHEN SCORE >= 96 THEN 0.2
            WHEN SCORE >= 90 THEN 0.15
            WHEN SCORE >= 80 THEN 0.1
            ELSE 0.0 END) AS BONUS
    FROM SCORE
)

SELECT EMP.EMP_NO, EMP.EMP_NAME, GRD.GRADE,
        ROUND(EMP.SAL * GRD.BONUS) AS BONUS
FROM HR_EMPLOYEES AS EMP
    INNER JOIN GRADE AS GRD ON EMP.EMP_NO = GRD.EMP_NO
ORDER BY EMP_NO
```

## 대장균 개체 테이블

### [특정 세대의 대장균 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/301650)

> `ECOLI_DATA` 테이블은 실험실에서 배양한 대장균들의 정보를 담은 테이블입니다.
>
> 3세대의 대장균의 ID(`ID`) 를 출력하는 SQL 문을 작성해주세요. 이때 결과는 대장균의 ID 에 대해 오름차순 정렬해주세요.

세대별로 `JOIN` 연산을 중첩해서 사용하여 3세대 대장균의 ID(`ID`)를 도출하는 문제입니다.

1세대 대장균(`GEN1`)은 부모 개체의 ID(`PARENT_ID`)가 `NULL` 인 경우입니다.

2세대 대장균(`GEN2`)은 1세대(`GEN1`) 대장균 개체의 ID(`ID`)가 부모 개체의
ID(`PARENT_ID`)인 경우입니다. 두 항목을 `INNER JOIN` 하여 공통된 경우만 2세대로 판단합니다.

3세대 대장균은 2세대 대장균(`GEN2`)을 구한 것과 동일한 방식으로 `INNER JOIN` 연산합니다. 해당하는 3세대 대장균의 ID(`ID`)를 출력합니다.

```sql
WITH GEN1 AS (
    SELECT DISTINCT ID
    FROM ECOLI_DATA
    WHERE PARENT_ID IS NULL
),

GEN2 AS (
    SELECT DISTINCT ECOLI.ID
    FROM ECOLI_DATA AS ECOLI
        INNER JOIN GEN1 AS PARENT ON ECOLI.PARENT_ID = PARENT.ID
)

SELECT DISTINCT ECOLI.ID
FROM ECOLI_DATA AS ECOLI
    INNER JOIN GEN2 AS PARENT ON ECOLI.PARENT_ID = PARENT.ID
ORDER BY ID;
```

### [멸종위기의 대장균 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/301651)

> `ECOLI_DATA` 테이블은 실험실에서 배양한 대장균들의 정보를 담은 테이블입니다.
>
> 각 세대별 자식이 없는 개체의 수(`COUNT`)와 세대(`GENERATION`)를 출력하는 SQL문을 작성해주세요.
> 이때 결과는 세대에 대해 오름차순 정렬해주세요. 단, 모든 세대에는 자식이 없는 개체가 적어도 1개체는 존재합니다.

재귀 쿼리를 사용해 이전 세대의 대장균 ID(`ID`)와 `ECOLI_DATA` 테이블의 부모 개체 ID(`PARENT_ID`)가
동일한 경우를 반복해서 탐색합니다. 다음 세대가 없을 때까지 조회한 모든 결과를 결합하고,
대장균의 ID(`ID`)가 어떠한 부모 개체의 ID(`PARENT_ID`)에도 포함되지 않는 경우만 선택하여,
세대(`GENERATION`)별 개체의 수(`COUNT`)를 집계하는 문제입니다.

앞선 문제처럼 n세대까지 `JOIN` 연산을 중첩하려다가 도저히 아닌 것 같아서 찾아봤는데,
재귀 쿼리를 사용하여 해결할 수 있는 문제였습니다. 평소에 재귀 쿼리를 사용해보지 않아
`GEN_DATA` 를 도출하는 과정은 검색 결과를 참고했습니다.

`GEN_DATA` 에서 자식이 없는 개체만 선택하고 `GENERATION` 그룹별로 COUNT 집계한 결과를 조회합니다.

```sql
WITH RECURSIVE GEN_DATA AS(
    SELECT ID, 1 AS GENERATION
    FROM ECOLI_DATA
    WHERE PARENT_ID IS NULL

    UNION ALL

    SELECT ECOLI.ID, PARENT.GENERATION+1 AS GENERATION
    FROM ECOLI_DATA AS ECOLI
    INNER JOIN GEN_DATA AS PARENT
        ON ECOLI.PARENT_ID = PARENT.ID
)

SELECT COUNT(PARENT.GENERATION) AS COUNT, PARENT.GENERATION
FROM GEN_DATA AS PARENT
WHERE PARENT.ID NOT IN (
    SELECT DISTINCT PARENT_ID FROM ECOLI_DATA WHERE PARENT_ID IS NOT NULL)
GROUP BY GENERATION
ORDER BY GENERATION;
```
