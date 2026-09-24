---
title: "Grafana 클론코딩 #3 - DB 데이터를 Table 패널로 표시하기"
date: "2026-09-25T00:43:21+09:00"
layout: "post"
description: >
  Grafana Table 패널을 클론코딩하며 PostgreSQL 분석 데이터를 Go query API와 React Table에 연결합니다.
  DataFrame과 TableFrame, 숫자와 날짜 서식, 정렬, 페이지네이션, 총계 행, 읽기 전용 SQL과 timeout 처리까지 구현하고 검증합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/r80lnshqk8ob9m6unenj3/grafana-clone-04-table-panel.webp?rlkey=iea03sqcuuofi56xtvd7ffjaw&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/aemlct9pg86wza6kwd7da/grafana-00-logo.webp?rlkey=ud43ycrmipiugi9hjwfh1zmgp&raw=1"
categories: ["Project", "Grafana Clone"]
tags: ["Grafana", "Grafana 클론코딩", "Grafana Table Panel", "BI 대시보드", "DataFrame", "PostgreSQL", "Go", "React", "TypeScript", "Vite", "Docker Compose", "SQL"]
series: ["Grafana 클론코딩"]
---

{{< series "Grafana 클론코딩" "Grafana 클론코딩 #[0-9]+ - " >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

[이전 글](/blog/grafana-clone-2/)에서는 DB에 저장한 대시보드 목록과 상세 정보를 화면에 표시했습니다.
이번에는 PostgreSQL의 분석 데이터를 실제 Table 패널까지 전달해,
날짜와 숫자가 있는 결과를 정렬하고 페이지별로 탐색할 수 있는 대시보드를 만듭니다.

Grafana의 Table 패널은 단순한 HTML 표가 아니라, 데이터소스의 결과를 공통 DataFrame으로 받아
필드 타입과 표시 형식, 정렬, 페이지네이션, 총계 행을 결합합니다. Grafana 소스와 문서를 먼저 확인하고,
그 흐름을 Go의 query API와 React Table 컴포넌트로 작게 재구현합니다.

- **[Grafana Table 패널](#grafana-table-패널-살펴보기)**: `TablePanel`, `TableNG`, `TableOptions`로 보는 Grafana Table의 데이터와 옵션 구조를 살펴봅니다.
- **[분석 DB query API](#분석-db-query-api)**: 분석용 PostgreSQL 연결부터 읽기 전용 SQL 검사, 타임아웃, `TableFrame` JSON 응답까지 구현합니다.
- **[React Table 패널](#react-table-패널)**: 날짜와 숫자 서식, `thead`와 `tbody`, 열 정렬, 총계 행, 페이지네이션을 하나의 표 화면으로 연결합니다.
- **[테스트와 빌드 검증](#테스트와-빌드-검증)**: 허용 SQL, 빈 결과, 행 제한, 타임아웃과 Docker Compose API 응답을 확인합니다.
{{% /hint %}}

[이전 글](/blog/grafana-clone-2/)에서는 대시보드 제목과 설명을 메타데이터 DB에 저장하고,
목록과 상세 URL을 구현했습니다. `sales-overview`를 열면 제목과 설명은 보이지만,
정작 대시보드가 보여 줄 매출 데이터는 아직 없었습니다.

이번에는 분석용 PostgreSQL에 SQL을 실행하고 그 결과를 첫 번째 표로 표시합니다.
날짜, 매출, 영업이익처럼 여러 열과 행으로 이루어진 결과를 읽기 좋게 보여 주는 것이 목표입니다.

Grafana의 표에는 각 열의 색을 바꾸거나, 숫자를 막대나 작은 그래프로 보이게 하거나,
셀을 눌러 다른 페이지로 이동하는 기능도 있습니다. 이런 기능은 사용자가 열마다 설정을 바꾸고
그 설정을 저장하는 화면이 먼저 필요합니다. 아직은 그 화면이 없으므로 이번 글에서는
날짜와 숫자의 표시 형식, 열 정렬, 페이지 나누기, 합계처럼 결과를 바로 읽는 데 필요한 기능만 구현합니다.

## Grafana Table 패널 살펴보기

Table 패널을 만들기 전에 Grafana의 현재 소스에서 다음 경로를 확인했습니다.

```text
public/app/plugins/panel/table/TablePanel.tsx
public/app/plugins/panel/table/module.tsx
public/app/features/table/hooks.ts
public/app/features/panel/table/addTableCustomPanelOptions.ts
packages/grafana-schema/src/common/common.gen.ts
docs/sources/visualizations/panels-visualizations/visualizations/table/index.md
```

`TablePanel.tsx`는 패널이 받은 `data.series` 중 표시할 DataFrame을 고르고,
`TableNG` 컴포넌트에 데이터, 정렬 상태, 페이지네이션, 열 너비 변경 함수를 전달합니다.
실제로 셀과 헤더를 그리는 역할은 `TableNG`가 맡습니다.

```tsx
// public/app/plugins/panel/table/TablePanel.tsx
export function TablePanel(props: Props) {
  ...
  const commonTableProps = useCommonTableProps(options, fieldConfig);
  const currentIndex = getCurrentFrameIndex(frames, options);
  const main = frames[currentIndex];

  const tableElement = (
    <TableNG
      {...commonTableProps}
      data={main}
      sortByBehavior={sortByBehavior}
      onSortByChange={(sortBy) => onSortByChange(sortBy, props)}
      onColumnResize={(displayName, resizedWidth, fieldScope) =>
        onColumnResize(displayName, resizedWidth, fieldScope, props)
      }
    />
  );
  ...
}
```

여기서 중요한 점은 Table 패널이 SQL 결과를 직접 해석하지 않는다는 점입니다.
`data`라는 공통 결과 모델을 받고, 각 필드의 이름과 타입, 값에 따라 표를 그립니다.
다른 데이터소스나 다른 패널도 같은 DataFrame 구조를 공유할 수 있는 이유입니다.

Grafana의 `TableOptions`에는 헤더 표시, 고정 열, 셀 높이, 페이지네이션, 정렬 상태가 들어 있습니다.
각 필드에는 정렬 가능 여부, 정렬 방향, 요약 행에 적용할 연산, 텍스트 줄바꿈 같은 별도 설정을 둘 수 있습니다.

```ts
// packages/grafana-schema/src/common/common.gen.ts
export interface TableOptions {
  cellHeight?: TableCellHeight;
  enablePagination?: boolean;
  frameIndex: number;
  frozenColumns?: { left?: number };
  pageSize?: number;
  showHeader: boolean;
  sortBy?: Array<TableSortByFieldState>;
}
```

이 중 이번 작은 구현에 필요한 기능은 필드 타입, 열 정렬, 페이지네이션, 요약 행입니다.
헤더를 클릭하면 기본 상태, 내림차순, 오름차순을 순서대로 바꾸는 동작도 Grafana 문서에서 확인했습니다.

## 분석 DB query API

대시보드 제목과 설명은 메타데이터 DB에서 읽지만, 매출과 영업이익은 분석 DB에서 읽어야 합니다.
두 DB를 섞지 않도록 Go 서버는 각각 별도의 `*sql.DB`를 만들고,
분석 DB 연결만 `query.NewPostgresRunner()`에 전달합니다.

### 서버에 분석 DB 연결하기

먼저 `PostgresRunner`는 **분석 DB에 SQL을 보내고 표 데이터를 받아 오는 역할**을 맡는 타입입니다.
대시보드 메타데이터를 읽는 `PostgresStore`와 달리, 이 타입은 매출처럼 화면에 표시할 분석 데이터를 조회합니다.

`NewPostgresRunner`는 이전 글에서 본 `NewPostgresStore`와 같이,
이미 만든 `*sql.DB`를 받아 `PostgresRunner`를 조립하는 생성 함수입니다.

```go
// backend/internal/query/query.go
type PostgresRunner struct {
	db *sql.DB
}

func NewPostgresRunner(db *sql.DB) *PostgresRunner {
	return &PostgresRunner{db: db}
}
```

`main()`은 환경 변수 `ANALYTICS_DATABASE_URL`에서 분석 DB의 접속 주소를 읽습니다.
이 URL에는 PostgreSQL 서버의 호스트, 포트, 데이터베이스 이름, 사용자 이름, 비밀번호가 들어 있습니다.
이 프로젝트의 Docker Compose 환경에서 백엔드 컨테이너는 `analytics-db:5432`에 있는 `profit_demo` 데이터베이스에 접속합니다.

`sql.Open()`은 드라이버를 선택하고 연결 풀 관리자를 만들지만, 이 시점에 항상 PostgreSQL 서버와 통신하는 것은 아닙니다.
그래서 바로 뒤에 `PingContext()`를 호출합니다. 이 호출은 풀에서 연결 하나를 확보해 `analytics-db`라는 호스트를 찾고,
5432 포트에 접속한 뒤, URL의 계정으로 인증하고, PostgreSQL 서버가 요청을 받을 수 있는지 확인합니다.
호스트 이름, 포트, 비밀번호, 데이터베이스 이름 중 하나라도 잘못되었거나 DB가 아직 준비되지 않았다면 오류가 반환되고 서버는 시작하지 않습니다.

연결 확인을 통과하면 메타데이터 DB의 `PostgresStore`와 분석 DB의 `PostgresRunner`를 함께 handler에 전달합니다.
둘은 모두 DB를 사용하지만, 어느 DB에서 어떤 데이터를 읽을지 역할을 나눠 둔 것입니다.

```go
// backend/cmd/api/main.go
func main() {
    ...
    analyticsDB, err := sql.Open("pgx", os.Getenv("ANALYTICS_DATABASE_URL"))
    if err != nil {
        log.Fatalf("open analytics database: %v", err)
    }
    defer analyticsDB.Close()

    if err := analyticsDB.PingContext(context.Background()); err != nil {
        log.Fatalf("ping analytics database: %v", err)
    }

    server := &http.Server{
        Addr:              ":" + port,
        Handler:           newHandler(dashboard.NewPostgresStore(db), query.NewPostgresRunner(analyticsDB)),
        ReadHeaderTimeout: 5 * time.Second,
    }
    ...
}
```

`newHandler`는 기존 대시보드 Store 외에 query Runner를 추가 인자로 받습니다.
`query.NewPostgresRunner(analyticsDB)`가 만든 값은 뒤에서 소개할 `Runner`가 요구하는
`Query()` 메서드를 가지고 있으므로 여기에 전달할 수 있습니다.
이렇게 하면 handler 테스트에서는 실제 PostgreSQL 연결 대신 같은 `Query()` 메서드를 가진 가짜 Runner를 넣을 수 있습니다.

```go
// backend/cmd/api/main.go
func newHandler(store dashboard.Store, runner query.Runner) http.Handler {
    mux := http.NewServeMux()
    mux.HandleFunc("GET /api/health", health)
    mux.HandleFunc("GET /api/v1/dashboards", listDashboards(store))
    mux.HandleFunc("GET /api/v1/dashboards/{uid}", getDashboard(store))
    mux.HandleFunc("POST /api/v1/query", runQuery(runner))
    return cors(mux)
}
```

### TableFrame과 Runner

Grafana의 DataFrame 전체를 처음부터 구현하지 않고, 표를 구성하는데 필요한 부분만 `TableFrame`으로 정의했습니다.

`Fields`는 열의 이름과 타입을, `Rows`는 행마다 들어갈 값을 가집니다.
열 이름만 문자열 배열로 보내면 `2026-07-01T00:00:00Z` 등의 날짜와 `49770800.00` 등의 숫자가 모두 문자열처럼 보입니다.
타입에 따라 사용자에게 더 보기 좋은 서식으로 보여주기 위해 API가 `time`, `number`, `string` 타입을 함께 전달하도록 만들었습니다.

```go
// backend/internal/query/query.go
type TableFrame struct {
    Fields []Field `json:"fields"`
    Rows   [][]any `json:"rows"`
}

type Field struct {
    Name string `json:"name"`
    Type string `json:"type"`
}

type Runner interface {
    Query(context.Context, string) (TableFrame, error)
}
```

`Runner`는 SQL 문장과 요청 context를 받아 `TableFrame`으로 바꾸는 메서드만 선언합니다.
HTTP handler는 PostgreSQL 구현인지, 테스트 대역인지 알 필요가 없습니다.

### 읽기 전용 SQL 실행

`PostgresRunner.Query()`는 받은 SQL을 바로 실행하지 않습니다. 먼저 문장을 정리하고,
조회만 허용되는지 검사한 뒤, 읽기 전용 트랜잭션 안에서 실행합니다. 마지막에는 DB 결과를 `TableFrame`으로 바꿉니다.

`Query()`가 가장 먼저 실행하는 코드는 아래 두 줄입니다. `normalizeStatement()`는 문장을 정리하고,
`isReadOnlyStatement()`는 정리된 문장이 조회용 SQL인지 확인합니다. 다음 단계로 넘어가기 전에 두 보조 함수를 먼저 살펴보겠습니다.

```go
// backend/internal/query/query.go
var ErrInvalidStatement = errors.New("only SELECT statements are allowed")

func (r *PostgresRunner) Query(ctx context.Context, statement string) (TableFrame, error) {
	statement = normalizeStatement(statement)
	if !isReadOnlyStatement(statement) {
		return TableFrame{}, ErrInvalidStatement
	}
	...
}
```

`normalizeStatement()` 함수는 SQL 앞뒤의 공백을 없애고, 맨 마지막 세미콜론 하나만 제거합니다.
예를 들어 브라우저가 `"  SELECT * FROM sales;  "`를 보내면
검사하기 전에 `"SELECT * FROM sales"`로 바뀝니다.
끝의 세미콜론은 SQL을 한 문장으로 쓸 때 흔히 붙지만, 이 API에서는 필요하지 않기 때문입니다.

```go
// backend/internal/query/query.go
func normalizeStatement(statement string) string {
	statement = strings.TrimSpace(statement)
	statement = strings.TrimSuffix(statement, ";")
	return strings.TrimSpace(statement)
}
```

`isReadOnlyStatement()` 함수는 그 다음에 실행됩니다. 이 함수는 문장 중간에 세미콜론이 있으면 여러 SQL 문장을
보내려는 시도로 보고 거부합니다. 이어서 첫 단어가 `SELECT` 또는 `WITH`일 때만 `true`를 반환합니다.
`WITH`는 임시 결과를 만든 뒤 마지막에 `SELECT`하는 CTE 문법을 허용하기 위해 포함했습니다.

```go
// backend/internal/query/query.go
func isReadOnlyStatement(statement string) bool {
	if strings.Contains(statement, ";") {
		return false
	}

	keywords := strings.Fields(statement)
	if len(keywords) == 0 {
		return false
	}

	switch strings.ToLower(keywords[0]) {
	case "select", "with":
		return true
	default:
		return false
	}
}
```

`strings.Fields(statement)`는 문자열을 공백, 탭, 줄바꿈을 기준으로 나누어 단어 배열로 만드는 Go 함수입니다.
예를 들어 `"SELECT order_date FROM sales_daily"` SQL이 전달된다면 첫 번째 값은 `"SELECT"`가 됩니다.

따라서 `keywords[0]`을 검사하면 한 줄 SQL과 줄바꿈 SQL을 같은 조회문으로 판단할 수 있습니다.
검사를 통과하지 못하면 `Query()`는 앞의 코드처럼 빈 `TableFrame`과 `ErrInvalidStatement`를 반환하고,
아래의 트랜잭션과 실제 쿼리 실행은 시작하지 않습니다.

SQL 검사를 통과한 다음에야 `Query()`는 분석 DB의 트랜잭션을 시작합니다.
`r.db`는 `PostgresRunner`가 보관한 분석 DB 연결 풀이고, `BeginTx()`는 그 풀에서 연결 하나를 빌려
`tx`라는 트랜잭션 객체를 만듭니다.

```go
// backend/internal/query/query.go
func (r *PostgresRunner) Query(ctx context.Context, statement string) (TableFrame, error) {
	...
	tx, err := r.db.BeginTx(ctx, &sql.TxOptions{ReadOnly: true})
	if err != nil {
		return TableFrame{}, err
	}
	defer tx.Rollback()

	...
}
```

`ReadOnly: true`는 이 트랜잭션 안에서 데이터를 바꾸는 명령을 DB가 거부하도록 하는 두 번째 안전장치입니다.
위의 문자열 검사와 별개로 DB에도 읽기 전용이라는 제약을 전달합니다.
`defer tx.Rollback()`은 함수가 어느 지점에서 끝나도 트랜잭션을 정리하도록 예약합니다.
정상 경로에서 뒤의 `tx.Commit()`이 먼저 끝낸 경우에는 `Rollback()`이 할 일이 없습니다.

다음으로 `SET LOCAL`로 현재 트랜잭션에만 3초 타임아웃 제한을 설정하고, 사용자가 보낸 SQL을 실행합니다.
`ExecContext()`는 결과 행을 받을 필요 없는 설정 SQL을 실행할 때 사용합니다.
반면 `QueryContext()`는 조회 결과 행을 받을 때 사용합니다.

```go
// backend/internal/query/query.go
func (r *PostgresRunner) Query(ctx context.Context, statement string) (TableFrame, error) {
	...
	if _, err := tx.ExecContext(ctx, "SET LOCAL statement_timeout = '3000ms'"); err != nil {
		return TableFrame{}, err
	}

	rows, err := tx.QueryContext(ctx, "SELECT * FROM ("+statement+") AS dashboard_lab_query LIMIT 100")
	if err != nil {
		return TableFrame{}, err
	}
	defer rows.Close()

	...
}
```

`SET LOCAL`은 이 트랜잭션이 끝나면 함께 사라지므로, 다음 요청에 타임아웃 설정이 남지 않습니다.
사용자 SQL을 `SELECT * FROM (...) AS dashboard_lab_query LIMIT 100`으로 감싼 이유는
결과를 최대 100행으로 제한하기 위해서입니다.
`defer rows.Close()`도 함수가 끝날 때 DB가 사용한 결과 자원을 반납하도록 예약합니다.

`ColumnTypes()`는 PostgreSQL이 반환한 각 열의 이름과 DB 타입을 제공합니다.
이 정보를 `Field` 배열로 바꾸고, `rows.Scan()`으로 읽은 실제 행을 뒤에 붙입니다.

```go
// backend/internal/query/query.go
func (r *PostgresRunner) Query(ctx context.Context, statement string) (TableFrame, error) {
	...
	columnTypes, err := rows.ColumnTypes()
	if err != nil {
		return TableFrame{}, err
	}
	fields := make([]Field, len(columnTypes))
	for index, column := range columnTypes {
		fields[index] = Field{Name: column.Name(), Type: fieldType(column.DatabaseTypeName())}
	}

	frame := TableFrame{Fields: fields, Rows: make([][]any, 0)}
	...
}
```

`fields`에는 `날짜`는 `time`, `매출`은 `number`처럼 각 열의 표시용 타입을 담습니다.
DB 타입은 `fieldType()`에서 표에 필요한 `time`, `number`, `string` 세 종류로 축소합니다.

```go
// backend/internal/query/query.go
func fieldType(databaseType string) string {
	switch strings.ToUpper(databaseType) {
	case "INT2", "INT4", "INT8", "FLOAT4", "FLOAT8", "NUMERIC", "DECIMAL":
		return "number"
	case "DATE", "TIMESTAMP", "TIMESTAMPTZ":
		return "time"
	default:
		return "string"
	}
}
```

이어서 `rows.Next()`가 결과의 다음 행으로 이동할 때마다,
그 행의 값을 `values` 배열에 채우고 `frame.Rows`에 추가합니다.

```go
// backend/internal/query/query.go
func (r *PostgresRunner) Query(ctx context.Context, statement string) (TableFrame, error) {
	...
	for rows.Next() {
		values := make([]any, len(fields))
		pointers := make([]any, len(fields))
		for index := range values {
			pointers[index] = &values[index]
		}
		if err := rows.Scan(pointers...); err != nil {
			return TableFrame{}, err
		}
		frame.Rows = append(frame.Rows, values)
	}

	if err := rows.Err(); err != nil {
		return TableFrame{}, err
	}
	if err := tx.Commit(); err != nil {
		return TableFrame{}, err
	}
	return frame, nil
}
```

`values`에는 현재 행의 값이 들어가고, `pointers`에는 그 값들이 기록될 위치가 들어갑니다.
`Scan()`은 값을 넣을 위치를 받아야 하므로 `&values[index]`를 전달합니다.
모든 행을 읽은 뒤 `rows.Err()`로 순회 중 오류가 없었는지 확인하고,
`tx.Commit()`으로 트랜잭션을 정상 종료한 후 `frame`을 반환합니다.

PostgreSQL은 `statement_timeout`으로 취소된 쿼리에 SQLSTATE `57014`를 반환합니다.
SQLSTATE는 DB가 오류 종류를 구분하기 위해 함께 보내는 다섯 자리 코드입니다.
`IsTimeout`은 드라이버의 `*pgconn.PgError`를 꺼내 이 코드인지 확인하고,
handler가 일반적인 500 오류 대신 504 응답을 만들 수 있게 합니다.

```go
// backend/internal/query/query.go
func IsTimeout(err error) bool {
    var postgresError *pgconn.PgError
    return errors.As(err, &postgresError) && postgresError.Code == "57014"
}

func FormatError(err error) string {
    if errors.Is(err, ErrInvalidStatement) {
        return err.Error()
    }
    return fmt.Sprintf("query failed: %v", err)
}
```

### 쿼리 요청과 응답

`POST /api/v1/query`는 `{ "sql": "..." }` JSON을 받아 `Runner`에 전달합니다.
허용하지 않은 SQL은 `400 Bad Request`, 3초 제한을 넘긴 SQL은 `504 Gateway Timeout`,
그 밖의 DB 오류는 `500 Internal Server Error`로 구분했습니다.

```go
// backend/cmd/api/main.go
type queryRequest struct {
    SQL string `json:"sql"`
}

func runQuery(runner query.Runner) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        var request queryRequest
        if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
            writeError(w, http.StatusBadRequest, "request body must contain SQL")
            return
        }

        frame, err := runner.Query(r.Context(), request.SQL)
        if errors.Is(err, query.ErrInvalidStatement) {
            writeError(w, http.StatusBadRequest, err.Error())
            return
        }
        if query.IsTimeout(err) {
            writeError(w, http.StatusGatewayTimeout, "query timed out after 3 seconds")
            return
        }
        if err != nil {
            writeError(w, http.StatusInternalServerError, query.FormatError(err))
            return
        }

        writeJSON(w, http.StatusOK, frame)
    }
}
```

`analytics.profit_daily()` 테이블 함수로
2026년 7월의 일별 매출과 영업이익을 집계하는 SQL은 다음과 같습니다.
대시보드 편집 기능은 아직 없으므로 이 SQL은 프론트엔드 상수로 두었습니다.

```sql
SELECT
    order_date AS "날짜"
  , SUM(payment_amount) AS "매출"
  , SUM(profit) AS "영업이익"
FROM analytics.profit_daily(DATE '2026-07-01', DATE '2026-07-31')
GROUP BY order_date
ORDER BY order_date
```

정상 응답의 `fields`는 값만 보내지 않고 각 열의 타입도 포함합니다.

```json
{
  "fields": [
    { "name": "날짜", "type": "time" },
    { "name": "매출", "type": "number" },
    { "name": "영업이익", "type": "number" }
  ],
  "rows": [
    ["2026-07-01T00:00:00Z", "49770800.00", "16170800.00"]
  ]
}
```

## React Table 패널

### Vite proxy와 데이터 요청

브라우저가 `localhost:8080`으로 직접 요청하는 대신, Vite 개발 서버의 `/api` 경로로 요청하게 바꿨습니다.
`vite.config.ts`는 `/api`로 시작하는 요청을 Docker 네트워크 안의 `backend:8080`에 전달합니다.
이렇게 하면 브라우저는 `localhost:5173`이라는 같은 출처로 요청하고,
개발 환경에서 API 주소를 화면 코드에 반복해서 쓰지 않아도 됩니다.

```ts
// frontend/vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: process.env.VITE_PROXY_TARGET ?? 'http://backend:8080',
        changeOrigin: true,
      },
    },
  },
});
```

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/9lif23ld42ketd35a2sbe/grafana-clone-05-api-query.webp?rlkey=cv6guxa7l0v67go98y3xq9ro6&raw=1"
  alt="http://localhost:5173/api/v1/query"
  caption="크롬 브라우저에서 확인되는 네트워크 요청" >}}

프론트엔드의 `TableFrame`과 `TableField`도 API JSON과 같은 구조로 선언합니다.
`type`을 문자열 전체가 아니라 세 개의 값으로 제한해, 표시와 정렬 코드가 예상 밖의 타입을 받지 않게 했습니다.

```tsx
// frontend/src/main.tsx
type TableFrame = {
  fields: TableField[];
  rows: unknown[][];
};

type TableField = {
  name: string;
  type: 'number' | 'string' | 'time';
};
```

`DailySalesTable`은 처음 표시될 때 query API를 호출합니다.
요청 중에는 "표 데이터를 불러오는 중입니다." 문구를,
빈 배열이면 "조회된 데이터가 없습니다." 문구를,
API가 실패하면 서버가 보낸 오류 메시지를 표시합니다.

```tsx
// frontend/src/main.tsx
function DailySalesTable() {
  const [frame, setFrame] = useState<TableFrame>();
  const [error, setError] = useState<string>();

  useEffect(() => {
    fetch(`${apiURL}/api/v1/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sql: dailySalesQuery }),
    })
      .then(async (response) => {
        if (!response.ok) {
          const body = await response.json().catch(() => undefined) as { message?: string } | undefined;
          throw new Error(body?.message ?? '표 데이터를 불러오지 못했습니다.');
        }
        return response.json() as Promise<TableFrame>;
      })
      .then(setFrame)
      .catch((reason: unknown) => setError(reason instanceof Error ? reason.message : '알 수 없는 오류가 발생했습니다.'));
  }, []);

  return (
    <section aria-labelledby="daily-sales-panel-title" className="panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Table</p>
          <h2 id="daily-sales-panel-title">일별 매출과 영업이익</h2>
        </div>
        <span>2026. 7. 1. - 2026. 7. 31.</span>
      </div>
      {error ? <p className="error-message">{error}</p> : null}
      {!frame && !error ? <p className="muted">표 데이터를 불러오는 중입니다.</p> : null}
      {frame && frame.rows.length === 0 ? <p className="muted">조회된 데이터가 없습니다.</p> : null}
      {frame && frame.rows.length > 0 ? <Table frame={frame} /> : null}
    </section>
  );
}
```

### 타입별 표시와 총계 행

`Table`은 `time` 필드를 `YYYY-MM-DD`로, `number` 필드를 소수점 없는 `#,##0` 형식으로 표시합니다.
API에서 숫자가 문자열 형태로 도착해도 field type이 `number`이면 숫자로 변환해 표시합니다.

```tsx
// frontend/src/main.tsx
function formatCell(value: unknown, field: TableField) {
  if (value === null) {
    return '-';
  }

  const text = String(value);
  if (field.type === 'time' && isISODate(text)) {
    return text.slice(0, 10);
  }
  if (field.type === 'number' && isNumeric(text)) {
    return new Intl.NumberFormat('ko-KR', { maximumFractionDigits: 0 }).format(Number(text));
  }
  return text;
}

function cellClassName(field: TableField) {
  return field.type === 'number' ? 'numeric-cell' : undefined;
}
```

Grafana의 요약 행은 열마다 계산한 결과를 표시합니다. 이번 패널에는 그중 합계 하나만 고정해,
모든 행의 숫자 열을 합산합니다. 페이지네이션으로 현재 페이지가 바뀌어도 합계는 전체 query 결과를 기준으로 유지됩니다.

```tsx
// frontend/src/main.tsx
function calculateTotals(frame: TableFrame) {
  return frame.fields.map((field, columnIndex) => frame.rows.reduce((total, row) => {
    const value = String(row[columnIndex]);
    return field.type === 'number' && isNumeric(value) ? total + Number(value) : total;
  }, 0));
}
```

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/alarpaaee6m6auxrgx3vg/grafana-clone-06-table.webp?rlkey=4dk1iwp2i7fjz89nnnw0h950n&raw=1"
  alt="Table > 일별 매출과 영업이익"
  caption="타입별 표시와 총계 행을 반영한 Table 패널" >}}

### 열 정렬과 페이지네이션

Grafana처럼 열 헤더를 누르면 기본 순서, 내림차순, 오름차순을 순환합니다.
정렬 상태에는 어느 열인지와 어느 방향인지가 들어갑니다. 다른 열을 처음 누르면 내림차순부터 시작하고,
같은 열을 다시 누르면 오름차순, 한 번 더 누르면 정렬하지 않은 원래 순서로 돌아갑니다.

아래는 `Table` 함수의 시작 부분입니다. 함수의 나머지 JSX는 다음 코드 블록에서 이어집니다.

```tsx
// frontend/src/main.tsx
function Table({ frame }: { frame: TableFrame }) {
  const [sort, setSort] = useState<SortState>();
  const [page, setPage] = useState(0);
  const totals = calculateTotals(frame);
  const rows = sortRows(frame, sort);
  const pageSize = 10;
  const pageCount = Math.ceil(rows.length / pageSize);
  const visibleRows = rows.slice(page * pageSize, (page + 1) * pageSize);

  function changeSort(columnIndex: number) {
    setPage(0);
    setSort((current) => {
      if (current?.columnIndex !== columnIndex) {
        return { columnIndex, direction: 'desc' };
      }
      if (current.direction === 'desc') {
        return { columnIndex, direction: 'asc' };
      }
      return undefined;
    });
  }

  // 아래 JSX에서 헤더, 현재 페이지의 행, 총계 행, 페이지 버튼을 렌더링합니다.
  ...
}
```

`sortRows`는 원래 `frame.rows` 배열을 직접 정렬하지 않고 `[...frame.rows]`로 복사한 배열을 정렬합니다.
`Array.sort()`는 원본 배열을 바꾸므로, API 응답으로 받은 원래 순서를 보존하기 위해서입니다.

```tsx
// frontend/src/main.tsx
function sortRows(frame: TableFrame, sort: SortState | undefined) {
  if (!sort) {
    return frame.rows;
  }

  const field = frame.fields[sort.columnIndex];
  return [...frame.rows].sort((left, right) => {
    const leftValue = sortValue(left[sort.columnIndex], field.type);
    const rightValue = sortValue(right[sort.columnIndex], field.type);
    const result = leftValue < rightValue ? -1 : leftValue > rightValue ? 1 : 0;
    return sort.direction === 'asc' ? result : -result;
  });
}

function sortValue(value: unknown, type: TableField['type']) {
  return type === 'number' ? Number(value) : String(value);
}
```

Table 패널은 열 제목을 담는 `thead`, 실제 데이터를 담는 `tbody`, 그리고 집계값을 담는 `tfoot`으로 나뉩니다.
여기서 `thead`는 `frame.fields`를 순회해 `날짜`, `매출`, `영업이익` 같은 열 제목을 만듭니다.
각 제목은 클릭 가능한 `button`이므로 마우스뿐 아니라 Tab 키와 Enter 키로도 정렬을 실행할 수 있습니다.

```tsx
// frontend/src/main.tsx
function Table({ frame }: { frame: TableFrame }) {
  ...
  return (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            {frame.fields.map((field, columnIndex) => (
              <th aria-sort={sortAriaValue(sort, columnIndex)} className={field.type === 'number' ? 'numeric-cell' : undefined} key={field.name}>
                <button className="sort-button" onClick={() => changeSort(columnIndex)} type="button">
                  {field.name}<SortIndicator sort={sort} columnIndex={columnIndex} />
                </button>
              </th>
            ))}
          </tr>
        </thead>
        {/* 아래 데이터 행 JSX가 이어집니다. */}
        <tbody>...</tbody>
        {/* 아래 총계 행 JSX가 이어집니다. */}
        <tfoot>...</tfoot>
      </table>
      {/* 아래 페이지네이션 JSX가 이어집니다. */}
      <div className="table-pagination">...</div>
    </div>
  );
}
```

`tbody`는 표의 실제 데이터 행을 그리는 부분입니다.
앞에서 만든 `visibleRows`에는 현재 페이지에 보여 줄 최대 10개의 행만 들어 있습니다.
바깥쪽 `map()`이 각 행마다 `tr` 한 줄을 만들고, 안쪽 `map()`이 그 행의 값마다 `td` 셀 하나를 만듭니다.
각 셀은 `formatCell()`을 거쳐 날짜는 `YYYY-MM-DD`, 숫자는 천 단위 쉼표가 있는 정수 형식으로 표시됩니다.
`cellClassName()`은 숫자 셀에 `numeric-cell` 클래스를 붙여 오른쪽 정렬되게 합니다.

```tsx
// frontend/src/main.tsx
function Table({ frame }: { frame: TableFrame }) {
  ...
  return (
    <div className="table-scroll">
      <table>
        <thead>...</thead>
        <tbody>
          {visibleRows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((value, columnIndex) => (
                <td className={cellClassName(frame.fields[columnIndex])} key={`${rowIndex}-${columnIndex}`}>
                  {formatCell(value, frame.fields[columnIndex])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
        {/* 아래 총계 행 JSX가 이어집니다. */}
        <tfoot>...</tfoot>
      </table>
      {/* 아래 페이지네이션 JSX가 이어집니다. */}
      <div className="table-pagination">...</div>
    </div>
  );
}
```

`tfoot`은 표의 맨 아래에 총계처럼 별도 성격의 행을 두는 HTML 영역입니다.
이 구현에서는 첫 번째 열에 `합계`라는 레이블을 표시하고,
숫자 열에는 `calculateTotals()`가 모든 조회 행을 더해 만든 값을 넣습니다.
따라서 현재 화면에 10행만 보이더라도 총계는 현재 페이지가 아니라 조회된 전체 31행을 기준으로 계산됩니다.

```tsx
// frontend/src/main.tsx
function Table({ frame }: { frame: TableFrame }) {
  ...
  return (
    <div className="table-scroll">
      <table>
        <thead>...</thead>
        <tbody>...</tbody>
        <tfoot>
          <tr>
            {frame.fields.map((field, columnIndex) => (
              <td className={columnIndex === 0 ? 'total-label' : 'numeric-cell'} key={field.name}>
                {columnIndex === 0 ? '합계' : formatCell(totals[columnIndex], field)}
              </td>
            ))}
          </tr>
        </tfoot>
      </table>
      {/* 아래 페이지네이션 JSX가 이어집니다. */}
      <div className="table-pagination">...</div>
    </div>
  );
}
```

표 아래의 페이지네이션은 `tfoot`과 달리 `table` 바깥에 둡니다.
`span` 요소는 현재 보고 있는 행 범위와 전체 행 수를 보여 줍니다.
예를 들어 첫 페이지에서는 `1-10 / 31행`, 마지막 페이지에서는 `21-31 / 31행`이 표시됩니다.
이전 버튼은 첫 페이지에서, 다음 버튼은 마지막 페이지에서 비활성화해 더 이상 이동할 수 없는 방향으로
`page` 값이 바뀌지 않게 했습니다.

```tsx
// frontend/src/main.tsx
function Table({ frame }: { frame: TableFrame }) {
  ...
  return (
    <div className="table-scroll">
      <table>
        <thead>...</thead>
        <tbody>...</tbody>
        <tfoot>...</tfoot>
      </table>
      <div className="table-pagination">
        <span>{rows.length === 0 ? '0' : `${page * pageSize + 1}-${Math.min((page + 1) * pageSize, rows.length)}`} / {rows.length}행</span>
        <div>
          <button aria-label="이전 페이지" disabled={page === 0} onClick={() => setPage((current) => current - 1)} type="button">이전</button>
          <button aria-label="다음 페이지" disabled={page >= pageCount - 1} onClick={() => setPage((current) => current + 1)} type="button">다음</button>
        </div>
      </div>
    </div>
  );
}
```

`thead`, `tbody`, `tfoot` 및 페이지네이션으로 구성된 `Table` 패널은
최종적으로 다음과 같이 표시됩니다.

![Table > 일별 매출과 영업이익 + 페이지네이션](https://dl.dropboxusercontent.com/scl/fi/9zngr3gqyf1tdynprs2tu/grafana-clone-07-table-panel.webp?rlkey=26y7mkm3d9ka8ijs2wutnd938&raw=1)

## 테스트와 빌드 검증

### query 패키지 테스트

`PostgresRunner`의 실제 SQL 실행은 PostgreSQL 컨테이너가 필요하지만,
SQL 문장 허용 여부, 타임아웃 오류 판별, DB 타입 변환은 DB 연결 없이 단위 테스트할 수 있습니다.

`DELETE`가 거부되는지, `SELECT`와 `WITH ... SELECT`가 허용되는지,
끝 세미콜론과 줄바꿈이 있는 `SELECT`도 같은 방식으로 처리되는지 확인했습니다.

```go
// backend/internal/query/query_test.go
func TestPostgresRunnerAcceptsSelectAndWithStatements(t *testing.T) {
  for _, statement := range []string{
    "SELECT id FROM items",
    "SELECT id FROM items;",
    "SELECT\n  id\nFROM items",
    "WITH recent AS (SELECT id FROM items) SELECT id FROM recent",
  } {
    if !isReadOnlyStatement(normalizeStatement(statement)) {
      t.Fatalf("expected statement to be accepted: %s", statement)
    }
  }
}

func TestFieldType(t *testing.T) {
  tests := map[string]string{
    "NUMERIC": "number",
    "TIMESTAMPTZ": "time",
    "TEXT": "string",
  }

  for databaseType, expected := range tests {
    if actual := fieldType(databaseType); actual != expected {
      t.Fatalf("fieldType(%q) = %q, want %q", databaseType, actual, expected)
    }
  }
}
```

handler 테스트의 가짜 `Runner`도 `TableFrame`을 반환하도록 만들었습니다.
이 테스트는 실제 분석 DB를 거치지 않고도 `POST /api/v1/query`가 200과 표 JSON을 반환하는지 확인합니다.

```go
// backend/cmd/api/main_test.go
type fakeQueryRunner struct {
  frame query.TableFrame
  err   error
}

func (r fakeQueryRunner) Query(context.Context, string) (query.TableFrame, error) {
  return r.frame, r.err
}

func TestRunQuery(t *testing.T) {
  runner := fakeQueryRunner{frame: query.TableFrame{
    Fields: []query.Field{{Name: "name", Type: "string"}},
    Rows:   [][]any{{"dashboard-lab"}},
  }}
  req := httptest.NewRequest(http.MethodPost, "/api/v1/query", strings.NewReader(`{"sql":"SELECT name FROM items"}`))
  res := httptest.NewRecorder()

  newHandler(fakeDashboardStore{}, runner).ServeHTTP(res, req)

  if res.Code != http.StatusOK {
    t.Fatalf("expected status %d, got %d", http.StatusOK, res.Code)
  }
}
```

백엔드와 프론트엔드는 각각 다음 명령으로 검증했습니다.

```bash
backend % GOWORK=off go test ./...
ok      github.com/minyeamer/dashboard-lab/backend/cmd/api       0.875s
?       github.com/minyeamer/dashboard-lab/backend/internal/dashboard  [no test files]
ok      github.com/minyeamer/dashboard-lab/backend/internal/query 0.493s
```

```bash
frontend % npm run build

> dashboard-lab-frontend@0.0.0 build
> tsc -b && vite build

vite v6.3.5 building for production...
✓ 28 modules transformed.
dist/index.html                   0.40 kB │ gzip:  0.27 kB
dist/assets/index-Bsv2pEYB.css    2.47 kB │ gzip:  0.97 kB
dist/assets/index-CLLJfmqU.js   200.67 kB │ gzip: 63.20 kB
✓ built in 343ms
```

### Docker Compose와 API 검증

Docker Compose를 다시 빌드하면 backend는 새 query 패키지를 포함하고,
frontend는 Vite proxy를 통해 같은 출처의 `/api`를 요청합니다.

```bash
docker compose up --build -d
```

API에는 실제 패널과 같은 일별 매출 SQL을 보냈습니다. `fields`에 날짜와 숫자 타입이 포함되고,
`rows`에 31일치 집계 결과가 반환되는 것을 확인했습니다.

```bash
curl -X POST http://localhost:5173/api/v1/query \
  -H 'Content-Type: application/json' \
  --data @- <<'JSON'
{"sql":"SELECT order_date, SUM(payment_amount) AS sales FROM analytics.profit_daily(DATE '2026-07-01', DATE '2026-07-31') GROUP BY order_date ORDER BY order_date"}
JSON
```

```json
{"fields":[{"name":"order_date","type":"time"},{"name":"sales","type":"number"}],
"rows":[["2026-07-01T00:00:00Z","49770800.00"],["2026-07-02T00:00:00Z","40776100.00"],
["2026-07-03T00:00:00Z","36713400.00"],["2026-07-04T00:00:00Z","31201100.00"],
["2026-07-05T00:00:00Z","37108800.00"],["2026-07-06T00:00:00Z","44565700.00"],
["2026-07-07T00:00:00Z","41845100.00"],["2026-07-08T00:00:00Z","40029000.00"],
["2026-07-09T00:00:00Z","40173400.00"],["2026-07-10T00:00:00Z","34544600.00"],
["2026-07-11T00:00:00Z","30925300.00"],["2026-07-12T00:00:00Z","35074200.00"],
["2026-07-13T00:00:00Z","45485000.00"],["2026-07-14T00:00:00Z","41307000.00"],
["2026-07-15T00:00:00Z","39374000.00"],["2026-07-16T00:00:00Z","39839600.00"],
["2026-07-17T00:00:00Z","34682500.00"],["2026-07-18T00:00:00Z","30436000.00"],
["2026-07-19T00:00:00Z","36589400.00"],["2026-07-20T00:00:00Z","43821200.00"],
["2026-07-21T00:00:00Z","40555000.00"],["2026-07-22T00:00:00Z","39674500.00"],
["2026-07-23T00:00:00Z","40975900.00"],["2026-07-24T00:00:00Z","36746200.00"],
["2026-07-25T00:00:00Z","31678900.00"],["2026-07-26T00:00:00Z","36848500.00"],
["2026-07-27T00:00:00Z","44660500.00"],["2026-07-28T00:00:00Z","41259400.00"],
["2026-07-29T00:00:00Z","39927100.00"],["2026-07-30T00:00:00Z","39591900.00"],
["2026-07-31T00:00:00Z","35815600.00"]]}
```

빈 기간을 조회하면 `rows: []`가 반환되고, 101행을 만드는 쿼리는 100행으로 제한됩니다.
`SELECT pg_sleep(4)`는 3초 뒤 `504`와 `query timed out after 3 seconds` 응답을 반환합니다.

## React와 Go 개념 정리

본문에서는 Table 패널의 흐름을 따라 코드를 살펴봤습니다. 여기서는 그 과정에서 나온 기능을 특정 화면이나 프로젝트와 분리해 정리합니다.

### JavaScript 숫자 서식

`Intl.NumberFormat`은 JavaScript가 제공하는 지역화된 숫자 서식 도구입니다. 숫자 자체를 바꾸지 않고,
사용자가 읽을 문자열만 만듭니다. 따라서 계산과 정렬에는 원래 숫자를 쓰고, 화면에 넣을 때만 `format()`을 호출하는 편이 안전합니다.

```ts
const integerFormatter = new Intl.NumberFormat('ko-KR', {
  maximumFractionDigits: 0,
});

integerFormatter.format(49770800.75); // "49,770,801"
```

첫 번째 인자인 `'ko-KR'`은 한국어권 숫자 표기 규칙을 뜻합니다. 이 값에 따라 천 단위 구분 기호, 소수점 기호,
일부 언어권에서는 숫자 문자 자체도 달라질 수 있습니다. `maximumFractionDigits: 0`은 소수점 아래를 표시하지 않으며,
값을 단순히 잘라 내는 것이 아니라 반올림합니다. 소수점을 항상 두 자리까지 보여 줘야 한다면
`minimumFractionDigits: 2`와 `maximumFractionDigits: 2`를 함께 지정합니다.

통화, 퍼센트, 단위도 같은 방식으로 표현할 수 있습니다.

```ts
const currencyFormatter = new Intl.NumberFormat('ko-KR', {
  style: 'currency',
  currency: 'KRW',
  maximumFractionDigits: 0,
});

const rateFormatter = new Intl.NumberFormat('ko-KR', {
  style: 'percent',
  maximumFractionDigits: 1,
});

currencyFormatter.format(49770800); // "₩49,770,800"
rateFormatter.format(0.1234); // "12.3%"
```

퍼센트 서식은 `0.1234`를 `12.34%`로 해석하므로, API가 이미 `12.34`처럼 백분율 단위의 값을 보내는지,
비율인 `0.1234`를 보내는지 먼저 정해야 합니다. 날짜에는 같은 국제화 API 계열인 `Intl.DateTimeFormat`을 사용할 수 있습니다.

### Vite proxy로 같은 출처 요청

브라우저는 `http://localhost:5173`과 `http://localhost:8080`을 서로 다른 출처로 봅니다. 프로토콜, 호스트,
포트 중 하나라도 다르면 다른 출처이며, 브라우저는 이런 요청에 CORS 정책을 적용합니다.

Vite의 `server.proxy`는 개발 중 특정 경로의 요청을 API 서버로 대신 전달합니다. 아래 설정에서 브라우저는
`/api/items`만 요청하고, Vite가 이를 `http://api:8080/api/items`로 전달합니다. 브라우저가 보는 요청 대상은
여전히 Vite가 제공한 같은 출처이므로 API 서버에 개발용 CORS 설정을 추가하지 않아도 됩니다.

```ts
import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://api:8080',
        changeOrigin: true,
      },
    },
  },
});
```

`changeOrigin: true`는 전달하는 요청의 `Host` 헤더를 대상 서버 기준으로 바꿉니다. 가상 호스트나 Host 헤더 검사를 사용하는
서버와 연결할 때 필요할 수 있습니다. 프록시 규칙은 Vite의 개발 서버 설정이므로, 정적 파일을 배포할 때는 Nginx,
로드 밸런서, 백엔드 서버 같은 배포 환경의 프록시가 같은 역할을 맡아야 합니다.

### SQL 열 메타데이터

`database/sql`의 `rows.Columns()`는 열 이름만 반환합니다. `rows.ColumnTypes()`는 이름 외에 DB가 알려 준 타입,
길이, null 허용 여부 같은 열 메타데이터를 반환합니다. 다만 어떤 정보를 제공하는지는 드라이버에 따라 달라질 수 있으므로,
모든 DB에서 같은 세부 정보를 얻는다고 가정하면 안 됩니다.

```go
type Column struct {
	Name string
	Type string
}

func readColumns(rows *sql.Rows) ([]Column, error) {
	columnTypes, err := rows.ColumnTypes()
	if err != nil {
		return nil, err
	}

	columns := make([]Column, len(columnTypes))
	for index, columnType := range columnTypes {
		columns[index] = Column{
			Name: columnType.Name(),
			Type: columnType.DatabaseTypeName(),
		}
	}
	return columns, nil
}
```

`DatabaseTypeName()`이 돌려주는 `NUMERIC`, `VARCHAR`, `TIMESTAMPTZ` 같은 이름은 DB마다 다릅니다.
그래서 API가 이 이름을 그대로 화면에 넘기기보다, 애플리케이션이 필요한 `number`, `string`, `time` 같은 공통 분류로 변환하는
표현 계층을 두는 편이 좋습니다. 프론트엔드는 이 공통 분류로 정렬 방식, 기본 서식, 셀 정렬을 결정할 수 있습니다.

### 트랜잭션과 context

Go의 `sql.Tx`는 여러 DB 작업을 하나의 트랜잭션으로 묶고, 같은 연결에서 실행하게 합니다.
모든 단순 조회에 트랜잭션이 필요한 것은 아니지만, 여러 작업이 하나의 결과로 성공하거나 실패해야 할 때,
같은 연결에서 세션 설정을 유지해야 할 때, 읽기 전용 제약을 DB에도 전달하고 싶을 때 사용합니다.

```go
func listNames(parent context.Context, db *sql.DB) ([]string, error) {
	ctx, cancel := context.WithTimeout(parent, 3*time.Second)
	defer cancel()

	tx, err := db.BeginTx(ctx, &sql.TxOptions{ReadOnly: true})
	if err != nil {
		return nil, err
	}
	defer tx.Rollback()

	rows, err := tx.QueryContext(ctx, "SELECT name FROM items")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var names []string
	for rows.Next() {
		var name string
		if err := rows.Scan(&name); err != nil {
			return nil, err
		}
		names = append(names, name)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	if err := tx.Commit(); err != nil {
		return nil, err
	}
	return names, nil
}
```

`context.WithTimeout()`은 정해 둔 시간이 지나면 context를 취소합니다. `QueryContext()`처럼 context를 받는 DB 메서드는
클라이언트 연결이 끊기거나 시간이 초과됐을 때 작업을 취소할 기회를 얻습니다. DB가 제공하는 시간 제한과 함께 사용하면,
애플리케이션과 DB 양쪽에서 오래 걸리는 요청을 제어할 수 있습니다.

`defer tx.Rollback()`은 트랜잭션을 시작한 직후에 예약하는 관례입니다. 중간 단계에서 오류가 나도 함수가 끝날 때
Rollback이 실행되므로 정리를 빠뜨리지 않습니다. 모든 작업이 성공한 경우 `Commit()`이 먼저 트랜잭션을 끝내며,
그 뒤 예약된 Rollback 호출은 아무 작업도 하지 않습니다. 트랜잭션을 시작했다면 `db.QueryContext()`가 아니라
`tx.QueryContext()`처럼 `tx`의 메서드만 사용해야 같은 트랜잭션 안에서 작업이 이어집니다.

## 다음 작업

이번 글에서는 고정된 SQL을 실행해 하나의 Table 패널에 표시했습니다. 이제 대시보드는 데이터를 읽을 수 있지만,
패널 제목과 SQL, 순서가 코드에 고정되어 있어 사용자가 바꿀 수는 없습니다.

다음에는 Grafana의 편집 모드를 관찰한 뒤 대시보드 편집 화면을 구현할 계획입니다.
패널 제목과 SQL을 수정하고, 패널을 추가하거나 삭제하고, 순서를 바꾼 뒤
`PUT /api/v1/dashboards/:uid`로 저장합니다.

이 과정에서 지금은 프론트엔드 상수로 둔 `dailySalesQuery`를 대시보드 JSON으로 옮기고,
조회용 화면 상태와 편집 중인 화면 상태를 분리해 보겠습니다.
