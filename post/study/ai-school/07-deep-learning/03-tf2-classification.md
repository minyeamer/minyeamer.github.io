---
layout: post
title: "[AI SCHOOL 5기] 딥러닝 실습 - TF2 Classification"
date: 2022-04-14 17:32:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Deep Learning, TensorFlow]
slug: aischool-07-03-tf2-classification
draft: true
---

> Keras 모델 생성 방법
- Sequential
- Functional

- model.trainable = False
- 파라미터 세타 고정

- 사전 학습된 ConvNet을 이용한 전이 학습 (Tensorflow Official) @ https://j.mp/3bK0PXA

* Transfer Learning & Domain Adaptation @ http://j.mp/2XBsXsM
* (CodeLab) Your first Keras model, with transfer learning @ http://j.mp/2XAb8tt
* 사전 학습된 ConvNet을 이용한 전이 학습 (Tensorflow Official) @ https://j.mp/3bK0PXA

```python
model = models.Sequential() # Build up the "Sequence" of layers (Linear stack of layers)

# Dense-layer (with he-initialization)

model.add(layers.Dense(input_dim=8, units=256, activation=None, kernel_initializer=initializers.he_uniform())) # he-uniform initialization

# model.add(layers.BatchNormalization()) # Use this line as if needed
model.add(layers.Activation('elu')) # elu or relu (or layers.ELU / layers.LeakyReLU)

model.add(layers.Dense(units=512, activation=None, kernel_initializer=initializers.he_uniform())) 
model.add(layers.Activation('elu')) 

model.add(layers.Dense(units=512, activation=None, kernel_initializer=initializers.he_uniform())) 
model.add(layers.Activation('elu'))

model.add(layers.Dense(units=256, activation=None, kernel_initializer=initializers.he_uniform())) 
model.add(layers.Activation('elu')) 
model.add(layers.Dropout(rate=0.5)) # Dropout-layer

model.add(layers.Dense(units=2, activation='softmax')) # Apply softmax function on model's output
```

```python
model = models.Sequential() # Build up the "Sequence" of layers (Linear stack of layers)

# Dense-layer (with he-initialization)
model.add(layers.Dense(input_dim=13, units=64, activation=None, kernel_initializer=initializers.he_uniform())) # he-uniform initialization
# model.add(layers.BatchNormalization()) # Use this line as if needed
model.add(layers.Activation('elu')) # elu or relu (or layers.ELU / layers.LeakyReLU)

model.add(layers.Dense(units=64, activation=None, kernel_initializer=initializers.he_uniform())) 
model.add(layers.Activation('elu'))

model.add(layers.Dense(units=32, activation=None, kernel_initializer=initializers.he_uniform())) 
model.add(layers.Activation('elu'))
model.add(layers.Dropout(rate=0.4)) # Dropout-layer

model.add(layers.Dense(units=1, activation=None))
```
