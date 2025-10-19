---
layout: post
title: "[AI SCHOOL 5기] 머신 러닝"
date: 2022-04-13 16:31:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Machine Learning]
slug: aischool-06-00-machine-learning
---

# 인공지능
- Intelligent Agents를 만드는 것
- 주변 환경들을 인식하고 원하는 행동을 취하여 목표를 성취하는 것

## Artificial Narrow Intelligence
- 제한된 기능만 수행할 수 있는 인공지능
- weak AI

## Artificial General Intelligence
- 사람만큼 다양한 분야에서 기능을 수행할 수 있는 인공지능
- strong AI

## Artificial Super Intelligence
- 모든 분야에서 사람보다 뛰어난 인공지능

---

# 모델
- 데이터를 가장 잘 설명할 수 있는 함수 (`y = ax + b`)
- 모델에서 `θ`는 Parameter(가중치, Weight) 의미
- 모델에서 `h(x)`는 Hypotheses(가설) 의미
- 모델에서 `b`는 Bias(편향, 보정치) 의미

---

# 머신러닝
- 어떠한 과제를 해결하는 과정에서 특정한 평가 기준을 바탕으로 학습의 경험을 쌓는 프로그램

## 머신러닝 분류

![51p](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/00-machine-learning/51p.png?raw=true)

## Supervised
- 입력값에 대한 정답을 예측하기 위해 학습
- 데이터와 정답이 같이 존재
- **회귀(Regression)**: 결과가 실수 영역 전체에서 나타남
- **분류(Classification)**: 결과가 특정 분류에 해당하는 불연속값으로 나타남
- ex) 주식 가격 예측, 이미지 인식 등

## Unsupervised
- 입력값 속에 숨어있는 규칙성을 찾기 위해 학습
- 정답이 없는 데이터를 주고 비슷한 집단을 분류
- ex) 고객군 분류, 장바구니 분석(Association Rule) 등

## Reinforcement
- Trial & Error를 통한 학습
- 최종적으로 얻게 될 기대 보상을 최대화하기 위한 행동 선택 정책 학습
- 각 상태에 대해 결정한 행동을 통해 환경으로부터 받는 보상을 학습
- ex) 로봇 제어, 공정 최적화 등

## Automated ML
- 어떤 모델(함수, 알고리즘)을 써야할지를 컴퓨터가 알아서 정하게 함
- 인공신경망 레이어의 범위, 후보 등을 정해놓고 그 안에서 가장 좋은 조합을 찾음
- ex) AutoML Tables (행의 수가 1000건이 넘어야하는 제약)

---

# 학습
- 데이터를 가장 잘 설명하는 방법을 찾는 과정
- 데이터에 맞는 모델을 찾는 과정 (= Model Fitting)
- 실제 정답과 예측 결과 사이의 오차(Loss, Cost, Error)를 줄여나가는 최적화 과정

## 학습 과정
1. 초기 모델에 데이터를 입력
2. 결과를 평가 (예측/분류의 정확도 등)
3. 결과를 개선하기 위해 모델을 수정 (모델 내부 Parameter 수정 등)

## Model's Capacity

![44p](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/00-machine-learning/44p.png?raw=true)

- 2번 모델은 3번 모델보다 오차가 크지만 새로운 데이터가 생겼을 때 비슷하게 예측 가능
- 3번 모델은 오차가 가장 적지만 새로운 데이터가 생겼을 때 오차가 매우 커질 수 있음
- 3번 모델과 같은 Overfitting(과적합)이 발생하기 전에 학습을 멈춤

## Cross Validation
- 새로운 데이터들에 대해서도 좋은 결과를 내게 하기 위해 데이터를 3개 그룹으로 나눠 학습
- 60%의 Training Data로 모델을 학습
- 20%의 Validation Data로 모델을 최적화/선택
- 20%의 Test Data로 모델을 평가
- 데이터를 분리하는 비율은 모델에 따라 달라짐

## K-Fold Cross Validation
- 후보 모델 간 비교 및 선택을 위한 알고리즘
- Training Data를 **K** 등분하고 그 중 하나를 Validation Data로 설정
- **K** 값은 자체적으로 결정하며 보통 10-Fold 사용 (시간이 없으면 5-Fold)
- 머신러닝에서 **K**는 주로 사용자가 결정하는 상수
- **Stratified**: 층화 표집 방법, 데이터의 분류 별 비율이 다르면 K-Fold 조각 안에서 비율을 유지시킴

## 10-Fold 학습 과정
> 데이터를 80%의 Training Data와 20%의 Test Data로 나누고 Training Data를 10등분   
> Phase 1. Training Data(0:9) + Validation Data(TD 9)를 사용해 점수 측정   
> Phase 2. Training Data(0:8,9) + Validation Data(TD 8)를 사용해 점수 측정   
> . . .   
> Phase 10. Training Data(1:10) + Validation Data(TD 0)를 사용해 점수 측정   
> 마지막으로 Training Data 전체를 학습하고 Test Data로 검증

---

# Scikit-learn
- 파이썬으로 전통적인 머신 러닝 알고리즘들을 구현한 오픈 소스 라이브러리
- 다른 라이브러리들과의 호환성이 좋음 (Numpy, Pandas, Matplotlib 등)

## 머신러닝 학습 과정

1. 데이터셋 불러오기

```python
sklearn.load_[DATA]()
```

2. Train/Test set으로 데이터 나눔

```python
sklearn.model_selection.train_test_split(X, Y, test_size)
```

3. 모델 객체 생성

```python
sklearn.linear_model.LinearRegression()
sklearn.linear_model.LogisticRegression()
sklearn.neighbors.KNeighborsClassifier(n_neighbors)
sklearn.cluster.KMeans(n_clusters)
sklearn.decomposition.PCA(n_components)
sklearn.svm.SVC(kernel, C, gamma)
```

4. 모델 학습 시키기

```python
model.fit(train_X, train_Y)
```

5. 모델로 새로운 데이터 예측 (Scaler를 적용했으면 새로운 데이터에도 적용)

```python
model.predict(test_X)
model.predict_proba(test_X)
sklearn.metrics.mean_squared_error(predicted_Y, test_Y)
sklearn.metrics.accuracy_score(predicted_Y, test_Y)
sklearn.metrics.precision_score
sklearn.metrics.recall_score
```

## 머신러닝 분류 기준
- [Choosing the right estimator](https://scikit-learn.org/stable/tutorial/machine_learning_map/)

![estimator](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/00-machine-learning/estimator.png?raw=true)

---

# Feature Normalization

## Numeric Column
- Min-Max Algorithm
- Standardization

## Categorical Column
- One-Hot Encoding, One-Hot Vector
- 열과 목록 개수만큼 0으로 채워진 행렬을 만들고 값이 해당하는 위치에 1을 표시
- 범주형 데이터(카테고리)의 숫자가 크고 작음에 관계없이 카테고리의 위치값만을 판단

---

# Supervised Algorithm

## [Linear Regression (선형 회귀)](https://minyeamer.github.io/blog/aischool-06-01-linear-regression/)
- 종속 변수 y와 독립 변수 x 사이의 선형 상관 관계를 모델링하는 회귀분석 기법

## [Logistic Regression (로지스틱 회귀)](https://minyeamer.github.io/blog/aishcool-06-02-logistic-regression/)
- 이진 분류(0 또는 1) 문제를 해결하기 위한 모델
- ex) 스팸 메일 분류, 질병 양성/음성 분류 등

## [Gradient Boosting Regression (XG Boost)](https://minyeamer.github.io/blog/aishcool-06-03-gradient-boosting/)
- 대용량 분산 처리를 위한 Gradient Boosting 라이브러리
- ex) 테니스를 쳤던 과거 데이터를 보고 날씨 정보를 이용해 의사결정

## [K-Nearest Neightbor Algorithm (KNN)](https://minyeamer.github.io/blog/aishcool-06-04-knn/)
- 기존의 가까운 이웃 데이터를 살펴 새로운 데이터를 분류하는 알고리즘

## [Kernel Support Vector Machine (KSVM)](https://minyeamer.github.io/blog/aishcool-06-05-kernelized-svm/)
- 데이터를 분류하는 Margin을 최대화하는 결정 경계를 찾는 기법

---

# Unsupervised Algorithm

## [K-Means Algorithm](https://minyeamer.github.io/blog/aishcool-06-06-k-means/)
- 데이터를 K개의 클러스터로 분류하는 알고리즘

## [Principal Component Analysis](https://minyeamer.github.io/blog/aishcool-06-07-pca/)
- 차원 축소를 통해 최소 차원의 정보로 원래 차원의 정보를 모사하는 알고리즘

---

# Model Saving & Loading

## Model Saving

```python
import joblib

joblib.dump(model, 'model_v1.pkl', compress=True)
```

## Model Loading

```python
import joblib

model_loaded = joblib.load('model_v1.pkl')
```