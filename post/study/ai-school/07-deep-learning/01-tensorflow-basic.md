---
layout: post
title: "[AI SCHOOL 5기] 딥러닝 실습 - TensorFlow Basic"
date: 2022-04-14 17:28:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Deep Learning, TensorFlow]
slug: aischool-07-01-tensorflow-basic
draft: true
---

# TensorFlow
- 산술 연산 및 딥러닝을 위한 오픈 소스 라이브러리
- Python API를 제공하지만 실제 코드가 실행되는 환경은 C/C++
- GPU에서 일반 연산을 수행하게 하는 CUDA 확장기능 사용 가능
- TensorFlow.js: JavaScript로 딥러능 모델 로딩 및 예측 구현
- TensorFlow Lite: 모바일 앱을 위한 모델 경량화
- TensorFlow 2.0: Eager mode를 기본 문법으로 적용, 기능이 중복된 API 제거

## TensorFlow Two STeps
1. Building a TensorFlow Graph: Tensor들 사이의 연산 관계를 계산 그래프로 정의 및 선언 (Difinition)
2. Executing the TensorFlow Graph: 계산 그래프에 정의된 연산을 tf.Session을 통해 실행 (Execution)

## Tensor
- TensorFlow의 기본 자료 구조 및 타입을 가진 다차원 배열
- N-dimensional Matrix (벡터의 확장 개념)
- Scalar: rank-0 Tensor
- Vector: rank-1 Tensor
- Matrix: rank-2 Tensor

---

# TensorFlow 1.0

```python
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
```

## tf.Session()

```python
a = tf.add(3,5)
sess = tf.Session()
with tf.Session() as sess:
    print(sess.run(a))
```

- 그래프에서 연산을 실행하고 저장
- Thread와 비슷한 기능으로 사용 후 `close()`로 닫아야 함 (또는 `with`문 사용)

## Flow

```python
x = 2
y = 3
op1 = tf.add(x, y)
op2 = tf.multiply(x, y)
op3 = tf.pow(op2, op1)

with tf.Session() as sess:
    op3 = sess.run(op3)
    print(op3)
```

- 특정 Tensor(`op3`)를 실행 시 관련된 Tensor들(`op1`, `op2`)을 자동으로 실행
- 관계없는 Tensor를 무시하여 연산을 절약
- 여러 Tensor 실행 시 리스트로 묶음 (`sess.run([op3,op2])`)

---

# Gradient Descent Practice

## Prepare the data

```python
x_data = datasets.load_boston().data[:, 12]
y_data = datasets.load_boston().target
df = pd.DataFrame([x_data, y_data]).transpose()
```

## Build the model

```python
w = tf.Variable(tf.random_normal([1]))
b = tf.Variable(tf.random_normal([1]))

y_predicted = w * x_data + b
```

- `tf.Variable`: Parameter `θ`(`w`, `b`) 초기화, Gradient Descent의 대상
- `w * x_data + b`: 모델
- 랜덤하게 1개 꺼내기 (특정 행 꺼낼 시 `([1])` 대신 `[2,3]` 등과 같이 입력)

## Set the criterion

```python
loss = tf.reduce_mean(tf.square(y_predicted - y_data)) # MSE
optimizer = tf.train.GradientDescentOptimizer(0.001)
train = optimizer.minimize(loss)
```

## Train the model

```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(10000):
        sess.run(train)
        if step % 1000 == 0:
            print('Step {}: w {} b {}'.format(step, sess.run(w), sess.run(b)))
            print('loss {}'.format(sess.run(loss)))

    w_out, b_out = sess.run([w, b])
```

- `sess.run(tf.global_variables_initializer())`: `tf.Variables` 초기화
- `ses.run(train)`: 실제로 Gradient Descent가 실행되는 코드

## Visualize the result

```python
plt.figure(figsize = (10,10))
plt.plot(x_data, y_data, 'bo', label='Real data')
plt.plot(x_data, x_data * w_out + b_out, 'ro', label='Prediction')
plt.legend()
plt.show()
```

- `x_data * w_out + b_out`: 예측값

<!-- ![gradient-graph]() -->

---

# Neural Network Practice

## Build the data

```python
_x_data = tf.reshape(x_data, [len(x_data), 1])
_y_data = tf.reshape(y_data, [len(y_data), 1])

W1 = tf.Variable(tf.random_normal([1, 5], dtype=tf.float64))
W2 = tf.Variable(tf.random_normal([5, 10], dtype=tf.float64))
W_out = tf.Variable(tf.random_normal([10, 1], dtype=tf.float64))

hidden1 = tf.nn.elu(tf.matmul(_x_data, W1))
hidden2 = tf.nn.elu(tf.matmul(hidden1, W2))
output = tf.matmul(W2, W_out)
```

- `tf.reshape()`: 506행 데이터를 [506,1] 행렬로 변환
- `tf.matmul()`: 행렬곱
- TensorFLow의 Low-level API는 차원을 잘 맞춰주는 것이 중요

## Set the criterion

```python
loss = tf.reduce_mean(tf.square(output - _y_data))
optimizer = tf.train.AdamOptimizer(0.001)
train = optimizer.minimize(loss)
```

## Train the model

```python
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    for step in range(50000):
        sess.run(train)
        if step % 5000 == 0:
            print('Step {} || Loass : {}'.format(step, sess.run(loss)))

    output = sess.run([w, b])
```

## Visualize the result

```python
plt.figure(figsize = (10,10))
plt.plot(x_data, y_data, 'bo', label='Real data')
plt.plot(x_data, output, 'ro', label='Prediction')
plt.legend()
plt.show()
```

<!-- ![neural-graph]() -->

---

# Placeholders

## tf.placeholder()
- `X = tf.placeholder(tf.int64, shape=(None, 10))`
- 실제 Data가 담길 일종의 접시
- 용도에 따라 Data Type과 Shape를 선언하고 사용
- Batch Size 조정을 위해 행을 `None`으로 설정

## feed_dict
- `sess.run(train, feed_dict={X: X_data})`
- `sess.run()` 함수에게 전달하는 Placeholder와 실제 Data의 쌍
- Key에 해당하는 Placeholder는 고정하고 실행 단계에서 흘려보낼 Data만 입력