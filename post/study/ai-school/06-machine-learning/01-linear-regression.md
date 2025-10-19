---
layout: post
title: "[AI SCHOOL 5기] 머신 러닝 실습 - 선형 회귀"
date: 2022-04-13 16:31:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Machine Learning, Linear Regression, Gradient]
slug: aischool-06-01-linear-regression
---

# Linear Regression
- 종속 변수 y와 독립 변수 x 사이의 선형 상관 관계를 모델링하는 회귀분석 기법
- 정답이 있는 데이터의 추세를 잘 설명하는 선형 함수를 찾아 x에 대한 y를 예측
- **Linear Combination (선형 결합)**: 더하기와 곱하기로만 이루어진 식
- **단순 회귀분석**: 1개의 독립변수(x)가 1개의 종속변수(y)에 영향을 미칠 때
- **다중 회귀분석**: 2개 이상의 독립변수(x)가 1개의 종속변수(y)에 영향을 미칠 때
- 선형 회귀는 가장 적합한 θ들의 집합을 찾는 것이 목표

## Cost Function
- 예측 값과 실제 값의 차이를 기반으로 모델의 성능(정확도)을 판단하기 위한 함수
- Objective (MIN or MAX) 함수 안에 Cost Function이 존재
- 선형 회귀에서는 **Mean Squre(d) Error Function (평균 제곱 오차 함수)** 활용
- MSE(Cost)가 최소가 되는 θ(a & b)를 찾아야하며,   
  이를 위한 최적화 기법으로 **Gradient Descent Algorithm (경사하강법)** 활용

## Mean Squre Error Function
- 회귀 분석을 위한 Cost Function
- y축 방향의 차이를 에러로 판단하는데 전체 에러를 단순하게 합칠 경우   
  양 에러와 음 에러가 상쇄되어 올바른 판단을 할 수 없음
- 부호를 제거하기 위해 모든 에러에 제곱을 취하고 그 평균을 구한 것이 MSE
- MSE(Cost)가 0에 가까울수록 에러가 적다고 판단
- 값에 제곱을 취하기 때문에 이상치가 있으면 영향을 많이 받아 이상치를 찾아내기 쉬움
- 제곱 대신에 절댓값을 사용하는 **MAE Function**은 이상치에 영향을 덜 받음

## Gradient Descent Algorithm
- Cost Function의 값을 최소로 만드는 θ를 찾아나가는 방법
- Cost Function의 Gradient(기울기)에 상수를 곱한 값을 빼서 θ를 조정
- 어느 방향으로 θ를 움직이면 Cost가 작아지는지 현재 위치에서 함수를 미분하여 판단
- 변수(θ)를 움직이면서 전체 Cost 값이 변하지 않거나 매우 느리게 변할 때까지 접근
- MSE를 미분했을 때 0이 나오는 지점을 찾아도 되지만, 빅데이터에서 x 데이터 역행렬이 오래걸림
- 그래프 중간에 함정처럼 페인 부분을 Local Minima라 부름 (목표점은 Global Minima)
- 가던 방향에서 조금 더 가는 발전된 Gradient Descent 기법을 통해 함정을 빠져나감
- Local Minima도 Global Minima와 비슷하게 떨어지기 때문에 에러가 적음

$$\text{repeat until convergence}\ \{ \theta_j:=\theta_j-{\alpha}\frac{\delta}{\delta\theta_j}J(\theta_0,\theta_1)\quad(\text{for}j=0\text{and}j=1) \}$$

- 계산식에서 J(θ0, θ1)는 MSE를 의미하며 이를 미분한 것에 ⍺를 곱함
- ⍺는 한 번 이동하는 길이를 결정하는 상수 (Step Size, 보폭, Learning Rate)
- ⍺와 같이 사람이 결정해야 하는 값을 **Hyper-Parameter**라 부름

## Hyper-Parameter
- 사람이 결정하는 파라미터, 모델 클래스 생성 시 집어 넣는 파라미터
- 모델을 선택하는 것, 인공신경망의 층을 몇개로 구성할 것인지 등
- Hyper-Parameter를 설정하는 것을 Model Tuning, Hyper-Parmas Tuning,   
  또는 Hyper-Parameter Optimizator(HPO)라 부름

## AutoML
- Hyper-Parameter Tuning을 컴퓨터에게 맡김
- Automated FE (Feature Engineering): 결측치 채움, x열(feature) 생성
- Automated MS (Model Selection)
- Automated HPO (Hyper Parameter Optimization)

---

# Learning Process

## Load Data
- `pd.read_excel()`로 엑셀 데이터 불러오기
- 엑셀 데이터를 `np.array()` 안에 넣어 Numpy Array 형태로 변경

## Select Feature
- Numpy Array는 2차원 행렬이어야 하기 때문에 `data[:, 1:2]` 형식으로 열을 꺼냄
  (`data[:, 1]`는 1차원 행렬을 반환)

## Training & Test Set

```python
from sklearn import model_selection

x_train, x_test, y_train, y_test = \
   model_selection.train_test_split(boston_X, boston_Y, test_size=0.3, random_state=0)
```

## Create Model

```python
from sklearn import linear_model

model = linear_model.LinearRegression()
```

## Model Fitting

```python
model.fit(x_train, y_train)
```

- `model.coef_`: a에 해당하는 θ 값
- `model.intercept_`: b에 해당하는 θ 값 (y 절편)

## Model Predict

```python
model.predict(x_train)
```

## MSE

```python
print(np.mean((model.predict(x_train) - y_train) ** 2))
```

```python
from sklearn.metrics import mean_squared_error

print(mean_squared_error(model.predict(x_train), y_train))
```

- Training Data와 Test Data의 MSE 차이를 원본 데이터와 함께 비교하여 Overfitting 판단
- 선형회귀는 성능을 기대하기 어려움

---

# Plot Linear Model

```python
plt.figure(figsize=(10, 10))

plt.scatter(x_test, y_test, color="black") # Test data
plt.scatter(x_train, y_train, color="red", s=1) # Train data

plt.plot(x_test, model.predict(x_test), color="blue", linewidth=3)

plt.show()
```

<div style="display:flex; justify-content:center;">
<img src="https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/01-linear-regression/linear.png?raw=true" style="max-width:700px">
</div>