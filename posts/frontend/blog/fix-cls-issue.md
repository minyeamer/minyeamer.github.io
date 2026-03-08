---
title: "구글 CLS 이슈 해결기 - Hugo 블로그 레이아웃 이동 97% 줄이기"
date: "2026-03-08T22:23:58+09:00"
layout: "post"
description: >
  어느 날 Google Search Console에서 CLS 이슈 경고가 들어왔는데, 알고 보니 새 테마를 적용한 날부터 시작된 문제였습니다.
  원인은 <img> 태그에 width, height 속성이 없는 단순한 이유였지만, 드롭박스 공유 링크를 사용하다 보니
  Hugo 빌드 중 자동으로 크기를 명시하는 방법이 필요했습니다.
  Lighthouse로 단계별 CLS를 측정하며 0.067에서 0.002까지 97% 개선했고, 보름 후 Search Console 경고도 해제되었습니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/q0wel6c9420c4c2a31ia6/fix-cls-00-desktop.webp?rlkey=4bsjs5whpbswtp2trukmz3o1k&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/ri8i00p8ccygvthzqzorp/fix-cls-00-score.webp?rlkey=dancwfkbl6ako6k2f5vue2ft2&raw=1"
categories: ["Frontend", "Blog"]
tags: ["CLS", "CLS 이슈", "구글 CLS 이슈", "Cumulative Layout Shift", "Core Web Vitals", "Hugo", "Hugo 블로그", "Lighthouse", "Google Search Console", "서택스 테마"]
series: ["Hugo 테마 만들기"]
---

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Google Search Console에서 특정 날짜부터 CLS 이슈 경고가 발생한다면, 그날 배포한 변경사항이 원인일 가능성이 높습니다.
서택스 테마를 새로 적용한 직후부터 경고가 시작되었고,
분석해보니 이미지 태그에 `width` 와 `height` 속성이 없어서 레이아웃이 이동하는 것이 주범이었습니다.
Lighthouse로 단계별로 확인하며 CLS를 0.067에서 0.002까지 줄였고,
약 보름 후 Google Search Console에서도 경고가 해제되었습니다.

- **[CLS 발생 원인 분석](#cls-발생-원인-분석)**: 이미지에 `width`, `height` 속성이 없는게 핵심 원인이고, 그 외 동적 렌더링 요소들의 영향도 분석
- **[이미지 크기 추가하기](#이미지-크기-추가하기)**: 드롭박스 공유 링크는 유지하면서 Hugo 빌드 시 `width`, `height` 속성을 자동 삽입하는 방식
- **[Reading Time 개선](#reading-time-cls-개선)**: JavaScript 동적 삽입 대신 Hugo 서버사이드 추정값으로 공간을 미리 확보하는 방법
- **[Font Awesome CDN 내재화](#font-awesome-cdn-내재화)**: Font Awesome CDN 링크를 IcoMoon 서브셋 폰트로 대체해 LCP, FCP 수치 개선
- **[Lighthouse 측정 결과](#lighthouse-측정-결과)**: 개선 단계별 CLS 수치 비교와 Google Search Console 반영 타임라인
{{% /hint %}}

블로그를 구글 검색 엔진에 등록한 후, [Google Search Console](https://search.google.com/search-console)을 매일마다 확인하다가
어느 날부터 [Core Web Vitals](https://developers.google.com/search/docs/appearance/core-web-vitals?hl=ko)
지표에 대한 Severity가 <span style="background-color: #0F9D58; color: #fff;">Good</span>으로
표시되던 URL들이 <span style="background-color: #F4B400; color: #000;">Need improvement</span>로
바뀌는 순간을 보았습니다. 그 이후로 지속적으로 경고 상태가 지속되어 조치가 필요하다 느꼈는데,
마침 경고로 변경된 순간인 26년 1월 26일이 서택스(SeoTax) 테마를 처음 적용한 날짜라서 원인은 명확했습니다.

![Google Search Console > Core Web Vitals > Desktop](https://dl.dropboxusercontent.com/scl/fi/c7y7t7w62gfle1waswbct/fix-cls-01-desktop-dates.webp?rlkey=g71l892s9j3969cao14o54wrs&raw=1)

문제가 되는 대상은 특정했지만 왜 문제가 되는지도 알아야 했습니다. 그것은 바로 밑에서 설명하고 있습니다.
CLS라는 지표가 (아마도 데스크탑에서) 0.1보다 크다는 것입니다. 지금은 해결해서 0건으로 보이지만,
당시에는 14개 정도의 URL들이 전부 CLS issue로 집계되었습니다.

![CLS issue: more than 0.1 (desktop)](https://dl.dropboxusercontent.com/scl/fi/0l04ciabjk1g6f9kcfnm3/fix-cls-02-why.webp?rlkey=ur4h6sa6mk89npubuvlpx2ap0&raw=1)

처음엔 경고를 해결해야겠다 생각하면서도 한창 서택스 테마를 개발하던 시기라서
열흘 정도 미뤄왔습니다. 테마가 어느 정도 안정화된 후 Google Search Console에서
CLS issue가 무엇인지 찾아보니까 SEO 점수에 영향을 줄 수 있는 지표라는 것을 알게 되었습니다.
그래서 당장 서택스 테마에 무슨 문제가 있는지 분석하게 되었습니다.

덕분에 CLS라는 지표를 제대로 공부하게 되었고,
Hugo 블로그의 구조적인 문제를 발견하고 고치는 좋은 기회가 되었습니다.
최종적으로 CLS 지표를 **0**에 가깝게 줄이는 데 성공했고, 그 과정을 이 글에서 공유합니다.

## CLS (Cumulative Layout Shift)

**CLS(누적 레이아웃 이동)** 란 페이지 로딩 중에 예상치 못하게 콘텐츠가 이동하는 현상을 수치로 나타낸 지표입니다.
예를 들어 글을 읽다가 이미지가 뒤늦게 로드되면서 텍스트가 아래로 밀리는 경험을 해본 적이 있을 것입니다.
바로 그런 상황이 CLS를 발생시킵니다.

Google Core Web Vitals의 세 가지 핵심 지표 중 하나로,
사용자가 느끼는 시각적 안정성을 정량화합니다.

{{% hint %}}
- **Good**: 0 ~ 0.1
- **Needs Improvement**: 0.1 ~ 0.25
- **Poor**: 0.25 이상
{{% /hint %}}

CLS가 중요한 이유는 단순히 눈에 거슬리는 문제가 아니라
**검색 랭킹에도 영향을 미치는 신호**이기 때문입니다.
Google은 Core Web Vitals를 SEO 순위 요소로 활용하며,
CLS가 나쁜 페이지는 상대적으로 불이익을 받을 수 있습니다.

## CLS 발생 원인 분석

Google Search Console에서 경고를 받은 이후, CLS가 왜 발생하는지를 먼저 파악해야 했습니다.
서택스 테마의 코드베이스 전체를 AI에게 분석 요청했고 아래 네 가지가 주요 원인을 보고받았습니다.

### 이미지 크기 미지정

가장 큰 원인은 `<img>` 태그에 `width`, `height` 속성이 없는 것이었습니다.

```html
<!-- 문제가 되는 코드 -->
<img src="https://dl.dropboxusercontent.com/scl/fi/.../cover.webp" 
     class="content-cover">
<!-- width, height 없음 → 이미지 로드 시 레이아웃 이동 발생 -->
```

브라우저는 이미지를 다운로드하기 전까지 그 크기를 알 수 없습니다.
그래서 이미지 자릿수를 아무것도 없는 것으로 처리하다가,
다운로드가 완료되는 순간 실제 크기만큼 공간이 확보되면서 주변 레이아웃이 통째로 밀려나게 됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/8ej6e7zusz4vbqatkqs0v/fix-cls-03-cover-shift.webp?rlkey=hx32zwyk80y7zqr1korhu0uv5&raw=1"
  alt="Lighthouse 필름스트립"
  caption="(모바일) Lighthouse 필름스트립 - 웹 페이지 로딩 과정 시각화" >}}

커버 이미지처럼 화면 상단에 위치한 이미지일수록 CLS에 미치는 영향이 큽니다.
위 캡쳐 이미지를 보면 웹 페이지 로딩 중 이미지가 중간에 불러와지면서 하위 모든 요소들이
이미지 높이만큼 아래로 밀려나는 것을 확인할 수 있습니다.
저는 모든 글에 높이가 제각각인 커버 이미지를 배치했기 때문에 블로그 전반에 걸쳐 영향을 받고 있었습니다.

이러한 문제가 발생한 것은 제가 이미지를 드롭박스(Dropbox)에 올리고
**외부 URL을 가지고 이미지를 표시하고 있었기 때문**입니다.
Hugo는 `resources.Get` API를 사용하여 로컬 이미지 파일의 크기를 자동으로 읽어낼 수 있지만,
외부 URL에서 가져온 이미지에는 이 방법을 사용할 수 없습니다.

### Reading Time 동적 계산

서택스 테마는 JavaScript로 글을 읽는데 걸리는 시간을 계산하여 화면에 표시합니다.
페이지 로드 직후에는 해당 자리가 비어있다가 스크립트가 실행되고 나서야 텍스트가 삽입되는데,
이 텍스트 삽입이 미세한 레이아웃 이동을 유발합니다.

```javascript
document.getElementById('reading-time').innerText = calculateReadingTime();
```

단순히 작은 라벨 영역 하나지만,
모든 글의 최상단에 공통적으로 위치해서 CLS에 어느정도 영향이 있을 것이라 생각했습니다.

### 아이콘 폰트 로딩

블로그 전반에 표시되는 아이콘은 로컬 이미지가 아니라
[Font Awesome](https://fontawesome.com/)이라는 외부 서비스에서 제공하는
CDN 링크를 이용하고 있었습니다. Font Awesome 아이콘 폰트가 로드되기 전까지
폴백(Fallback) 폰트가 사용되다가 폰트 전환 시점에 레이아웃이 미세하게 밀릴 수 있는데,
CDN 링크를 사용하면 사용자의 네트워크 속도에 따라 폰트 로딩이 느려질 수 있습니다.

`font-display` 설정에 따라 폰트가 로드되기 전 텍스트가 잠깐 보이지 않거나
폰트 교체 시점에 자간이나 행간 차이로 레이아웃이 조금씩 움직일 수도 있는데,
저는 `font-display` 설정에도 문제가 있었습니다.

### i18n 텍스트 동적 렌더링

서택스 테마는 시스템 언어를 감지하여 클라이언트에서 다국어 텍스트를 렌더링합니다.
`aria-label` 같은 접근성 속성은 화면에 직접 보이지 않아 CLS 영향이 거의 없지만,
보이는 텍스트의 일부도 동적으로 교체되는 경우 미세한 이동이 생길 수 있습니다.

i18n의 경우에는 텍스트가 동적으로 바뀌는 불편함보다 외국어 독자들이
메뉴를 더 직관적으로 인식하도록 유도하는 것이 더 중요하다고 판단했고,
이미 이전 원인들을 개선하면서 CLS 문제는 해결되어 해당 기능은 유지했습니다.

## Lighthouse - 초기 CLS 측정

각각의 원인을 해결해도 Google Search Console에서 CLS 지표가 실제로 개선되었는지
확인하려면 배포 후 하루 이상이 소요될 수 있습니다. 하지만, 문제되는 요소가 실제로
해결되지 않았다면 또다시 배포하고 다음 측정 결과가 나올 때까지 반복해서 기다려야 합니다.

[Lighthouse](https://developer.chrome.com/docs/lighthouse/overview)는
웹페이지 품질을 개선하는 데 도움이 되는 오픈소스 자동화 도구입니다.
화면의 안정성을 나타내는 CLS와 함께, 가장 큰 컨텐츠가 나타나는데 걸리는 시간인
LCP (Largest Contentful Paint)를 포함한 5가지 지표를 측정 및 분석해줍니다.

블로그를 배포하기 전에 CLS가 어느정도 수치까지 개선되었는지 확인할 수 있는 최적의
도구로 사용할 수 있습니다.

![Lighthouse - Analyze page load](https://dl.dropboxusercontent.com/scl/fi/15exov2x5a1gtrd1yb8nf/fix-cls-04-lighthouse.webp?rlkey=0lh4i70e2k071iitcx11693xb&raw=1)

Lighthouse로 CLS를 측정하는 방법은 간단합니다. 대상 웹페이지가 활성화된 크롬 브라우저에서
개발자 도구(DevTools)를 열고 `Lighthouse` 탭을 클릭하면 됩니다.
모바일, 데스크탑 등 분석 옵션을 선택하고 "Analyze page load" 버튼을 클릭하면
몇 초 후에 다음과 같은 분석 결과를 확인할 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/qxfgr44cn3uxtx90kj1xr/fix-cls-05-lighthouse-first-gauge.webp?rlkey=cv969jf92u80lcguwtncyioau&raw=1"
  alt="Lighthouse 초기 분석 결과" >}}

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/h9x4l6guvcvmet0fo5l2r/fix-cls-06-lighthouse-first-metrics.webp?rlkey=ku875b48cqk2b6eiothgza58o&raw=1"
  alt="Lighthouse 초기 분석 결과"
  caption="(모바일) Lighthouse 분석 결과 - 5가지 지표" >}}

분석 결과만 봐선 CLS는 정상이고, 컨텐츠 로딩과 관련된 LCP 지표가 문제되는 것으로 보입니다.
관련해서 검색해보니 Lighthouse는 실험실 환경과 같은 시뮬레이션으로 CLS를 측정하지만,
구글 검색 엔진은 실제 사용자 데이터를 기반으로 평균적인 CLS를 측정한다는 것을 확인했습니다.

저는 로컬에 빌드된 정적 페이지에 `localhost` 로 접속한 후 실험실 환경에서 측정하여 `0.067` 이라는
수치를 얻었지만, Github Pages로 배포된 블로그에 접속한 어떤 사용자에게는 더 높은 수치로
기록될 수 있습니다. 모든 사용자들에게 적은 영향을 주기 위해선
CLS 수치를 최대한 `0` 에 가깝게 줄일 필요가 있다고 느꼈습니다.

## 이미지 크기 추가하기

CLS 이슈의 핵심 원인인 이미지 크기 미지정 문제를 어떻게 해결할지 방법을 검토했습니다.

### 해결 방안 검토

#### 방안 1: CSS aspect-ratio

```css
.content-cover {
  aspect-ratio: 1200 / 350;
  width: 100%;
}
```

CSS 한 줄로 간단하게 적용할 수 있지만,
커버 이미지는 각각 다른 비율을 가지고 있기 때문에 하나씩 대응이 어렵고,
모든 이미지를 같은 비율로 맞춰버리면 이미지가 왜곡되는 문제도 있습니다.
이 방안은 채택하지 않았습니다.

#### 방안 2: Hugo `resources.Get` 으로 자동 감지

```go-html
{{ $image := resources.Get .Params.cover }}
{{ if $image }}
  <img src="{{ .Params.cover }}" 
       width="{{ $image.Width }}" height="{{ $image.Height }}">
{{ end }}
```

Hugo가 자동으로 이미지 크기를 계산해주는 정석적인 방법이지만,
`resources.Get` 으로 이미지를 읽어오는 건 프로젝트 내 로컬 파일에만 접근할 수 있습니다.
드롭박스 공유 링크가 전달되면 이미지 크기를 얻을 수 없어서 그대로 사용하기 어려웠습니다.

드롭박스 이미지 호스팅을 사용하지 않고 다시 로컬 파일로 돌아가는 방법도 있겠지만,
Github 저장소에 모든 이미지를 업로드했을 때 장기적으로 저장소 용량을 감당할 수 없을 것 같아서
다른 방안을 탐색했습니다.

#### 방안 3: 하이브리드 방식 (채택)

드롭박스 이미지 호스팅은 유지하면서, Hugo 빌드 시 이미지 크기를 자동으로 감지하는 방법을 고민했습니다.
결론은 **동일한 이미지 파일을 로컬에도 보관하여 빌드 시에만 크기를 읽는 것**입니다.

{{% hint %}}
1. Dropbox 공유 링크는 그대로 사용
2. 동일 파일을 `assets/_images/` 폴더에 보관
3. Hugo 빌드 시 로컬 파일에서 `width`, `height` 값만 추출
4. 추출한 크기를 `<img>` 태그의 속성으로 추가
{{% /hint %}}

로컬 이미지 파일은 Hugo가 빌드 결과물(`public/`)에 복사하지 않으므로
실제 블로그에는 배포되지 않고 크기 정보만 활용할 수 있습니다.
(`.gitignore` 에도 해당 경로를 추가하여 Github 저장소에도 업로드되지 않습니다.)

### 이미지 파일 구조 설계

로컬 이미지 파일은 `themes/seotax/assets/` 아래 `_images/` 폴더에 보관합니다.
`_images/` 하위 경로는 마크다운 컨텐츠가 있는 `content/posts/` 경로 구조와 동일하게 유지하여
페이지 경로에서 자동으로 이미지 경로를 유추할 수 있도록 설계했습니다.

```bash
themes/seotax/assets/
└── _images/
    └── frontend/
        └── blog/
            ├── hugo-00-cover.webp
            ├── hugo-01-screenshot.webp
            └── seotax-40-codeblock-wide.webp
```

그리고 Dropbox URL에서 로컬 이미지 파일 경로를 추출하는 매핑 로직은 다음과 같이 동작합니다.

```bash
Dropbox URL:
https://dl.dropboxusercontent.com/.../${hugo-00-cover.webp}?rlkey=...&raw=1
                                        ↓ 파일명 추출 (쿼리스트링 제거)
페이지 경로:
/blog/posts/${frontend/blog}/hugo-blog-1/
                                        ↓ _images/ 경로로 변환 및 파일명 조합
매핑 결과:
assets/_images/${frontend/blog}/${hugo-00-cover.webp}
```

### 이미지 크기 계산하기

이미지 크기를 계산하는 로직을 여러 템플릿에서 공통으로 사용할 수 있도록
`img-size.html` 부분 템플릿으로 분리하여 구현했습니다.

부분 템플릿은 `partial "content/img-size" (dict "Page" .Page "Url" $src)`
과 같은 방식으로 호출하여 사용할 수 있으며, 계산된 이미지 크기가 `1920x1080`
형태의 해상도 문자열로 반환됩니다.

부분 템플릿에서 이미지 파일 경로를 추출하고 `width`, `height` 값을 읽어오는 과정은
다음의 코드로 구현할 수 있습니다.

```go-html
<!-- 마크다운 컨텐츠 경로로부터 이미지 폴더 경로 추출 -->
{{- $pageDir := cond $page.File $page.File.Dir "" -}}
{{- $relPath := strings.TrimPrefix (default site.Params.posts.section "posts/") $pageDir -}}
{{- $rootPath := default site.Params.imageDir "_images" -}}
{{- $imagePath := printf "%s/%s" $rootPath $relPath -}}

<!-- 드롭박스 공유 링크로부터 이미지 파일명 추출 -->
{{- /* Get filename from image URL */ -}}
{{- $urlParts := split (index (split $imageUrl "?") 0) "/" -}}
{{- $fileName := index $urlParts (sub (len $urlParts) 1) -}}
{{- /* Try 1: Exact filename match */ -}}
{{- $fullPattern := printf "%s%s" $imagePath $fileName -}}

<!-- 조합된 경로에 해당하는 이미지 파일이 있으면 읽기 -->
{{- with resources.Get $fullPattern -}}
  {{- $width = .Width -}}
  {{- $height = .Height -}}
<!-- 일치하는 이미지 파일이 없을 경우 확장자를 무시하고 찾기 -->
{{- else -}}
  {{- $baseName := index (split $fileName ".") 0 -}}
  {{- $namePattern := printf "%s%s.*" $imagePath $baseName -}}
  {{- with resources.GetMatch $namePattern -}}
    {{- $width = .Width -}}
    {{- $height = .Height -}}
  {{- end -}}
{{- end -}}
```

저는 로컬의 PNG 이미지 원본과 드롭박스에 올리는 WEBP 이미지의 확장자가 달라서
확장자를 무시하고 검색하는 과정을 추가로 넣었습니다.

이미지를 찾고 `width`, `height` 값을 알아냈다면
두 값을 `1920x1080` 형태의 해상도 문자열로 변환하여 반환합니다.

추가로, 저는 드롭박스에 이미지를 업로드할 때 이미지의 최대 크기를 제한하여
일정 크기를 넘어가는 이미지는 동일 비율로 축소합니다.
따라서, Hugo 설정에 `maxImageSize` 라는 파라미터를 넣어서 원본 이미지 크기를
동일 비율로 축소하는 계산 과정도 넣었습니다.

```go-html
{{- if and $width $height -}}
  {{- $maxSize := default 0 site.Params.maxImageSize -}}
  {{- $maxDim := cond (gt $width $height) $width $height -}}
  {{- if and $maxSize (gt $maxDim $maxSize) -}}
    {{- $width = div (mul $width $maxSize) $maxDim -}}
    {{- $height = div (mul $height $maxSize) $maxDim -}}
  {{- end -}}
  {{- $resolution = printf "%dx%d" $width $height -}}
{{- end -}}
{{- return $resolution -}}
```

이미지 크기를 계산하는 부분 템플릿 `img-size.html` 의 전체 내용은
[Github 링크](https://github.com/minyeamer/hugo-seotax/blob/main/layouts/_partials/content/img-size.html)를
참고해주시기 바랍니다.

### 이미지 크기 계산 결과 적용

이제 이 부분 템플릿을 커버 이미지, 마크다운 이미지, Shortcode 이미지 등에 각각 적용합니다.

대표적으로 커버 이미지에서는 다음과 같은 방식으로 부분 템플릿을 활용합니다.

```go-html
{{ if .Params.cover }}
<div class="content-cover-wrap">
  {{- $resolution := partial "content/img-size" (dict "Page" . "Url" .Params.cover) -}}
  {{- $attrs := "" -}}
  {{- if $resolution -}}
    {{- $dims := split $resolution "x" -}}
    {{- $width := index $dims 0 -}}
    {{- $height := index $dims 1 -}}
    {{- $attrs = printf `width="%spx" height="%spx"` $width $height -}}
  {{- end -}}
  <img src="{{ .Params.cover | absURL }}" class="content-cover" alt="Cover Image" {{ $attrs | safeHTMLAttr }} decoding="async">
</div>
{{ end }}
```

로컬 이미지 파일이 있고 부분 템플릿이 해상도 문자열을 반환했다면
`x` 구분자를 기준으로 `width` 와 `height` 를 나눠서 `<img>` 태그의 속성으로 부여합니다.
적용 결과, 빌드된 HTML에서 커버 이미지가 다음과 같이 변경되었습니다.

```html
<!-- Before -->
<img src="https://dl.dropboxusercontent.com/.../cover.webp" class="content-cover"
      alt="Cover Image" decoding="async">

<!-- After -->
<img src="https://dl.dropboxusercontent.com/.../cover.webp" class="content-cover"
      alt="Cover Image" width="1200px" height="350px" decoding="async">
```

브라우저가 이제 이미지를 다운로드하기 전에도 `1200px x 350px` 크기의 공간을 미리 확보합니다.
이미지가 나중에 로드되어도 레이아웃이 이동하지 않습니다.

### Lighthouse - 개선된 CLS 측정

이미지 크기를 속성으로 추가한 후 Lighthouse 도구를 사용해 다시 한 번 CLS 지표를 측정했습니다.

![Lighthouse METRICS - CLS 0.003](https://dl.dropboxusercontent.com/scl/fi/91je59w36nl2iixbhrw7q/fix-cls-07-lighthouse-second-metrics.webp?rlkey=8kp2uz15tm5ef0vriya7i3piz&raw=1)

0.067이었던 CLS 수치가 0.003으로 크게 개선된 것을 확인할 수 있었습니다.
추가로, METRICS 영역 하단에 웹 페이지 로딩 과정을 시각화한 필름스트립을 보면
커버 이미지가 있어야 하는 공간을 미리 확보하고 있는 것을 확인할 수 있습니다.
[이미지 크기 미지정](#이미지-크기-미지정) 문단에서 커버 이미지가 로딩되면서 하위 컨텐츠가
전부 아래로 밀리는 것과 비교했을 때 안정적이게 바뀌었습니다.

## Reading Time CLS 개선

이전 이미지 작업 후 Lighthouse로 CLS를 측정해보니 **0.003**까지 떨어졌습니다.
이미지 적용만으로 0에 가까운 수치에 도달했지만, CLS 지표를 더 줄일 수 있는 부분이 있습니다.

마크다운 본문의 헤더에 공통적으로 있는 `읽는데 n분` 텍스트가
JavaScript로 동적 삽입되어 미세한 레이아웃 이동을 유발하고 있었습니다.

```html
<!-- 페이지 로드 직후: 빈 자리 -->
<span id="reading-time"></span>

<!-- reading-time.js 실행 후: 텍스트 삽입 → 레이아웃 이동 -->
<span id="reading-time"> • 읽는데 5분</span>
```

서택스 테마에서 글을 읽는데 걸리는 시간을 계산하는 `reading-time.js` 는
다국어별 WPM/CPM, 코드블록 수, 이미지 연속성 등을 꼼꼼히 고려하는 정밀한 로직이라
Hugo 문법만으로 완벽히 재현하기 어렵습니다.
그래서 Hugo에서 구현 가능한 로직으로 계산한 추정값으로 미리 공간을 확보하고,
스크립트 실행 후 정밀한 값으로 교체하는 **하이브리드 방식**을 택했습니다.

```go-html
<span id="reading-time">
  {{- $textMinutes := div $.WordCount 200 -}}
  {{- $numBlocks := div (len (findRE "```" $.RawContent)) 2 -}}
  {{- $codeMinutes := div $numBlocks 2 -}}
  {{- $numImages := len (findRE "!\\[.*?\\]\\(.*?\\)" $.RawContent) -}}
  {{- $imageMinutes := div $numImages 6 -}}
  {{- $totalMinutes := add $textMinutes (add $codeMinutes $imageMinutes) -}}
  {{- if lt $totalMinutes 1 -}}{{ $totalMinutes = 1 }}{{- end -}}
  {{ replace (i18n "reading.time.min" | default "%m min read") "%m" $totalMinutes }}
</span>
```

기존에는 `#reading-time` 영역이 비어있었지만, 이제부터는 정적 페이지에
읽는데 걸리는 시간이 소스코드 내에 추가됩니다. 독자가 블로그 글에 접속할 때
JavaScript로 인해 해당 영역의 숫자 값이 변경될 수는 있지만,
기존 대비 레이아웃의 이동이 많아야 한 글자 정도밖에 발생하지 않을 것입니다.

Lighthouse로 어느 정도 변화가 있는지 확인해보았습니다.

![Lighthouse METRICS - CLS 0.002](https://dl.dropboxusercontent.com/scl/fi/tjos805vlmrd81ujmp4zn/fix-cls-08-lighthouse-third-metrics.webp?rlkey=d2gkxma0tdh5ld7qh4j1i3e08&raw=1)

이 작업 후 **0.003 → 0.002**로 한 단계 더 개선되었습니다.

## Font Awesome CDN 내재화

CLS 작업을 하면서 Lighthouse 리포트를 자세히 들여다보니
Font Awesome CDN을 통해 800KB 이상의 폰트 파일을 불러오고 있었습니다.
실제로 사용하는 아이콘은 **26개**뿐인데도 전체 라이브러리를 로드하고 있었던 것입니다.

CLS에 직접적인 영향을 주는 부분은 아니었지만,
초기 페이지 로드 속도와 관련된 LCP, FCP 지표에 영향을 줄 수 있어 함께 개선하기로 했습니다.

### IcoMoon 서브셋 폰트 생성

[IcoMoon](https://icomoon.io/)은 아이콘 폰트 또는 SVG 아이콘을 직접 내려받아서
사용하는데 도움을 주는 사이트입니다.

![IcoMoon](https://dl.dropboxusercontent.com/scl/fi/1n48ejxje2fqqzxnii57f/fix-cls-09-icomoon.webp?rlkey=8rncst0pzauso1bh0sanjhz6i&raw=1)

IcoMoon에서 자체적으로 제공하는 아이콘도 있지만,
Font Awesome 또는 Material Icons 등 기존 서비스에서 제공하는 아이콘도 가져와
무료로 내려받을 수 있습니다.
Font Awesome에서 지정된 아이콘의 이름을 그대로 검색하면
비슷한 아이콘을 찾을 순 있지만, 아쉽게도 모든 아이콘을 가지고 있진 않았습니다.

IcoMoon에서 사용 중인 Font Awesome 아이콘과 유사한
26개 아이콘만 선택해 서브셋 폰트를 생성했습니다.
(폰트 생성 시 사이트 하단에서 좌측에 "Generate SVG & More" 링크와
우측에 "Generate Font" 링크가 있는데, 우측의 링크를 선택해야 아이콘 폰트로 생성됩니다.)

생성된 서브셋 폰트를 Font Awesome CDN과 비교하면 확실히 가벼워졌다는 것을 확인할 수 있습니다.

| 구분 | Font Awesome CDN | IcoMoon 서브셋 |
|------|-----------------|----------------|
| 용량 | 800KB+ | 약 40KB |
| 아이콘 수 | 수천 개 | 26개 |
| CDN 의존성 | 있음 | 없음 |

### IcoMoon 서브셋 폰트 적용

IcoMoon 서브셋 폰트는 ZIP 파일로 내려받아집니다.
압축 파일은 다음과 같은 폴더 구조로 되어 있습니다.

```bash
icomoon/
├── demo-files/
│   ├── demo.css
│   └── demo.js
├── fonts/
│   ├── icomoon.eot
│   ├── icomoon.svg
│   ├── icomoon.ttf
│   └── icomoon.woff
├── Read Me.txt
├── demo.html
├── selection.json
└── style.css
```

압축 파일 내 모든 파일을 가져다 쓰진 않고, `fonts/` 경로 내 폰트 파일들과
`style.css` 의 내용만 가져갈 것입니다.

우선, `fonts/` 경로의 파일들은 서택스 테마의 `static/` 경로 하위에
폴더 째로 이동시킵니다. Hugo에서 `static/` 경로는 아무런 처리 없이
루트 경로로 복사되는 파일들을 놓는 곳입니다.
여기에 `fonts/` 폴더를 복사해 놓는다면 Hugo 빌드 후에
`public/fonts/` 경로에 폰트 파일들이 위치하게 됩니다.

그리고, `style.css` 를 `assets/` 경로 아래에 이동시킵니다.
파일명을 그대로 사용해도 문제는 없지만 구분하기 어려우니 저는
`icon.css` 명칭으로 변경했습니다.

해당 CSS 파일을 import하면 서브셋 폰트가 테마에 적용됩니다.
하지만, CSS 파일에서 한 가지 변경해야 할 게 있는데,
`font-display: block;` 라인을 `font-display: swap;` 로
변경하는 것입니다.

`font-display` 속성의 `block` 값은 아이콘 폰트가 로딩될 때까지
아이콘 영역을 숨기지만, `swap` 값은 폴백 폰트를 대신 표시합니다.
저는 폴백 폰트를 따로 설정하지 않아서 아이콘 폰트가 로딩될 때까지는
네모 안에 X가 들어간 형태의 아이콘으로 보여질 것입니다.

```scss
@font-face {
  ...
  font-display: swap;
}
```

이후 레이아웃 파일 전체에서 Font Awesome의 `fa-*` 클래스를
IcoMoon으로부터 내려받은 커스텀 아이콘에 할당한 클래스인 `icon-*` 으로
일괄 변경하여 교체를 마쳤습니다.

## Lighthouse 측정 결과

IcoMoon 서브셋 폰트 적용 직후엔 따로 Lighthouse 측정을 하지 않았습니다.
그 이후에 사소한 변경사항이 있었지만, 지금 다시 측정해도
Reading Time CLS 개선 후 결과와 지표가 크게 달라지지는 않았습니다.

{{% columns %}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/h9x4l6guvcvmet0fo5l2r/fix-cls-06-lighthouse-first-metrics.webp?rlkey=ku875b48cqk2b6eiothgza58o&raw=1"
  alt="Lighthouse 초기 분석 결과 - CLS 0.067, LCP 12.6s"
  caption="(모바일) Lighthouse 초기 분석 결과 - CLS 0.067" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/tjos805vlmrd81ujmp4zn/fix-cls-08-lighthouse-third-metrics.webp?rlkey=d2gkxma0tdh5ld7qh4j1i3e08&raw=1"
  alt="Lighthouse 개선 후 분석 결과 - CLS 0.002, LCP 4.2s"
  caption="(모바일) Lighthouse 개선 후 분석 결과 - CLS 0.002" >}}
{{% /columns %}}

해당 지표는 제가 `localhost` 상에서 측정한 것이고, Github Pages로 배포된
`minyeamer.github.io/` 사이트에서는 또 다른 결과가 만들어집니다.
개선 전후 Lighthouse 측정 결과를 정리하면 다음과 같습니다.

| 지표 | 개선 전 | 개선 후 | 변화 |
|------|---------|---------|------|
| **CLS** | 0.067 | **0.002** | **-97%** |
| **TBT** | 170ms | 0ms | -100% |
| **LCP** | 12.6s | 4.2s | -66.7% |
| Performance | 65점 | 82점 | +17점 |

CLS는 97% 줄었고, Font Awesome CDN 제거 등 부수적인 개선으로
TBT와 LCP도 함께 눈에 띄게 좋아졌습니다.

## 마치며

Google Search Console에서 측정하는 CLS 지표는
최근 28일 간 실제 사용자 데이터를 평균 내기 때문에 반영하는데 시간이 걸립니다.

![Google Search Console > Core Web Vitals > Desktop](https://dl.dropboxusercontent.com/scl/fi/c7y7t7w62gfle1waswbct/fix-cls-01-desktop-dates.webp?rlkey=g71l892s9j3969cao14o54wrs&raw=1)

Core Web Vitals의 그래프를 보면 2월 8일에 한 번 경고가 사라진 적이 있었는데
그 때가 제가 CLS 개선 작업을 블로그에 반영한 날짜입니다.
아쉽게도 이후로 다시 경고가 발생해 지속되다가 거의 보름이 지난 2월 23일에서야
<span style="background-color: #F4B400; color: #000;">Need improvement</span>가
<span style="background-color: #0F9D58; color: #fff;">Good</span>으로 변경되었습니다.
이때 잠깐 Good URL로 인식되다가 지금은 아무런 상태가 표시되고 있지 않습니다.

제가 겪은 CLS 이슈의 주요 원인은 이미지 태그에 `width`, `height` 속성이 추가되지 않은 것이었습니다.
이미지의 크기를 지정해준 것만으로 CLS 지표가 크게 줄어들었고,
그 외에 동적으로 변경되는 요소가 있다면 기본값을 할당해주거나, 값이 바뀌어도 크기가 변경되지 않도록
최소 너비나 높이를 지정해주면 CLS 지표를 개선하는데 도움이 될 것입니다.
