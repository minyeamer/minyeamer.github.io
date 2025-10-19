---
layout: post
title: "[AI SCHOOL 5기] 통계분석 실습 - Numpy & Pandas"
date: 2022-03-29 16:11:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Statistics, Numpy, Pandas]
slug: aischool-04-01-numpy-pandas
---

# Numpy
- Numpy Array 내부의 데이터는 하나의 자료형으로 통일
- Numpy Array에 값을 곱하면 전체 데이터 그대로 복사되는 리스트와 달리 데이터에 각각 곱해짐
- `np.array([])`: Numpy Array 생성
- `np.dtype`: Numpy Array의 Data Type
- `np.shape`: Numpy Array 모양(차원)
- `np.arange()`: `range`를 바탕으로 Numpy Array 생성
- `np.reshape()`: Numpy Array 모양을 변경, 열에 `-1`을 입력하면 자동 계산
- `np.dot()`: 행렬곱

---

# Pandas
- `pd.Series([], index=[])`: Key가 있는 리스트(Series) 생성
- `Series.values`: Series의 값
- `Series.index`: Series의 키 값
- `df.ammount`: 띄어쓰기 없이 영단어로 구성된 열은 변수처럼 꺼내 쓸 수 있음
- `df.insert(column, 'key', 'value')`: index 기준으로 특정 위치에 새로운 열 삽입
- `df[(con1) & (con2)]`: 여러 개의 조건을 사용할 땐 각각의 조건을 괄호 안에 묶어야 함
- `df['key'].value_counts()`: 값의 출현 빈도 합계 (`sort=False`로 정렬 해제)
- `df['key'].value_counts().plot(kind='pie')`: 빈도수를 기준으로 원형차트 생성
- `df['key'].apply()`: 조건에 따라 변환된 값을 가진 열 반환
- `df['key'].replace()`: 변환값이 1대1 대응 시 `apply()` 대신 `replace()` 사용 가능   
  `df['gender'].replace([1, 2], ['male', 'female'])`
