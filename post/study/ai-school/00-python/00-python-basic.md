---
layout: post
title: "[코드라이언] 파이썬 기초"
date: 2022-03-20 16:53:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Python]
slug: aischool-00-01-python-basic
---

# for문
- 문장을 여러 번 실행할 떄 복사 붙여넣기로 길게 늘이지 않고 단순하게 표현하기 위한 구문
- for문에 적용되는 문장은 들여쓰기를 해야 함

```python
for _ in range(30):
    print(random.choice(["a", "b", "c"]))
```

# while문
- for문과 마찬가지로 문장을 반복실행할 수 있는 구문
- 조건을 충족할 경우 반복을 멈춤
- True를 조건으로 사용 시 무한루프 발생 `while True:`
- `break` 명령어를 통해 반복문 종료 가능

# 변수
- 객체에 이름표를 붙이고 이름표가 불리면 내용물인 객체를 반환   
`lunch = random.choice(["a", "b", "c"])`

# 딕셔너리
- "xx은 xx이다"를 코드로 표현한 자료구조
- 딕셔너리의 get 명령어는 Key에 해당하는 값을 반환
- 값을 추가할 때는 `dict[a] = b` 형식으로 추가
- 딕셔너리의 clear 명령어는 딕셔너리 내용을 초기화

# 집합
- 중복된 값을 제거하여 표현하는 자료구조
- `set()`으로 집합 생성
- 합집합: `set1 | set2`
- 교집합: `set1 & set2`
- 차집합: `set1 - set2`

# 조건문
- 상황에 따른 처리를 하기 위한 구문
- `if 조건:`으로 조건문 선언
- 같은 경우를 구할 땐 `a == b`
- 나머지 경우에 대해서는 `else` 사용

# pip/conda
- pip: 파이썬에서 지원받는 패키지만을 가져옴 (라이브러리만 맞으면 설치)
- conda: 아나콘다에서 지원받는 패키지만을 가져옴 (아나콘다에서 유리)
- conda의 장점: 기존 Python 및 라이브러리 버전 충돌을 체크함
- conda의 단점: 설치 속도가 너무 느림
- 설치가 너무 느리거나 다른 라이브러리에 대한 영향이 없을 경우 pip 사용
- 라이브러리 참조 파일 생성 시 `pip install -r requirements.txt`

# 기타 명령어
1. random.choice(): 리스트 안에서 랜덤한 객체 하나를 반환
2. time.sleep(): 입력값만큼의 시간(초) 동안 딜레이 발생
3. len(): 리스트/딕셔너리의 목록 개수 반환