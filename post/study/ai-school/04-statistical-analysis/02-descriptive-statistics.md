---
layout: post
title: "[AI SCHOOL 5기] 통계분석 실습 - 빈도 분석 & 기술통계량 분석"
date: 2022-04-02 22:09:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Statistics]
slug: aischool-04-02-descriptive-statistics
---

# Chart

## Pie Chart

```python
df['column'].value_counts().plot(kind = 'pie')
```

![pie-chart](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/pie-chart.png?raw=true)

## Bar Chart

```python
df['column'].value_counts().plot(kind = 'bar')
```

![bar-chart](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/bar-chart.png?raw=true)

---

# Descriptive Statistics
- `df['column'].max()`: 최댓값 (행방향 기준: `axis=1`)
- `df['column'].min()`: 최솟값
- `df['column'].sum()`: 합계
- `df['column'].mean()`: 평균
- `df['column'].variance()`: 분산
- `df['column'].std()`: 표준편차
- `df['column'].describe()`: 기술통계량

---

# 분포의 왜도와 첨도
- `df['column'].hist()`: 히스토그램

![job-histogram](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/job-histogram.png?raw=true)

- `df['column'].skew()`: 왜도 (분포가 좌우로 치우쳐진 정도)
- 왜도(Skewness): 0에 가까울수록 정규분포 (절대값 기준 3 미초과)   
  우측으로 치우치면 음(negative)의 왜도, 좌측으로 치우치면 양(positive)의 왜도
- `df['column'].kurtosis()`: 첨도 (분포가 뾰족한 정도)
- 첨도(Kurtosis): 1에 가까울수록 정규분포 (절대값 기준 8 또는 10 미초과)
- 왜도가 0, 정도가 1일 때 **완전한 정규분포**로 가정
- `sns.distplot(df['column'], rug=True)`: distribution plot   
  `rug`: 막대 그래프를 표시할지 여부

![sns-plot](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/sns-plot.png?raw=true)

- `sns.jointplot(x='column1', y='column2', data=df)`: 산점도와 히스토그램 한번에 표시

![joint-plot](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/joint-plot.png?raw=true)

- `sns.jointplot(..., kind="kde")`: 밀집된 분포 곡선을 표시

![kde-plot](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/kde-plot.png?raw=true)

---

# Outlier 탐지 및 제거
- `df.boxplot(column='column')`: 데이터 전체에 걸쳐서 분포 밀집도를 표시

![boxplot](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/boxplot.png?raw=true)

## IQR 활용
- IQR(Inter-Quantile Range): 바닥부터 75% 지점의 값 - 바닥부터 25% 지점의 값
- 상한치: 바닥부터 75% 지점의 값 + IQR의 1.5배
- 하한치: 바닥부터 25% 지점의 값 - IQR의 1.5배
- 상한/하한치를 넘으면 Outlier로 판단

```python
Q1 = df['column'].quantile(0.25)
Q3 = df['column'].quantile(0.75)

IQR = Q3 - Q1

df_IQR = df[ (df['column'] < Q3 + IQR * 1.5) & (df['column'] > Q1 - IQR * 1.5) ]
df_IQR.boxplot(column='column')
```

![outlier-boxplot](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/outlier-boxplot.png?raw=true)

## Outlier 제거 전후 분포 비교

## Histogram

|Before|After|
|:-:|:-:|
|![before](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/before.png?raw=true)|![after](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/after.png?raw=true)|

## Joint-Plot

|Before|After|
|:-:|:-:|
|![jointplot-before](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/jointplot-before.png?raw=true)|![jointplot-after](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/jointplot-after.png?raw=true)|

---

# Log 함수를 활용한 데이터 스케일링
- 왜도 혹은 첨도가 너무 큰 경우, Log 함수를 적용해 왜도/첨도를 낮춰주는 전처리를 적용
- `processed_df['log_column'] = np.log(processed_df['column'])`

|Before|After|
|:-:|:-:|
|![log-before](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/log-before.png?raw=true)|![log-after](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/04-statistical-analysis/02-descriptive-statistics/log-after.png?raw=true)|