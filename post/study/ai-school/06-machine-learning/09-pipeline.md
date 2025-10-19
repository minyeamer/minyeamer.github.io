---
layout: post
title: "[AI SCHOOL 5기] 머신 러닝 실습 - Pipeline"
date: 2022-04-13 22:13:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Machine Learning, Pipeline]
slug: aischool-06-09-pipeline
---

# Feature Transformer

## Import Libraries

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
```

## ColumnTransformer

```python
numeric_features = ['CRIM', 'ZN', 'INDUS', 'NOX', 'RM', 'AGE', 'DIS', 'TAX', 'PTRATIO', 'B', 'LSTAT']
numeric_transformer = StandardScaler()

categorical_features = ['CHAS', 'RAD']
categorical_transformer = OneHotEncoder(categories='auto')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])
```

**`OneHotEncoder()`의 `handle_unknown` 설정**
- `error`: 숫자로 변환된 분류형 범주에 새로운 문자열 데이터가 들어올 경우 에러를 발생시킴   
- `ignore`: 카테고리에 해당되는 번호가 없으면 자동으로 0으로 바꿈

---

# Preprocessing-Only

```python
preprocessor_pipe = Pipeline(steps=[('preprocessor', preprocessor)])
```

- `steps`: 전처리 도구를 순서대로 적용 (모델도 입력 가능)

## Model Fitting

```python
preprocessor_pipe.fit(x_train)

x_train_transformed = preprocessor_pipe.transform(x_train)
x_test_transformed = preprocessor_pipe.transform(x_test)
```

- Numeric Variables에 대한 11개의 열,   
  Categorical Variables에 대한 2개의 열,   
  카테고리 별 One-Hot Encoding이 적용된 9개의 열을 함께 표시
- Pipeline을 통해 전처리를 진행할 경우 데이터를 원래대로 되돌리는 `inverse_trasnform` 불가능

---

# Preprocessing + Training

```python
from sklearn.ensemble import GradientBoostingClassifier

model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', GradientBoostingClassifier(n_estimators=200, random_state=0))])
```

- Preprocessing과 Training을 같이 묶을 경우 다른 모델을 끼워넣기 어려움
- 위 단점 떄문에 전처리만을 사용하는 것을 권장

---

# Preprocessing + Training + HPO

```python
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('classifier', GradientBoostingClassifier())])

param_grid = {
    'classifier__loss': ['deviance', 'exponential'],
    'classifier__learning_rate': [0.01, 0.001],
    'classifier__n_estimators': [200, 400],
    'classifier__min_samples_split': [2, 4],
    'classifier__max_depth': [2, 4],
    'classifier__random_state': [0]
}

grid_search = GridSearchCV(model, param_grid,
                           refit=True, cv=3, n_jobs=1, verbose=1, scoring= 'accuracy')
```
