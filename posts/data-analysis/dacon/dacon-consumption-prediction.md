---
title: "DACON 소비자 데이터 기반 소비 예측 AI 경진대회 - EDA + Soft Voting Ensemble"
date: "2022-08-22T14:31:44+09:00"
layout: "post"
description: >
  DACON 소비자 데이터 기반 소비 예측 경진대회 참가 및 분석 결과입니다.
  EDA 시각화, Label Encoding, 파생 변수 생성, Optuna 하이퍼파라미터 튜닝, Soft Voting Ensemble
  기법을 활용하여 NMAE 0.18533 성적으로 36위를 달성한 과정을 공유합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/a9p1jkt6m3c44nigy5lnd/consumption-prediction-00-cover.webp?rlkey=4f4szfbtri7noe9lw8tw11bp4&raw=1"
categories: ["Data Analysis", "Dacon"]
tags: ["DACON", "소비 예측", "회귀 모델", "EDA", "데이터 분석", "Ensemble", "Soft Voting", "Optuna", "LGBM", "XGBoost", "CatBoost"]
series: ["DACON 경진대회"]
---

{{< series "DACON 경진대회" >}}

{{< bookmark "https://dacon.io/competitions/official/235893/codeshare/4921" >}}

## 분석 목표 및 결과

- 소비자 데이터를 바탕으로 고객의 제품 총 소비량을 예측했습니다.
- 팀 프로젝트를 통해 습득한 EDA 시각화를 최대한 활용해보는 것을 목적으로 진행했습니다.
- Ensemble 기법 중 Soft Voting 방식을 사용해 NMAE 기준 `0.18533` 수치를 달성하여 36위를 기록했습니다.

## 학습 데이터

- [소비자 데이터](https://dacon.io/competitions/official/235893/data)
- 베이스라인에서 데이터 결측치가 없음을 확인받고 전처리 없이 EDA 진행했습니다.

![train.csv](https://dl.dropboxusercontent.com/scl/fi/y4e3kpu0yxm2ax2deeyxp/consumption-prediction-01-data.webp?rlkey=3arpouhstnsbnspq75vnjp7as&raw=1)

## EDA

### Target

- 예측해야할 소비량 데이터는 6부터 2525 사이의 범위에 존재하며,
  전체 데이터 중 50퍼센트 이상이 500 이하의 값에 편향됨을 확인했습니다.

![target histogram, target ratio](https://dl.dropboxusercontent.com/scl/fi/ezj2gsbjx264j6fix9g1e/consumption-prediction-02-label.webp?rlkey=j5h87z12gr5agelh1itg3difa&raw=1)

### 출생 연도와 소득

- 출생 연도와 소득 데이터에서 이상치가 있음을 확인하고 해당 데이터를 제외한 그래프를 새롭게 표시했습니다.
- 두 데이터 간에 관계가 있음을 기대하며 출생 연도에 따른 소득의 총합과 평균값 그래프를 추가로 표시했습니다.
- 중년층에서 가장 높은 소득이 나타남을 알 수 있었고, 청년층과 노년층에서는 반대의 결과를 확인했습니다.

![Year_Birth histogram, Year_Birth ratio, Income histogram](https://dl.dropboxusercontent.com/scl/fi/8dz8q7x1ftmhjdqlh8jto/consumption-prediction-03-birth-year.webp?rlkey=y9j3p9043dixyma828k9ozo76&raw=1)

![Income sum by Year_Birth, Income mean by Year_Birth](https://dl.dropboxusercontent.com/scl/fi/o70gefb3uu3cjv1fer8nu/consumption-prediction-04-birth-income.webp?rlkey=x9qpxnhbfi1nstfw4ee023t1b&raw=1)

![Year_Birth histogram, Year_Birth ratio, Income histogram](https://dl.dropboxusercontent.com/scl/fi/gwqfx0s60ogl834pjcxzk/consumption-prediction-05-income.webp?rlkey=v0ls1gekn36fprxqojo6gdkz2&raw=1)

### 구매 건수

- 구매 건수 데이터에서도 일부 이상치가 발생하는 것을 확인했지만,
  이상치의 수가 무시할 수는 없는 수준이고 실제로 이상치를 남겨둔 경우에 더 높은 성능이 나오는 것을 확인했습니다.

![NumDealsPurchases, NumWebPurchases, NumCatalogPurchases, NumStorePurchases, NumWebVisitsMonth](https://dl.dropboxusercontent.com/scl/fi/vbpv1uo2uqqxxwx47h0wu/consumption-prediction-06-purchases.webp?rlkey=6a2s67g1oedoqqmtp01t40iib&raw=1)

### 고객 등록 일자

- 문자열로 된 날짜 데이터를 분리해 연, 월, 일에 해당하는 데이터를 각각 그래프로 표시했습니다.

![Year_Customer, Month_Customer, Day_Customer](https://dl.dropboxusercontent.com/scl/fi/2j3qoouhyus6ti3ysz1ir/consumption-prediction-07-customer-ymd.webp?rlkey=vmrkbp6kkq3mfxsbmi5bmba87&raw=1)

### 범주형 데이터

- 나머지 범주형 데이터도 그래프로 표시하여 각 범주의 분포를 확인했습니다.
- 결혼 상태 데이터에 한해서 같은 종류의 범주를 하나로 묶어서 분석할 수 있는 가능성 인지했습니다.

![AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5, Response](https://dl.dropboxusercontent.com/scl/fi/fvo3m112c35zlaqsy5ef1/consumption-prediction-08-categorical1.webp?rlkey=3wzvj0vlhy0ojgzz5wufaymvq&raw=1)

![Education, Martial_Status, Kidhome, Teenhome, Complain](https://dl.dropboxusercontent.com/scl/fi/kcbtb8mfjd4e2435s1o0x/consumption-prediction-08-categorical2.webp?rlkey=lckqiru6j1xo9t7ouqypt0udj&raw=1)

## 데이터 전처리

- 문자열로 된 범주형 데이터에 Label Encoding 적용했습니다.
- 더욱 다양한 특징을 보여주기 위해 기존 변수들로부터 파생 변수 생성했습니다.
- train 데이터에 한정해서 출생 연도와 소득에서 발견된 이상치 제거했습니다.
- 숫자형 데이터와 범주형 데이터에 각각 Standardization 및 One-Hot Encoding 적용했습니다.

## 모델 최적화

- Pycaret으로 해당 데이터에서 회귀 모델 간 비교를 진행하여 가져갈 모델 선택했습니다.
- 각각의 모델에 대해 NMAE 점수를 기준으로 Optuna를 사용하여 하이퍼파라미터 튜닝했습니다.
- 개별 모델의 모든 조합에 대해 Soft Voting을 시도하였을 때,
  LGBM, XGB, CatBoost, GBR의 조합이 가장 높은 성능을 보여줌을 확인했습니다.
- 마찬가지로 Hard Voting 방식을 사용해 모든 조합에 대해 비교해봤지만 Soft Voting의 성능엔 못미쳤습니다.

## 회고

- 머신러닝에 대한 깊이가 깊지 않다보니 매번 Ensemble을 진행할 때 모든 경우에 대해 확인해 보는데,
  해당 작업에 긴 시간이 요구되고 자원 사용량도 만만치 않기에 다른 방법을 탐색할 필요성을 느꼈습니다.
- 순위가 매겨지는 대회에 참가해보니 아직 많이 부족함을 느꼈습니다.
