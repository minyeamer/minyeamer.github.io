---
title: "[OSSCA] 2025 오픈소스 컨트리뷰션 아카데미 - PyTorch 문서 한글화 참여 후기"
date: "2025-10-28T23:23:55+09:00"
layout: "post"
description: >
  2025 OSSCA 오픈소스 컨트리뷰션 아카데미 [체험형-2차]에서 PyTorch 문서 한글화 프로젝트에 참여한 경험을 공유합니다.
  샘플 번역부터 통번역까지의 과정, RST 문법 이슈 해결, 용어집 추가, PR 리뷰 반영 등을 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/aznkzro8brx3fc2jukjx9/ossca-00-cover.webp?rlkey=kril9lwgp3t4qcktr8l3e537j&dl=0"
categories: ["Project", "Open Source"]
tags: ["OSSCA", "PyTorch", "OpenUp", "Open Source", "Translation", "RST", "Github", "파이토치", "오픈소스", "번역"]
---

{{% hint success %}}
<i class="fa-solid fa-lightbulb"></i> 오픈소스 컨트리뷰션 아카데미 소개
- 오픈소스 컨트리뷰션 아카데미 **체험형 프로그램**은 오픈소스 프로젝트에 익숙하지 않은 예비 개발자를 위한 **6주 간**의 속성 컨트리뷰션 체험형 패키지 입니다.
- 제가 참여한 **PyTorch 문서 한글화 프로젝트**는 파이토치 한국어 튜토리얼 문서를 번역하여 PR을 올리고 멘토/멘티로부터 리뷰를 받는 활동을 했습니다.
- 아카데미 활동에 관심있다면 [해당 링크](https://www.contribution.ac/)로 이동하여 향후 일정을 확인할 수 있습니다.
{{% /hint %}}

25년 9월 17일부터 10월 31일까지 6주간 OSSCA에 멘티로 참여하면서 경험한 과정을 공유드리고자 합니다.

## OSSCA 참가 신청

### 참여하게 된 계기

OSSCA라는 과정을 처음 알게 된 건 2025 파이콘의 OpenUp 부스를 접하게 된 것입니다.

평소에 오픈소스에 기여하는 활동을 동경했고, Github에 개인 프로젝트를 올리다 보면 오픈소스 단체로부터 메일을 받아 디스코드에 참가하는 경우도 있었습니다.
하지만, 아쉽게도 Github이란 도구를 통해서 팀 프로젝트를 진행한 경험이 없었고, PR을 올리는 법도 몰라 감히 기여해보겠다는 생각을 갖지 못했습니다.

그렇게 솔로 코딩만 해오던 저에게 OSSCA 과정은 오픈소스라는 영역에 첫 발을 내딛을 수 있는 기회가 될 것이라 생각했습니다.
더욱이, 체험형은 기간도 6주로 비교적 짧고 직장인도 참여할 수 있어서 부담없이 참가 신청하게 되었습니다.

### 프로젝트 선택

![OSSCA 체험형 프로그램 프로젝트 목록](https://dl.dropboxusercontent.com/scl/fi/hgsyav8yjoq0xoqlw90pz/ossca-01-projects.webp?rlkey=gx1og65bhox5o21n202ursz8q&dl=0)

이번 체험형 프로그램에는 PyTorch, MDN, Ubuntu, Yocto, Braillify 프로젝트 중 하나를 선택할 수 있었습니다.
내가 선택한다고 합격이 보장되는 건 아니지만, 그래도 개인적으로는 과거 딥러닝 모델을 학습하면서 활용한 PyTorch가 가장 익숙했고,
그 외엔 MDN과 Ubuntu가 아는 거라 눈에 띄었습니다.

참가 신청할 때 아마 2지망까지 고를 수 있었던 걸로 기억하는데, 1지망으로 PyTorch를 고르고 다음으로 MDN을 골랐을 것입니다.
다행히 1지망인 PyTorch 프로젝트에 합격하여 이번 6주 간의 과정을 완주하게 되었습니다.

### 디스코드 참여

아쉽게도 오프라인 발대식에는 개인 일정과 겹쳐서 참가하지 못했고,   
해당 일정 전에 OSSCA 디스코드에 초대받아 어떤걸 하게 될지 둘러보았습니다.

![OSSCA 디스코드 팀별 채널 입장](https://dl.dropboxusercontent.com/scl/fi/jzcxanqph2toa1opzjit1/ossca-02-discord.webp?rlkey=5uhscn4wjapisuqbyggculzfe&dl=0)

프로젝트 시작 전에 특별히 볼 건 없었고 팀별 채널에서 대화를 나누면서 향후 일정을 전달받게 되었습니다.

처음 미팅은 온라인으로 진행했고, 첫 번째 과제로 멘토님의 테스트 repo에서 샘플 번역할 것을 전달받았습니다.

## 1주차 - PyTorch 문서 샘플 번역

PyTorch 튜토리얼에는 advanced, beginner, intermediate, recipes 4가지 폴더가 있는데,
각 조별로 특정 폴더에 할당되어 개인 별로 폴더 내 문서 하나를 선택해 3줄 정도의 샘플 번역을 진행했습니다.

### PR 올리기

로컬에서 샘플 번역한 결과는 테스트 repo에 PR을 올리고 조원들 간에 PR 리뷰 댓글을 달았습니다.

![Github에서 첫 번째 PR 및 리뷰](https://dl.dropboxusercontent.com/scl/fi/2k12c5urpxrdunc3pzq9f/ossca-03-week1-pr.webp?rlkey=yqj6w1kqdam1plc987e16fhm2&dl=0)

저는 `advanced/generic_join.rst` 문서를 선택했고 조금 의욕이 들어 35줄 정도를 번역해서 올렸습니다.

클로드로 문서를 전체 번역한 후에 직접 한 줄씩 다듬는 방식으로 하다보니 이때 이미 번역 초안은 완성되어 있었습니다.
그래서, 마지막 주차에 문서 전체를 번역하는 과제에서 다시 해당 문서를 선택했습니다.

샘플 번역을 진행한 후엔 로컬에서 전체 튜토리얼을 렌더링하여
단순히 번역 퀄리티 뿐 아니라, reStructuredText 문법이 잘못된게 없는지 시각적으로 확인했습니다.

### 이슈사항 (1) - RST 문법

이 과정에서, 마크다운만 알다가 RST라는 형식을 작성하다 보니, 일부 문법의 차이에서 오는 오류를 경험했습니다.
대표적으로 인라인 코드블럭을 마크다운에서는 백틱(\`) 하나로 감싸서 표현했는데, RST에서는 백틱 2개로 감쌌습니다.
그리고, 백틱과 한글이 겹치면 외부 링크가 텍스트로 노출되어 보기에 좋지 않았습니다.

![PyTorch 튜토리얼 문서 렌더링](https://dl.dropboxusercontent.com/scl/fi/c99s2xckv2lif310zrrhb/ossca-04-week1-rendor.webp?rlkey=6hkj41gky49v53a3zb3k5nwdd&dl=0)

### 이슈사항 (2) - 한국어 문법

온라인 미팅에서
[PyTorchKorea 번역 가이드](https://github.com/PyTorchKorea/tutorials-kr/blob/master/TRANSLATION_GUIDE.md) 및
[번역 모범 사례](https://github.com/javascript-tutorial/ko.javascript.info/wiki/번역-모범-사례)를
공유 받았는데, 이 중에서 특히 신경써야 했던게 콜론(:)을 마침표(.)로 변환하는 규칙이었습니다.
평소에 특수문자 사용에 신경을 쓰지 않았다 보니, 그리고 개인적으로도 영어로 된 공식 문서를 자주 읽어 콜론 사용이 익숙하다 보니
처음 번역할 때 이러한 표현을 놓치는 경우가 많았습니다.

!["In this tutorial, you will see:" -> "이 튜토리얼에서는 다음을 다룹니다."](https://dl.dropboxusercontent.com/scl/fi/c1kswrpmj5dulx0bwsnjd/ossca-05-week1-changes.webp?rlkey=xv68qey3bvuo3k376ne1gj67e&dl=0)

### 이슈사항 (3) - 코드 블럭

마지막으로 겪었던 문제는 로컬에서 렌더링할 때 인라인 코드블럭이 아래 이미지처럼 공백 단위로 분리되어 보였습니다.

![\`join_hook(self,\` \`**kwargs)\` \`->\` \`JoinHook\`](https://dl.dropboxusercontent.com/scl/fi/s5gwp9weuxvmee640vuyo/ossca-06-week1-code1.webp?rlkey=6qhmftt2a3ygga957amgxf7hk&dl=0)

원문 튜토리얼과 샘플 번역한 문서 간에 인라인 코드블럭을 표현하는 문법에 차이가 없기 때문에
로컬에서 렌더링할 때만 발생하는 문제겠지만 그래도 거슬려서 해결해보기로 했습니다.

다행히 해당 사례에 대한 해결법이 Stack Overflow에 올라왔었고,
이를 참고하여 python 코드 블럭으로 인식하는 Role을 추가했습니다.
Role에 대한 설명은 [Sphinx 공식 문서](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html#roles)에서
확인할 수 있습니다.

{{< bookmark "https://stackoverflow.com/questions/10870719/inline-code-highlighting-in-restructuredtext" >}}

```python
.. role:: python(code)
    :language: python

- :python:`__init__(self, joinables: List[Joinable], enable: bool = True, throw_on_early_termination: bool = False)`
```

위와 같이 수정하고 다시 렌더링하니 아래 이미지처럼 보기 좋게 나타났습니다.   
하지만, 마지막 주차에서 번역할 때 원문과 형식을 맞추기 위해 해당 표현은 제외했습니다.

![\`join_hook(self, **kwargs) -> JoinHook\`](https://dl.dropboxusercontent.com/scl/fi/8gu8dka3otou9qzs0vavp/ossca-07-week1-code2.webp?rlkey=5qyr6u0m5z2jrv8l3o3yrfv6j&dl=0)

## 2주차 - 기존 문서 오탈자 수정

2주차 과제는 (1) 기존 문서 번역을 개선하고 (2) 용어집에 새 용어를 추가하는 2개의 활동을 전달받았습니다.

두 작업 간에 순서는 없지만, 중간에 추석 연휴가 끼어서 이번 과제를 3주차까지 진행했기 때문에 편의상 각각의 주차로 나눴습니다.

### 문법 오류 수정

기존 문서 번역을 개선하는 과제는 `advanced_source/rpc_ddp_tutorial.rst` 문서를 대상으로 진행했습니다.
분산 모델 병렬 처리를 결합하여 간단한 모델 학습시키는 방법에 대해 설명하는 문서인데,
번역 퀄리티를 개선할만한 점은 찾지 못했지만 [이슈사항 (1) - RST 문법](#이슈사항-1---rst-문법)에 해당하는
링크가 텍스트로 노출되는 이슈 사항을 해결했습니다.

!["\`여기 <https...>__\`에서" -> "\`여기 <https...>__\` 에서"](https://dl.dropboxusercontent.com/scl/fi/e9dm9fvnu3ez2w81nbc75/ossca-08-week2-typo.webp?rlkey=05ysmhykoh935wbz9pq9mawb7&dl=0)

[#1010](https://github.com/PyTorchKorea/tutorials-kr/pull/1010) PR을 올려 현재는 Merged 되었습니다.

## 3주차 - 용어집에 새 용어 추가

오탈자 수정과 동시에 진행한 용어집 추가 과제는
[PyTorch 튜토리얼 번역 가이드](https://github.com/PyTorchKorea/tutorials-kr/blob/master/TRANSLATION_GUIDE.md#용어-사용-규칙)에
적절한 단어를 등록하는 과제입니다.

### 용어 선정

OSSCA 프로그램 참가자들 간에 투표를 통해 추가될 용어를 선정하기 때문에
(즉, 충분한 투표를 받지 않으면 용어집에 등록될 수 없기 때문에)
아무 단어나 고르지 않고 PyTorch를 사용하는 모두가 알만한 단어를 찾으려 했습니다.

제가 선정한 단어는 `confusion matrix` 입니다.
정확도, 정밀도 등 모델의 성능 평가 시 사용되는 성능 지표를 도출할 때 바탕이 되는
참 긍정(TP), 거짓 긍정(FP) 수치를 나타낸 이 행렬은
PyTorch로 딥러닝 모델 학습을 해본 사람이라면 누구나 알만한 개념이라 생각했습니다.

### 이슈 올리기

물론, 제 생각만을 설득의 근거로 사용할 순 없기 때문에
아래 이미지와 같이 [#978](https://github.com/PyTorchKorea/tutorials-kr/issues/978) 이슈를 올리면서 실제 번역 사례를 제시했습니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/rfv4oagugifuazt3lgomv/ossca-09-week3-issue.webp?rlkey=4fpavcp4lpy64tmk5ebzhiey7&dl=0"
  alt="혼동/오차 행렬 번역 사례"
  max-width="750px"
  align="center" >}}

`confusion matrix` 는 "오차 행렬" 또는 "혼동 행렬" 이라고 번역되는 사례가 있는데,
비교적 공신력 있는 문서에서는 "혼동 행렬" 이라고 번역되는 사례가 많아서 후자를 선택했습니다.
PyTorch 튜토리얼에서 "오차 행렬" 이라고 번역된 사례가 있어 고민했지만,
개인이 번역한 문서보다는 위키나 논문에서 사용된 사례가 더 공신력 있다고 판단했습니다.

### 용어 투표

제안된 용어는 디스코드 채널에서 민주적으로 투표하여 선정했고,
제가 제안한 `confusion matrix` 도 채택되었습니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/hmsdnkm7fdq9tmf1remp1/ossca-10-week3-vote.webp?rlkey=tb650kys85utvhhkduczxtd6f&dl=0"
  alt="디스코드 용어 투표"
  max-width="400px"
  align="center" >}}

[#1009](https://github.com/PyTorchKorea/tutorials-kr/pull/1009) PR을 올려 현재 Merged 되었으며
[PyTorch 튜토리얼 번역 가이드](https://github.com/PyTorchKorea/tutorials-kr/blob/master/TRANSLATION_GUIDE.md#용어-사용-규칙)에서
아래 표와 같이 보여지고 있습니다.

<div class="center-table">

|영문|한글|작성자|추가 설명|
|---|---|:---:|---|
|...|...|...|...|
|CUDA|CUDA|박지은|번역안함|
|confusion matrix|혼동 행렬|김민엽||
|convolution|합성곱|김현길||
|...|...|...|...|

</div>

## 4~6주차 - PyTorch 문서 통번역

앞선 과제가 끝나고 다음 2주 동안은 PyTorch 튜토리얼에서 아직 번역되지 않은 문서를 선택해
통번역을 진행하는 과제를 수행했습니다.

물론, 제 선택은 1주차에 진행한 `advanced/generic_join.rst` 문서입니다.

2주 동안 진행되는 과제였지만, 이미 1주차에 만들어둔 번역 초안이 있어서 1주 내에 끝냈습니다.
에디터에서 영어 원문과 클로드가 한글로 번역한 문장을 비교해 보면서 어색한 표현을 고치는 방식으로 진행했습니다.
이후 마지막 주차에는 멘토분들이 PR 리뷰를 달아주며 번역 중 놓친 부분들을 추가로 개선했습니다.

![불균등한 입력에 대한 분산 학습을 위한 Join 컨텍스트 관리자(context manager) 사용 예시](https://dl.dropboxusercontent.com/scl/fi/qtggnxpepvwyeq6rrzbks/ossca-11-week4-changes.webp?rlkey=d692z6p7fa6gw8uuo0pbdz5pj&dl=0)

### 고려사항 (1) - 고유명사 구분

이번에 번역한 문서는 불균등한 입력이 주어지는 상황에서 분산 학습을 하기 위해
`Join Context Manager` 를 사용하는 예시를 안내합니다.
여기서 `Context Manager` 는 `컨텍스트 관리자` 라고 번역할 수 있는데,
`Join` 은 해당 문서에서 설명하는 컨텍스트 관리자를 나타내는 고유명사로 강조해야 한다고 판단해
(그리고 이에 대한 번역 사례도 없어서) 영문으로 표기했습니다.

또한, 번역을 하면 할수록 문서 전반적으로 `Join` 을 언급하는 경우가 많고,
예제의 클래스명이나 메서드명으로도 사용되어 더더욱 영문 표기가 맞다고 생각했습니다.

중간에 아래의 문장처럼 `join` 을 동사로 사용하는 경우도 있었는데 아래 한글 문장처럼 번역했습니다.

> \`\`Join\`\` is a context manager ... The context manager allows the ranks
that exhaust their inputs early (i.e. \*join\* early) to shadow the collective
communications performed by those that have not yet joined.

> \`\`Join\`\` 은 ... 컨텍스트 관리자입니다.
입력이 먼저 끝난 (즉, 먼저 \*join\* 된) 랭크는
아직 \*join\* 되지 않은 랭크가 수행하는 집합통신을 모방할 수 있게 됩니다.

원문에서 `join` 동사를 이탤릭체로 강조하기도 했고, 위와 같은 맥락에서 한글로 번역해버리면
(위 예시에서 "\*join\* early" 를 "먼저 참가된" 으로 번역하면)
문서에서 설명하는 고유명사 `Join` 과의 관련성을 잃어버릴 것 같아 영문으로 표기했습니다.
대신, 명사처럼 인라인 코드블럭으로 표현하지 않고 원문과 동일한 이탤릭체로 나타냈습니다.

### 고려사항 (2) - 링크 검증

문서를 번역할 때 다른 문서와 연결된 링크도 올바른지 확인했습니다.

연결된 페이지가 잘못된 경우는 없었지만, 한글로 번역된 페이지가 있음에도 원문으로 연결되는 경우 `[1]` 와,
영문 페이지의 특정 문단으로 향하는 앵커를 한글로 번역된 페이지 대상으로 그대로 사용하여 앵커가 동작하지 않는 경우 `[2]` 가 있었습니다.

두 가지 경우를 모두 충족하는 사례가 아래 문장입니다.

> In \`Getting Started with Distributed Data Parallel - Basic Use Case\`_, you saw
the general skeleton for using \`DistributedDataParallel\`_ to perform data
parallel training. This implicitly schedules all-reduces in each backward pass
to synchronize gradients across ranks.

> 분산 데이터 병렬 처리 시작하기 - 기본적인 사용법 \<https://tutorials.pytorch.kr/intermediate/ddp_tutorial.html#id3\>\`_ 에서,
\`DistributedDataParallel\`_ 을 사용한 데이터 병렬 학습의 기본 구조를
살펴보았습니다.

문장 도입부에 `Getting Started...` 링크는 렌더링되면서
[https://tutorials.pytorch.kr/intermediate/ddp_tutorial.html#basic-use-case](https://tutorials.pytorch.kr/intermediate/ddp_tutorial.html#basic-use-case)
로 연결되는데, 원문의 `Basic Use Case` 목차가 `기본적인 사용법` 이라고 번역되면서 `#basic-use-case` 앵커가 `#id3` 로 변환되었습니다.
따라서, 링크에 대한 표시 텍스트를 한글로 번역하는 김에 앵커도 한글로 번역된 문서에 맞게 직접 지정했습니다.

### PR 올리기 및 리뷰 반영

파이썬 코드를 포함해 450줄 분량을 번역했는데 작업량이 많다보니 놓치는 부분도 있었습니다.

[#1009](https://github.com/PyTorchKorea/tutorials-kr/pull/1009) PR을 올린 후에
멘티와 멘토들로부터 리뷰를 받아 추가로 반영했습니다.

예를 들어, 아래 이미지처럼 문장 끝에 마침표를 빼먹어 추가해야 함을 요청 받은 경우도 있고,
용어집과 다른 단어를 사용한 경우나 원문의 형식(공백 등)을 유지하지 않은 경우를 지적받기도 했습니다.

![긴 문서 번역하느라 고생 많으셨습니다. 다음과 같이 리뷰 드립니다.](https://dl.dropboxusercontent.com/scl/fi/gyj5ot23oosxzryt2t8zv/ossca-12-week4-review.webp?rlkey=42jjjauy71ee4tdn2921ekpaa&dl=0)

리뷰로 제안된 사항을 반영한 후 리뷰를 남긴 멘토님들에게 커밋 해시를 포함한 답변을 남겼습니다.
커밋 해시를 적으면 Github에서 커밋에 대한 변경사항을 보여주는 페이지로 링크를 달아줘서 편했습니다.

> 요청주신 변경사항은 새로운 커밋([`564104a`](https://github.com/PyTorchKorea/tutorials-kr/commit/564104add1b94cfc66d65b2ccec814f9f7b1dd7a))을 통해 반영되었습니다!

## 활동을 돌아보며

PyTorch 팀에서 튜토리얼 문서 번역을 통해 오픈소스에 기여하는 활동을 해보며,
PR 등 오픈소스에 기여하는 방식을 익히고 문서 번역 시에 고려해야 할 사항들을 배웠습니다.
오프라인 모임에서 직장인, 대학생 분들과 사소한 개발 토크를 나누며 네트워킹도 해보고,
매주마다 주어진 목표를 달성하는 성취감을 느낄 수 있어서 매우 보람찼습니다.

앞으로는 OSSCA와 마찬가지로 2025 파이콘에서 알게 된 Airflow 한국 사용자 모임에서
활동하며 PyTorch와 같은 오픈소스인 Airflow의 기능적 개선에 기여해보려 합니다.
OSSCA 과정은 제가 오픈소스에 기여하기 위한 첫 경험을 제공해주었고 이 경험은 앞으로도 잊지 않을 것입니다.
