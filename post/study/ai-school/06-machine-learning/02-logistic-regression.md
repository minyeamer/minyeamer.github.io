---
layout: post
title: "[AI SCHOOL 5기] 머신 러닝 실습 - 로지스틱 회귀"
date: 2022-04-13 17:03:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Machine Learning, Logistic Regression]
slug: aischool-06-02-logistic-regression
---

# Logistic Regression
- 이진 분류(0 또는 1) 문제를 해결하기 위한 모델
- 다항 로지스틱 회귀(k-class), 서수 로지스틱 회귀(k-class & ordinal)도 존재
- **Sigmoid Function**을 이용하여 입력값이 양성 클래스에 속할 확률을 계산
- 로지스틱 회귀를 MSE 식에 넣으면 지수 함정의 특징 때문에 함정이 많은 그래프가 나옴
- 분류를 위한 Cost Function인 **Cross-Entropy** 활용
- 성능 지표로는 Cross-Entropy 외에 **Accuracy** 등을 같이 사용
- ex) 스팸 메일 분류, 질병 양성/음성 분류 등

## 양성/음성 분류 모델

<img src="https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/02-logistic-regression/positive-negative.png?raw=true" style="max-width:600px">

- 선형 모델은 새로운 데이터가 들어오면 양성/음성 판단 기준이 크게 바뀜
- 모델을 지수 함수인 **Sigmoid Function**으로 변경

## Sigmoid Function

<img src="https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/02-logistic-regression/sigmoid.png?raw=true" style="max-width:600px">

- θ 값에 따라 기울기나 x축의 위치가 바뀌는 지수 함수
- y축을 이동하는 선형 함수와 다르게 x축을 이동
- y가 0.5가 되는 지점을 기준으로 대칭되는 형태
- y값은 조건부 확률로 해석 (X가 있을 때 양성 클래스일 확률값)

## Cross-Entropy Function
- 예측값의 분포와 실제값의 분포를 비교하여 그 차이를 Cost로 결정
- 인공신경망에 각 행을 열단위로 쪼개 입력으로 넣었을 때 마지막에 카테고리 개수만큼의 수를 반환
- **Softmax Function**을 통과시키면 개수는 그대로지만 합쳤을 때 1이되는 숫자로 변경
- 인공신경망 결과로 뱉어낸 카테고리별 확률을 정답과 비교해 Cross-Entropy 계산
- One-Hot Encoding이 적용된 정답을 One-Hot Label이라 부름
- 정답 확률이 높고 오답 확률이 낮은 모델이 나은 모델
- Cross-Entropy는 하나의 분포를 다른 분포로 옮겨내는 거리라고도 불림

## Softmax Algorithm

$$S(y_i)=\frac{e^{y_i}}{\Sigma_j{e^{y_i}}}$$

- 다중 클래스 분류 문제를 위한 알고리즘
- 모델의 결과에 해당하는 점수를 각 클래스에 소속될 확률에 해당하는 값들의 벡터로 변환   
  (클래스 개수만큼의 숫자를 입력 받으면 합이 1이 되는 확률값으로 변환)

---

# ROC Curve
- Receiver Operating Characteristic Curve
- 얼마나 신호에 민감하게 반응할지를 그려낸 곡선
- Threshold를 끌어올리거나 끌어내리는 과정에서 발생
- Threshold를 끌어롤리면 양성 기준이 엄격해지고 끌어내리면 양성 기준이 너그러워짐
- 모델이 엄격할 때는 양성율이 낮지만 이를 억지로 끌어올리는 과정에서 위양성율이 발생
- 선이 직각일수록 이상적인 모델, 반면 모델의 성능이 안좋아 실수가 많으면 선이 아래로 내려옴

## Confusion Matrix

<img src="https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/02-logistic-regression/confusion-matrix.png?raw=true" style="max-width:700px">

- 분류 모델이 학습 결과를 뱉어낸 것을 바탕으로 만든 표
- 모델이 얼마나 혼동하고 있는지를 나타냄
- **Accuracy(정확성)**: (참긍정 + 참부정) / 총 예시 수
- **Recall(재현율)**: 정답에서 참인 것을 골라냄, TP / (FN + TP)
- **Precision(정밀도)**: 분류한 것들 중 정답을 골라냄, TP / (TP + FP)
- 스팸 메일 분류의 경우 정밀도를 높일 필요가 있음
- **F1-Score**: Recall과 Precision의 조화평균, 2RP / (R + P)
- **F-beta score**: Recall과 Precision에 가중치 부여

## AUC
- Area Under the ROC Curve
- ROC 커브 밑에 있는 영역의 크기
- 0.5에서 1 사이의 값이 나오며, 0.7 후반을 쓸만한 모델로 판단

---

# Learning Process

## Load Data
- `pd.read_excel()`로 엑셀 데이터 불러오기
- 엑셀 데이터를 `np.array()` 안에 넣어 Numpy Array 형태로 변경

## Select Feature
- 떨어진 열들을 꺼낼 때 `data[:, (5, 12)]` 형식으로 열을 꺼냄

## Training & Test Set

```python
from sklearn import model_selection

x_train, x_test, y_train, y_test = \
   model_selection.train_test_split(boston_X, boston_Y, test_size=0.3, random_state=0)
```

## Create Model

```python
from sklearn import linear_model

model = linear_model.LogisticRegression()
```

## Model Fitting

```python
model.fit(x_train, y_train)
```

## Model Predict

```python
model.predict(x_train)
```

## Accuracy

```python
from sklearn.metrics import accuracy_score

print(accuracy_score(model.predict(x_test), y_test))
```

## 양성/음성 확률

```python
model.predict_proba(x_test)
```

---

# Plot ROC Curve

```python
from sklearn.metrics import roc_curve, auc

fpr, tpr, _ = roc_curve(y_true=y_test, y_score=pred_test[:,1])
roc_auc = auc(fpr, tpr)
```

- `y_true`가 정답, `y_score`가 양성이 나올 확률
- `fpr`: ROC 커브를 그리기 위한 x좌표
- `tpr`: ROC 커브를 그리기 위한 y좌표

```python
plt.figure(figsize=(10, 10))

plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')

plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.title("ROC curve")

plt.show()
```

<div style="display:flex; justify-content:center;">
<img src="https://github.com/minyeamer/til/blob/main/.media/study/ai-school/06-machine-learning/02-logistic-regression/roc-curve.png?raw=true" style="max-width:700px">
</div>