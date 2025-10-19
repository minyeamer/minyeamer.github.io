---
layout: post
title: "[AI SCHOOL 5기] 데이터 분석"
date: 2022-03-23 21:04:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Data Analysis]
slug: aischool-01-00-data-analysis
---

# Data Types
- Structured Data
   - Relational Database
   - Spread Sheets
- Semi-structured Data
   - System Logs
   - Sensor Data
   - HTML
- Unstructured Data
   - Image / Video
   - Sound
   - Document

---

# Data Collection Tools
- Logstash: 로그 데이터 (SQL 구조화)
- Elasticsearch: 데이터가 자유로움
- Kibana: 그래프 자동화
- Elastic Stack, Zepplin

---

# API Meanings
1. 웹 상에서의 API
2. 라이브러리/프로그램 도구 (텐서플로우에서의 함수 등)

## Open API
1. 공익적인 목적
2. 서비스 활성화 목적 (서드파티 앱 지원)
3. SNS에서 무분별한 크롤링으로 인한 서버 과부하 대비

---

# Missing Data Handling
1. 랜덤하게 채워넣기
2. 주변 (행의) 값들로 채워넣기
3. 열의 대푯값을 계싼해서 채워넣기 (mea, median)
4. 전체 행들을 그룹으로 묶어낸 후 그룹 내 해당 열의 값을 예측해 채워넣기
5. 나머지 열들로 머신러닝 예측모델을 만든 후 해당 열의 값을 예측해 채워넣기
6. 특정 기준 비율 이상으로 빠져있을 시 해당 열 삭제

---

# Pandas Functions

## Referring
- `df = pd.read_excel()`: 엑셀 파일 열기   
- (엑셀 파일 원본은 행과 열로 구성된 `pandas.DataFrame()` 타입)
- `df.head()`: 위에서부터 값을 참조 (default 5)
- `df.tail()`: 밑에서부터 값을 참조 (default 5)
- `df.describe()`: 기술 통계량 반환 (평균, 최솟값 등)
- `df.info()`: DataFrame 정보 반환 (Non-Null 행에서 유효성 확인)
- `df.loc[row]`: DataFrame에서 행 꺼내기 (추가로 column도 지정 가능)
- `df.iloc[row]`: DataFrame에서 인덱스 번호를 기준으로 행 꺼내기
- `df[column]`: DataFrame에서 열 꺼내기
- `df[column].apply(lambda x: x+1)`: 특정 열에 속한 값에 1씩 더해서 반환

## Modifiying
- `df.drop([row])`: DataFrame에서 행 삭제
- `del df[column]`: DataFrame에서 열 삭제
- `df.rename(columns=, inplace=True)`:   
DataFrame에서 열 이름 바꾸기 (`inplace` 옵션은 덮어쓰기를 의미)
- `df.sort_values(by=, inplace=True)`:   
DataFrame에서 열 내부의 값을 정렬 (내림차순 정렬 시 `ascending=False` 옵션 추가)
- `pd.pivot_table(df, index=, aggfunc=np.mean)`:   
기존 DataFrame에서 특정 행을 index로 설정한 새로운 DataFrame 생성 (피벗 테이블)
`aggfunc` 옵션에 계산식을 넣을 수 있음 (`count`, `np.sum` 등)

## Copying
- `df_2 = df`: 얕은 복사 (원본 변경 시 복사본도 같이 변경)
- `df_3 = df.copy()`: 깊은 복사 (원본 변경이 복사본에 영향을 미치지 않음)