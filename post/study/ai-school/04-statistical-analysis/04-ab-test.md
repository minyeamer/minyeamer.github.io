---
layout: post
title: "[AI SCHOOL 5기] 통계분석 실습 - A/B Test"
date: 2022-04-02 22:50:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Statistics]
slug: aischool-04-04-ab-test
---

# 마케팅 비용 분석
- 매월 유튜브에 광고 비용을 지출하여 신규 유저(구매 고객 or 회원가입 고객)를 획득
- 월별로 10,000원 단위의 유튜브 광고 비용과 해당 월에 신규로 획득된 유저 수가 측정되었다고 가정

## 비교 데이터

![youtube](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/04-ab-test/youtube.png?raw=true)

## 단순 CAC 계산
- CAC(Customer Acquisition Cost, 신규고객 유치 비용)
- @ https://j.mp/35O5NRe

```python
cac = ad_df['Marketing_Costs'].sum() / ad_df['User_Acquired'].sum()
print(cac * 10000)

# Output
446원
```

위의 금액에 추가로 획득하기를 원하는 유저 수를 곱한 금액을   
유튜브 광고 비용으로 쓰면 그만큼 유저가 늘어날까?   
== 위의 금액 만큼 유튜브 광고에 쓰면 정말로 유저가 1명 늘어날까?

## 피어슨 상관계수

```python
stats.pearsonr(ad_df['Marketing_Costs'], ad_df['User_Acquired'])

# Output
피어슨 상관계수 : 0.8035775069546849
p-value : 0.0016386012345537505
```

- p-value가 0.0016(<0.05)이므로,   
  월별 유튜브 광고 비용과 신규 유저 수가 통계적으로 유의미한 상관관계가 없다
- 월별 유튜브 광고 비용과 신규 유저 수 사이에는   
  통계적으로 유의미한 강한 상관관계(+0.8)가 있다
- 피어슨 상관계수 값에 대한 해석 기준 (Strong/Moderate/Weak) @ https://j.mp/3mH8FWN
- 파이썬 프로그래밍 없이 상관관계 분석을 진행할 수 있는 도구 @ https://j.mp/324551c

---

# A/B Test (독립표본)
- 페이지 구성과 세부 디자인을 다르게 만든 2개의 웹사이트 시안을 기반으로 A/B Test 진행
- 웹사이트 시안 A와 B 각각에 유입된 유저들이   
  실제로 각 웹사이트 내에서 이탈하기까지의 시간(체류시간, Duration time)을 측정
- T-Test를 진행하기 이전에 Null인 데이터들은 제외

## 비교 데이터

![duration](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/04-ab-test/duration.png?raw=true)

## 독립표본 T-Test

```python
stats.ttest_ind(web_a.Duration_A.values, 
                web_b.Duration_B.values, 
                equal_var=False)

# Output
Ttest_indResult(statistic=3.0165632092150694, pvalue=0.008734970056646718)
```

- `equal_var=True` : 두 개의 열의 분산값이 동일할거라 가정
- `equal_var=False`: 분산값이 동일하지 않기 때문에 `False`로 설정
- 2개의 측정 그룹이 동일한 수가 아니거나 유사한 분산값을 갖지 않을 경우   
  Welch's t-test를 사용 @ https://j.mp/3kLFwcE
- p-value가 0.0087(<0.05)이므로,   
  웹 시안 A와 B에 대한 체류시간의 평균값이 통계적으로 유의미한 차이가 없다
- 이러한 전제 하에 위와 같은 체류시간 측정 결과가 나올 확률이 0.87%라고 이해할 수 있음
- 웹 시안 A와 B에 대한 유저들의 체류 시간 사이에는 통계적으로 유의미한 차이가 있다

---

# A/B Test (카이제곱 검정)
- 최종 구매를 위한 버튼을 2개의 서로 다른 시안으로 제작해 각기 다른 유저들에게 노출
- 해당 버튼을 누르면 구매가 확정된다고 가정

## 비교 데이터

![clicked](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/04-ab-test/clicked.png?raw=true)

## Conversion Rate (전환율)
- 전체 웹사이트 사용자 중에서 얼마나 많은 사용자들이 동작을 마치는지에 대한 지표

```python
conversion_rate = click_df['Clicked'] / (click_df['Clicked'] + click_df['Unclicked']) * 100

# Output
Button_A    5.746209
Button_B    7.737226
dtype: float64
```

## Click-Through Rate (CTR, 클릭율)
- 얼마나 많은 사용자들이 웹사이트에 접근하기 위해 광고를 클릭하는지에 대한 지표
- Button_A는 5.75%
- Button_B는 7.73%

## 카이제곱 검정
- 버튼 A/B에 대한 클릭 여부가 정리된 위 테이블 == Contingency Table(분할표)   
  @ https://j.mp/384CcFR
- chi2_contingency 함수 활용 시 Contingency Table을 기반으로 카이제곱 검정   
  @ https://j.mp/3mH1Nsr

```python
stats.chi2_contingency([click_df['Clicked'], click_df['Unclicked']])[1]

# Output
0.004968535119697213
```

- p-value가 0.0049(<0.05)이므로,   
  버튼 A/B에 대한 클릭 여부가 통계적으로 유의미한 연관성이 없다는 전제 하에,   
  이러한 클릭 수 측정 결과가 나올 확률이 0.49%라고 이해할 수 있음
- 배너 버튼 시안 A와 B에 대한 유저들의 클릭 수 사이에는 통계적으로 유의미한 차이가 있다

---

# A/B Test References
- A/B Testing에 대한 기초적인 정보들 @ https://j.mp/3eeo2TA
- 데이터를 활용한 디지털 마케팅 효과분석 @ https://j.mp/2P7YHCO
- P-hacking에 대하여 @ https://j.mp/3mLMOgP / https://j.mp/31XJBTF

## p-value
p-value의 높고 낮음과 별개로 실제 실험의 효과 크기 역시도 중요하게 고려해야한다.   
예를 들어 어떤 웹사이트의 구매 버튼의 디자인을 변경하여 구매 수가 n 만큼 증가되었고,   
디자인 변경 전/후에 대한 구매 버튼 클릭 수 사이의 관계를 대상으로 통계 검정 후 p-value가 0.05보다 낮게 나왔더라도,   
정작 증가된 구매 수에 해당하는 n이 미미하다면 낮은 p-value에도 불구하고 디자인 변경의 실질적인 효용이 적기 때문이다.   
(통계적으로만 유의미할 뿐 독립변수의 변화에 따른 종속변수의 변화값이 실질적/실용적인 의미를 갖지 않음)