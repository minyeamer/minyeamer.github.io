---
layout: post
title: "[AI SCHOOL 5기] 딥러닝 실습 - TF Classification"
date: 2022-04-14 17:32:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Deep Learning, TensorFlow]
slug: aischool-07-02-tf-classification
draft: true
---

```python
from tensorflow.keras import datasets

(train_data, train_label), (test_data, test_label) = datasets.mnist.load_data()
```

- Keras에서 MNIST 데이터셋 가져오기

```python
import matplotlib.pyplot as plt

plt.imshow(train_data[0], cmap='gray')
```

- 첫번째 데이터에 들어있는 그림

이미지 데이터는 standard scaler 적용할 필요 없음

```python
from tensorflow.keras import utils

train_label = utils.to_categorical(train_label) # 0~9 -> one-hot vector
test_label = utils.to_categorical(test_label)
```

- keras 원핫인코딩
