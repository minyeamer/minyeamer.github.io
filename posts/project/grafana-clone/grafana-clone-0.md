---
title: "Grafana 클론코딩 #0 - Grafana 구조 분석과 개발 환경 만들기"
date: "2026-09-13T21:58:04+09:00"
layout: "post"
description: >
  Grafana를 AI와 함께 분석하며 React/TypeScript 프론트엔드, Go 백엔드,
  데이터 소스, DataFrame, 플러그인 구조를 초보자 눈높이에서 정리합니다.
  PostgreSQL과 Docker Compose로 BI 대시보드 클론코딩용 개발 환경을 구성한 기록입니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/zwq4u706rujc3ghn4w020/grafana-01-index.webp?rlkey=0n10p1u9ji3v11dgx3vxqrrcv&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/aemlct9pg86wza6kwd7da/grafana-00-logo.webp?rlkey=ud43ycrmipiugi9hjwfh1zmgp&raw=1"
categories: ["Project", "Grafana Clone"]
tags: ["Grafana", "Grafana 클론코딩", "대시보드 플랫폼", "BI 대시보드", "React", "TypeScript", "Go", "PostgreSQL", "Docker Compose"]
series: ["Grafana 클론코딩"]
---

{{< series "Grafana 클론코딩" "Grafana 클론코딩 #[0-9]+ - " >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Grafana는 모니터링 도구로 알려져 있지만,
PostgreSQL 같은 SQL 데이터소스를 연결하면 BI 대시보드의 기반으로도 사용할 수 있습니다.
그렇다면 대시보드 화면, 사용자 권한, 데이터소스 쿼리는 React와 Go 코드에서 어떻게 연결될까요?

이 글은 AI에게 Grafana의 구조를 먼저 질문하고, 실제 Grafana UI와 Network 요청,
소스 코드를 다시 확인하며 답을 찾는 클론코딩 기록의 시작입니다.
완성된 코드를 그대로 베끼기는 것을 목적으로 하기 보다,
향후 나만의 대시보드 플랫폼을 만들 때 필요한 구조를 직접 이해하는 데 초점을 맞춥니다.

- **[Grafana를 선택한 이유](#grafana를-선택한-이유)**: Grafana를 BI 대시보드 클론코딩의 참고 대상으로 고른 이유를 설명합니다.
- **[Grafana UI 둘러보기](#grafana-ui-둘러보기)**: PostgreSQL 데이터소스 연결부터 대시보드/패널 생성, 사용자 권한, 알림 설정까지 직접 확인합니다.
- **[Grafana 전체 구조](#grafana의-전체-구조)**: React 프론트엔드, Go 서버, 메타데이터 DB, 외부 데이터 소스가 어떤 역할을 나누는지 살펴봅니다.
- **[클론코딩 개발 환경](#클론코딩-개발-환경-만들기)**: PostgreSQL 데모 데이터와 React, Go, Docker Compose로 구성한 개발 환경을 소개합니다.
{{% /hint %}}

## 시작하며

저는 예전부터 회사에서 사용할 수 있는 BI 대시보드 플랫폼을 직접 만들어 보고 싶었습니다.
데이터베이스와 SQL을 다루는 일은 익숙하지만,
프론트엔드와 백엔드 애플리케이션을 바닥부터 설계하고 구현한 경험은 많지 않아
실천에 옮기기엔 어려웠습니다.

다행히 이제 AI를 활용하면 빠르게 UI와 API를 만들 수 있는 시대가 되었습니다.
저도 간간이 AI의 도움을 받아 오픈소스 프로젝트에 원하는 기능을 추가하는 기여를 한 경험이 있습니다.
이제는 바이브 코딩을 통해 생각만 하고 있었던 대시보드 플랫폼을 만들기로 마음먹었지만,
사용자 권한, 대시보드 버전 관리, 데이터소스 연결, 이벤트 알림 등
다양한 기능이 연결된 상용에 준하는 서비스를 구현하고 지속적으로 유지보수하려면
AI에게만 코드를 맡기기만 해선 부족하다고 생각했습니다.

그래서 바로 새로운 대시보드 플랫폼을 만들기보다, 이미 널리 사용되는
오픈소스 대시보드 플랫폼인 **Grafana**를 작은 단위로 클론코딩하며 직접 구조를 익히기로 했습니다.
Grafana와 똑같은 제품을 만들거나 기존 제품을 대체하는 것이 목표는 아닙니다.
대시보드가 화면에 나타나고 SQL이 실행되어 차트가 되는 과정에서
프론트엔드와 백엔드가 어떤 역할을 나누는지 이해하는 것이 목표입니다.

### Grafana란?

Grafana는 다양한 데이터소스의 결과를 조회하고,
이를 대시보드와 패널 형태로 시각화할 수 있는 오픈소스 플랫폼입니다.

일반적으론 서버 CPU나 메모리 사용량, 애플리케이션 오류율처럼 관측 데이터를 표시하는 도구로 많이 사용됩니다.
하지만 PostgreSQL, MySQL, ClickHouse 같은 SQL 데이터베이스도 데이터소스로 연결할 수 있어
매출액 또는 광고비처럼 배치로 적재되는 업무 데이터를 분석하는 BI 용도로도 활용할 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/v0wdtv5po81peifvp6l4a/grafana-02-edit-panel.webp?rlkey=0i1wuupzbc4y9hl3jhwpbzd42&raw=1"
  alt="Dashboards > New dashboard > Edit panel"
  caption="Grafana 패널 - 시계열 데이터로 Line chart 표현" >}}

하나의 **대시보드**에는 여러 패널을 배치할 수 있고, 각 **패널**은 데이터소스에 쿼리를 보내
표, 시계열 그래프, 스코어 카드, 막대 그래프 등으로 결과를 표현합니다.
또한 사용자와 조직, 폴더, 권한, 대시보드 저장과 버전 관리, 알림 기능도 함께 제공합니다.

### Grafana를 선택한 이유

대시보드 플랫폼으로는 Grafana 외에도 Kibana, Metabase, Apache Superset 같은 선택지가 있습니다.
각각 검색과 로그 분석, BI용 SQL 탐색, 데이터 시각화에 강점이 있어 목적에 따라 적합한 도구가 달라집니다.

![대시보드 플랫폼 - Grafana, Apache Superset, Kibana, Metabase](https://dl.dropboxusercontent.com/scl/fi/lsffavip53rj87q1bq4k1/dashboard-logos.webp?rlkey=4xi7x2lpqwz6i4rswavl9rq2j&raw=1)

저는 [**Grafana**](https://github.com/grafana/grafana)를 참고 대상으로 선택했습니다.
백엔드가 Go로 구현되어 있고, React 기반의 프론트엔드와 Go 서버가 비교적 명확하게 분리되어 있기 때문입니다.

특히, 백엔드를 중심으로 비교했을 때 [**Kibana**](https://github.com/elastic/kibana)는 Node.js,
[**Apache Superset**](https://github.com/apache/superset)은 Flask 기반으로 구현되어 있는데,
Node.js는 싱글 스레드의 한계로 대규모 트래픽 처리에 걱정도 있고 병렬 처리를 배울 수 없을 것 같아 제외하고
Flask는 러닝 커브가 가장 낮지만 동적 타입 언어의 한계로 안정성이 떨어질 것 같은 걱정에 제외했습니다.
마지막으로 [**Metabase**](https://github.com/metabase/metabase)의 경우 Clojure 언어로 구현되어 있는데,
배웠을 때 어디에 사용할지도 모르겠고 함수형 언어라는 특성까지 이해해야 해서 고려 대상에도 포함되지 않았습니다.

향후에는 선택하지 않은 대시보드 플랫폼들도 BI 대시보드 기능을 고도화하기 위해 참고할 계획이 있습니다.
대표적으로 **Apache Superset**은 관계형 DB 기반 BI 플랫폼의 핵심 모델인 데이터베이스, 데이터셋, 차트, 대시보드를
가장 정석적으로 다뤄서 좋은 참고 자료가 될 것으로 기대하고,
**Metabase**도 비개발자도 다루기 쉬운 UX를 참고하는 용도로 사용할 수 있을 것 같습니다.
**Kibana**는 대시보드 기능 그 자체보다는 Elasticsearch와 결합한 검색 기능 개선에 도움이 될 것으로 보입니다.

결론적으로, Go와 React를 중심으로 웹 프로덕트의 백엔드 및 프론트엔드 구조를 학습하기 위해 Grafana를 선택했습니다.

## Grafana를 어떻게 공부할 것인가

Grafana는 오래된 대형 오픈소스 프로젝트입니다.
저장소를 처음 열어 보면 TypeScript, React, Go, SQL, 플러그인 SDK, Docker, Kubernetes
관련 파일이 한꺼번에 보여서 어느 파일부터 읽어야 할지 알기 어렵습니다.

그래서 이번 공부에서는 제가 Grafana 구조를 처음부터 혼자 추측하지 않습니다.
먼저 AI에게 질문을 던져 전체적인 학습 지도를 만듭니다.

AI의 답변은 정답지가 아니라 **소스 코드를 읽기 위한 지도**로 사용합니다.
그 뒤에는 직접 Grafana UI를 눌러 보고,
브라우저의 Network 탭에서 HTTP 요청을 확인하고, 해당 문자열을 저장소에서 검색합니다.

예를 들어 Network 탭에서 `POST /api/ds/query`를 발견하면
`pkg/api` 경로에서 `"/ds/query"`에 해당하는 라우트를 찾고,
Handler가 호출하는 Go service를 따라갑니다.
이렇게 하면 수천 개의 파일을 순서대로 읽지 않아도 한 사용자 행동에 관련된 코드만 추적할 수 있습니다.

{{< bookmark "https://github.com/grafana/grafana" >}}

## Grafana UI 둘러보기

소스 분석 전에 Grafana 컨테이너를 올려서 직접 사용해 보았습니다.
사용자 입장에서 화면을 눌러 보고, 각 기능이 어떤 동작을 수행하는지 기록했습니다.

### 데이터 소스

데이터 소스는 **Connections** 메뉴에서 추가할 수 있습니다.
**"Add new connection"** 하위 메뉴를 클릭하면 Grafana에서 지원하는 다양한 데이터 소스 유형을 볼 수 있는데,
제가 미리 준비해둔 데모 데이터를 연결하기 위해 **PostgreSQL**를 선택했습니다.

![Connections > Add new connection](https://dl.dropboxusercontent.com/scl/fi/8k8x4ef335q0rl6bj4o3c/grafana-03-add-new-connection.webp?rlkey=9hot8zdremvxhdbyq80pzog42&raw=1)

PostgreSQL 데이터 소스를 추가하는 화면에서 **"Add new data source"** 버튼을 클릭하면
데이터 소스가 추가되면서 설정 편집 화면으로 이동합니다.

![Connections > Data sources](https://dl.dropboxusercontent.com/scl/fi/zys75u7hgo5o51qptvfua/grafana-04-data-sources.webp?rlkey=jse7wmy3k7oy7zmq6gnfci63s&raw=1)

화면에서 Host, 데이터베이스, 사용자명, 비밀번호를 입력하고 **"Save & test"** 버튼을 실행하면
PostgreSQL 데이터베이스 연결을 확인합니다. 연결에 성공하면 **"Database Connection OK"**
텍스트를 표시하면서 DB 연결 정보가 저장됩니다.

![Connections > Data sources > Save & test](https://dl.dropboxusercontent.com/scl/fi/6iiows894rswribkjqkuo/grafana-05-db-connection-ok.webp?rlkey=49vrewpgaszukx7vsn8ea4bil&raw=1)

### 대시보드와 패널

Grafana의 대시보드는 하나 이상의 패널을 배치한 화면입니다.
패널은 데이터를 표시하는 단위이며, 표, 시계열 그래프, 스코어 카드, 막대 그래프처럼 서로 다른 시각화를 선택할 수 있습니다.

대시보드는 **Dashboards** 메뉴에서 추가할 수 있습니다.
우측 상단의 `+` 아이콘을 클릭하고 **"New dashboard"** 링크를 클릭하면 대시보드 및 패널 추가 화면으로 이동합니다.

![Dashboards > New dashboard](https://dl.dropboxusercontent.com/scl/fi/c4y2plz8sccbtgvk7tp50/grafana-06-new-dashboard.webp?rlkey=amsx6x2ix94ofv58eb51gmosr&raw=1)

**"New dashboard"** 화면에 접속하면 우측에 **"Add new element"** 라벨을 가지는 `+` 아이콘이
자동으로 활성화되며 사이드바가 열려있습니다. 사이드바에서 Panel 아래 `+` 아이콘에 해당하는
**"Add new panel"** 버튼을 클릭하면 대시보드에 새로운 패널이 추가됩니다.

![Dashboards > New dashboard > Configure visualization](https://dl.dropboxusercontent.com/scl/fi/zz7jerhf13svlmnztp8oo/grafana-07-configure-visualization.webp?rlkey=hni48n4dtulnz4gp98rk1vijv&raw=1)

새로 추가된 패널에서 **"Configure visualization"** 버튼을 클릭하면 패널 편집 화면으로 이동합니다.
하단의 Quries 탭에서 데이터 소스와 조회할 칼럼을 선택하면 규칙에 맞게 쿼리가 자동으로 생성되지만,
저는 이 부분이 직관적이지 않아서 **"Run query"** 버튼 옆에 `Code` 탭을 클릭해 쿼리 편집기를 열고 SQL 쿼리를 입력했습니다.

그러고 나서 **"Run query"** 버튼을 클릭하면 대시보드에 표시할 그래프 미리보기가 만들어집니다.
데모 데이터는 2026년 7월 범위만 만들었기 때문에 조회 기간을 조정하면 최종적으로 제가 보여주고 싶은 Line chart가 나타납니다.

![Dashboards > New dashboard > Edit panel](https://dl.dropboxusercontent.com/scl/fi/exy4fhir4ky7ke38krerw/grafana-08-edit-panel.webp?rlkey=izqqgo3hvs5taubnl8eb2qalq&raw=1)

패널을 저장하기 위해 **"Save"** 버튼을 누르고 대시보드 페이지로 이동하면
아래와 같이 왼쪽 구석에 Line chart를 표시하는 패널이 위치하는 것을 확인할 수 있습니다.

![Dashboards > New dashboard + New panel](https://dl.dropboxusercontent.com/scl/fi/6rk8symj6kzc4egr1jodi/grafana-09-dashboard.webp?rlkey=rp4evrdgm51ermvzjqirnjyb5&raw=1)

다시 처음의 Dashboards 메뉴로 이동하면 새로 생성한 **New dashboard** 가 목록에 추가된 것을 볼 수 있습니다.
향후 대시보드가 많아진다면 **"New folder"** 기능으로 폴더를 추가해 여러 개의 대시보드를 묶어서 관리할 수 있습니다.

![Dashboards](https://dl.dropboxusercontent.com/scl/fi/syb01hq0oy5yqozay1fjl/grafana-10-dashboards.webp?rlkey=jmfc3ks24itweni83625bg5za&raw=1)

### 사용자 권한

Grafana에 접속할 때 사용자 계정으로 로그인해야 합니다.
사용자 계정은 **Administration** 메뉴에서 생성 및 관리할 수 있습니다.
Grafana 서비스를 실행하면 기본적으로 **admin** 사용자가 생성됩니다.

![Administration > Users and access > Users > All users](https://dl.dropboxusercontent.com/scl/fi/5yf4ut01ngjb5fli86s9m/grafana-11-all-users.webp?rlkey=yglt0s79su3221lntafhdphfg&raw=1)

**Users** 목록에서 **admin** 사용자를 클릭하면 편집 UI로 이동합니다.
사용자를 식별하기 위한 ID만 고정값이고 사용자명, 비밀번호, 이메일 등은 자유롭게 수정할 수 있습니다.
Organization 내에서 권한도 Viewer, Editor, Admin 중에서 하나를 지정할 수 있습니다.

![Administration > Users and access > Users > admin](https://dl.dropboxusercontent.com/scl/fi/g6ppuqndyv3bsexlojqmk/grafana-12-user-admin.webp?rlkey=luvq7tcr674l0cgg51n75a2kp&raw=1)

### 알림

**Alerting** 메뉴에서는 알림을 설정할 수 있습니다.

![Alerting](https://dl.dropboxusercontent.com/scl/fi/wwnvbztpvqkh79acec461/grafana-13-alerting.webp?rlkey=7pwt8mcze6jrhc5df0ftxn1mp&raw=1)

**Alert rules** 하위 메뉴에서 알림을 생성하거나 관리할 수 있습니다.

![Alerting > Alert rules](https://dl.dropboxusercontent.com/scl/fi/3oprz9ag3qffkxg528v7w/grafana-14-alert-rules.webp?rlkey=tp8i8blf7j3o7nnfdho9vh27z&raw=1)

**New alert rule** 버튼을 클릭해 새로운 알림 생성을 시도하면
데이터 소스와 쿼리를 입력하고 알림 조건을 정의할 수 있습니다.
그 외 알림 주기나 알림 메시지 등을 추가로 지정할 수 있습니다.

![Alerting > Alert rules > New alert rule](https://dl.dropboxusercontent.com/scl/fi/osq5lb0l5bqjuhfp00clj/grafana-15-new-alert-rule.webp?rlkey=l4g82y4c6x68lp4e50kwtir9p&raw=1)

## Grafana의 전체 구조

Grafana는 크게 브라우저에서 동작하는 프론트엔드, Go 서버, 메타데이터 DB, 그리고 외부 데이터 소스로 나눠 볼 수 있습니다.

```text
사용자 브라우저
└── React 화면 / Router / 상태 / Panel renderer
    ├── 대시보드 정의 요청
    └── 패널별 데이터 쿼리 요청

Go 서버
├── 인증 / 권한 / HTTP API / 도메인
│   └── 메타데이터 DB
│       └── 사용자, 조직, 데이터 소스 설정, 대시보드 JSON, 폴더, 버전 등
└── 서비스 / 플러그인 관리
    └── 외부 데이터 소스
        └── PostgreSQL, MySQL, Prometheus 등
```

여기서 가장 중요한 구분은 DB가 두 종류라는 점입니다.

| 구분 | 무엇을 저장하거나 조회하는가? | 예시 |
| --- | --- | --- |
| 메타데이터 DB | Grafana가 동작하기 위한 설정과 리소스 | 사용자, 데이터 소스 연결 정보, 대시보드 JSON 등 |
| 외부 데이터 소스 | 대시보드가 보여 줄 실제 데이터 | Prometheus의 CPU 메트릭, Loki의 로그 등 |

Grafana 자체는 기본 설정에서 SQLite를 메타데이터 DB로 사용할 수 있고,
운영 환경에서는 PostgreSQL이나 MySQL 같은 외부 데이터 소스를 사용할 수 있습니다.
앞선 UI 둘러보기 과정에서 패널이 참조하는 PostgreSQL도 사용자가 별도로 등록한 외부 데이터 소스입니다.
같은 DB라도 책임이 다르므로, 클론코딩 과정에서도 분리하기로 했습니다.

## 프론트엔드 구조

Grafana 프론트엔드는 TypeScript와 React를 기반으로 합니다.
현재 소스에서 먼저 볼 수 있는 경로는 `public/app/`입니다.

```bash
public/app/
├── index.ts    # 브라우저 앱 시작점
├── core/       # 공통 서비스, 네비게이션, 공통 컴포넌트
├── features/   # 대시보드 또는 알림 같은 기능별 코드
├── plugins/    # 기본 패널/데이터 소스 플러그인
├── routes/     # URL과 페이지 연결
├── store/      # Redux Toolkit 기반 전역 상태
└── types/      # 애플리케이션 타입
```

### 브라우저 앱은 어떻게 시작될까?

`public/app/index.ts`는 JavaScript bundle이 로드된 뒤 바로 모든 화면을 그리지 않습니다.
먼저 서버가 제공한 `grafanaBootData`를 기다리고,
사용자/조직/기능 플래그 같은 초기 정보를 준비한 뒤 `initApp()`을 호출합니다.

초보자 입장에서는 React 컴포넌트부터 실행된다고 생각하기 쉽지만,
실제 서비스에서는 로그인한 사용자와 설정에 따라 처음 보여 줄 화면이 달라집니다.
따라서 앱 초기화와 페이지 렌더링 사이에 `grafanaBootData` 단계가 존재합니다.

### 대시보드 주소와 화면 연결

대시보드 URL은 보통 아래와 같은 모양입니다.

```text
/d/:uid/:slug?
```

`uid`는 대시보드를 식별하는 값이고, `slug`는 사람이 읽기 쉬운 제목입니다.
`public/app/routes/routes.tsx`에서 URL은 대시보드(`dashboard`) 페이지로 연결되고,
페이지는 `uid`로 대시보드 정의를 가져옵니다.

프론트엔드는 기능별로 `features/` 아래에 코드를 모읍니다.
예를 들어 대시보드(`dashboard`)와 알림(`alerting`)은 서로 다른 기능이므로,
화면 컴포넌트와 API 호출, 상태 관리 코드도 가능한 한 같은 feature 경계 안에 둡니다.

### 상태는 한 곳에만 있지 않다

Grafana에는 React local state, Redux store, API cache, URL query string,
Scene object가 함께 존재합니다. 처음에는 복잡해 보이지만 상태의 수명에 따라 위치가 다릅니다.

- 모달 열림처럼 화면 하나에서 잠깐 쓰는 값은 React local state
- 서버에서 읽어 온 목록이나 설정은 API cache
- 네비게이션이나 알림처럼 여러 화면이 공유하는 값은 Redux store
- 시간 범위와 변수처럼 공유 링크에도 남아야 하는 값은 URL
- 여러 패널이 동시에 반응하는 대시보드 상호작용은 Scene object의 shared state

클론코딩에서는 이 구조를 모두 복사하지 않습니다.
먼저 React 화면과 URL, API 응답만으로 시작하고,
실제로 state가 복잡해질 때 필요한 구조를 추가할 예정입니다.

## 백엔드 구조

Grafana의 백엔드는 Go로 작성되어 있습니다.
브라우저에서 대시보드를 열거나 저장하면 프론트엔드는 Go 서버에 HTTP 요청을 보냅니다.
서버는 로그인한 사용자를 확인하고, 필요한 정보를 DB에서 읽거나 저장한 뒤 JSON으로 응답합니다.

대시보드 플랫폼에는 성격이 다른 두 종류의 데이터가 있습니다.
사용자, 폴더, 권한, 대시보드의 패널 배치와 설정은 메타데이터 DB에 저장합니다.
반면 판매수량이나 매출액처럼 차트에 표시할 실제 업무 데이터는 외부 데이터 소스에서 조회합니다.
Grafana 서버는 이 둘 사이에서 요청을 알맞은 곳으로 보내는 역할을 합니다.

Grafana 저장소에서는 백엔드 코드 대부분을 `pkg/` 아래에서 찾을 수 있습니다.

```bash
pkg/
├── api/          # 브라우저의 HTTP 요청을 받는 route와 Handler
├── server/       # 서버의 시작 및 종료와 필요한 기능의 조립
├── services/     # 대시보드, 데이터 소스, 쿼리, 사용자 기능의 처리 규칙
├── infra/        # DB 연결, log, metric, tracing 같은 공통 기술 기능
├── middleware/   # 인증과 같은 요청 전 공통 처리
├── plugins/      # 데이터 소스 플러그인을 찾고 실행 및 통신하는 기능
└── setting/      # 설정 파일과 환경 변수 읽기
```

### 서버는 어떻게 요청을 처리할까?

Grafana는 한 파일에서 모든 일을 처리하지 않습니다. `pkg/api`는 브라우저 요청을 처음 받고,
`pkg/services`는 대시보드 조회나 사용자 권한 확인처럼 실제 기능을 처리합니다.
DB 연결과 로그 기록 같은 공통 기능은 `pkg/infra`에,
로그인 확인처럼 모든 요청에 공통으로 필요한 처리는 `pkg/middleware`에 둡니다.

예를 들어 대시보드를 열면 API가 먼저 요청을 받고 사용자가 볼 수 있는 대시보드인지 확인합니다.
그다음 service가 메타데이터 DB에서 대시보드 정의를 찾습니다.
마지막으로 API는 찾은 결과를 JSON으로 바꿔 React 화면에 돌려줍니다.

```text
React 화면
  → API: 요청을 받습니다
  → service: 필요한 일을 처리합니다
  → DB: 데이터를 읽거나 저장합니다
  → JSON 응답
```

이렇게 역할을 나누면 기능이 늘어나도 코드를 찾기 쉽습니다.
대시보드를 찾는 규칙을 화면과 분리할 수 있으므로, 브라우저를 띄우지 않고도 그 규칙을 테스트할 수 있습니다.
이 구조가 익숙해지면 새로운 API를 추가할 때도 어느 폴더부터 살펴봐야 할지 판단할 수 있습니다.

### 차트 데이터 조회와 DataFrame

대시보드를 열면 먼저 패널의 제목, 위치, 데이터 소스 같은 설정을 가져옵니다.
이후 각 패널은 자신이 그릴 데이터를 별도로 요청합니다.
예를 들어 일별 매출 패널은 Go 서버를 통해 PostgreSQL에 SQL을 실행하고,
반환된 결과를 Time series나 Bar chart로 표시합니다.

패널은 차트나 표 하나를 보여 주는 화면 단위이고,
데이터 소스는 PostgreSQL이나 Prometheus처럼 실제 데이터가 있는 곳과 Grafana를 연결하는 기능입니다.
패널은 데이터 소스마다 다른 쿼리 언어를 직접 알 필요가 없습니다.
PostgreSQL에는 SQL, Prometheus에는 PromQL을 보내는 일은 데이터 소스가 맡습니다.

데이터 소스마다 결과 모양도 다릅니다. Grafana는 이를 DataFrame이라는 공통 형식으로 바꿉니다.
DataFrame은 이름과 타입을 가진 열에 데이터를 담은 표라고 생각하면 됩니다.
패널은 데이터 소스의 원래 형식 대신 DataFrame만 받아서 화면에 표시하므로,
데이터 소스와 패널을 각각 늘릴 수 있습니다.

```text
Panel
  ↓ 쿼리 요청
Data source
  ↓ DataFrame
Panel 렌더링
```

### 서버는 필요한 부품을 조립한다

`pkg/server`는 대시보드를 직접 조회하는 곳이 아니라, 서버가 시작할 때 필요한 부품을 준비하고 연결하는 곳입니다.
DB 연결, 설정, 인증 기능, 대시보드 service, HTTP API를 만든 뒤 서로 필요한 대상을 전달하고 서버를 실행합니다.
`pkg/setting`은 이 과정에서 환경 변수와 설정 파일을 읽어 포트나 DB 주소 같은 값을 제공합니다.

Grafana는 Wire라는 도구로 이런 조립 작업을 관리합니다. 처음에는 다소 거창해 보이지만 의미는 단순합니다.
대시보드 service가 DB 연결을 필요로 한다면, 서버가 시작할 때 DB 연결을 만들어 service에 전달하는 구조입니다.
필요한 부품을 함수 안에서 제각각 만들지 않으므로 테스트할 때는 실제 DB 대신 테스트용 구현으로 바꾸기도 쉬워집니다.

이번 클론코딩은 작은 단위에서 시작하므로 Grafana의 구조를 전부 복사하지 않습니다.
먼저 API 하나가 메타데이터 DB에서 대시보드를 읽어 JSON으로 돌려주는 흐름부터 만듭니다.
그다음 외부 데이터 소스 쿼리와 차트를 추가하고,
기능이 늘어날 때 API, service, DB 접근 코드를 필요한 만큼 나눌 예정입니다.

## 인프라와 플러그인 구조

Grafana 서버는 HTTP 요청만 처리하는 프로그램이 아닙니다.
실행에 필요한 설정을 읽고, DB에 연결하고, 로그와 성능 정보를 남기며,
필요한 경우 백그라운드 작업과 플러그인도 관리합니다.
이런 제품 전체에 공통으로 필요한 기능을 인프라라고 부릅니다.

```bash
pkg/
├── setting/   # 설정 파일과 환경 변수 읽기
├── infra/     # DB 연결, 로그, 성능 측정 같은 공통 기능
├── registry/  # 서버가 시작할 때 실행할 작업의 등록과 관리
└── plugins/   # 플러그인을 찾고 실행·통신하는 기능
```

이 중 `pkg/setting`과 `pkg/infra`는 비교적 쉽게 이해할 수 있습니다.
예를 들어 서버의 포트와 DB 주소는 환경 변수에서 읽고, DB 연결과 로그 기록은 여러 기능이 함께 사용합니다.
이런 공통 코드를 대시보드나 사용자 기능 안에 각각 작성하지 않고 한곳에 모아 둡니다.

플러그인은 Grafana가 모든 데이터 소스 기능을 서버 본체에 직접 넣지 않기 위한 확장 방식입니다.
어떤 플러그인은 브라우저에서 동작하는 화면 코드만 제공하지만,
DB 접속 정보처럼 민감한 값을 다루거나 외부 API와 통신해야 하는 플러그인은 Go 기반의 백엔드를
함께 가질 수 있습니다. Grafana 서버는 이런 백엔드 플러그인을 별도 프로세스로 실행하고 gRPC로 통신합니다.
플러그인 하나에 문제가 생겨도 Grafana 서버 전체가 함께 멈추지 않도록 하기 위한 구조입니다.

다만 이 구조는 많은 데이터 소스와 플러그인을 지원하는 Grafana에 필요한 설계입니다.
이번 클론코딩은 외부 플러그인 시스템을 만들지 않습니다.
처음에는 Go 서버가 PostgreSQL 하나에 직접 연결합니다.
이후 두 번째 데이터 소스가 실제로 필요해질 때,
공통 인터페이스를 만들고 PostgreSQL 구현을 그 안으로 옮기는 방식으로 확장할 예정입니다.

## 클론코딩 개발 환경 만들기

Grafana 구조를 바탕으로, 첫 단계에서는 복잡한 마이크로서비스 대신 작은 단일 애플리케이션을 만들었습니다.

```text
브라우저
└── React + TypeScript (localhost:5173)
    └── Go API (localhost:8080)

메타데이터 PostgreSQL (localhost:15431)
└── 이후 사용자, dashboard, datasource, 권한, version 저장

분석 PostgreSQL (localhost:15432)
└── 매출 데이터를 조회하는 analytics.profit_daily() 테이블 함수
```

{{< bookmark "https://github.com/minyeamer/dashboard-lab" >}}

### 데모 데이터 구성

클론코딩에서 사용할 분석 데이터는 실제 서비스의 마트 테이블을 단순화해 만든 가상 데이터입니다.
기간은 **2025-08-01 ~ 2026-07-31**까지로 잡았습니다. 1년치 일별 데이터가 있어
일/주/월 단위의 흐름, 기간 필터, 그리고 전년/전월 비교 같은 대시보드 기능을 연습할 수 있습니다.

상품은 식품팀과 가전팀의 **125개 상품**으로 구성했습니다.
브랜드는 `솔담건강`, `들꽃찬`, `모노에어`, `루미에르홈`, `한결웰빙`의 다섯 가지입니다.
쇼핑몰도 스마트스토어, 쿠팡, 11번가, G마켓, 옥션, 카카오톡 선물하기의 여섯 곳을 넣었습니다.
따라서 이후에는 브랜드별 매출 추이, 상품 카테고리별 이익,
쇼핑몰별 판매 점유율처럼 BI 대시보드에서 자주 보는 비교 차트를 만들 수 있습니다.

핵심 시계열인 `demo.sales_daily` 테이블에는 **39,684건**의 일별 판매 기록이 있습니다.
단순히 정상 주문만 넣지 않고 반품, 교환, 취소, 빈박스, 증정, 배송, 광고, 비용 상태도 함께 넣었습니다.
판매수량과 결제금액뿐 아니라 공급가, 원가, 배송비, 광고비, 기타 비용을 포함했기 때문에
매출뿐 아니라 마진과 영업이익을 계산할 수 있습니다.

`analytics.profit_daily(시작일, 종료일)` 테이블 함수는 판매 기록, 상품 정보, 쇼핑몰 정보,
추가 손익을 하나로 합쳐서 조회하기 쉽게 만들어 둔 함수입니다.
이 함수의 결과에는 날짜, 브랜드, 상품, 쇼핑몰, 주문 상태, 매출, 원가, 비용, 이익이 함께 들어 있습니다.

```sql
SELECT *
FROM analytics.profit_daily(
  DATE '2026-07-01',
  DATE '2026-07-31'
);
```

데이터는 `dashboard-lab/demo_db/` 경로에 CSV와 초기화 SQL로 함께 포함했습니다.
따라서 저장소를 내려받고 Docker Compose를 실행하면
별도의 파일 준비나 외부 DB 연결 없이 같은 데이터를 바로 조회할 수 있습니다.

### Docker Compose로 실행하기

저장소 루트에서 아래 명령을 실행하면 프론트엔드, 백엔드, 두 가지 PostgreSQL 컨테이너가 함께 시작됩니다.

```bash
cp .env.example .env
docker compose up --build
```

| 서비스 | 역할 | 포트 |
| --- | --- | --- |
| `frontend` | React 정적 화면 | `5173` |
| `backend` | Go HTTP API | `8080` |
| `metadata-db` | 메타데이터 설정 | `15431` |
| `analytics-db` | 매출/영업이익 분석 데이터 | `15432` |

이번 단계에서는 실제 대시보드 API는 아직 만들지 않았습니다.
`http://localhost:5173`에는 비어 있는 Dashboards 화면이 표시되고,
`http://localhost:8080/api/health`로 백엔드 상태를 확인할 수 있습니다.

```json
{
  "status": "ok",
  "phase": "0"
}
```

Docker 환경에서 4개의 컨테이너를 실제로 실행하여 React 빌드와 Go 헬스 체크 테스트를 통과했습니다.

```bash
% docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS                   PORTS               NAMES
835007e944a4   dashboard-lab-frontend   "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes             0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp     dashboard-lab-frontend-1
d6c752260563   dashboard-lab-backend    "/dashboard-lab-api"     1 minutes ago   Up 1 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp     dashboard-lab-backend-1
8b6e4e1397d3   postgres:16-alpine       "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes (healthy)   0.0.0.0:15431->5432/tcp, [::]:15431->5432/tcp   dashboard-lab-metadata-db-1
4896c0b43d44   postgres:16-alpine       "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes (healthy)   0.0.0.0:15432->5432/tcp, [::]:15432->5432/tcp   dashboard-lab-analytics-db-1
```

## 다음 작업

이번 회차에서는 Grafana를 살펴보고 개발 환경만 준비했습니다.
`dashboard-lab`에 작성한 React 프론트엔드와 Go 백엔드 코드 자체는 아직 자세히 분석하지 않았습니다.

다음 회차에서는 먼저 코드를 다시 읽으며 React 화면이 어떻게 시작되고,
Go 서버가 어떻게 HTTP 요청을 받아 응답하는지 확인할 예정입니다.
아직 기능이 거의 없는 작은 코드이므로, 프론트엔드와 백엔드가 연결되는 가장 단순한 구조를 이해하기에 적합합니다.

그다음 첫 번째 기능으로 대시보드 목록을 구현할 것입니다.
메타데이터 DB에 대시보드 정보를 저장하고, Go API가 목록을 JSON으로 반환하며,
React 화면이 그 결과를 목록으로 표시하는 흐름을 만들 계획입니다.
