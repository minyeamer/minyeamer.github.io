---
layout: post
title: "[AI SCHOOL 5기] 머신 러닝 실습 - Model Stacking"
date: 2022-04-13 22:10:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Machine Learning, Stacking]
slug: aischool-06-08-model-stacking
---

# Model Stacking
- 서로 다른 모델들을 모으고 Ensemble 기법을 사용해 개선된 모델을 만드는 것
- 기존 모델들로부터 예측 결과를 도출하는 **1st Stage**와   
  이를 기반으로 추가적인 판단을 진행하는 **2nd Stage**로 나뉨

## 1st Stage
1. train_X를 가지고 1번 모델을 Training
2. Training을 거친 1번 모델에 train_X를 넣었을 때 결과(예측값)을 저장
3. 다른 모델에도 동일한 작업을 했을 때 나온 1열의 예측값들을 묶어 S_train을 생성
   (기존 Ensemble은 S_train을 행별로 투표해서 분류함)

## 2nd Stage
4. 새로운 모델 생성 (1st Stage에서 사용한 것과 다른 모델 사용 가능)
5. S_train_X, train_Y를 가지고 새로운 모델을 Training

## Test Model
6. test_X를 1st Stage 모델에 넣고 결과로 나온 예측값들의 묶음 S_test를 생성
   (2nd Stage 모델의 학습 데이터는 원본 데이터와 다르기 때문에 test_X를 바로 넣으면 안됨)
7. S_train_X, train_Y를 2nd Stage 모델에 넣었을 때 결과를 가지고 Accuracy 계산

---

# Functional API

## Import Library

```python
from vecstack import stacking
```

## 1st Level Models

```python
models = [
    ExtraTreesClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3),
    RandomForestClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3),
    XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimators = 100, max_depth = 3)]
```

## Stacking

```python
S_train, S_test = stacking(models,
                           X_train, y_train, X_test,
                           regression = False,
                           metric = accuracy_score,
                           n_folds = 4, stratified = True, shuffle = True,
                           random_state = 0, verbose = 2)
```

- S_train과 S_test를 같이 생성 (y_test는 2차 모델 성능 평가에서만 사용)
- `metric`: Focus를 맞출 대상

## 2nd Level Model

```python
model = XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimators = 100, max_depth = 3, eval_metric='mlogloss')

model = model.fit(S_train, y_train)

y_pred = model.predict(S_test)
```

- `accuracy_score(y_test, y_pred)`를 확인하여 모델의 성능 평가

---

# Scikit-learn API

## Import Library

```python
from vecstack import StackingTransformer
```

## 1st Level Estimators

```python
estimators = [
    ('ExtraTrees', ExtraTreesClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3)),
    ('RandomForest', RandomForestClassifier(random_state = 0, n_jobs = -1, n_estimators = 100, max_depth = 3)),
    ('XGB', XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1, n_estimators = 100, max_depth = 3, eval_metric='mlogloss'))]
```

- `stacking`과 다르게 모델 이름과 모델 객체를 같이 튜플로 묶음

## StackingTransformer

```python
stack = StackingTransformer(estimators,
                            regression = False,
                            metric = accuracy_score,
                            n_folds = 4, stratified = True, shuffle = True,
                            random_state = 0, verbose = 2)
```

- `stacking`과 다르게 x data와 y data를 입력하지 않고 객체 자체를 모델처럼 사용

## Model Fitting

```python
stack = stack.fit(X_train, y_train)

S_train = stack.transform(X_train)
S_test = stack.transform(X_test)
```

- `stacking`은 새로운 데이터를 넣을 때 어려움이 있지만,   
  `StackingTransformer`는 전처리 도구처럼 사용 가능

## 2nd Level Estimator

```python
model = XGBClassifier(seed = 0, n_jobs = -1, learning_rate = 0.1,n_estimators = 100, max_depth = 3, eval_metric='mlogloss')
model = model.fit(S_train, y_train)

y_pred = model.predict(S_test)
```
