---
title: "[OSSCA] 2026 오픈소스 컨트리뷰션 아카데미 - Apache Airflow"
date: "2026-05-16T22:12:04+09:00"
layout: "post"
description: >
  2026 OSSCA 체험형 Git 활용 및 Apache Airflow 과정 1주차에서 Airflow UI 한글 번역에 참여한 경험을 정리합니다.
  남아 있던 8개 번역 문자열 분담, uv와 Breeze를 이용한 로컬 실행, PR #66080 제출과 리뷰 과정을 소개합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/tgnuwk2kzmmfflucmr2ld/ossca-00-cover.webp?rlkey=20s2fofpvio9gv37jy2ekgrm8&raw=1"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["OSSCA", "Apache Airflow", "Git", "Github", "Open Source", "Translation", "i18n", "Localization", "Breeze", "uv", "에어플로우", "오픈소스", "번역"]
series: ["오픈소스 컨트리뷰션 아카데미"]
---

{{< series "오픈소스 컨트리뷰션 아카데미" >}}

{{% hint info %}}
<i class="fa-solid fa-lightbulb"></i> 오픈소스 컨트리뷰션 아카데미 소개
- 오픈소스 컨트리뷰션 아카데미 **체험형 프로그램**은 오픈소스 프로젝트에 익숙하지 않은 예비 개발자를 위한 **6주 간**의 속성 컨트리뷰션 체험형 패키지입니다.
- 제가 참여한 **Git 활용 및 Apache Airflow** 과정은 Apache Airflow 프로젝트에 실제 개선 사항을 PR로 반영해보는 활동입니다.
- 이번 글에서는 1주차에 수행한 Airflow UI 한국어 번역 작업을 정리합니다.
- 아카데미 활동에 관심있다면 [해당 링크](https://www.contribution.ac/)로 이동하여 향후 일정을 확인할 수 있습니다.
{{% /hint %}}

2026 OSSCA 체험형 프로그램에서 Apache Airflow 트랙에 멘티로 참여하고 있습니다.

작년에도 OSSCA 체험형 프로그램으로 [PyTorch 문서 한글화](/blog/openup-handson)에 참여한적이 있었는데,
이번에는 제가 주로 사용하는 Apache Airflow 프로젝트에 기여하는 과정이 생겨서 한 번 더 신청했고
희망대로 멘티로 선정되었습니다.

## Git 활용 및 Apache Airflow 과정

이번 과정의 목적은 Apache Airflow 프로젝트에 기여를 함께 경험하는데 초점이 맞춰져 있었습니다.
작은 수정이라도 직접 브랜치를 만들고 커밋을 남기고 PR을 올리고,
다른 사람의 PR을 읽고 리뷰까지 남겨보는 흐름 전체를 체험하는 방식입니다.

작년 PyTorch 과정에서 한국어 공식 문서 번역을 경험했다면, 이번 Apache Airflow 과정은
UI를 포함한 실제 릴리즈에 좀 더 가까운 작업이라는 점이 달랐습니다.
첫 주차에는 비슷하게 번역 과제를 수행했는데 같은 번역이라도 웹 화면 어디에 노출되는지,
실제 맥락에서 어색하지 않은지, 그리고 변경 사항을 PR에 어떻게 증빙할지까지 함께 확인해야 했습니다.

> Apache Airflow 체험형 프로그램 과정을 소개하는 구글 슬라이드는
[이곳](https://docs.google.com/presentation/d/1VUAekTHNHvz_nONuYZpr__FP2EseyeNxzRFVYgMS_U8/edit?slide=id.p#slide=id.p)에서
확인할 수 있습니다.

## 오픈소스 컨트리뷰션 아카데미 발대식

합격 메일을 받은 후 멘토와 멘티들은 발대식에서 처음 만나게 됩니다.
작년에는 예비군 일정에 겹쳐서 발대식에 참석하지 못했는데,
이번에도 예비군 일정과 겹칠 뻔했지만 다행히 1주 차이로 일정이 갈라져 이번엔 참석할 수 있었습니다.

발대식은 서초역 인근에 있는 오픈업 센터에서 진행했습니다.
이후 [체험형] 프로그램도 OSSCA 과정을 지원하는 오픈업 센터에서 진행합니다.

![오픈업 센터 - GROUND 4](https://dl.dropboxusercontent.com/scl/fi/7grusphuwrl4udm4zca2k/ossca-01-openup-ground4.webp?rlkey=th0au7z687oihqs9hjigrslen&raw=1)

작년엔 모든 과정의 멘토, 멘티들이 모여서 발대식을 했다고 하는데,
이번에는 과정이 많아서 여러 날짜로 나눠 각 과정의 멘토, 멘티들끼리만 모였습니다.

발대식에서는 주최측으로부터 이번 [체험형] 프로그램에 대한 간단한 설명과,
향후 진행될 오픈소스 컨트리뷰션 아카데미 [참여형] 프로그램에 대한 안내를 받았습니다.
이후, 멘토와 대면하면서 Apache Airflow 과정에 대한 설명도 전달받았습니다.

## 1주차 - Airflow UI 번역

1주차 과제는 Airflow UI의 한국어 번역 문자열을 정리하는 작업이었습니다.

이미 대부분의 UI 문구가 번역된 상태였기 때문에 처음부터 대규모 번역을 하는 것은 아니었고,
남아 있던 TODO 문자열 몇 개를 참가자들이 나눠 맡아 실제 기여 흐름을 익히는 형태로 진행되었습니다.

번역 현황 요약 표를 보면 한국어 번역은 전체 821개 문자열 중 813개가 이미 반영되어 있었고, 남은 TODO는 8개뿐이었습니다.
파일 기준으로는 `components.json` 에 2개, `dag.json` 에 6개가 남아 있었습니다.
즉, 제한된 인원만 실제 번역 문자열을 1개씩 맡았고, 나머지 작업은 주석에서 `DAG` 표기를 `Dag` 로 맞추는 정리 작업 위주로 진행되었습니다.

![Translation Progress: ko - 813/821](https://dl.dropboxusercontent.com/scl/fi/7mw81mb7bhizjii782uj4/ossca-02-translation-progress.webp?rlkey=nzwccx9cbtsv7fvtilery4o7u&raw=1)

### 내가 맡은 문자열

제가 맡은 문구는 스케줄이 없는 DAG을 트리거할 때 백필 옵션에 마우스를 올리면 나타나는 툴팁이었습니다.
원문과 번역은 아래와 같습니다.

| 원문 | 번역 |
| :---: | :---: |
| This Dag's schedule does not support backfills | 이 Dag의 스케줄은 백필을 지원하지 않습니다. |

문장 자체는 짧지만, Airflow UI에서 이 메시지가 발생하는 맥락이 중요합니다.
여기서 백필(backfill)은 과거 논리적 날짜 구간을 대상으로 DAG을 다시 실행하는 기능인데,
스케줄이 없는 DAG은 그 특성상 백필을 지원하지 않기 때문에 해당 옵션이 비활성화되고 이를 툴팁으로 알려주는 것입니다.

### 로컬에서 실제 화면 확인하기

이번 과제에서 좋았던 점은 단순히 번역 문자열만 고치는 것으로 끝내지 않고,
실제로 로컬에서 Airflow UI를 띄워 변경 위치를 확인하는 과정까지 포함되어 있었다는 점입니다.

문자열 번역은 텍스트만 봐서는 자연스러워 보여도,
실제 화면에 얹어보면 길이나 어감, 띄어쓰기, 용어 통일이 달라 보일 수 있기 때문입니다.

덕분에 단순 번역이었다면 몇 초만에 끝날 작업이었겠지만, 이 문구가 어디서 나타나는지 확인하기 위해
Airflow UI의 실제 코드를 찾아보면서 조금이라도 그 구조를 이해하고 유용하게 시간을 보낼 수 있었습니다.

로컬 검증을 위해선 먼저 `uv`를 설치한 뒤 Breeze를 아래 명령어로 설치해야 합니다.

```bash
uv tool install -e ./dev/breeze
```

Breeze는 Airflow 개발자 및 기여자를 위해 제공되는 Docker 기반의 통합 개발 및 테스트 환경 도구입니다.
복잡한 환경 설정 없이도 Airflow를 빠르고 쉽게 실행할 수 있어 구성 요소를 수정하고 테스트하는데 편리함을 제공합니다.

Airflow 개발용 컨테이너를 실행하기 위해 아래 Breeze 명령어를 입력합니다.

```bash
breeze --backend postgres start-airflow --dev-mode --load-example-dags
```

여기서 `--load-example-dags` 옵션을 함께 준 이유는 번역이 실제로 보이는 예제 DAG 화면까지 바로 확인하기 위해서였습니다.

최초 실행은 컨테이너 이미지 다운로드와 초기 환경 구성이 한 번에 일어나서 약 30분 정도 걸렸습니다.

짧은 문자열 하나를 바꾸는 작업인데도 환경을 올리는 데 꽤 시간이 필요했지만,
이 과정 덕분에 Airflow 프로젝트에 기여한다는 것의 무게감을 느낄 수 있었습니다.

### 툴팁이 적용되는 위치

실제 확인은 `example_failed_dag` 화면에서 진행했습니다.

트리거 모달을 열면 `백필` 옵션이 비활성화되어 있고, 해당 영역에 마우스를 올렸을 때
기존에는 TODO 문구가 그대로 노출되다가 번역 후에는 자연스러운 한국어 문장으로 표시되는 것을 확인할 수 있었습니다.

이 부분은 PR에 캡처 이미지를 첨부하기에도 좋았습니다.

단순히 "문자열 하나를 바꿨습니다" 라고 설명하는 것보다, 번역 전에는 어떤 문구가 노출되었고
번역 후에는 실제 UI에서 어떻게 보이는지를 한 번에 보여줄 수 있었기 때문입니다.

> **번역 전**

![번역 전 - This Dag's schedule does not support backfills](https://dl.dropboxusercontent.com/scl/fi/yqrqxn5i5yr9lewbu2xvx/ossca-03-tooltip-todo-translate.webp?rlkey=5skjyagndom02u9uxzf8sj4be&raw=1)

> **번역 후**

![번역 후 - 이 Dag의 스케줄은 백필을 지원하지 않습니다.](https://dl.dropboxusercontent.com/scl/fi/p39xjo1aq1rwofkdujhpe/ossca-04-tooltip-translated.webp?rlkey=9rwmzxlgddr2v09adwqx7uz0y&raw=1)

### PR 올리기와 리뷰 남기기

수정한 내용은 [#66080](https://github.com/apache/airflow/pull/66080) PR로 올렸습니다.
문자열 하나를 번역한 작은 변경이었지만, 로컬에서 UI를 직접 확인하고 캡처까지 남긴 덕분에
어디가 어떻게 바뀌는지 PR만 읽어도 바로 이해할 수 있는 형태로 정리할 수 있었습니다.

![PR #66080](https://dl.dropboxusercontent.com/scl/fi/9esd1152ku0i5rodn1xz6/ossca-05-pr-66080-i18n.webp?rlkey=h5p0nrzvh2xek07phuvj3a3ax&raw=1)

이번 1주차에서 좋았던 점은 내 PR만 올리고 끝나는 구조가 아니었다는 점입니다.
다른 분들이 작업한
[#66088](https://github.com/apache/airflow/pull/66088),
[#66085](https://github.com/apache/airflow/pull/66085),
[#66084](https://github.com/apache/airflow/pull/66084),
[#66079](https://github.com/apache/airflow/pull/66079)
PR에도 `"LGTM"` 리뷰를 남겼습니다. 그 외에도 기존 PR과 중복되었음을 알리는 리뷰도 적었습니다.

아주 작은 리뷰였지만, 다른 사람의 작업을 읽어보고 검증하는 것 역시 오픈소스 협업의 중요한 일부라는 점을 첫 주부터 경험할 수 있었습니다.

![PR #66079 - 리뷰](https://dl.dropboxusercontent.com/scl/fi/6bgbjgaut6kipill8attk/ossca-06-pr-66079-review.webp?rlkey=tzb3ow3d4m8tjnsyuvjq4tdmf&raw=1)

## Airflow 3.2.2에 반영 예정

이번 1주차에 올라온 번역 작업들은 이후 [#66873](https://github.com/apache/airflow/pull/66873) PR을 통해
Apache Airflow 3.2.2 버전에 반영될 예정이라고 합니다.
짧은 문장 하나지만, 실제 릴리즈에 포함되어 더 많은 사용자에게 전달된다고 생각하니 기여의 무게감이 조금 다르게 느껴졌습니다.

UI 번역은 기능 추가처럼 눈에 띄는 변화는 아닐 수 있어도,
한국어 사용자 입장에서는 처음 Airflow를 접할 때의 진입장벽을 낮춰주는 꽤 실용적인 개선이라고 생각합니다.

![PR #66873 - 변경 사항](https://dl.dropboxusercontent.com/scl/fi/xmj5v54id8h2mcdmbti5n/ossca-07-pr-66873-changes.webp?rlkey=yulbnuevzgqgfk0ky88bhh71l&raw=1)


## 1주차를 돌아보며

작년 PyTorch 과정에서는 문서 번역과 렌더링 확인이 핵심이었다면,
이번 1주차 Airflow 번역 과정에서는 로컬 개발 환경을 올리고 실제 제품 UI에서 문자열 맥락을 확인하는 과정이 더 중요했습니다.

같은 번역 작업이어도 대상이 문서에서 제품 UI로 바뀌면 확인해야 할 범위가 이렇게 달라진다는 점을 1주차부터 체감했습니다.

결국 이번 작업은 문장 하나를 번역한 경험이라기보다,
오픈소스 프로젝트에서 작은 변경을 실제 사용자 화면까지 검증하고
PR로 연결하는 전체 흐름을 처음부터 끝까지 밟아본 경험에 더 가까웠습니다.
브랜치를 만들고, 로컬 환경을 준비하고, UI를 확인하고, 캡처를 남기고, PR을 올리고,
다른 사람의 PR에 리뷰를 남기는 과정이 한 번에 이어졌기 때문입니다.

다음 주차부터는 멘티들이 자발적으로 이슈를 탐색하면서 기여할 요소를 찾거나 직접 기능을 구현하는 작업이 진행됩니다.
저는 Airflow를 1년 이상 사용하고 있었고 사용 중 몇 가지 불편함을 느끼고 있어서
이참에 원하는 기능을 추가해보기로 방향을 잡았습니다.
글을 작성하는 시점에서 이미 마크다운 렌더링을 개선하는 PR을 하나 올리고 다양한 의견을 받았습니다.
다음에는 이 내용을 다루겠습니다.
