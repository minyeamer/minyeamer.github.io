---
title: "[OpenPyXL] 파이썬으로 엑셀 다루기 - 셀 서식, 셀 병합, 필터"
date: "2026-02-20T02:09:30+09:00"
layout: "post"
description: >
  Python OpenPyXL로 엑셀 파일을 읽고 서식을 편집하는 과정을 자동화하는 실전 가이드입니다.
  셀 서식, 열 너비 자동 조정, 조건부 서식, BFS 알고리즘 기반 셀 병합, 필터 XML 조작까지
  실무에서 즉시 활용 가능한 Python 함수 구현 방법을 코드 예제와 함께 상세히 설명합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/2agm4ko7b6978hv8ptp76/openpyxl-00-cover.webp?rlkey=7kduplna4paxq0gl22tn5sx6p&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/wuax6ut9ea84j5t1vosjc/openpyxl-00-logo.webp?rlkey=ahg48xcyed7mhlgaxxl8iavqt&raw=1"
categories: ["Data Analysis", "Excel"]
tags: ["Python", "OpenPyXL", "엑셀 자동화", "데이터 처리", "셀 서식", "조건부 서식", "BFS 알고리즘", "셀 병합", "엑셀 필터", "엑셀 XML"]
series: ["OpenPyXL 엑셀 자동화"]
---
<style>
pre.mermaid { display: flex; justify-content: center; }
.inline-table { display: inline-table; border-collapse: collapse; border: 1px solid var(--body-font-color); }
.inline-cell { display: table-cell; border: 1px solid var(--body-font-color); padding: 4px 10px; }
</style>

{{< series "OpenPyXL 엑셀 자동화" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Python OpenPyXL 라이브러리를 활용한 엑셀 자동화 완벽 가이드입니다.
데이터를 수집하고 보고서로 가공해 제출하는 자동화 파이프라인에서 엑셀 스타일링을 어떻게 구현했는지
실무에서 검증된 함수 코드와 함께 단계별로 설명합니다.
OpenPyXL에서 제공하는 기능을 가져다 사용하는데 그치지 않고,
BFS 알고리즘 기반 자동 셀 병합, XML 직접 조작을 통한 필터 적용 등 고급 기법까지 다룹니다.

- **[왜 OpenPyXL인가](#왜-openpyxl을-사용해야-하는가)**: `pandas.to_excel()` 한계, 대안 라이브러리 비교, 실무 활용 사례 (데이터 수집 → 보고서 제출)
- **[셀 서식](#셀-서식)**: Alignment, Border, PatternFill, Font, 숫자 서식 5가지 요소와 `style_cell()` 함수 구현
- **[조건부 서식](#조건부-서식)**: CellIsRule, FormulaRule 활용, `conditional_rule()` 함수로 조건부 서식 규칙 생성
- **[셀 병합](#셀-병합)**: BFS 알고리즘으로 인접 셀 탐색 및 최적 직사각형 범위 계산, `find_merge_ranges()` 함수 구현
- **[필터](#필터)**: auto_filter 드롭다운 표시, ZIP/XML 직접 조작으로 실제 행 숨기기, `apply_filters()` 함수 구현

**커스텀 함수 구현**: `style_cell()`, `conditional_rule()`, `find_merge_ranges()`, `apply_filters()` 등
{{% /hint %}}

데이터를 수집하고 분석하는 업무를 하다 보면 파이썬으로 가공한 데이터를
동료에게 공유하는 경우가 빈번히 발생합니다.
이 때, CSV 또는 JSON과 같은 형식을 활용할 수도 있지만,
일반적인 사무직군과 소통하는 경우에는 엑셀 형식으로 데이터를 전달하는 편이 효과적입니다.

엑셀은 셀 서식, 조건부 서식, 필터, 셀 병합, 틀 고정 등 테이블형 데이터를 보는데
가독성을 높일 수 있는 다양한 기능을 제공합니다. 이러한 서식은 엑셀 프로그램에서
수동으로 지정할 수도 있지만, 반복적으로 같은 유형의 데이터를 주고받는 경우에는
매번 파이썬 환경과 엑셀 프로그램을 오고 가는게 불편할 수 있습니다.

이 글에서는 제가 실무에서 구현한 엑셀 파일을 다루는 함수들을 소개하고,
각 기능을 어떻게 구현했는지 코드 예제와 함께 설명하겠습니다.

## 왜 OpenPyXL을 사용해야 하는가?

`OpenPyXL` 은 파이썬에서 엑셀 파일을 다루는 대표적인 라이브러리입니다.

엑셀 파일의 대표적인 확장자인 `.xlsx` 파일은 시트 목록, 셀 값, 셀 서식 등을 서술한
XML 파일들을 ZIP 압축으로 묶은 것입니다.
OpenPyXL 라이브러리는 이러한 복잡한 구조의 엑셀 파일을 함수 호출과 같은 방식으로
쉽게 편집할 수 있도록 지원합니다.

{{< bookmark "https://openpyxl.readthedocs.io/en/stable/" >}}

### OpenPyXL 활용 사례

저는 실무에서 데이터를 수집하고 가공하여 슬랙 채널에 엑셀 파일로 업로드하는 파이프라인을 개발했습니다.

```mermaid
flowchart LR
    A[데이터 수집] --> B[데이터 가공]
    B --> C[엑셀 변환<br/>및 스타일링]
    C --> D[슬랙 업로드]

    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#f3e5f5
```

이 파이프라인은 엑셀 프로그램이 없는 리눅스 서버에서 실행되며,
데이터 수집부터 슬랙 업로드까지의 전체 과정에서 사람이 개입하지 않습니다.
그렇기에 엑셀 프로그램으로 아래 이미지와 같은 서식을 넣는 것 또한 파이썬 환경에서 수행해야 했습니다.

![노란색 헤더와 조건부 서식이 포함된 엑셀 테이블](https://dl.dropboxusercontent.com/scl/fi/bjjzgyyopfwf23bzmkfva/openpyxl-01-example.webp?rlkey=mxozzirku20ewf593ve88m0r4&raw=1)

이 때 활용한 라이브러리가 OpenPyXL입니다.

### pandas와 비교

파이썬으로 데이터 분석을 해보셨다면 `pandas` 라이브러리에 대해서 아실겁니다.

`pandas` 라이브러리는 파이썬에서 데이터를 `DataFrame` 이라는 객체로 변환하고,
이 객체를 대상으로 결측치 처리, 데이터 필터링, 병합, 그룹화 등의 데이터 조작을
간편하게 수행할 수 있게 지원합니다.

{{< bookmark "https://pandas.pydata.org/" >}}

`pandas` 에서도 `.to_excel()` 이라는, `DataFrame` 을 엑셀 파일로 변환하는
메서드를 제공합니다. 비록, `pandas` 가 직접적으로 엑셀 쓰기 작업을 수행하지 않고
`xlsxwriter` 또는 `openpyxl` 과 같은 외부 엔진에게 엑셀 생성을 위임하며,
이는 결국 OpenPyXL에 의존하는 방식이라고 볼 수 있지만, `.to_excel()` 이라는 단 한 줄의
호출로 엑셀 파일을 만드는 점은 OpenPyXL을 능가하는 편리함으로 비춰집니다.

{{< bookmark "https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html" >}}

하지만, 제가 `pandas` 라이브러리로 엑셀 파일을 만들지 않고 굳이 OpenPyXL을 사용하려는 이유가 있습니다.

`.to_excel()` 메서드는 항상 아래 이미지와 같은 엑셀 파일을 생성합니다.
헤더에 굵은 글씨 및 테두리 서식이 적용되고 그 외에는 어떠한 서식도 없습니다.
이미지는 제가 임의로 셀 값에 맞춰서 열 너비를 조정했지만,
실제론 열 너비도 모두 일정한 기본 너비를 가집니다.

![굵은 글씨의 헤더와 8개 행으로 구성된 엑셀 테이블](https://dl.dropboxusercontent.com/scl/fi/2zgqh5dvsoxoc2c2b64kn/pandas-to-excel.webp?rlkey=f0zmhl2a0tk3yqlnbw2lviyn9&raw=1)

데이터를 간단하게 엑셀 파일로 추출하는 경우에는 `pandas` 라이브러리를
OpenPyXL의 대안으로 여길 수 있지만,
보기 좋은 서식을 넣기 위해서는 OpenPyXL을 사용해야 합니다.

### OpenPyXL의 대안

`pandas` 외에도 OpenPyXL을 대신할 수 있는 다양한 파이썬 라이브러리들이 있습니다.

|라이브러리|장점|단점|
|---|---|---|
|**openpyxl**|서식, 차트 등 모든 기능 지원|대용량 파일 처리 느림|
|**xlsxwriter**|쓰기 전용, 속도 빠름|기존 파일 수정 불가|
|**pandas.to_excel()**|간단한 사용법|고급 스타일링 제한적|
|**xlwings**|Excel과 직접 통합|Windows/Mac Excel 설치 필요|

저는 서식 기능이 필수였고, 기존 파일을 수정하는 경우도 있어서 OpenPyXL을 선택했습니다.

## OpenPyXL 기본 개념

OpenPyXL을 본격적으로 활용하기 전에 알아야 할 개념이 있습니다.

### Workbook, Worksheet, Cell

OpenPyXL에서 `Workbook` 은 엑셀 파일의 모든 문서 정보를 담는 최상위 컨테이너입니다.
`Workbook` 객체를 생성한다는 것은 엑셀 파일 하나를 생성한다는 것을 의미합니다.
만약 기존 엑셀 파일을 `Workbook` 객체로 읽고 싶다면 `load_workbook()` 함수를 사용할 수 있습니다.

`Workbook` 객체에는 여러 개의 시트가 있을 수 있습니다.
엑셀 파일을 열자마자 보이는 첫 번째 시트에 접근하려면 `active` 속성을 호출하면 되고,
특정 시트에 접근하려면 시트명을 키로 접근하면 됩니다.
시트에 접근하면 `Worksheet` 객체를 반환합니다.

`Worksheet` 객체는 행(`rows`)과 열(`columns`)로 구성된 테이블 구조입니다.
시트에서 특정 셀에 접근하려면 `A1` 과 같은 참조 문자열을 키로 접근할 수 있습니다.
셀에 접근하면 `Cell` 객체를 반환하며, 셀의 속성 중 `value` 는 셀의 값을 가리킵니다.

```python
from openpyxl import Workbook

# Workbook: 엑셀 파일
wb = Workbook()

# Worksheet: 엑셀 시트 (Sheet1, Sheet2 등)
ws = wb.active  # (1) 현재 활성화된 시트
ws = wb["Sheet1"]  # (2) 또는 시트명
ws = wb.create_sheet("새 시트")  # (3) 새 시트 생성

# Cell: 개별 셀 (A1, B2 등)
cell = ws['A1']  # 셀 직접 접근
cell.value = "Hello"  # 값 설정
```

### OpenPyXL 기본 사용 예제

다음은 엑셀 파일을 생성하고 저장하는 간단한 예제입니다.

```python
from openpyxl import Workbook

# 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.title = "데이터"

# 데이터 추가
data = [
    ["이름", "나이", "직업"],   # 헤더
    ["홍길동", 30, "개발자"],   # 1행
    ["김철수", 25, "마케터"],   # 2행
    ["이영희", 28, "기획자"],   # 3행
]
for row in data:
    ws.append(row)

# 파일 저장
wb.save("sample.xlsx")
```

OpenPyXL 공식 문서의 [Tutorial](https://openpyxl.readthedocs.io/en/stable/tutorial.html)에서
더 자세한 기본 사용법을 확인할 수 있습니다.

## 엑셀 다루기 (OpenPyXL 활용)

본격적으로 OpenPyXL을 활용하여 엑셀 파일을 다뤄보겠습니다.

```python
from openpyxl import load_workbook, Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.cell.cell import Cell

wb: Workbook = load_workbook("data.xlsx")
ws: Worksheet = wb.active
cell: Cell = ws["A1"]
```

아래 CSV 형식의 샘플 데이터 `data.csv` 를 엑셀 파일 `data.xlsx` 로 변환한 후 불러와주시기 바랍니다.   
(C열과 D열이 텍스트가 아닌 숫자로 인식되도록 주의해주세요.)

### 샘플 데이터 제공

{{< data-table headers=2 file-name="data.csv" >}}
제품 정보,제품 정보,판매 현황,판매 현황,재고 관리
제품명,제품 설명,판매 수량,매출액 (원),재고 상태
노트북 A15,15.6인치 FHD 디스플레이 / Intel i7 프로세서 / 16GB RAM / 512GB SSD / Windows 11 탑재,1245,1493750000,정상
무선 마우스,2.4GHz 무선 연결 / 1600DPI 광학 센서 / 인체공학적 디자인 / 6개월 배터리 수명,3420,85500000,정상
기계식 키보드,청축 스위치 / RGB 백라이트 / USB-C 케이블 / 알루미늄 프레임 / N-Key 롤오버,2156,258720000,부족
27인치 모니터,QHD 2560x1440 해상도 / IPS 패널 / 75Hz 주사율 / HDR10 지원 / 높이 조절 스탠드,892,312200000,정상
USB-C 허브,7-in-1 멀티포트 / HDMI 4K 출력 / 100W PD 충전 / USB 3.0 x3 / SD 카드 리더,4567,136557000,정상
노이즈캔슬링 헤드셋,액티브 노이즈 캔슬링 / Bluetooth 5.0 / 30시간 재생 / 폴더블 디자인 / 마이크 내장,1789,214680000,부족
외장 SSD 1TB,USB 3.2 Gen2 / 읽기 1050MB/s / 쓰기 1000MB/s / 충격 방지 / 5년 보증,2341,444990000,품절
웹캠 FHD,1080p 30fps / 자동 밝기 조정 / 듀얼 마이크 / 110도 광각 / USB 플러그앤플레이,3128,93840000,정상
{{< /data-table >}}

## 셀 서식

OpenPyXL의 셀 서식은 다음 5가지 요소로 구성됩니다.

```python
from openpyxl.styles import Alignment, Border, PatternFill, Font, Side

# 1. 정렬 (https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.alignment.html)
cell.alignment = Alignment(
    horizontal = "center",      # 왼쪽(left), 가운데(center), 오른쪽(right) 등
    vertical = "center",        # 상단(top), 중앙(center), 하단(bottom) 등
    wrap_text = True,           # 자동 줄바꿈 허용
)

# 2. 테두리 (https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.borders.html)
cell.border = Border(
    left = Side(style="thin"),  # 상하좌우 외에 대각선(diagonal) 등 테두리 지원
    right = Side(style="thin"), # Side: 점선(dotted), 이중선(double) 등 테두리 옵션
    top = Side(style="thin"),
    bottom = Side(style="thin"),
)

# 3. 채우기 (https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fills.html)
cell.fill = PatternFill(
    start_color = "FFFF00",     # RGB 색상 코드 (노란색)
    end_color = "00FFFF00",     # 또는 알파 값을 추가한 aRGB 색상 코드 (노란색)
    fill_type = "solid",
)

# 4. 폰트 (https://openpyxl.readthedocs.io/en/stable/api/openpyxl.styles.fonts.html)
cell.font = Font(
    name = "Arial",
    size = 11,
    bold = True,
    color = "000000",           # RGB 색상 코드 (검은색)
)

# 5. 숫자 서식
cell.number_format = "#,##0"    # 천 단위 구분
cell.number_format = "0.00%"    # 백분율
cell.number_format = "yy-mm-dd" # 날짜
```

OpenPyXL 공식 문서 [Working with styles](https://openpyxl.readthedocs.io/en/stable/styles.html)에서
더 많은 스타일 옵션을 확인할 수 있습니다.

### 5가지 셀 서식 적용

위 5가지 셀 서식 옵션을 받아서 일괄로 적용하는 `style_cell()` 함수를
다음과 같이 정의해볼 수 있습니다.

```python
from openpyxl.styles import Alignment, Border, Side, PatternFill, Font

def style_cell(
        cell: Cell,
        alignment: dict | None = None,      # 정렬
        border: dict | None = None,         # 테두리
        fill: dict | None = None,           # 채우기
        font: dict | None = None,           # 폰트
        number_format: str | None = None,   # 숫자 서식
    ):
    if alignment:
        cell.alignment = Alignment(**alignment)
    if border:
        cell.border = create_border(**border)   # 주의) 테두리 옵션은 Side 객체로 전달해야 함
    if fill:
        cell.fill = PatternFill(**fill)
    if font:
        cell.font = Font(**font)
    if number_format:
        cell.number_format = number_format

def create_border(**kwargs: dict) -> Border:
    return Border(**{side: Side(**options) for side, options in kwargs.items()})
```

만약 헤더 행에 가운데 정렬, 바깥 테두리, 노란색 배경, 볼드체를 적용한다면
`style_cell()` 함수를 이렇게 응용할 수 있습니다.

```python
header_style = {
    "alignment": {"horizontal": "center", "vertical": "center"},                        # 가운데 정렬
    "border": {side: {"style": "thin"} for side in ["left", "right", "top", "bottom"]},    # 바깥 테두리
    "fill": {"start_color": "FFFF00", "end_color": "FFFF00", "fill_type": "solid"},     # 노란색 배경
    "font": {"bold": True, "color": "000000"},                                          # 볼드체
}

# 헤더(1행, 2행)에 서식 적용합니다.
for header_row in [1, 2]:
    for cell in ws[header_row]:
        style_cell(cell, **header_style)

# 추가로, 숫자 열에 1,000 단위 구분 서식을 추가합니다.
for numeric_column in ['C', 'D']:
    for cell in ws[numeric_column]:
        style_cell(cell, number_format = "#,##0")
```

샘플 데이터에 대해 위 스타일을 적용하면 다음과 같은 결과를 확인할 수 있습니다.   
(숫자 서식이 적용되지 않는다면, 값이 텍스트가 아니고 숫자로 불러온게 맞는지 확인해주시기 바랍니다.)

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/58cl2jwo8t5y3s5rdx0zf/openpyxl-02-cell-styles.webp?rlkey=j9h05wygohmvinpefl0hxtg2z&raw=1"
  alt="샘플 데이터 - 셀 서식 적용 (노란색 헤더)"
  max-width="384px"
  align="center" >}}

## 열 너비, 행 높이 지정

너비 또는 높이는 각각 열 또는 행 단위로 지정할 수 있습니다.

OpenPyXL에서 너비 또는 높이를 지정하려면
[`dimensions` 모듈](https://openpyxl.readthedocs.io/en/stable/api/openpyxl.worksheet.dimensions.html)을
사용합니다.

```python
ws.column_dimensions['A'].width = 8.43  # A열 너비 지정
ws.row_dimensions[1].height = 15.0      # 1행 높이 지정
```

### 열 너비, 행 높이 자동 조절

OpenPyXL은 너비 또는 높이를 지정하지 않으면 공통적으로 기본값이 적용됩니다.
하지만, 기본 너비로 저장한 엑셀 파일을 열어볼 때는 항상 셀 값에 맞춰서 수동으로
너비를 조절해야 하는 불편함이 있습니다.
이 문제를 해결하기 위해 셀 값에 맞춰서 자동으로 너비를 확장 또는 축소하는 기능을 만들어보겠습니다.

아이디어는 간단합니다. 하나의 열을 구성하는 모든 셀의 값에 대한 길이를 계산하고 그 최댓값을 구하는 것입니다.

셀의 값에 대한 길이를 구하는 방법은 따로 제공되지 않지만, 다음 공식을 이용하면 비슷하게 유추할 수 있습니다.

```python
def get_cell_width(value: str) -> float:
    try:
        # 한글: 1.8배, 공백: 1.2배, 영문/숫자: 1배
        return sum(1.8 if ord(c) > 12799 else 1.2 if c.isspace() else 1. for c in value)
    except:
        return 0.
```

열의 모든 셀을 순회하면서 `get_cell_width()` 함수를 사용하면 맞춤 열 너비를 구할 수 있습니다.

```python
column = 'A'
max_width = 8.43    # 최소 너비 (초깃값)

for cell in ws[column]:
    if cell.value:
        max_width = max(max_width, get_cell_width(str(cell.value)))

ws.column_dimensions[column].width = min(max_width + 2., 25.)   # 좌우 1씩 여백, 최대 너비 25 제한
```

샘플 데이터의 모든 열에 맞춤 열 너비를 적용해보았습니다.

최대 너비 25로 제한하여 B열은 완전히 펼쳐지지 않았지만,
기존에 값이 잘려서 표시되던 나머지 열들은 모두 완전히 펼쳐졌습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/mxv1q6skyjfjj3kps9mce/openpyxl-03-column-width.webp?rlkey=ie5bvflg4zyk8t6t6yfesc6cy&raw=1"
  alt="샘플 데이터 - 자동 너비 적용"
  max-width="619px"
  align="center" >}}

## 조건부 서식

조건부 서식(Conditional Formatting)은 셀 값에 따라 자동으로 스타일을 변경하는 기능입니다.   
(예를 들어 숫자 값으로 구성된 범위에 대해 특정 값 이상이면 빨간색, 이하면 파란색으로 표시할 수 있습니다.)

OpenPyXL에서 조건부 서식은 시트(Worksheet) 단위로 적용하며,
조건부 서식을 적용할 범위 문자열을 `Rule` 객체와 함께 전달합니다.

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

# 범위 내 값이 1000 이상이면 빨간 배경색 서식을 표시하는 조건부 서식
rule_gte = CellIsRule(
    operator = "greaterThanOrEqual",
    formula = ["1000"],
    stopIfTrue = False,
    fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid"),
)
ws.conditional_formatting.add("C3:C10", rule_gte)
```

`Rule` 객체의 유형은 OpenPyXL 공식 문서
[Conditional Formatting](https://openpyxl.readthedocs.io/en/stable/formatting.html)에서
예제와 함께 확인할 수 있습니다.

저는 이상(≥), 이하(≤)와 같은 단순 연산자에 기반한 규칙 `CellIsRule`, 그리고
`ISBLANK` 와 같은 수식에 기반한 규칙 `FormulaRule` 을 주로 사용합니다.
이 외에 `ColorScale`, `DataBar` 등의 규칙도 사용할 수 있습니다.

### 규칙 생성 및 적용

`Rule` 객체를 간편하게 생성하기 위해 `conditional_rule()` 이라는 함수를 정의했습니다.

```python
from openpyxl.formatting.rule import Rule, CellIsRule, FormulaRule
from typing import Literal, Sequence

def conditional_rule(
        operator: Literal[
            "endsWith", "containsText", "beginsWith", "lessThan", "notBetween", "lessThanOrEqual",
            "notEqual", "notContains", "between", "equal", "greaterThanOrEqual", "greaterThan", "formula"],
        formula: Sequence | None = None,    # 수식 또는 피연산자
        stop_if_true: bool | None = None,   # 우선순위 규칙
        border: dict | None = None,         # 스타일 - 테두리
        fill: dict | None = None,           # 스타일 - 채우기
        font: dict | None = None,           # 스타일 - 폰트
    ) -> Rule:
    if operator == "formula":
        return formula_rule(formula, stop_if_true, border, fill, font)

    styles = dict()
    if border:
        styles["border"] = create_border(**border)
    if fill:
        styles["fill"] = PatternFill(**fill)
    if font:
        styles["font"] = Font(**font)
    return CellIsRule(operator=operator, formula=formula, stopIfTrue=stop_if_true, **styles)
```

단순 연산자에 기반한 규칙 `CellIsRule` 은 연산자 `operator` 와 피연산자 `formula` 를 매개변수로 받습니다.
이 연산 조건을 만족했을 때 3가지 서식(테두리, 채우기, 폰트)을 지원합니다.

`operator` 에 `formula` 값은 `CellIsRule` 규칙에서 지원하는 건 아니고,
제가 임의로 수식 규칙 `FormulaRule` 을 구분하기 위해 추가한 것입니다.
`FormulaRule` 은 별도의 연산자 없이 수식 `formula` 를 매개변수로 받습니다.
이것을 `formula_rule()` 함수로 정의했습니다.

```python
def formula_rule(
        formula: Sequence | None = None,    # 수식
        stop_if_true: bool | None = None,   # 우선순위 규칙
        border: dict | None = None,         # 스타일 - 테두리
        fill: dict | None = None,           # 스타일 - 채우기
        font: dict | None = None,           # 스타일 - 폰트
    ) -> Rule:
    styles = dict()
    if border:
        styles["border"] = create_border(**border)
    if fill:
        styles["fill"] = PatternFill(**fill)
    if font:
        styles["font"] = Font(**font)
    return FormulaRule(formula=formula, stopIfTrue=stop_if_true, **styles)
```

샘플 데이터에도 조건부 서식을 적용해보았습니다.

```python
# 값이 3,000 이상인 경우의 조건부 서식
rule_gte = dict(
    operator = "greaterThanOrEqual",
    formula = ["3000"],
    stop_if_true = True,
    fill = dict(start_color="FE968D", end_color="FE968D", fill_type="solid"),
)

# 값이 1,000 이하인 경우의 조건부 서식
rule_lte = dict(
    operator = "lessThanOrEqual",
    formula = ["1000"],
    stop_if_true = True,
    fill = dict(start_color="41B0F6", end_color="41B0F6", fill_type="solid"),
)

ws.conditional_formatting.add("C3:C10", conditional_rule(**rule_gte))
ws.conditional_formatting.add("C3:C10", conditional_rule(**rule_lte))
```

C열에 대해
값이 3,000 이상인 경우 <span style="background: #fe968d; color: #000;">빨간 배경색</span> 서식으로,
값이 1,000 이하인 경우 <span style="background: #41b0f6; color: #000;">파란 배경색</span> 서식으로
보이게끔 두 가지 조건부 서식을 추가했습니다.
(만약 조건부 서식이 의도대로 적용되지 않는다면, 값이 텍스트가 아니고 숫자로 불러온게 맞는지 확인해주시기 바랍니다.)

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/pv4l8084moxulkqjvqsdw/openpyxl-04-conditional-formatting.webp?rlkey=4460c7qwcsujnf304o8therfn&raw=1"
  alt="샘플 데이터 - 조건부 서식 (3000 이상 빨간색 배경, 1000 이하 파란색 배경)"
  max-width="619px"
  align="center" >}}

## 셀 병합

동일한 값을 가지는 범위를 하나로 병합하면 가독성을 높일 수 있습니다.

OpenPyXL에서는 조건부 서식과 마찬가지로 시트(Worksheet) 단위로 병합을 수행할 수 있습니다.
병합 범위는 참조 문자열 또는 행/열 번호를 지정할 수 있습니다.
병합된 셀에 서식을 적용하고 싶다면 범위 내 첫 번째(좌상단) 셀 하나에 서식을 부여하면 됩니다.

```python
ws.merge_cells("A1:B1")  # A1부터 B1까지 병합
ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=2)  # 또는 행/열 번호로 지정
```

### 셀 병합 대상 탐색 (자동 셀 병합)

저의 [OpenPyXL 활용 사례](#openpyxl-활용-사례)처럼 데이터를 가공하는 과정에서
사람이 개입하지 않는 경우, 어떤 범위를 병합했을 때 가독성을 높일 수 있을지 알 수 없습니다.
이렇게 데이터의 내용을 모르는 상태에서, 모든 셀을 순회하면서 셀 병합할 만한 대상을 찾는 기능을 만들어보겠습니다.

셀 병합할 만한 대상은 다음 2가지 경우로 정의합니다.

1. 동일한 값을 가지는 범위 (예를 들어, A1:A3 범위:
   <span class="inline-table">
   <span class="inline-cell">홍길동</span>
   <span class="inline-cell">홍길동</span>
   <span class="inline-cell">홍길동</span>
   </span>)

2. 첫 번째 값만 있고 나머지는 값이 없는 범위 (예를 들어, A1:A3 범위:
   <span class="inline-table">
   <span class="inline-cell">홍길동</span>
   <span class="inline-cell">　　　</span>
   <span class="inline-cell">　　　</span>
   </span>)

막상 구현하려니 경우의 수가 많아서 막막했지만,
인접한 셀의 값을 탐색한다고 생각하니까 BFS 알고리즘을 떠올릴 수 있었습니다.
BFS는 그래프의 특정 시작 지점부터 인접한 노드를 차례로 방문하면서 그래프 내 모든 연결된 요소를 찾는 알고리즘입니다.
해당 기능에서는 동일한 값이 연속되거나 빈 값으로 채워진 범위를 "연결된 요소"로 볼 수 있습니다.

BFS 알고리즘을 기반으로 구현한 함수 `find_merge_ranges()` 의 내용을 3개 부분으로 나눠서 설명드리겠습니다.

```python
from collections import deque
from openpyxl.utils import range_boundaries

range_string: str = "A1:E10"
mode: Literal["blank", "same_value"] = "same_value"

# --- [0] --- 함수의 첫 번째 부분: 2차원 배열 초기화
min_col, min_row, max_col, max_row = range_boundaries(range_string)
num_rows, num_cols = (max_row - min_row + 1), (max_col - min_col + 1)

rows = [list(row) for row in ws.iter_rows(min_row, max_row, min_col, max_col, values_only=True)]
visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]
```

먼저, 임의의 A1:E10 범위를 2차원 배열 `rows` 로 정의합니다.   
그리고, `rows` 와 동일한 크기로 셀 방문 여부를 체크할 `visited` 배열도 생성합니다.

범위 문자열로부터 범위의 크기를 계산하는 것은 OpenPyXL에서 지원하는 유틸리티 함수 `range_boundaries()` 을 활용했습니다.
이 함수에 범위 문자열을 전달하면 워크시트 상에서 대상 범위가 위치한 4군데 모서리 좌표를 반환합니다.

`rows` 와 `visited` 를 활용하는 `_bfs()` 함수는 다음과 같이 정의할 수 있습니다.

```python
# --- [1] --- 함수의 두 번째 부분: BFS 구현
def _bfs(row_seq: int, col_seq: int) -> list[tuple[int,int]]:
    queue, cells = deque(), [(row_seq, col_seq)]
    queue.append((row_seq, col_seq))
    visited[row_seq][col_seq] = True
    value = rows[row_seq][col_seq]

    while queue:
        r, c = queue.popleft()
        for nr, nc in [(r, c+1), (r+1, c)]: # [(오른쪽), (아래쪽)]
            if (0 <= nr < num_rows) and (0 <= nc < num_cols) and (not visited[nr][nc]):
                if (rows[nr][nc] == value) if mode == "same_value" else (rows[nr][nc] is None):
                    visited[nr][nc] = True
                    queue.append((nr, nc))
                    cells.append((nr, nc))
    return cells
```

시작 지점인 셀의 행과 열 번호를 입력으로 전달하면 워크시트 상의 좌표 지점부터
오른쪽, 그리고 아래쪽 방향으로 이동하면서 인접한 셀에 동일한 값이 있는지(`mode = "same_value"`),
또는 빈 값이 있는지(`mode = "blank"`)를 파악합니다.

만약 워크시트 범위를 넘어가거나 한번 방문한 셀에 도달하면 반복문이 종료됩니다.
그리고, 최종적으로 시작 지점을 포함해 조건에 부합하는 인접한 셀의 좌표들을 배열로 반환합니다.

이 `_bfs()` 함수를 모든 방문하지 않은 셀에서 호출합니다.

```python
from openpyxl.utils import get_column_letter as colstr

merge_ranges: list = list()
priority: Literal["width", "height"] = "width"

# --- [2] --- 함수의 세 번째 부분: 병합 범위 선택
for row_seq in range(num_rows):
    for col_seq in range(num_cols):
        if (not visited[row_seq][col_seq]) and (rows[row_seq][col_seq] is not None):
            cells = _bfs(row_seq, col_seq)
            if len(cells) < 2:
                continue

            # 최적의 직사각형 범위 구하기
            best_corners = get_largest_rectangle(cells, top_left=cells[0], priority=priority)
            (row_start, col_start) = best_corners[0][0] # 좌상단 모서리 좌표
            (row_end, col_end) = best_corners[1][1] # 우하단 모서리 좌표

            for r, c in cells:
                # 직사각형 범위에 선택되지 않은 셀은 방문 기록 제거
                if not ((row_start <= r <= row_end) and (col_start <= c <= col_end)):
                    visited[r][c] = False

            if (row_start != row_end) or (col_start != col_end):
                # 범위 문자열로 치환하여 병합 대상 범위에 추가
                merge_ranges.append(f"{colstr(col_start+min_col)}{row_start+min_row}:{colstr(col_end+min_col)}{row_end+min_row}")
            else:
                # 직사각형 범위가 1x1 크기일 경우 인접한 셀에 대한 방문 기록 제거
                for r, c in cells[1:]:
                    visited[r][c] = False
```

조건에 부합하는 인접한 셀의 좌표를 알아냈지만, 이를 가지고 병합할 범위를 도출하려면 별도로 고려할 사항이 있습니다.
만약 동일한 크기를 가지는 서로 다른 직사각형 범위가 있다면 어떤 범위를 우선할지 여부입니다.

<div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
  <div>
    <div style="margin-bottom: 0.5rem; text-align: center; font-weight: bold;">원본 (A)</div>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
    </span>
  </div>

  <div style="font-size: 1.5rem; font-weight: bold;">→</div>

  <div>
    <div style="margin-bottom: 0.5rem; text-align: center; font-weight: bold;">세로 우선 (B)</div>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
    </span>
  </div>

  <div style="font-size: 1.5rem; font-weight: bold;">or</div>

  <div>
    <div style="margin-bottom: 0.5rem; text-align: center; font-weight: bold;">가로 우선 (C)</div>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
      <span class="inline-cell">O</span>
    </span><br/>
    <span class="inline-table">
      <span class="inline-cell" style="color: var(--body-background)">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
      <span class="inline-cell" style="color: var(--body-background)">O</span>
    </span>
  </div>
</div>

탐색 범위가 3x3 크기라 가정하고 (2, 2) 좌표의 셀을 제외한 나머지 모든 값이 동일하다면
조건에 부합하는 인접한 셀의 좌표들은 `원본(A)` 에서 `O` 로 표시된 부분이라고 볼 수 있습니다.

셀 병합은 직사각형 범위만 가능하므로 이 경우에는 6개 셀로 구성된 직사각형 범위가 최적이지만,
문제는 동일한 크기의 직사각형 범위가 2종류나 발생합니다.
이런 상황에서 가로를 우선할지, 세로를 우선할지 결정하는 매개변수 `priority` 를 입력으로 받아,
직사각형 범위의 모서리 좌표를 반환하는 `get_largest_rectangle()` 함수를
다음과 같이 정의할 수 있습니다.

```python
from typing import TypeVar

Node = TypeVar("Node", bound=tuple[int, int])
TopLeft = TypeVar("TopLeft", bound=Node)
TopRight = TypeVar("TopRight", bound=Node)
BottomLeft = TypeVar("BottomLeft", bound=Node)
BottomRight = TypeVar("BottomRight", bound=Node)

def get_largest_rectangle(
        nodes: list[Node],
        top_left: Node,
        priority: Literal["width","height"] = "width",
    ) -> tuple[tuple[TopLeft, TopRight], tuple[BottomLeft, BottomRight]]:
    node_set = set(nodes)
    y0, x0 = top_left

    best_score = (0, 0)
    best_corners = (
        ((top_left, top_left), (top_left, top_left)),
        ((top_left, top_left), (top_left, top_left)),
    )

    max_width = 0
    while (y0, x0 + max_width) in node_set:
        max_width += 1

    min_height = float("inf")
    for width in range(1, max_width + 1):
        height = 0
        while (y0 + height, x0 + width - 1) in node_set:
            height += 1

        min_height = min(min_height, height)
        area = width * min_height
        score = (area, min_height if priority == "height" else width)

        if score > best_score:
            best_score = score
            y_max, x_max = (y0 + int(min_height) - 1), (x0 + width - 1)
            best_corners = (
                ((y0, x0), (y0, x_max)),
                ((y_max, x0), (y_max, x_max))
            )

    return best_corners
```

최종적으로 셀 병합 대상을 자동으로 탐색하는 함수 `find_merge_ranges()` 를 구현했습니다.

`mode` 에는 `all` 옵션을 하나 더 추가해서 주어진 범위를 그대로 전체 병합하도록 했습니다.

{{< tabs "find-merge-ranges" >}}

{{% tab "요약" %}}
```python
Range = TypeVar("Range", bound=str)

def find_merge_ranges(
        ws: Worksheet,
        range_string: Range,
        mode: Literal["all", "blank", "same_value"] = "all",
        priority: Literal["width", "height"] = "width",
    ) -> list[Range]:
    if mode == "all":
        return [range_string]
    merge_ranges = list()

    # --- [0] --- 함수의 첫 번째 부분: 2차원 배열 초기화

    # --- [1] --- 함수의 두 번째 부분: BFS 구현

    # --- [2] --- 함수의 세 번째 부분: 병합 범위 선택

    return merge_ranges
```
{{% /tab %}}

{{% tab "전체" %}}
```python
from collections import deque
from openpyxl.utils import range_boundaries
from openpyxl.utils import get_column_letter as colstr
from typing import TypeVar

Range = TypeVar("Range", bound=str)

def find_merge_ranges(
        ws: Worksheet,
        range_string: Range,
        mode: Literal["all", "blank", "same_value"] = "all",
        priority: Literal["width", "height"] = "width",
    ) -> list[Range]:
    if mode == "all":
        return [range_string]
    merge_ranges = list()

    min_col, min_row, max_col, max_row = range_boundaries(range_string)
    num_rows, num_cols = (max_row - min_row + 1), (max_col - min_col + 1)

    rows = [list(row) for row in ws.iter_rows(min_row, max_row, min_col, max_col, values_only=True)]
    visited = [[False for _ in range(num_cols)] for _ in range(num_rows)]

    def _bfs(row_seq: int, col_seq: int) -> list[tuple[int,int]]:
        queue, cells = deque(), [(row_seq, col_seq)]
        queue.append((row_seq, col_seq))
        visited[row_seq][col_seq] = True
        value = rows[row_seq][col_seq]

        while queue:
            r, c = queue.popleft()
            for nr, nc in [(r, c+1), (r+1, c)]:
                if (0 <= nr < num_rows) and (0 <= nc < num_cols) and (not visited[nr][nc]):
                    if (rows[nr][nc] == value) if mode == "same_value" else (rows[nr][nc] is None):
                        visited[nr][nc] = True
                        queue.append((nr, nc))
                        cells.append((nr, nc))
        return cells

    for row_seq in range(num_rows):
        for col_seq in range(num_cols):
            if (not visited[row_seq][col_seq]) and (rows[row_seq][col_seq] is not None):
                cells = _bfs(row_seq, col_seq)
                if len(cells) < 2:
                    continue

                best_corners = get_largest_rectangle(cells, top_left=cells[0], priority=priority)
                (row_start, col_start) = best_corners[0][0]
                (row_end, col_end) = best_corners[1][1]

                for r, c in cells:
                    if not ((row_start <= r <= row_end) and (col_start <= c <= col_end)):
                        visited[r][c] = False

                if (row_start != row_end) or (col_start != col_end):
                    merge_ranges.append(f"{colstr(col_start+min_col)}{row_start+min_row}:{colstr(col_end+min_col)}{row_end+min_row}")
                else:
                    for r, c in cells[1:]:
                        visited[r][c] = False
    return merge_ranges
```
{{% /tab %}}

{{< /tabs >}}

샘플 데이터에 `find_merge_ranges()` 함수를 사용해봅시다.

<span class="inline-table">
    <span class="inline-cell">제품 정보</span>
    <span class="inline-cell">제품 정보</span>
    <span class="inline-cell">판매 현황</span>
    <span class="inline-cell">판매 현황</span>
    <span class="inline-cell">재고 관리</span>
</span>

일부러 샘플 데이터의 1행은 병합이 가능하도록 구성했습니다.

```python
>>> find_merge_ranges(ws, range_string = "A1:E1", mode = "same_value")
["A1:B1", "C1:D1"]
```

함수를 실행하면 의도대로 동일한 "제품 정보" 값을 가지는 A1:B1 범위와,
동일한 "판매 현황" 값을 가지는 C1:D1 범위가 탐색되었습니다.

```python
for range_string in find_merge_ranges(ws, range_string = "A1:E1", mode = "same_value"):
    ws.merge_cells(range_string)
```

이렇게 탐색된 범위를 그대로 워크시트의 `.merge_cells()` 메서드에 넣어서 샘플 데이터의 헤더를 병합했습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/wnoyvve0ro1zrmyqnh7by/openpyxl-05-merge-cells.webp?rlkey=17mtmw6iabm3z4q5y38l8afue&raw=1"
  alt="샘플 데이터 - 셀 병합 (A1:B1, C1:D1)"
  max-width="619px"
  align="center" >}}

## 필터

엑셀에서 필터는 방대한 데이터를 탐색하는데 필요한 핵심 기능입니다.

OpenPyXL에서는 아쉽게도 필터를 "표시만" 할 수 있습니다.

```python
from openpyxl.utils import get_column_letter

ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
```

워크시트에서 `auto_filter` 속성의 `ref` 범위 값을 작성하면 엑셀 프로그램에서
필터 아이콘을 클릭한 것과 같은 동작을 하여 헤더 행에 드롭다운이 표시됩니다.

### 필터 항목

드롭다운에서 선택될 항목을 결정하는건 `filters` 모듈을 활용할 수 있습니다.

```python
from openpyxl.worksheet.filters import FilterColumn, Filters, DateGroupItem
from openpyxl.worksheet.filters import Top10, DynamicFilter, BlankFilter, ColorFilter, IconFilter
from openpyxl.worksheet.filters import CustomFilters, CustomFilter

filter_column = FilterColumn(colId = 0)

# 1. 값 필터
filter_column.filters = Filters(
    blank = True,                   # 빈 값 허용
    calendarType = "gregorian",     # 달력 유형 (양력 등)
    filter = ["값1", "값2"],         # 필터할 값
    dateGroupItem = [DateGroupItem(year=2026, month=2, day=20)],    # 필터할 날짜
)

# 2. 상위/하위 필터
filter_column.top10 = Top10(
    top = True,         # True면 상위, False면 하위
    percent = True,     # True면 백분율(%), False면 항목 수
    val = 10.0,         # 항목 수 또는 백분율(%) <-- 필수
    filterVal = 50.0,   # 실제 기준값 <-- 선택
)

# 3. 평균/날짜 필터
filter_column.dynamicFilter = DynamicFilter(
    # "평균 이상", "오늘", "이번 달" 등 평균/날짜 관련 필터 타입 지원
    type: Literal["aboveAverage", "today", "thisMonth", ...] = "null",
    val: Float = None,          # 기준값 (숫자)
    valIso: DateTime = None,    # 기준값 (날짜)
    maxVal: Float = None,       # 최대 기준값 (숫자)
    maxValIso: DateTime = None, # 최대 기준값 (날짜)
)

# 4. 연산자 필터
filter_column.customFilters = CustomFilters(
    # 여러 개 연산 조건 허용
    customFilter = [
        CustomFilter(
            # "같음", "초과", "미만" 등 연산자 필터 타입 지원
            operator: Literal["equal", "lessThan", "greaterThan", ...] = "equal"
            val: String = "",   # 기준값 (텍스트)
        ),
        ...
    ]
)

# 5. 공백 필터, 색상 필터, 아이콘 필터 (설명 생략)
filter_column.filters = Filters(blank=True, filter=[BlankFilter()])
filter_column.colorFilter = ColorFilter(...)
filter_column.iconFilter = IconFilter(...)

# 0. 필터 항목 적용 (항목만 선택, 실제 적용 X)
ws.auto_filter.filterColumn = filter_column
```

OpenPyXL 공식 문서 [Using filters and sorts](https://openpyxl.readthedocs.io/en/stable/filters.html)에서
사용가능한 필터 항목과 예제를 확인할 수 있습니다.

### 필터 적용 (실제 데이터 숨기기)

OpenPyXL에서 제공하는 `auto_filter` 의 문제점은 필터 드롭다운에서 항목을 선택하는 것까지는
지원하지만, 선택된 항목을 숨기는 것은 지원하지 않습니다.
실제로 행을 숨기고 싶다면 엑셀 프로그램에서 드롭다운을 열고 수동으로 확인(Apply) 버튼을 눌러야 합니다.

대안으로 이렇게 행을 직접 숨길 수 있습니다.
하지만, 이것은 행을 전체 지정해서 "숨기기"하는 동작이기 때문에,
필터를 해제한다고 숨겨진 행이 자동으로 펼쳐지지 않습니다.

```python
ws.row_dimensions[1].hidden = True
```

엑셀에서 실제로 필터를 적용한 것과 같은 동작은 어떻게 구현할 수 있을까요?
아쉽게도 OpenPyXL에서는 방법이 없고 엑셀 파일을 구성하는 XML 문서를 직접 수정해야 합니다.

실제로 필터 대상 행을 숨기는 기능을 하는 함수 `apply_filters()` 를 이렇게 구현할 수 있습니다.

```python
import xml.etree.ElementTree as ET
import tempfile
import os

Sheet = TypeVar("Sheet", bound=int)
Row = TypeVar("Row", bound=int)

def apply_filters(wb: Workbook, filtered_rows: dict[Sheet, set[Row]]) -> Workbook:
    for index, rows in filtered_rows.items():
        ws = wb.worksheets[index-1]
        if not (ws.auto_filter and ws.auto_filter.filterColumn):
            continue

        ns = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        ET.register_namespace('', ns["main"])

        # Workbook 객체를 직접 다룰 수 없으므로 임시 파일로 저장
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
            input_path = tmp_file.name
            wb.save(input_path)

        try:
            # 실제로 행을 숨기는 동작은 이어서 설명
            wb = _apply_filter(input_path, index, rows, ns)
        finally:
            os.remove(input_path)

    return wb
```

`apply_filters()` 함수를 사용하기 위해선 필터 대상 행을 정리한 `filtered_rows` 딕셔너리가 있어야 합니다.
`filtered_rows` 딕셔너리는 1부터 시작하는 시트 인덱스 번호 `Sheet` 를 키로,
필터 대상 행 번호의 집합 `set[Row]` 을 값으로 가집니다.

`Workbook` 객체를 임시 파일로 쓰고, 해당 임시 파일에서 XML 문서를 읽어서 필터 대상 행을 숨길 것입니다.
그러한 동작을 다음 `_apply_filter()` 함수에서 처리합니다.

```python
def _apply_filter(input_path: str, sheet_index: Sheet, filtered_rows: set[Row], ns: dict) -> Workbook:
    from openpyxl import load_workbook
    from tempfile import NamedTemporaryFile
    import xml.etree.ElementTree as ET
    import zipfile
    import os

    with zipfile.ZipFile(input_path, 'r') as zip_in:
        sheet_xml = f"xl/worksheets/sheet{sheet_index}.xml"
        with zip_in.open(sheet_xml) as zip_file:
            tree = ET.parse(zip_file)
            root = tree.getroot()

        sheet_data = root.find(".//main:sheetData", ns)
        if sheet_data is not None:
            for row in sheet_data.findall(".//main:row", ns):
                row_idx = int(row.get('r', 0))
                if row_idx in filtered_rows:
                    row.set("hidden", '1')      # 필터 대상 행 숨기기
                elif row.get("hidden"):
                    del row.attrib["hidden"]    # 필터 대상이 아닌 행 펼치기

        # 또 다른 임시 파일 생성
        with NamedTemporaryFile(delete=False, suffix=".xlsx") as file:
            output_path = file.name

        try:
            # 필터 적용된 임시 파일을 저장하고,
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for zip_info in zip_in.infolist():
                    if zip_info.filename == sheet_xml:
                        xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
                        zip_out.writestr(zip_info, xml_bytes)
                    else:
                        zip_out.writestr(zip_info, zip_in.read(zip_info.filename))
            # 임시 파일을 `load_workbook()` 함수로 다시 `Workbook` 객체로 불러오기
            return load_workbook(output_path)
        finally:
            os.remove(output_path)
```

샘플 데이터에는 필터를 적용하진 않고 필터 드롭다운을 표시하는 것만 해보겠습니다.

```python
ws.auto_filter.ref = "A2:E10"
```

2행을 헤더로 하여 필터를 추가하면 각 헤더 열마다
필터 항목을 선택할 수 있는 드롭다운 버튼이 표시됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/88cp0xdd3axld9uhagjx8/openpyxl-06-auto-filter.webp?rlkey=uh34lvjudbr7fibed9h21b7uh&raw=1"
  alt="샘플 데이터 - 필터 드롭다운 표시"
  max-width="619px"
  align="center" >}}

## 기타 기능

그 외에 자주 사용하는 엑셀 기능들을 안내드립니다.

### 하이퍼링크

셀에 하이퍼링크를 추가하고 싶다면 `Cell` 객체의
`hyperlink` 속성에 URL 문자열을 작성하면 됩니다.

```python
cell.hyperlink = url
```

셀의 값을 인식해서 URL 값을 가지는 셀에 자동으로 하이퍼링크를 추가할 수도 있습니다.

```python
for col_idx, column in enumerate(ws.columns, start=1):
    for row_idx, cell in enumerate(column, start=1):
        if hyperlink and text.startswith("https://"):
            cell.hyperlink = text
            cell.font = Font(color="0000FF", underline="single")
```

하이퍼링크를 추가한다고 링크
서식(<span style="background: #fff; color: #0000FF; text-decoration: underline;">파란색 글씨 및 밑줄</span>)이
자동으로 적용되는게 아니기 때문에 서식도 같이 적용해줍시다.

### 틀 고정

스크롤 시 헤더를 항상 유지하는 기능으로 적용해두면 데이터를 탐색할 때 편합니다.

```python
# 첫 행 고정 (A2부터 스크롤)
ws.freeze_panes = "A2"

# 첫 열도 함께 고정 (B2부터 스크롤)
ws.freeze_panes = "B2"

# 여러 행/열 고정 (C3부터 스크롤 = 2행 2열 고정)
ws.freeze_panes = "C3"
```

### 줌 배율

시트의 확대/축소 비율도 설정할 수 있습니다.

```python
ws.sheet_view.zoomScale = 85    # 85% 크기로 표시
```

## 마치며

제가 실무에서 OpenPyXL로 엑셀 데이터를 보기 좋게 꾸미기 위해 알아본
내용을 한번 정리해보았습니다.

이제 엑셀 파일을 다룰 때 주로 사용하는 셀 서식, 열 너비 지정, 조건부 서식, 셀 병합, 필터 등의
기능을 엑셀 프로그램을 거치지 않고 파이썬에서 처리하실 수 있을겁니다.

저는 매일 수집한 데이터를 엑셀 파일 형식으로 가공해 사내 구성원들에게 보고서로 공유하는데,
현업에서 이러한 반복적인 업무를 수행하고 있다면 OpenPyXL을 자동화 프로세스에 접목해보시기 바랍니다.

이번 글에서는 OpenPyXL의 각 기능들에 대해 알아봤는데,
다음 글에서는 이러한 기능들을 엮어서, CSV 또는 JSON 형태의 파이썬 데이터를
엑셀 파일로 변환하는 하나의 통합된 함수를 구현해보고자 합니다.
