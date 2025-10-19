---
layout: post
title: "[AI SCHOOL 5기] 텍스트 분석 실습 - 텍스트 데이터 분석"
date: 2022-03-25 19:09:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Text Analysis]
slug: aischool-02-02-text-data-exploration
---

# Tokenizing Text Data

## Import Libraries

```python
import nltk
from nltk.corpus import stopwords
from collections import Counter
```

## Set Stopwords

```python
stop_words = stopwords.words("english")
stop_words.append(',')
stop_words.append('.')
stop_words.append('’')
stop_words.append('”')
stop_words.append('—')
```

## Open Text Data

```python
file = open('movie_review.txt', 'r', encoding="utf-8")
lines = file.readlines()
```

## Tokenize

```python
tokens = []
for line in lines:
    tokenized = nltk.word_tokenize(line)
    for token in tokenized:
        if token.lower() not in stop_words:
            tokens.append(token)
```

---

# Counting Nouns

## POS Tagging

```python
tags = nltk.pos_tag(tokens)

word_list = []
for word, tag in tags:
    if tag.startswith('N'):
        word_list.append(word.lower())
```

## Counting Nouns

```python
counts = Counter(word_list)
print(counts.most_common(10))
```

> **Output**

```python
[('movie', 406), ('batman', 303), ('film', 284), ('joker', 219), ('dark', 136), ('ledger', 131), ('knight', 124), ('time', 112), ('heath', 110), ('performance', 87)]
```

---

# Counting Adjectives

## POS Tagging

```python
tags = nltk.pos_tag(tokens)

word_list = []
for word, tag in tags:
    if tag.startswith('J'):
        word_list.append(word.lower())
```

## Counting Adjectives

```python
counts = Counter(word_list)
print(counts.most_common(10))
```

> **Output**

```python
[('good', 141), ('best', 102), ('great', 78), ('many', 54), ('much', 52), ('comic', 43), ('real', 29), ('bad', 28), ('little', 26), ('new', 25)]
```

---

# Counting Verbs

## POS Tagging

```python
tags = nltk.pos_tag(tokens)

word_list = []
for word, tag in tags:
    if tag.startswith('V'):
        word_list.append(word.lower())
```

## Counting Verbs

```python
counts = Counter(word_list)
print(counts.most_common(10))
```

> **Output**

```python
[('see', 59), ('get', 54), ('made', 49), ('think', 46), ('seen', 45), ('make', 45), ('say', 41), ("'ve", 37), ("'m", 32), ('going', 31)]
```

---

# Visualizing Tokens

## Import Libraries

```python
import matplotlib.pyplot as plt
import re
```

## 정규표현식으로 토큰 분류

```python
tokens = []

for line in lines:
    tokenized = nltk.word_tokenize(line)
    for token in tokenized:
        if token.lower() not in stop_words:
            if re.match('^[a-zA-Z]+', token):
                tokens.append(token)
```

- 정규표현식 개념 소개 @ https://j.mp/3bJQJHg
- 정규표현식 기본 문법 정리 @ https://j.mp/3bLXSqB
- 상세한 정규표현식 설명 @ http://j.mp/2PzgFO8
- 상세한 정규표현식 예제 @ https://hamait.tistory.com/342
- 점프 투 파이썬 정규표현식 @ https://wikidocs.net/4308

## Visualizing Tokens

```python
plt.figure(figsize=(10, 3)) 
plt.title('Top 25 Words',fontsize=30)

corpus.plot(25)
```

## Top 25 Words Chart

![token-chart](https://github.com/minyeamer/til/blob/main/.media/study/ai-school/02-text-analysis/02-text-data-exploration/token-chart.png?raw=true)

---

# Similar Words

```python
print('Similar words : ')
corpus.similar('batman')
```

> **Output**

```bash
Similar words : 
superhero film action movie character better iconic seen acting actor heath performance modern difficult villain second end good come best
```

---

# Collocation

```python
print('Collocation')
corpus.collocation()
```

> **Output**

```bash
Collocation
Dark Knight; Heath Ledger; Christian Bale; comic book; Harvey Dent; Christopher Nolan; Bruce Wayne; Aaron Eckhart; Morgan Freeman; Gary Oldman; Batman Begins; Two Face; Gotham City; Maggie Gyllenhaal; Rachel Dawes; Michael Caine; special effect; Tim Burton; Jack Nicholson; dark knight
```