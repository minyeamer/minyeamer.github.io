---
title: "Grafana 클론코딩 #1 - React와 Go 개발 환경 만들기"
date: "2026-09-15T23:56:38+09:00"
layout: "post"
description: >
  Grafana 클론코딩을 위한 React, Go, PostgreSQL, Docker Compose 개발 환경을 구성하고 코드를 분석합니다.
  Vite, JSX, Go ServeMux, JSON 응답, CORS를 따라가며 대시보드 플랫폼의 출발점을 만듭니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/c6utjr50c2rcz5hyyd280/grafana-clone-00-empty-state.webp?rlkey=9kbr4r9duc3yhdhf6ay7t0njy&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/aemlct9pg86wza6kwd7da/grafana-00-logo.webp?rlkey=ud43ycrmipiugi9hjwfh1zmgp&raw=1"
categories: ["Project", "Grafana Clone"]
tags: ["Grafana", "Grafana 클론코딩", "React", "TypeScript", "Go", "Go HTTP Server", "PostgreSQL", "Vite", "Docker Compose"]
series: ["Grafana 클론코딩"]
---

{{< series "Grafana 클론코딩" "Grafana 클론코딩 #[0-9]+ - " >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

[이전 글](/blog/grafana-clone-0/)에서 Grafana를 직접 사용해 보고
React, Go, 데이터소스, 메타데이터 DB가 나뉘는 큰 그림을 살펴봤습니다.
이번에는 `dashboard-lab` 개발 환경을 구성하고, 아주 작은 React와 Go 코드를 한 줄씩 읽습니다.

React의 `createRoot()`가 화면을 시작하고, Go의 `ServeMux`가 URL을 받아 JSON을 돌려주는 흐름을 살펴봅니다.
다음 글에서 대시보드 목록 API와 화면을 구현하기 전에, 각 기술이 어디에서 시작되고 어떻게 연결되는지 확인합니다.

- **[클론코딩 개발 환경](#클론코딩-개발-환경-만들기)**: `dashboard-lab`을 만들고 React, Go, 두 PostgreSQL과 데모 데이터를 Docker Compose로 구성합니다.
- **[React 프론트엔드 분석](#react-프론트엔드-분석)**: HTML의 `root` 요소, `main.tsx`, JSX, CSS, Vite와 Docker의 역할을 순서대로 살펴봅니다.
- **[Go 백엔드 분석](#go-백엔드-분석)**: 서버 시작점, 라우팅, health handler, JSON 응답, CORS, 테스트가 연결되는 흐름을 읽습니다.
- **[DB와 Docker Compose 연결](#db와-docker-compose-연결)**: 아직 DB를 사용하지 않는 Go 서버가 이후 DB에 연결될 준비를 어떻게 해 두었는지 확인합니다.
{{% /hint %}}

[이전 글](/blog/grafana-clone-0/)에서는 Grafana UI를 직접 눌러 보며
대시보드, 패널, 데이터소스가 어떻게 보이는지 확인했습니다. 이어서 Grafana의 프론트엔드와 Go 백엔드,
메타데이터 DB, 외부 데이터소스가 역할을 나누는 방식도 큰 흐름으로 정리했습니다.

이번 글부터는 `dashboard-lab`이라는 이름으로 작은 독립 프로젝트를 만들고,
Grafana에서 관찰한 흐름을 직접 구현해 봅니다.
처음에는 React 화면, Go API, 메타데이터 PostgreSQL, 분석용 PostgreSQL만 실행되는 빈 애플리케이션으로 시작합니다.

이번 글에서는 React와 Go를 처음 접하는 입장에서, 초기 코드가 어떤 역할을 하는지 AI와 함께 읽어 보겠습니다.
대시보드 목록과 상세 조회 기능은 다음 글에서 이 기반 위에 추가합니다.

AI에게 각 파일의 역할과 낯선 문법을 질문한 뒤,
답변을 그대로 믿기보다 코드와 실행 결과를 다시 대조하는 방식으로 읽었습니다.

## 클론코딩 개발 환경 만들기

먼저 `dashboard-lab`이라는 이름으로 클론코딩 프로젝트를 만들었습니다.

{{< bookmark "https://github.com/minyeamer/dashboard-lab" >}}

Grafana 구조를 바탕으로, 처음에는 복잡한 마이크로서비스 대신 작은 단일 애플리케이션을 구성했습니다.

```text
브라우저
└── React + TypeScript (localhost:5173)
    └── Go API (localhost:8080)

메타데이터 PostgreSQL (localhost:15431)
└── 이후 사용자, dashboard, datasource, 권한, version 저장

분석 PostgreSQL (localhost:15432)
└── 매출 데이터를 조회하는 analytics.profit_daily() 테이블 함수
```

### 분석용 데모 데이터 구성

클론코딩에서 사용할 분석 데이터는 실제 서비스의 마트 테이블을 단순화해 만든 가상 데이터입니다.
기간은 **2025-08-01 ~ 2026-07-31**까지로 잡았습니다. 1년치 일별 데이터가 있어
일/주/월 단위의 흐름, 기간 필터, 그리고 전년/전월 비교 같은 대시보드 기능을 연습할 수 있습니다.

상품은 식품과 가전 카테고리의 **125개 상품**으로 구성했습니다.
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
docker compose up --build -d
```

| 서비스 | 역할 | 포트 |
| --- | --- | --- |
| `frontend` | React 정적 화면 | `5173` |
| `backend` | Go HTTP API | `8080` |
| `metadata-db` | 메타데이터 설정 | `15431` |
| `analytics-db` | 매출/영업이익 분석 데이터 | `15432` |

Docker 환경에서 4개의 컨테이너를 실제로 실행하여 React 빌드와 Go 헬스 체크 테스트를 통과했습니다.

```bash
% docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS                   PORTS               NAMES
835007e944a4   dashboard-lab-frontend   "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes             0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp     dashboard-lab-frontend-1
d6c752260563   dashboard-lab-backend    "/dashboard-lab-api"     1 minutes ago   Up 1 minutes             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp     dashboard-lab-backend-1
8b6e4e1397d3   postgres:16-alpine       "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes (healthy)   0.0.0.0:15431->5432/tcp, [::]:15431->5432/tcp   dashboard-lab-metadata-db-1
4896c0b43d44   postgres:16-alpine       "docker-entrypoint.s…"   1 minutes ago   Up 1 minutes (healthy)   0.0.0.0:15432->5432/tcp, [::]:15432->5432/tcp   dashboard-lab-analytics-db-1
```

아직 실제 대시보드 API를 만들지는 않았습니다.
`http://localhost:5173`에는 비어 있는 Dashboards 화면이 표시됩니다.

![Dashboards > 아직 대시보드가 없습니다](https://dl.dropboxusercontent.com/scl/fi/c6utjr50c2rcz5hyyd280/grafana-clone-00-empty-state.webp?rlkey=9kbr4r9duc3yhdhf6ay7t0njy&raw=1)

헬스 체크 목적의 `http://localhost:8080/api/health` API로는 백엔드 상태를 확인할 수 있습니다.

```bash
curl http://localhost:8080/api/health
```

```json
{
  "status": "ok"
}
```


## React 프론트엔드 분석

프론트엔드 코드는 `frontend/` 아래에 있습니다.
React는 화면을 작은 컴포넌트 단위로 작성하는 라이브러리이고,
TypeScript는 JavaScript에 타입 검사를 더한 언어입니다.
Vite는 이 코드를 브라우저가 실행할 수 있는 파일로 변환하고,
개발 중 변경 사항을 빠르게 반영해 주는 도구입니다.

```bash
frontend/
├── index.html      # 브라우저가 처음 받는 HTML 문서
├── src/main.tsx    # React 앱의 시작점과 현재 화면
├── src/styles.css  # 화면 스타일
├── package.json    # React, Vite, TypeScript와 실행 명령
└── Dockerfile      # 프론트엔드 컨테이너 실행 방법
```

### HTML에서 React 화면까지

브라우저는 먼저 아래 `index.html`을 받습니다.
`<div id="root"></div>`는 아직 비어 있는 상자이고,
마지막의 `<script type="module" src="/src/main.tsx"></script>`가
`main.tsx`를 불러옵니다. 여기까지가 HTML의 역할입니다.
실제 화면을 만드는 React 코드는 다음 절에서 살펴보겠습니다.

```html
<!-- frontend/index.html -->
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>dashboard-lab</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### App 컴포넌트와 JSX

이제 `main.tsx`를 살펴보겠습니다. 이 파일은 세 가지 일을 합니다.
먼저 `styles.css`를 불러오고, 다음으로 `App` 함수에서 화면 모양을 정의하며,
마지막으로 HTML의 `root` 상자에 `App`을 연결합니다.
코드의 맨 아래 `createRoot(...)`가 HTML과 React를 잇는 연결 지점이라고 볼 수 있습니다.

현재 화면은 아무 기능이 없는 정적 페이지를 만들기 때문에 전체 코드는 짧습니다.
`main.tsx`와 화면 스타일을 탭으로 함께 보겠습니다.

{{< tabs "frontend-source" >}}

{{% tab "main.tsx" %}}
```tsx
// frontend/src/main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import './styles.css';

function App() {
  return (
    <main>
      <header>
        <p className="eyebrow">dashboard-lab</p>
        <h1>Dashboards</h1>
        <p>Grafana의 공개된 흐름을 독립적으로 재구현하는 학습 환경입니다.</p>
      </header>
      <section aria-labelledby="empty-state-title" className="empty-state">
        <h2 id="empty-state-title">아직 대시보드가 없습니다</h2>
        <p>대시보드 목록과 `/d/:uid` 조회를 구현할 예정입니다.</p>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```
{{% /tab %}}

{{% tab "styles.css" %}}
```css
/* frontend/src/styles.css */
:root {
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #1f2937;
  background: #f7f8fa;
}

* { box-sizing: border-box; }
body { margin: 0; }
main { margin: 0 auto; max-width: 960px; padding: 72px 24px; }
h1, h2, p { margin-top: 0; }
h1 { font-size: 2.25rem; margin-bottom: 12px; }
.eyebrow { color: #6b7280; font-size: 0.875rem; font-weight: 600; }
.empty-state { background: #fff; border: 1px solid #e5e7eb; border-radius: 8px; margin-top: 40px; padding: 36px; }
.empty-state h2 { font-size: 1.25rem; }
.empty-state p, header > p { color: #4b5563; }
```
{{% /tab %}}

{{< /tabs >}}

HTML처럼 보이지만 `App` 함수 안의 내용은 TypeScript 파일에 작성한 JSX입니다.
JSX는 화면 구조를 표현하는 문법이며, Vite가 브라우저가 이해하는 JavaScript로 변환합니다.
HTML의 `class` 대신 `className`을 쓰는 점도 JSX의 특징입니다.
`styles.css`의 `.empty-state` 선택자는 이 `className`을 찾아 카드 모양의 배경, 테두리, 여백을 적용합니다.

코드 마지막의 `document.getElementById('root')`는 앞 절의 HTML에서 `root` 상자를 찾습니다.
`createRoot()`는 그 상자를 React가 관리할 화면 영역으로 바꾸고,
`<App />`은 위에서 정의한 `App` 함수를 그 안에 표시합니다.
`<App />`을 감싸는 `StrictMode`는 사용자에게 보이는 UI를 추가하는 컴포넌트가 아닙니다.
개발 중 문제가 될 수 있는 오래된 방식이나 예상하지 못한 부작용을 더 쉽게 발견하도록 React가 검사하는 도구입니다.

아직은 `App` 하나로 충분하지만, 목록과 상세 페이지가 생기면 모든 코드를 이 함수에 계속 넣을 수는 없습니다.
다음 구현부터는 대시보드 목록을 보여 주는 컴포넌트와 API 요청 코드를 분리할 이유가 생깁니다.

### package.json과 Dockerfile

`package.json` 파일은 프론트엔드 프로젝트가 사용하는 도구와 실행 명령을 기록한 파일입니다.
`npm run dev` 명령어는 Vite 개발 서버를 실행하고,
`npm run build` 명령어는 TypeScript 검사 뒤 배포용 파일을 만듭니다.
Dockerfile은 같은 실행 환경을 컨테이너 안에 만듭니다.

{{< tabs "frontend-setup" >}}

{{% tab "package.json" %}}
```json
{
  "name": "dashboard-lab-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite --host 0.0.0.0",
    "build": "tsc -b && vite build"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "react": "latest",
    "react-dom": "latest",
    "vite": "latest"
  },
  "devDependencies": {
    "@types/react": "latest",
    "@types/react-dom": "latest",
    "typescript": "latest"
  }
}
```
{{% /tab %}}

{{% tab "Dockerfile" %}}
```dockerfile
# frontend/Dockerfile
FROM node:22-alpine

WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev"]
```
{{% /tab %}}

{{< /tabs >}}

`--host 0.0.0.0` 옵션은 컨테이너 밖의 브라우저에서도 Vite 서버에 접속할 수 있게 합니다.

이번 단계에서 중요한 것은 React가 특별한 서버에서만 동작하는 것이 아니라는 점입니다.
React는 `main.tsx`에서 시작해 브라우저의 `root` 요소에 HTML을 그립니다.
API에서 받은 데이터도 결국 이 화면을 다시 그리는 데 사용하게 됩니다.

## Go 백엔드 분석

백엔드 코드는 `backend/cmd/api/main.go` 파일에서 시작합니다.
Go에서는 실행 가능한 프로그램의 시작점을 `package main`과 `func main()`으로 정합니다.
React의 `main.tsx`가 브라우저 앱의 출발점이라면, Go의 `main()`은 서버 프로그램의 출발점입니다.

```bash
backend/
├── cmd/api/main.go       # HTTP 서버 시작과 health API
├── cmd/api/main_test.go  # health API 테스트
├── go.mod                # Go 모듈과 Go 버전
└── Dockerfile            # Go 바이너리 빌드와 컨테이너 실행
```

`go.mod` 파일은 이 디렉터리가 하나의 독립 Go 모듈이라는 정보와 사용할 Go 버전을 기록합니다.
백엔드 Dockerfile은 Go로 실행 파일을 만든 뒤, 더 작은 Alpine 이미지에서 그 실행 파일만 실행합니다.

{{< tabs "backend-setup" >}}

{{% tab "go.mod" %}}
```go
module github.com/minyeamer/dashboard-lab/backend

go 1.26.3
```
{{% /tab %}}

{{% tab "Dockerfile" %}}
```dockerfile
# backend/Dockerfile
FROM golang:1.26-alpine AS build

WORKDIR /app
COPY go.mod ./
COPY cmd ./cmd
RUN go build -o /dashboard-lab-api ./cmd/api

FROM alpine:3.22
RUN addgroup -S app && adduser -S app -G app
USER app
COPY --from=build /dashboard-lab-api /dashboard-lab-api
EXPOSE 8080
ENTRYPOINT ["/dashboard-lab-api"]
```
{{% /tab %}}

{{< /tabs >}}

### main 함수와 HTTP 서버

`main.go` 파일은 네 부분으로 나뉩니다. import는 필요한 Go 기능을 가져오고,
`healthResponse`는 응답 JSON의 모양을 정합니다.
`main()`은 서버를 설정하고 시작하며, `health`와 `cors`는 요청을 처리하는 작은 기능입니다.

먼저 전체를 훑어 본 뒤, 서버 시작과 JSON 응답 부분을 차례로 살펴보겠습니다.

```go
// backend/cmd/api/main.go
package main

import (
  "encoding/json"
  "log"
  "net/http"
  "os"
)

type healthResponse struct {
	Status string `json:"status"`
}

func main() {
  port := os.Getenv("APP_PORT")
  if port == "" {
    port = "8080"
  }

  mux := http.NewServeMux()
  mux.HandleFunc("GET /api/health", health)

  server := &http.Server{
    Addr:    ":" + port,
    Handler: cors(mux),
  }

  log.Printf("dashboard-lab API listening on %s", server.Addr)
  log.Fatal(server.ListenAndServe())
}

func health(w http.ResponseWriter, _ *http.Request) {
  w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(healthResponse{Status: "ok"})
}

func cors(next http.Handler) http.Handler {
  return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Access-Control-Allow-Origin", "http://localhost:5173")
    next.ServeHTTP(w, r)
  })
}
```

`main()`은 먼저 `APP_PORT` 환경 변수를 읽고, 값이 없으면 `8080`을 기본 포트로 사용합니다.
환경 변수로 값을 받으면 로컬, Docker, 운영 환경에서 코드를 바꾸지 않고도 포트 같은 설정을 조정할 수 있습니다.

그다음 `http.NewServeMux()`로 URL별 처리 함수를 등록할 수 있는 표지판을 만듭니다.
`mux.HandleFunc("GET /api/health", health)`는 `GET /api/health` 요청이 들어오면
`health` 함수를 실행하도록 등록합니다.

`http.Server`는 포트와 처리기를 묶어 실제 서버를 만듭니다.
`ListenAndServe()`를 호출하면 프로그램은 8080 포트에서 브라우저 요청을 기다립니다.
여기까지가 서버를 켜는 코드이고, 실제 응답 내용은 `health` 함수가 담당합니다.

### JSON 응답과 Handler

`health` 함수는 Go의 HTTP Handler입니다. Handler는 요청을 받아 응답을 만드는 함수입니다.
이 API는 아직 DB를 읽지 않고, 서버가 실행 중이라는 사실만 JSON으로 돌려줍니다.

위 코드의 `healthResponse` 구조체에 있는 `Status`는 Go 코드에서 쓰는 필드 이름입니다.
뒤의 `json:"status"` 같은 태그는 JSON으로 바꿀 때 사용할 이름을 지정합니다.
그래서 브라우저는 Go의 대문자 필드 이름 대신 아래처럼 소문자 JSON을 받습니다.

```json
{
  "status": "ok"
}
```

`w.Header().Set("Content-Type", "application/json")` 헤더는 응답이 JSON이라는 정보를 브라우저에 알립니다.
이어서 `json.NewEncoder(w).Encode(...)`가 구조체를 JSON 문자열로 변환해 응답에 씁니다.
대시보드 목록 API도 같은 방식으로 Go 구조체 또는 목록을 JSON으로 반환하게 됩니다.

### CORS와 테스트

현재 React 개발 서버는 5173 포트, Go API는 8080 포트에서 실행됩니다.
포트가 다르면 브라우저는 두 주소를 다른 출처로 봅니다.
`cors` 함수는 `Access-Control-Allow-Origin` 응답 헤더를 추가해
`http://localhost:5173`에서 온 React 화면의 요청을 허용합니다.

이 구현은 지금의 단순한 `GET` 요청에는 충분하지만,
로그인 정보나 여러 HTTP 메서드를 다루는 운영용 CORS 구현은 아닙니다.
기능이 늘어나면 허용할 출처, 메서드, 헤더를 명시적으로 관리해야 합니다.

`main_test.go` 테스트 코드는 서버를 실제 포트에 띄우지 않고 `httptest`로 `health` 함수를 호출합니다.

```go
// backend/cmd/api/main_test.go
package main

import (
  "net/http"
  "net/http/httptest"
  "testing"
)

func TestHealth(t *testing.T) {
  req := httptest.NewRequest(http.MethodGet, "/api/health", nil)
  res := httptest.NewRecorder()

  health(res, req)

  if res.Code != http.StatusOK {
    t.Fatalf("expected status %d, got %d", http.StatusOK, res.Code)
  }

  if got := res.Body.String(); got != "{\"status\":\"ok\"}\n" {
    t.Fatalf("unexpected body %q", got)
  }
}
```

응답 상태가 200인지, JSON 본문이 기대한 값인지 검사합니다.
작은 API라도 테스트가 있으면 이후 대시보드 목록 기능을 추가하다가
health API를 실수로 바꾸는 일을 빠르게 발견할 수 있습니다.

## DB와 Docker Compose 연결

현재 Go 코드에는 PostgreSQL 드라이버나 SQL 쿼리가 아직 없습니다.
그럼에도 Compose는 백엔드에 `METADATA_DATABASE_URL`과 `ANALYTICS_DATABASE_URL`
환경 변수를 전달하고, 두 DB가 healthy 상태가 된 뒤에 백엔드를 시작합니다.
다음 단계에서 Go 코드가 DB에 연결할 때 주소를 새로 설계하지 않도록 미리 연결 지점을 준비한 것입니다.

메타데이터 DB에는 현재 `app_metadata` 테이블과 `schema_version` 값만 있습니다.
대시보드 목록을 구현하면서 이곳에 대시보드의 UID, 제목, 설명, 생성 및 수정 시각 같은 정보를
저장할 테이블을 추가하게 됩니다. 분석 DB는 아직 목록 기능에 사용하지 않습니다.
이후 패널 쿼리와 차트를 만들 때 매출과 영업이익 데이터를 조회하는 역할을 맡습니다.

```text
현재
React 정적 화면 ←─→ Go health API

다음 구현
React 목록 화면 ←─→ Go dashboard API ←─→ 메타데이터 PostgreSQL
```

Docker Compose의 `depends_on`과 health check는 "DB 컨테이너를 먼저 실행한다"는 순서를 보장합니다.
다만 백엔드가 DB 연결을 재시도하는 코드까지 대신해 주지는 않습니다.
실제 DB 기능을 추가할 때는 연결 실패를 어떻게 처리할지도 Go 코드에서 결정해야 합니다.

```yaml
services:
  metadata-db:
    ...

  analytics-db:
    ...

  backend:
    ...
    depends_on:
      metadata-db:
        condition: service_healthy
      analytics-db:
        condition: service_healthy

  frontend:
    ...
    depends_on:
      - backend
```

## React와 Go 개념 정리

본문에서는 실제 코드가 실행되는 흐름을 살펴봤습니다.
그 과정에서 나온 React와 Go의 함수, 타입, 인터페이스를 다시 정리합니다.

### React 컴포넌트

React 컴포넌트는 화면 일부를 반환하는 함수입니다. 함수 이름은 대문자로 시작하며,
반환값으로 JSX를 작성합니다. JSX는 화면 구조를 표현하는 JavaScript 또는 TypeScript 문법입니다.
HTML과 닮았지만 JavaScript 안에서 쓰이므로 HTML의 `class` 속성은 `className`으로 작성합니다.

```tsx
function Greeting() {
  return <p className="message">안녕하세요</p>;
}
```

### createRoot 함수

`createRoot()`는 HTML 요소 하나를 React가 관리하는 화면 영역으로 만듭니다.
그 뒤 `render()`에 전달한 컴포넌트를 해당 영역에 표시합니다.
`document.getElementById('root')!`의 `!`는 TypeScript에게 이 요소가 반드시 존재한다고 알려 주는 표기입니다.
요소가 실제로 없으면 실행 시 오류가 발생하므로, `index.html`의 `id`와 이름이 일치해야 합니다.

```tsx
const element = document.getElementById('root')!;

createRoot(element).render(<Greeting />);
```

`StrictMode`는 화면을 직접 만드는 컴포넌트가 아니라 개발 중 검사를 강화하는 React 도구입니다.
개발 환경에서 안전하지 않은 사용 방식이나 예상하지 못한 부작용을 더 빨리 발견하도록 돕습니다.
또한 Vite는 React 자체가 아니라 TypeScript와 JSX를 변환하고 개발 서버를 제공하는 빌드 도구입니다.

### Go의 Handler 인터페이스

Go 표준 라이브러리 `net/http`에서 HTTP 요청을 처리하는 기본 단위는 `http.Handler` 인터페이스입니다.
이 인터페이스는 `ServeHTTP` 메서드를 가진 값을 handler로 인정합니다.

```go
type Handler interface {
    ServeHTTP(ResponseWriter, *Request)
}
```

`http.Request`는 서버가 받은 요청을 담는 값입니다. HTTP 메서드, URL, 헤더, 요청 본문, 취소 정보 등을 읽을 수 있습니다.
`http.ResponseWriter`는 서버가 보낼 응답을 작성하는 값입니다. handler는 이 값을 통해 헤더, 상태 코드, 본문을 씁니다.

```go
func example(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        w.WriteHeader(http.StatusMethodNotAllowed)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    _, _ = w.Write([]byte(`{"status":"ok"}`))
}
```

응답은 헤더, 상태 코드, 본문 순서로 작성하는 편이 안전합니다.
본문을 먼저 쓰면 Go는 기본 상태 코드 `200 OK`를 이미 보낼 수 있으므로, 이후 상태 코드를 바꿀 수 없습니다.

일반 함수는 원래 `ServeHTTP` 메서드를 갖지 않지만, `http.HandlerFunc`를 사용하면
`func(http.ResponseWriter, *http.Request)` 형태의 함수를 handler로 바꿀 수 있습니다.

```go
handler := http.HandlerFunc(example)
```

### ServeMux와 http.Server

`http.NewServeMux()`는 요청 경로를 적절한 handler로 보내는 기본 라우터를 만듭니다.
`HandleFunc()`는 경로 패턴과 handler 함수를 등록하는 메서드입니다.
Go 1.22 이상에서는 `"GET /articles"`처럼 HTTP 메서드까지 포함한 패턴을 등록할 수 있습니다.

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /articles", listArticles)
mux.HandleFunc("GET /articles/{id}", getArticle)
```

`http.Server`는 실제 서버의 설정을 담는 구조체입니다.
`Addr`에는 요청을 받을 주소와 포트를, `Handler`에는 앞에서 만든 router 또는 handler를 넣습니다.
`ListenAndServe()`를 호출하면 서버가 요청을 받기 시작합니다.

```go
server := &http.Server{
    Addr:    ":8080",
    Handler: mux,
}

log.Fatal(server.ListenAndServe())
```

`log.Fatal`은 오류를 로그에 남긴 뒤 프로그램을 종료합니다. 서버 실행이 정상적으로 끝나는 일은 보통 없으므로,
`ListenAndServe()`가 반환한 값은 대개 서버를 시작하지 못했거나 실행 중 문제가 생겼다는 오류입니다.

### JSON 인코딩, 미들웨어, 테스트

`json.NewEncoder(w).Encode(value)`는 Go 값이나 구조체를 JSON으로 바꿔 `ResponseWriter`에 씁니다.
구조체 필드의 ``json:"name"`` 태그는 JSON에서 사용할 키 이름을 정합니다.

```go
type Status struct {
    Message string `json:"message"`
}

_ = json.NewEncoder(w).Encode(Status{Message: "ok"})
```

미들웨어는 handler의 앞이나 뒤에 공통 처리를 덧붙이는 함수입니다.
인증, 요청 로그, CORS 헤더처럼 여러 API에 반복되는 기능을 handler마다 복사하지 않기 위해 사용합니다.
다음 함수는 기존 handler를 감싸고, 응답 헤더를 추가한 뒤 원래 handler를 실행합니다.

```go
func addHeader(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-App-Version", "1.0")
        next.ServeHTTP(w, r)
    })
}
```

`httptest` 패키지는 실제 포트를 열지 않고 handler를 테스트할 때 사용합니다.
`httptest.NewRequest()`로 요청을 만들고, `httptest.NewRecorder()`로 응답을 기록한 다음,
handler의 `ServeHTTP()`를 직접 호출합니다. 이 방식으로 상태 코드와 JSON 본문을 빠르게 검사할 수 있습니다.

## 다음 작업

이번 글에서는 `dashboard-lab` 프로젝트를 만들고, React 화면과 Go HTTP 서버,
메타데이터 DB와 분석 DB가 함께 실행되는 초기 개발 환경을 구성했습니다.
또한 브라우저 화면이 시작되는 위치와 Go 서버가 요청에 JSON을 돌려주는 기본 흐름을,
AI가 작성한 소스코드를 직접 읽으면서 파악했습니다.

다음 글에서는 이번에 만든 빈 환경에 첫 번째 기능을 추가할 예정입니다.
PostgreSQL 메타데이터 테이블에 대시보드 정보를 저장하고,
Go API와 React의 대시보드 목록 및 상세 화면을 연결해 대시보드를 조회하는 흐름을 구현합니다.
