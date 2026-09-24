---
title: "Grafana 클론코딩 #2 - Go API와 React로 대시보드 목록 구현"
date: "2026-09-20T00:11:43+09:00"
layout: "post"
description: >
  PostgreSQL 메타데이터 테이블, Go HTTP API, React 화면을 연결해 대시보드 목록과 상세 조회를 구현합니다.
  Store 인터페이스, handler, React 상태, Docker 검증을 따라가며 첫 번째 대시보드 기능을 완성합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/g86ylkd4jk4cjvontrzu4/grafana-clone-01-dashboards.webp?rlkey=lb55o8m0i6mbbfqp1e8miwxzb&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/aemlct9pg86wza6kwd7da/grafana-00-logo.webp?rlkey=ud43ycrmipiugi9hjwfh1zmgp&raw=1"
categories: ["Project", "Grafana Clone"]
tags: ["Grafana", "Grafana 클론코딩", "Go", "Go HTTP Server", "PostgreSQL", "React", "TypeScript", "Docker Compose", "REST API"]
series: ["Grafana 클론코딩"]
---

{{< series "Grafana 클론코딩" "Grafana 클론코딩 #[0-9]+ - " >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

[이전 글](/blog/grafana-clone-1/)에서 `dashboard-lab`의 React, Go, PostgreSQL 개발 환경을 구성하고,
브라우저와 HTTP 서버가 시작되는 기본 흐름을 살펴봤습니다. 이번에는 비어 있던 화면에
대시보드 목록과 상세 조회를 처음으로 구현합니다.

PostgreSQL의 대시보드 메타데이터가 Go API를 거쳐 React 카드 화면에 나타나는 흐름을 따라갑니다.
DB 테이블, Store와 handler, React 상태, 테스트가 하나의 기능으로 연결되는 과정을 확인합니다.

- **[메타데이터 테이블](#메타데이터-테이블)**: 대시보드 UID, 제목, 설명, 수정 시각을 PostgreSQL에 저장합니다.
- **[Go 대시보드 API](#go-대시보드-api)**: Store, PostgreSQL 조회, HTTP handler와 오류 응답을 연결합니다.
- **[React 목록과 상세 화면](#react-목록과-상세-화면)**: API 응답을 상태에 저장하고 목록 카드와 상세 화면으로 렌더링합니다.
- **[테스트와 빌드 검증](#테스트와-빌드-검증)**: fake Store를 이용한 handler 테스트와 TypeScript, Vite 빌드를 확인합니다.
{{% /hint %}}

[이전 글](/blog/grafana-clone-1/)에서는 대시보드 플랫폼을 시작하기 위한
React, Go, 두 PostgreSQL 컨테이너를 준비하고, 각 프로그램이 실행되는 최소 코드를 읽었습니다.
이번에는 그 기반 위에 사용자가 처음으로 볼 기능인 대시보드 목록을 추가합니다.

목록에서 제목을 선택하면 UID를 가진 URL로 이동하고, 해당 대시보드의 설명을 보여 줍니다.
아직 패널과 차트는 없지만, 이 기능으로 메타데이터 DB, Go API, React 화면이 하나의 대시보드 리소스를 중심으로 연결됩니다.

## 대시보드 목록 구현

첫 번째 기능의 범위는 우선 작게 잡습니다.

```text
GET /api/v1/dashboards
GET /api/v1/dashboards/:uid

/dashboards
/d/:uid
```

메타데이터 DB에는 대시보드 목록을 저장하고, Go API는 이를 JSON으로 반환하며,
React는 결과를 목록으로 표시합니다. 목록에서 하나를 선택하면 UID를 포함한 상세 URL로 이동합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/95cn8mrp8sarnazm71ypt/grafana-clone-02-dashboards-list.webp?rlkey=9cgm4rvn49otsbpf0lwrctwjz&raw=1"
  alt="Dashboards"
  caption="대시보드 목록 페이지" >}}

DB 테이블에서 시작해 HTTP handler, React 화면, 테스트와 Docker 실행 결과 순서로 살펴보겠습니다.

### 메타데이터 테이블

`app_metadata` 테이블은 애플리케이션 설정을 기록하므로,
사용자가 조회할 대시보드는 별도 `dashboards` 테이블에 저장하겠습니다.
UID는 URL에 사용할 고유한 식별자이고 제목과 설명은 목록 카드에 표시합니다.

{{< tabs "metadata-query" >}}

{{% tab "CREATE" %}}
```sql
-- db/metadata/002_dashboards.sql
CREATE TABLE IF NOT EXISTS dashboards (
    uid text PRIMARY KEY
  , title text NOT NULL
  , description text NOT NULL DEFAULT ''
  , created_at timestamptz NOT NULL DEFAULT now()
  , updated_at timestamptz NOT NULL DEFAULT now()
);
```
{{% /tab %}}

{{% tab "INSERT" %}}
```sql
-- db/metadata/002_dashboards.sql
INSERT INTO dashboards (uid, title, description, created_at, updated_at)
VALUES
    ('sales-overview', '매출 현황', '일별 매출과 영업이익을 살펴볼 대시보드입니다.', '2026-07-31 09:00:00+09', '2026-07-31 09:00:00+09'),
    ('brand-performance', '브랜드별 성과', '브랜드별 매출과 이익을 비교할 대시보드입니다.', '2026-07-30 09:00:00+09', '2026-07-30 09:00:00+09'),
    ('channel-performance', '쇼핑몰별 성과', '쇼핑몰별 판매 성과를 확인할 대시보드입니다.', '2026-07-29 09:00:00+09', '2026-07-29 09:00:00+09')
ON CONFLICT (uid) DO UPDATE
SET
    title = EXCLUDED.title,
    description = EXCLUDED.description,
    updated_at = EXCLUDED.updated_at;
```
{{% /tab %}}

{{< /tabs >}}

초기 데이터로 매출 현황, 브랜드별 성과, 쇼핑몰별 성과 세 건을 넣었습니다.
새로 실행하는 환경에서는 위의 CREATE 및 INSERT 쿼리가 PostgreSQL 초기화 과정에 적용됩니다.
이미 만들어진 Docker volume에는 초기화 스크립트가 다시 실행되지 않으므로,
개발 중에는 새 마이그레이션을 다시 적용해야 합니다.

## Go 대시보드 API

목록 기능을 넣으면서 `main.go`는 HTTP 요청과 응답을 담당하고,
새로운 `internal/dashboard` 패키지를 만들어 대시보드 데이터와 PostgreSQL 조회를 담당하도록 분리했습니다.

`internal`은 Go의 특별한 디렉터리 이름입니다. 이 경우 `backend` 경로 밖의 다른 Go 모듈은
`backend/internal/dashboard` 패키지를 import할 수 없습니다.
외부에 노출할 필요 없이 백엔드 내부에서만 사용할 것이기에 이렇게 구성했습니다.

### 대시보드 모델과 인터페이스

`dashboard.go`에는 API가 다룰 대시보드의 구조체, DB에 접근하는 로직에 대한 인터페이스,
그리고 실제 PostgreSQL 구현이 함께 있습니다.
먼저 `Dashboard`는 DB 행과 JSON 응답이 공통으로 사용하는 데이터 모델입니다.
Go의 필드명은 대문자로 시작해야 다른 패키지에서 읽을 수 있고,
뒤의 ``json:"updatedAt"`` 태그는 JSON 응답에서 사용할 camelCase 이름을 정합니다.

```go
// backend/internal/dashboard/dashboard.go
type Dashboard struct {
    UID         string    `json:"uid"`
    Title       string    `json:"title"`
    Description string    `json:"description"`
    UpdatedAt   time.Time `json:"updatedAt"`
}
```

`Store`는 대시보드 데이터를 조회할 때 필요한 메서드 목록을 정의한 인터페이스입니다.
현재는 전체 대시보드 목록을 가져오는 `List`와 UID로 대시보드 하나를 가져오는 `GetByUID`를 선언했습니다.

각 메서드 첫 번째 인자인 `context.Context`에는 요청 취소나 시간 제한 같은 요청 수명 정보가 담깁니다.
브라우저가 요청을 취소하면 이후 DB 쿼리도 함께 취소될 수 있도록, handler에서 받은 context를 그대로 전달합니다.

```go
// backend/internal/dashboard/dashboard.go
type Store interface {
    List(context.Context) ([]Dashboard, error)
    GetByUID(context.Context, string) (Dashboard, error)
}
```

`Store` 인터페이스 덕분에 handler는 PostgreSQL인지, 테스트용 메모리 데이터인지 알 필요가 없습니다.
실행할 때는 `List`와 `GetByUID` 메서드가 구현된 `PostgresStore`를 넣고,
테스트할 때는 같은 메서드를 가진 가짜 `Store`를 넣을 수 있습니다.

### PostgresStore 구현

`PostgresStore`는 Go 표준 라이브러리 `database/sql`의 `*sql.DB`를 보관합니다.
`*sql.DB`는 하나의 물리 연결이 아니라 연결을 필요에 따라 빌려 주는 관리 객체입니다.

`NewPostgresStore`는 이 객체를 받아 `Store`를 만들고, 아래 두 메서드가 실제 SQL을 실행합니다.
Go에는 클래스를 만들 때 자동으로 호출되는 생성자 문법이 없어서, 보통 `NewTypeName` 형태의 함수를 직접 만듭니다.
`NewPostgresStore`도 새 DB 연결을 열거나 SQL을 실행하는 함수가 아니라,
이미 만든 `*sql.DB`를 `PostgresStore`의 `db` 필드에 담아 반환할 뿐입니다.
즉 `db`를 건네받아 `PostgresStore`를 조립하는 짧은 생성 함수라고 볼 수 있습니다.

```go
// backend/internal/dashboard/dashboard.go
type PostgresStore struct {
    db *sql.DB
}

func NewPostgresStore(db *sql.DB) *PostgresStore {
    return &PostgresStore{db: db}
}
```

전체 대시보드 목록을 가져오는 `List` 메서드는 `QueryContext`로 여러 개의 행 `rows`를 반환받습니다.
쿼리를 실행한 후엔 `defer` 키워드로 `rows.Close()` 실행을 예약해
함수가 어느 지점에서 끝나든 DB가 사용한 자원을 반납하게 합니다.

`rows.Next()`로 한 행씩 이동하고, `rows.Scan()`으로 현재 행의 각 열 값을
`Dashboard` 타입의 변수 `item`의 필드에 넣습니다.
`&item.UID`처럼 필드 앞에 `&`를 붙이는 이유는 `Scan()`이 해당 필드의 메모리 위치를 받아
직접 값을 기록해야 하기 때문입니다.

```go
// backend/internal/dashboard/dashboard.go
func (s *PostgresStore) List(ctx context.Context) ([]Dashboard, error) {
    rows, err := s.db.QueryContext(ctx, `
        SELECT uid, title, description, updated_at
        FROM dashboards
        ORDER BY updated_at DESC, uid ASC
    `)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    dashboards := make([]Dashboard, 0)
    for rows.Next() {
        var item Dashboard
        if err := rows.Scan(&item.UID, &item.Title, &item.Description, &item.UpdatedAt); err != nil {
            return nil, err
        }
        dashboards = append(dashboards, item)
    }

    return dashboards, rows.Err()
}
```

마지막의 `rows.Err()`는 행을 순회하는 도중 발생한 오류까지 확인합니다.
빈 목록은 오류가 아니라 길이가 0인 배열로 JSON에 반환됩니다.

반대로 UID로 한 건의 대시보드를 조회하는 `GetByUID`는 한 행만 반환하므로 `QueryRowContext`를 사용합니다.

`$1` 자리에 `uid`를 별도 값으로 넘기는 매개변수 쿼리이므로, URL 값을 SQL 문자열에 이어 붙이지 않습니다.
이 방식은 SQL 문법 오류를 줄이고 SQL injection을 막는 기본 방식입니다.

```go
// backend/internal/dashboard/dashboard.go
var ErrNotFound = errors.New("dashboard not found")

func (s *PostgresStore) GetByUID(ctx context.Context, uid string) (Dashboard, error) {
    var item Dashboard
    err := s.db.QueryRowContext(ctx, `
        SELECT uid, title, description, updated_at
        FROM dashboards
        WHERE uid = $1
    `, uid).Scan(&item.UID, &item.Title, &item.Description, &item.UpdatedAt)
    if errors.Is(err, sql.ErrNoRows) {
        return Dashboard{}, ErrNotFound
    }

    return item, err
}
```

조회 결과가 없을 때 PostgreSQL 드라이버가 돌려주는 `sql.ErrNoRows`는
`ErrNotFound`로 바꾸고, 나머지 오류는 그대로 호출자에게 넘깁니다.
이 동작은 SQL의 오류를 HTTP 404라는 애플리케이션 의미로 바꾸기 위함으로,
DB에서 행을 찾지 못한 경우와 DB 연결 자체가 실패한 경우에 대해 사용자에게 다른 응답을 주기 위한 목적입니다.

### API 서버와 Handler 구성

초기 코드에서는 `main()`이 라우트를 직접 만들었습니다. 대시보드 목록 기능을 넣으면서
`main()`은 서버가 실제로 사용할 DB를 준비하는 역할에 집중하고,
`newHandler(store)`가 URL과 handler를 조립하도록 분리했습니다.
이 분리는 "서버를 실행하는 코드"와 "HTTP 요청을 처리할 준비가 된 handler를 만드는 코드"를 나누는 방법입니다.
후자는 포트를 열지 않아도 테스트에서 바로 호출할 수 있습니다.

먼저 `main()`에서 PostgreSQL 드라이버와 연결을 준비합니다.
`pgx`는 PostgreSQL에 연결할 때 필요한 드라이버입니다.
언더바(`_`)를 사용해 import하면 프로그램이 시작될 때 드라이버가 `database/sql`에 등록됩니다.
그 덕분에 뒤에서 `sql.Open("pgx", databaseURL)` 실행으로 PostgreSQL 연결을 열 수 있습니다.

`Open`만으로는 실제 연결 성공을 보장하지 않으므로 시작 직후 `PingContext`로 연결을 확인합니다.
연결하지 못하면 대시보드 API가 실패한 채 실행되지 않도록 서버를 종료합니다.

```go
// backend/cmd/api/main.go
import (
	...
	_ "github.com/jackc/pgx/v5/stdlib"
)

func main() {
  databaseURL := os.Getenv("METADATA_DATABASE_URL")
  if databaseURL == "" {
      log.Fatal("METADATA_DATABASE_URL is required")
  }

  db, err := sql.Open("pgx", databaseURL)
  if err != nil {
      log.Fatalf("open metadata database: %v", err)
  }
  defer db.Close()

  if err := db.PingContext(context.Background()); err != nil {
      log.Fatalf("ping metadata database: %v", err)
  }
  ...
}
```

`dashboard.NewPostgresStore(db)`는 `PostgresStore`를 만들고, 그것을 `newHandler`에 전달합니다.
`newHandler`의 반환형은 추상적인 인터페이스인 `http.Handler`입니다.
내부에서는 `ServeMux`에 3개의 URL을 등록한 뒤, 기존 CORS wrapper까지 씌워 완성된 처리기를 반환합니다.

```go
// backend/cmd/api/main.go
func main() {
  ...
  server := &http.Server{
      Addr:    ":" + port,
      Handler: newHandler(dashboard.NewPostgresStore(db)),
  }
  ...
}

func newHandler(store dashboard.Store) http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /api/health", health)
    mux.HandleFunc("GET /api/v1/dashboards", listDashboards(store))
    mux.HandleFunc("GET /api/v1/dashboards/{uid}", getDashboard(store))
    return cors(mux)
}
```

`listDashboards(store)`처럼 Store를 받는 함수는
곧바로 응답을 만들지 않고 `http.HandlerFunc`를 반환합니다.
반환되는 익명 함수가 바깥의 `store`를 기억하는 클로저(closure)이므로,
전역 변수 없이도 요청마다 같은 Store를 사용할 수 있습니다.

```go
// backend/cmd/api/main.go
func listDashboards(store dashboard.Store) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        items, err := store.List(r.Context())
        if err != nil {
            writeError(w, http.StatusInternalServerError, "could not load dashboards")
            return
        }
        writeJSON(w, http.StatusOK, items)
    }
}
```

`getDashboard` 함수도 같은 방식입니다. 그리고, Go 1.22 이상의 `ServeMux`에
`"/api/v1/dashboards/{uid}"`처럼 변수 이름이 포함된 경로 패턴을 등록할 수 있습니다.
요청이 들어오면 `r.PathValue("uid")` 메서드로 `{uid}` 자리에 해당하는 값을 읽습니다.

```go
// backend/cmd/api/main.go
func getDashboard(store dashboard.Store) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        item, err := store.GetByUID(r.Context(), r.PathValue("uid"))
        if errors.Is(err, dashboard.ErrNotFound) {
            writeError(w, http.StatusNotFound, "dashboard not found")
            return
        }
        if err != nil {
            writeError(w, http.StatusInternalServerError, "could not load dashboard")
            return
        }
        writeJSON(w, http.StatusOK, item)
    }
}
```

`writeJSON`은 Content-Type, 상태 코드, JSON 변환을 한곳에 모은 보조 함수입니다.
여기서 `any` 타입은 어떤 값이든 받을 수 있다는 뜻입니다. `writeError` 함수는 `writeJSON` 함수를 재사용해
`{"message":"..."}` 형태의 오류 JSON을 만듭니다. 따라서 Store가 `ErrNotFound`를 돌려주면 404,
그 외 DB 오류면 500이라는 HTTP 의미가 handler에서 분명하게 결정됩니다.

```go
// backend/cmd/api/main.go
func writeJSON(w http.ResponseWriter, status int, value any) {
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(status)
    _ = json.NewEncoder(w).Encode(value)
}

func writeError(w http.ResponseWriter, status int, message string) {
    writeJSON(w, status, map[string]string{"message": message})
}
```

## React 목록과 상세 화면

프론트엔드는 한 파일에서 시작했지만, 이번 기능으로
`App`, `DashboardList`, `DashboardDetail` 세 컴포넌트로 나뉘었습니다.
아직 클라이언트 측 라우팅인 React Router는 넣지 않았습니다.
화면이 두 개뿐인 현재는 브라우저의 주소를 직접 읽는 방식으로
URL/API/컴포넌트가 연결되는 최소 흐름을 먼저 확인해 보았습니다.

### 대시보드 타입과 화면 선택

`Dashboard` 타입은 Go API가 보내는 JSON 모양을 TypeScript에 다시 적은 것입니다.
Go의 `time.Time`은 JSON으로 전송될 때 문자열이 되므로 프론트엔드에서는 `updatedAt: string`으로 받습니다.
`apiURL`은 Vite의 `VITE_BACKEND_URL` 환경 변수가 있으면 그 값을 쓰고, 없으면 로컬 Go 서버 주소를 기본값으로 씁니다.
배포 환경에서 API 주소가 달라져도 React 코드를 수정하지 않기 위한 준비입니다.

```tsx
// frontend/src/main.tsx
type Dashboard = {
  uid: string;
  title: string;
  description: string;
  updatedAt: string;
};

const apiURL = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8080';
```

`App`에서는 정규표현식 `/^\/d\/([^/]+)$/`으로 현재 경로가 `/d/값` 형태인지 검사합니다.
`match()` 결과가 있을 때의 첫 번째 묶음(`?.[1]`)이 UID이고, 없으면 목록 화면을 반환합니다.
이 방식은 뒤로 가기나 복잡한 중첩 URL을 다루기에는 부족하므로,
화면과 URL 규칙이 늘어나는 시점에는 라우터를 도입할 예정입니다.

```tsx
// frontend/src/main.tsx
function App() {
  const detailUID = window.location.pathname.match(/^\/d\/([^/]+)$/)?.[1];

  if (detailUID) {
    return <DashboardDetail uid={detailUID} />;
  }
  return <DashboardList />;
}
```

### 대시보드 목록 화면

`DashboardList`는 대시보드 목록 화면을 담당하는 컴포넌트입니다.

`useState`는 React 화면이 기억해야 하는 값을 보관합니다. 여기서는 두 가지 값을 기억합니다.
- `dashboards`: API에서 받아온 대시보드 목록입니다.
- `error`: API 요청에 실패했을 때 보여줄 오류 메시지입니다.

`setDashboards`와 `setError`는 이 값을 바꾸는 함수입니다.
이 함수로 값을 변경하면 React가 변경된 값을 바탕으로 화면을 다시 그립니다.
화면이 처음 열릴 때는 아직 API 응답을 받지 못했으므로 대시보드가 없는 빈 목록으로 시작하게 됩니다.

```tsx
// frontend/src/main.tsx
function DashboardList() {
  const [dashboards, setDashboards] = useState<Dashboard[]>([]);
  const [error, setError] = useState<string>();
  ...
}
```

`useEffect` 안의 코드는 `DashboardList` 화면이 처음 나타날 때 실행됩니다.
여기서는 `fetch`로 Go API에 대시보드 목록을 요청합니다.

API가 응답하면 먼저 `response.ok`를 확인합니다.
서버가 404나 500을 반환해도 네트워크 요청 자체는 성공할 수 있기 때문에,
응답 상태가 정상인지 별도로 확인해야 합니다.

정상 응답이면 `response.json()`으로 JSON을 읽고, 그 결과를 `setDashboards`에 전달해 목록을 저장합니다.
목록이 저장되면 React가 화면을 다시 그립니다.

요청 중 문제가 발생하면 `catch`가 실행되고, 오류 메시지를 `setError`로 저장합니다.
그러면 화면에 오류 메시지가 나타납니다.

```tsx
// frontend/src/main.tsx
function DashboardList() {
  ...
  useEffect(() => {
    fetch(`${apiURL}/api/v1/dashboards`)
      .then((response) => {
        if (!response.ok) throw new Error('대시보드 목록을 불러오지 못했습니다.');
        return response.json() as Promise<Dashboard[]>;
      })
      .then(setDashboards)
      .catch((reason: unknown) =>
        setError(reason instanceof Error ? reason.message : '알 수 없는 오류가 발생했습니다.')
      );
  }, []);
  ...
}
```

API 응답을 받으면 `dashboards`에는 여러 개의 대시보드 객체가 배열로 들어갑니다.
예를 들어 매출 현황 대시보드는 다음과 같은 값입니다.

```json
{
  "uid": "sales-overview",
  "title": "매출 현황",
  "description": "일별 매출과 영업이익을 살펴볼 대시보드입니다.",
  "updatedAt": "2026-07-31T00:00:00Z"
}
```

JSX의 중괄호 `{ ... }` 안에는 JavaScript 또는 TypeScript 표현식을 작성할 수 있습니다.
`dashboards.map(...)`은 목록의 대시보드를 하나씩 꺼내어, 각 대시보드에 대응하는 카드 JSX를 만듭니다.
따라서 대시보드가 세 건이면 카드도 세 개가 화면에 표시됩니다.

```tsx
// frontend/src/main.tsx
function DashboardList() {
  ...
  return (
    <main>
      <header>...</header>
      {error ? <p className="error-message">{error}</p> : null}
      <section aria-label="대시보드 목록" className="dashboard-list">
        {dashboards.map((dashboard) => (
          <a className="dashboard-card" href={`/d/${dashboard.uid}`} key={dashboard.uid}>
            <h2>{dashboard.title}</h2>
            <p>{dashboard.description}</p>
            <span>최근 수정 {new Date(dashboard.updatedAt).toLocaleDateString('ko-KR')}</span>
          </a>
        ))}
      </section>
    </main>
  )
}
```

`map()` 으로 `dashboards`를 순회할 때, 내부의 `dashboard`는 현재 처리 중인 대시보드 한 건입니다.
예를 들어 첫 번째 반복에서는 매출 현황 객체가 `dashboard`가 되고,
`dashboard.title`에는 매출 현황이 들어 있습니다.

바깥의 `<a>` 요소는 링크이면서 카드 전체의 클릭 영역입니다.
``href={`/d/${dashboard.uid}`}`` 속성은 UID를 주소에 넣는 표현입니다.
따라서 UID가 `sales-overview`라면 링크 주소는 `/d/sales-overview`가 됩니다.
사용자가 카드를 클릭하면 이 주소로 이동하고, 다음 절의 상세 화면이 해당 UID를 사용해 대시보드를 조회합니다.

`key={dashboard.uid}` 속성은 화면에 직접 보이지 않는 React 전용 식별자입니다.
React는 카드 목록이 다시 그려질 때 어떤 카드가 어떤 대시보드에 해당하는지 구분해야 합니다.
UID는 대시보드마다 고유하므로 `key`로 사용하기에 적합합니다.

카드 안에서는 제목, 설명, 수정 시각을 차례로 표시합니다.
`new Date(dashboard.updatedAt)`은 API에서 받은 날짜 문자열을 JavaScript 날짜 값으로 바꾸고,
`toLocaleDateString('ko-KR')`은 이를 한국식 날짜 형식으로 표시합니다.

### 대시보드 상세 화면

`DashboardDetail`은 대시보드 한 건을 보여 주는 컴포넌트입니다.
목록에서 사용자가 매출 현황 카드를 선택하면 주소가 `/d/sales-overview`로 이동되고,
`App` 컴포넌트는 주소에서 꺼낸 `sales-overview`를 `uid`라는 값으로 `DashboardDetail`에 전달합니다.

```tsx
// frontend/src/main.tsx
function App() {
  const detailUID = window.location.pathname.match(/^\/d\/([^/]+)$/)?.[1];

  if (detailUID) {
    return <DashboardDetail uid={detailUID} />;
  }
  ...
}
```

`DashboardDetail` 함수의 `{ uid }`는 전달받은 값에서 `uid`만 꺼내어 사용하는 문법입니다.
뒤의 `: { uid: string }` 표현은 TypeScript 타입 표기입니다.
이 컴포넌트는 문자열 형태의 UID를 반드시 받아야 한다는 뜻입니다.

상세 화면도 목록 화면처럼 API 응답과 오류 메시지를 화면 상태로 보관합니다.
`useState`로 대시보드 정보 `dashbaord`와 오류 메시지 `error` 값을 생성합니다.

```tsx
// frontend/src/main.tsx
function DashboardDetail({ uid }: { uid: string }) {
  const [dashboard, setDashboard] = useState<Dashboard>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    fetch(`${apiURL}/api/v1/dashboards/${uid}`)
      .then((response) => {
        if (!response.ok) throw new Error('대시보드를 불러오지 못했습니다.');
        return response.json() as Promise<Dashboard>;
      })
      .then(setDashboard)
      .catch((reason: unknown) =>
        setError(reason instanceof Error ? reason.message : '알 수 없는 오류가 발생했습니다.')
      );
  }, [uid]);
  ...
}
```

URL이 `/d/sales-overview`라면 `${uid}` 자리에 `sales-overview`가 들어가고,
실제로는 다음 API를 요청합니다.

```text
GET /api/v1/dashboards/sales-overview
```

목록 화면의 `useEffect`는 처음 화면에 나타날 때 한 번만 실행하면 되므로
검사 대상으로 빈 배열 `[]`을 사용했습니다. 반면 상세 화면은 `[uid]`를 사용합니다.
사용자가 다른 대시보드의 상세 URL로 이동하면 `uid`가 바뀌고,
그에 맞는 대시보드 정보를 다시 요청해야 하기 때문입니다.

상세 화면의 JSX는 항상 뒤로 가기 링크를 표시합니다.
오류가 있으면 오류 메시지를 표시하고,
`dashboard`에 API 응답이 저장된 경우에만 대시보드 카드 전체를 표시합니다.

```tsx
// frontend/src/main.tsx
function DashboardDetail({ uid }: { uid: string }) {
  ...
  return (
    <main>
      <a className="back-link" href="/dashboards">← Dashboards</a>
      {error ? <p className="error-message">{error}</p> : null}
      {dashboard ? (
        <section className="dashboard-detail">
          <p className="eyebrow">{dashboard.uid}</p>
          <h1>{dashboard.title}</h1>
          <p>{dashboard.description}</p>
          <p className="muted">패널과 차트는 이후 단계에서 이 화면에 추가합니다.</p>
        </section>
      ) : null}
    </main>
  )
}
```

`dashboard ? (...) : null`은 조건부 표시 문법입니다.
`dashboard`에 값이 있으면 괄호 안의 상세 카드를 표시하고,
값이 없으면 `null`을 반환해 아무것도 표시하지 않습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/z1is16e2lf41y6oe89fmc/grafana-clone-03-dashboard-uid.webp?rlkey=297tj2m49bqal32ff9434nw3x&raw=1"
  alt="Dashboards > sales-overview"
  caption="대시보드 상세 페이지: 매출 현황(sales-overview)" >}}

아직 패널과 차트는 없지만, URL이 대시보드를 가리키고 React가 해당 UID를 API로 보내며,
Go가 메타데이터 DB에서 찾아 JSON을 돌려주는 하나의 수직 흐름이 완성되었습니다.

## 테스트와 빌드 검증

이번 기능은 메타데이터 DB, Go API, React 화면을 연결합니다.
하지만 문제가 생겼을 때마다 Docker 컨테이너와 PostgreSQL을 모두 실행해 확인하면
원인을 찾는 데 시간이 오래 걸립니다.

먼저 Go handler는 실제 DB 없이 테스트합니다.
앞에서 `newHandler`가 구체적인 PostgreSQL 연결이 아니라
`dashboard.Store` 인터페이스를 받도록 만든 이유가 여기서 드러납니다.
실행 환경에서는 `PostgresStore`를 전달하지만,
테스트에서는 같은 `List`와 `GetByUID` 메서드를 구현한 `fakeDashboardStore`를 전달할 수 있습니다.

`fakeDashboardStore`는 메모리에 넣어 둔 대시보드 배열을 반환합니다.
따라서 테스트는 PostgreSQL의 데이터나 네트워크 연결 상태에 영향을 받지 않고,
handler가 Store의 조회 결과를 올바른 HTTP 응답으로 바꾸는지만 확인할 수 있습니다.

```go
// backend/cmd/api/main_test.go
type fakeDashboardStore struct {
    items []dashboard.Dashboard
}

func (s fakeDashboardStore) List(context.Context) ([]dashboard.Dashboard, error) {
    return s.items, nil
}

func (s fakeDashboardStore) GetByUID(_ context.Context, uid string) (dashboard.Dashboard, error) {
    for _, item := range s.items {
        if item.UID == uid {
            return item, nil
        }
    }
    return dashboard.Dashboard{}, dashboard.ErrNotFound
}
```

`TestListDashboards`는 대시보드 한 건이 들어 있는 가짜 Store를 준비합니다.
`httptest.NewRequest()`는 실제 브라우저 대신 `GET /api/v1/dashboards` 요청을 만들고,
`httptest.NewRecorder()`는 handler가 만든 응답을 기록합니다.

`newHandler(store).ServeHTTP(res, req)`를 호출하면 서버 포트를 열지 않아도
등록한 라우트와 handler를 실제 요청처럼 실행할 수 있습니다.
테스트는 응답 상태가 `200 OK`인지, 응답 JSON에 `sales-overview` UID가 포함됐는지 확인합니다.
즉, 목록 API의 라우팅, Store 호출, JSON 응답이 함께 동작하는지 검사합니다.

```go
// backend/cmd/api/main_test.go
func TestListDashboards(t *testing.T) {
    store := fakeDashboardStore{items: []dashboard.Dashboard{{
        UID: "sales-overview",
        Title: "매출 현황",
        UpdatedAt: time.Date(2026, 7, 31, 0, 0, 0, 0, time.UTC),
    }}}
    req := httptest.NewRequest(http.MethodGet, "/api/v1/dashboards", nil)
    res := httptest.NewRecorder()

    newHandler(store).ServeHTTP(res, req)

    if res.Code != http.StatusOK {
        t.Fatalf("expected status %d, got %d", http.StatusOK, res.Code)
    }
    if got := res.Body.String(); !strings.Contains(got, "sales-overview") {
        t.Fatalf("expected dashboard UID in response, got %q", got)
    }
}
```

`TestGetDashboardReturnsNotFound`는 비어 있는 가짜 Store에 존재하지 않는 UID를 요청합니다.
가짜 Store는 `dashboard.ErrNotFound`를 반환하고,
`getDashboard` handler는 이를 받아 `404 Not Found`와 오류 메시지 JSON으로 바꿉니다.

이 테스트는 "대시보드가 없음"과 DB 연결 실패 같은 서버 오류를 구분하는 코드가 유지되는지 확인합니다.
기존 `TestHealth`도 함께 실행되므로, 목록 기능을 추가하는 과정에서 health API가 깨지지 않았는지도 확인할 수 있습니다.

```go
// backend/cmd/api/main_test.go
func TestGetDashboardReturnsNotFound(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/api/v1/dashboards/unknown", nil)
    res := httptest.NewRecorder()

    newHandler(fakeDashboardStore{}).ServeHTTP(res, req)

    if res.Code != http.StatusNotFound {
        t.Fatalf("expected status %d, got %d", http.StatusNotFound, res.Code)
    }
    body, err := io.ReadAll(res.Body)
    if err != nil {
        t.Fatal(err)
    }
    if !strings.Contains(string(body), "dashboard not found") {
        t.Fatalf("unexpected body %q", body)
    }
}
```

`backend/` 경로에서 Go 테스트를 실행하여 성공하면 다음과 같은 테스트 결과가 출력됩니다.

```bash
backend % GOWORK=off go test ./...
ok      github.com/minyeamer/dashboard-lab/backend/cmd/api      0.499s
?       github.com/minyeamer/dashboard-lab/backend/internal/dashboard   [no test files]
```

Go 테스트와 별도로 `frontend/` 경로에서도 프론트엔드를 빌드합니다.
`npm run build` 명령어는 먼저 TypeScript 타입 검사를 수행하고,
그다음 Vite가 배포 가능한 프론트엔드 파일을 만듭니다.

```bash
frontend % npm run build

> dashboard-lab-frontend@0.0.0 build
> tsc -b && vite build

vite v8.2.2 building client environment for production...
✓ 15 modules transformed.
computing gzip size...
dist/index.html                   0.39 kB │ gzip:  0.26 kB
dist/assets/index-ByTC5GIm.css    1.00 kB │ gzip:  0.50 kB
dist/assets/index-BsqX21Rk.js   192.35 kB │ gzip: 60.80 kB
```

`go test ./...`는 백엔드의 모든 패키지를 컴파일하고 테스트 함수를 실행합니다.
`npm run build`는 먼저 TypeScript 타입 검사를 수행하고,
그다음 Vite가 배포 가능한 프론트엔드 파일을 만듭니다.

이 단계는 브라우저에서 카드 클릭까지 자동으로 검사하는 E2E 테스트는 아닙니다.
대신 Go API의 기본 동작과 React 코드의 타입 및 빌드 오류를 빠르게 발견하는 검증입니다.

## Docker Compose 실행 검증

테스트와 빌드가 통과한 뒤 Docker Compose로 전체 서비스를 실행했습니다.

```bash
docker compose up --build -d
docker compose ps
```

```bash
NAME                           IMAGE                    COMMAND                  SERVICE        CREATED       STATUS                 PORTS
dashboard-lab-analytics-db-1   postgres:16-alpine       "docker-entrypoint.s…"   analytics-db   8 hours ago   Up 8 hours (healthy)   0.0.0.0:15432->5432/tcp, [::]:15432->5432/tcp
dashboard-lab-backend-1        dashboard-lab-backend    "/dashboard-lab-api"     backend        8 hours ago   Up 8 hours             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp
dashboard-lab-frontend-1       dashboard-lab-frontend   "docker-entrypoint.s…"   frontend       8 hours ago   Up 8 hours             0.0.0.0:5173->5173/tcp, [::]:5173->5173/tcp
dashboard-lab-metadata-db-1    postgres:16-alpine       "docker-entrypoint.s…"   metadata-db    8 hours ago   Up 8 hours (healthy)   0.0.0.0:15431->5432/tcp, [::]:15431->5432/tcp
```

프론트엔드, 백엔드, 메타데이터 DB, 분석 DB 컨테이너가 모두 실행 중인 것을 확인했습니다.
이제 백엔드 API에 직접 요청해 health API, 대시보드 목록 API, 대시보드 상세 API가
메타데이터 DB의 값을 정상적으로 반환하는지 확인합니다.

### 대시보드 목록 API

기본적인 헬스 체크 API는 성공했음을 전제로, 먼저 대시보드 목록 API를 호출합니다.

```bash
curl http://localhost:8080/api/v1/dashboards
```

```json
[
  {
    "uid": "sales-overview",
    "title": "매출 현황",
    "description": "일별 매출과 영업이익을 살펴볼 대시보드입니다.",
    "updatedAt": "2026-07-31T00:00:00Z"
  },
  {
    "uid": "brand-performance",
    "title": "브랜드별 성과",
    "description": "브랜드별 매출과 이익을 비교할 대시보드입니다.",
    "updatedAt": "2026-07-30T00:00:00Z"
  },
  {
    "uid": "channel-performance",
    "title": "쇼핑몰별 성과",
    "description": "쇼핑몰별 판매 성과를 확인할 대시보드입니다.",
    "updatedAt": "2026-07-29T00:00:00Z"
  }
]
```

응답에는 메타데이터 DB에 넣은 세 개의 대시보드 정보가 배열로 반환됩니다.
`PostgresStore.List()`가 `dashboards` 테이블을 조회하고,
`listDashboards` handler가 그 결과를 JSON 배열로 변환한 결과입니다.

React의 목록 화면도 이 API를 호출합니다.

### 대시보드 상세 API

이어서 UID 하나를 지정해 대시보드 상세 정보를 조회합니다.

```bash
curl http://localhost:8080/api/v1/dashboards/sales-overview
```

```json
{
  "uid": "sales-overview",
  "title": "매출 현황",
  "description": "일별 매출과 영업이익을 살펴볼 대시보드입니다.",
  "updatedAt": "2026-07-31T00:00:00Z"
}
```

목록 API와 달리 배열이 아니라 대시보드 한 건만 반환됩니다.
URL의 `sales-overview`가 `getDashboard` handler의 `r.PathValue("uid")`로 전달되고,
`PostgresStore.GetByUID()`가 같은 UID를 가진 행을 조회합니다.

여기까지 확인하면서 메타데이터 DB의 대시보드 데이터가
Go API를 거쳐 React의 목록과 상세 화면까지 전달되는 흐름을 검증했습니다.

## React와 Go 개념 정리

이번 구현에서 사용한 React의 상태 관리와 비동기 요청, Go의 인터페이스, 오류 처리, 테스트 방식을 정리합니다.

### useState, useEffect

React 컴포넌트 안의 일반 변수는 화면이 다시 그려질 때 이전 값을 보관하지 않습니다.
`useState`는 화면이 기억해야 하는 값을 보관하고, 값을 바꾸는 함수를 함께 반환합니다.

```tsx
const [items, setItems] = useState<Item[]>([]);
```

위 코드에서 `items`는 현재 화면이 가진 목록이고,
`setItems`는 이 목록을 새 값으로 바꾸는 함수입니다.
예를 들어 API 응답을 `setItems`에 전달하면 React는 변경된 목록을 사용해 화면을 다시 그립니다.

`useEffect`는 화면을 그리는 작업과 별도로 실행할 작업을 작성할 때 사용합니다.
API 요청, 타이머 등록, 브라우저 이벤트 연결처럼 컴포넌트가 화면에 나타난 뒤
실행해야 하는 작업이 여기에 들어갑니다.

```tsx
useEffect(() => {
  fetch('/api/items')
    .then((response) => response.json() as Promise<Item[]>)
    .then(setItems);
}, []);
```

두 번째 인자인 `[]`은 이 Effect가 처음 화면에 나타날 때 한 번 실행된다는 뜻입니다.
반면 특정 ID가 바뀔 때마다 다시 요청해야 한다면, 그 값을 의존성 배열에 넣습니다.

```tsx
useEffect(() => {
  fetch(`/api/items/${itemID}`);
}, [itemID]);
```

목록을 화면에 표시할 때는 배열의 `map()`을 사용해 각 항목을 JSX로 바꿉니다.
`key`에는 목록 안에서 변하지 않고 서로 다른 값을 넣어 React가 항목을 구분할 수 있게 합니다.

```tsx
<ul>
  {items.map((item) => (
    <li key={item.id}>{item.name}</li>
  ))}
</ul>
```

### Go 인터페이스와 의존성 주입

Go 인터페이스는 어떤 타입이 제공해야 할 메서드의 형태를 정의합니다.
구조체가 인터페이스에 적힌 모든 메서드를 가지면 별도 선언 없이 그 인터페이스를 구현합니다.

```go
type Item struct {
    ID   string
    Name string
}

type Store interface {
    List(context.Context) ([]Item, error)
}
```

이 방식은 흔히 덕 타이핑이라고 부르는 개념과 닮아 있습니다.
덕 타이핑은 타입의 이름이나 상속 관계보다, 필요한 동작을 실제로 제공하는지를 기준으로 값을 사용하는 방식입니다.
Go에서는 이를 조금 더 정확하게 "구조적 인터페이스"라고 설명합니다.
`implements Store`처럼 구현 사실을 별도로 선언하지 않아도,
`List(context.Context) ([]Item, error)` 메서드가 정확히 일치하면 `Store`로 사용할 수 있습니다.

`Item`은 저장소가 다루는 한 건의 데이터입니다.
이러한 데이터를 메모리에 보관하는 `MemoryStore`는 다음처럼 `List` 메서드를 구현할 수 있습니다.

```go
type MemoryStore struct {
    items []Item
}

func (s MemoryStore) List(context.Context) ([]Item, error) {
    return s.items, nil
}
```

`MemoryStore` 코드 어디에도 `Store`를 구현한다고 적지 않았습니다.
하지만 `Store`가 요구하는 `List` 메서드의 이름, 인자, 반환값이 모두 일치하므로,
Go는 `MemoryStore` 값을 `Store`로 사용할 수 있다고 판단합니다.
실제 PostgreSQL을 읽는 `PostgresStore`도
같은 형태의 `List` 메서드를 가지면 같은 `Store` 인터페이스로 사용할 수 있습니다.

이처럼 필요한 값을 함수 인자로 전달하는 방식을 의존성 주입이라고 합니다.
이번에 구현한 `PostgresStore`도 이런 방식을 통해 전역 변수에 DB 연결을 보관하는 대신,
함수가 필요한 `Store`를 명시적으로 받아 사용하므로
코드를 읽거나 테스트할 때 어떤 데이터 접근 방식을 쓰는지 확인하기 쉬워집니다.

### 센티널 에러와 오류 매핑

센티널 에러는 코드 여러 곳에서 같은 상황을 식별하기 위해 이름을 붙여 둔 오류 값입니다.
`errors.New()`로 만든 `ErrNotFound`를 패키지 수준 변수로 두면,
대시보드 조회, 사용자 조회처럼 서로 다른 코드도 "요청한 항목을 찾지 못했다"는 상태를 같은 값으로 반환할 수 있습니다.

호출하는 쪽은 오류 문자열을 비교하지 않고 `errors.Is(err, ErrNotFound)`로 이 상태인지 확인합니다.
오류가 다른 오류로 감싸진 경우까지 검사할 수 있으므로,
직접 `err == ErrNotFound`를 비교하는 것보다 안전합니다.

DB 드라이버가 반환하는 오류는 기술적인 원인을 나타냅니다.
예를 들어 `sql.ErrNoRows`는 쿼리 결과가 없다는 뜻이지만,
HTTP API를 사용하는 클라이언트에는 "요청한 리소스가 없다"는 의미의 404 응답이 더 적절합니다.

```go
var ErrNotFound = errors.New("item not found")

if errors.Is(err, sql.ErrNoRows) {
    return Item{}, ErrNotFound
}
```

이 코드는 `sql.ErrNoRows`를 애플리케이션이 정의한 `ErrNotFound`로 매핑합니다.
handler는 `ErrNotFound`를 보고 404로 응답하고,
DB 연결 실패처럼 다른 오류는 500으로 처리할 수 있습니다.

## 다음 작업

이번 글에서는 대시보드의 제목과 설명처럼 애플리케이션이 관리하는 메타데이터를 조회하는 흐름을 구현했습니다.
다음에는 대시보드가 실제 분석 데이터를 표시할 수 있도록, 분석 DB에 SQL을 실행하는 기능을 추가합니다.

먼저 Grafana의 PostgreSQL 패널이 SQL 요청과 결과를 어떻게 다루는지 살펴본 뒤,
`POST /api/v1/query` API를 구현할 예정입니다.
SQL 결과의 열 이름과 행을 담는 작은 `TableFrame`을 정의하고,
일별 매출 쿼리 결과를 첫 번째 Table 패널에 표시해 보겠습니다.

처음부터 여러 데이터소스나 완전한 DataFrame을 만들지는 않습니다.
정상 결과뿐 아니라 SQL 문법 오류, 빈 결과, 조회 시간 초과가 발생했을 때
패널이 각각 어떤 상태를 보여야 하는지도 함께 구현할 계획입니다.
