---
title: "Hugo 블로그 만들기 (5) - 본문 레이아웃 개선 (헤더와 푸터 및 Disqus 댓글 기능 구현)"
date: "2025-12-15T11:01:49+09:00"
layout: "post"
description: >
  Hugo Book 테마의 본문 레이아웃을 개선하는 방법을 소개합니다.
  본문 헤더에 제목과 커버 이미지를 추가하고, 푸터에 이전/다음 게시글 네비게이션과 태그 목록을 구현합니다.
  Disqus 댓글 시스템 연동과 스크롤 진행도, 최신글 목록 등 부가 기능까지 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Disqus", "댓글 기능", "커버 이미지", "스크롤 진행도", "휴고 본문", "휴고 테마", "휴고 레이아웃", "Blog", "HTML", "CSS", "JavaScript", "Hugo Book"]
---

{{% hint info %}}
<i class="fa-solid fa-circle-info"></i> 대상 독자
- 마크다운으로 작성할 수 있는 나만의 블로그를 만들고 싶은 분들
- Hugo Book 테마를 사용해 본문 레이아웃을 개선하려는 분
- Disqus 등 외부 댓글 시스템 연동을 고려하는 분
{{% /hint %}}

{{% hint success %}}
<i class="fa-solid fa-lightbulb"></i> 주요 내용
- Book 테마에서 본문 헤더를 개선하는 과정 ([제목 추가하기](#본문-제목-추가하기) / [커버 이미지 표시하기](#본문-커버-이미지-표시하기))
- Book 테마에서 본문 푸터를 개선하는 과정 ([이전, 다음 게시글 링크 추가하기](#이전-다음-게시글-링크-추가하기) / [태그 목록 표시하기](#태그-목록-표시하기))
- Disqus 댓글 기능 추가하기 ([댓글 기능 추가하기 (Disqus)](#댓글-기능-추가하기-disqus))
{{% /hint %}}

[앞선 게시글](/blog/hugo-blog-4/)에서 Book 테마의 검색 프로세스를 개선했습니다.
기존 Book 테마에 없던 검색 페이지까지 추가되어 사용자가 원하는 키워드를 포함한 게시글을
더 직관적으로 알릴 수 있게 되었습니다.

이번 게시글에서는 본문 레이아웃을 구성하는 각각의 템플릿을 개선할 것입니다.
Book 테마에서 심심하게 느껴졌던 본문 상단에 헤더를 추가하고,
시리즈 게시글 탐색이 용이하도록 이전, 다음 페이지로 이동하는 링크를 하단에 추가할 것입니다.
추가로, 독자와 상호작용이 가능한 댓글 기능을 활용하는 것까지 진행하겠습니다.

## 본문 영역 파악하기

본문 레이아웃을 커스터마이징하기에 앞서 본문 영역이 어디서 구현되는지 알아보겠습니다.

시리즈 2번째 글에서 [메인 레이아웃을 커스터마이징](/blog/hugo-blog-2/#메인-레이아웃-개선하기)할 때
본문 영역이 `.book-page` 영역에서 시작되는 것을 확인했습니다.
해당 영역은 레이아웃을 구성하는 기본적인 틀인 `baseof.html` 파일에서 정의되어 있습니다.

```html
<!-- layouts/baseof.html -->

<body>
    <!-- ... -->
    <div class="book-page">
      <header class="book-header hidden">
        {{ template "header" . }} <!-- Mobile layout header -->
      </header>

      {{ partial "docs/inject/content-before" . }}
      {{ template "main" . }} <!-- Page Content -->
      {{ partial "docs/inject/content-after" . }}
<!-- ... -->
</body>
```

`.book-header` 영역은 메인 레이아웃을 커스터마이징할 때 이미 개선한 모바일 헤더입니다.
앞으로 추가할 본문 헤더는 여기가 아니라 별도의 템플릿을 만들 것입니다.

이어서 실제 본문 내용을 표시하는 `main` 템플릿이 호출되는데,
그 전후로 `content-before`, `content-after` 템플릿이
호출됩니다. 본문의 상단, 하단에 새로운 요소를 추가할 때 활용할 수 있을 것 같습니다.

```html
{{ define "main" }}
  <article class="markdown book-article">
    {{- .Content -}}
  </article>
{{ end }}
```

`main` 템플릿이 어떤 내용인지 이어서 확인해보았습니다.
`.book-article` 영역 내에 마크다운 콘텐츠인 `.Content` 가 배치됩니다.

`content-before`, `content-after` 템플릿은 따로 건든적이 없는데다가
원래도 비어있는 템플릿이기 때문에 ExampleSite 기준으로 아래 이미지처럼
본문 영역엔 마크다운 콘텐츠만 나타납니다.

![Hugo Book 본문](https://dl.dropboxusercontent.com/scl/fi/tqrspz13thhcfnxgk6awy/hugo-49-book-page.webp?rlkey=qe6olc3g75xhaqs0vdieeskne&raw=1)

## 본문 헤더 개선하기

### 본문 제목 추가하기

일반적인 블로그 플랫폼(대표적으로 항상 참고하는 티스토리 hELLO 테마)에서는
아래 이미지처럼 본문 상단에 카테고리, 제목, 작성일을 표시하고 있습니다.
딱 이정도만 있으면 좋을 것 같아 그대로 구현해보겠습니다.

![티스토리 본문 헤더](https://dl.dropboxusercontent.com/scl/fi/noni21f2m6d18j30v6zql/hugo-50-tistory-header.webp?rlkey=5uzz2mjz1yqer45j3lcx67r2f&raw=1)

본문 헤더를 `content-before` 템플릿에 추가할 수도 있지만,
개인적으로 분문 영역은 `.book-article` 영역 내부로 규정했기 때문에
본문 헤더도 별도의 템플릿을 만들고 `main` 템플릿에서 호출할 것입니다.

위 모습을 그대로 `layouts/_partials/docs/post-header.html` 템플릿 파일로 만들었습니다.

{{% tabs "post-header" %}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/post-header.html -->

<!-- ExampleSite 기준, 섹션이 다르다면 변경해줘야 합니다. -->
{{ if eq .Section "post" }}
<header class="post-header">

  {{ if .Params.categories }}
  <div class="post-header-category">
    {{ $categories := partial "categories/value" .Params.categories }}
    <a href="{{ "/categories/" | relURL }}{{ $categories | urlize }}/" class="post-header-category-link">
      {{ $categories }}
    </a>
  </div>
  {{ end }}

  <h1 class="post-header-title">{{ .Title }}</h1>

  {{ with .Date }}
  <div class="post-header-date">
    <time datetime="{{ .Format "2006-01-02T15:04:05Z07:00" }}">
      {{ .Format "2006. 1. 2. 15:04" }}
    </time>
  </div>
  {{ end }}

</header>
{{ end }}
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.post-header {
  text-align: center;
  padding-bottom: $padding-24;
  border-bottom: 1px solid var(--gray-200);

  .post-header-category {
    margin-bottom: $padding-8;
    font-size: $font-size-16;
    font-weight: 400;
  }

  .markdown .post-header-category-link {
    &[href] {
      color: var(--body-font-color);
    }

    &[href]:visited {
      color: var(--body-font-color);
    }

    &[href]:hover {
      text-decoration: none;
    }
  }

  .post-header-title {
    font-size: $font-size-40;
    font-weight: 700;
    color: var(--body-font-color);

    @media (max-width: $body-max-width) {
      font-size: $font-size-32;
    }
  }

  .markdown .post-header-title {
    margin: 0;
  }

  .post-header-date {
    color: var(--gray-500);
    font-size: $font-size-14;
    font-weight: 400;
    margin-top: $padding-8;
  }
}
```
{{% /tab %}}

{{% /tabs %}}

이렇게 템플릿 파일을 추가하고 `baseof` 의 `main` 템플릿에서
`docs/post-header` 템플릿을 호출하여 마크다운 콘텐츠 위에 헤더를 추가해줍니다.

```html
{{ define "main" }}
  <article class="markdown book-article">
    {{ partial "docs/post-header" . }}
    {{- .Content -}}
  </article>
{{ end }}
```

적용하고 게시글 하나를 들어가보면 글 제목이 직관적으로 보입니다.   
또한, 헤더의 카테고리 텍스트는 시리즈 3번째 글에서 생성했던
[카테고리 페이지](/blog/hugo-blog-3/#카테고리-페이지-추가)로 연결됩니다.

![본문 헤더 - Getting Started with Hugo](https://dl.dropboxusercontent.com/scl/fi/gvo9vryf9mqwi4of1h0ly/hugo-51-post-header.webp?rlkey=tvpqxkr0gwm7lt11ti8ijfjei&raw=1)

### 본문 커버 이미지 표시하기

티스토리와 함께 블로그 테마로 참고하는 Velog에서는 본문 상단에
커버 이미지를 표시합니다.

![Velog 본문 헤더](https://dl.dropboxusercontent.com/scl/fi/1gh92qmne98sywr15ei15/hugo-52-velog-header.webp?rlkey=7fa9p2hp7jkesywcvza5yr82k&raw=1)


제가 티스토리를 사용할 때는 커버 이미지가 눈에 띄지 않아 중요하게 생각하지 않았고
글 하나 쓸때마다 이미지를 만들어 넣는게 불편해서 신경쓰지 않았습니다.
하지만, 커버 이미지가 큼지막하게 표시되는 Velog를 이용하면서
커버 이미지가 있는 글이 없는 글보다 확실히 매력적으로 보이게 되었습니다.

티스토리 헤더 형식만으로는 역시 허전하여 헤더 아래에 커버 이미지를 추가하겠습니다.

{{% tabs "post-cover" %}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/post-header.html -->

<header class="post-header">
  <!-- ... -->
</header>

{{ if .Params.cover }}
<div class="book-cover">
  <img src="{{ .Params.cover | absURL }}" alt="Cover Image" class="book-cover-img">
</div>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
.book-cover {
  margin-top: $padding-32;
  margin-bottom: $padding-48;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;

  .book-cover-img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
  }
}
```
{{% /tab %}}

{{% /tabs %}}

템플릿은 동일하게 `post-header` 템플릿을 활용합니다.
위치는 `.post-header` 헤더 영역의 아래쪽에 추가하는데,
본문 헤더와 커버 이미지는 구분선으로 분리되어 표시되는게 더 보기 좋으므로
`<header>` 요소 밖에 커버 이미지를 추가하는걸 권장합니다.

커버 이미지 영역의 클래스명은 본문 헤더와 맞춰서 `post-cover` 를 사용하고 싶었지만
이 클래스명은 [게시글 항목 템플릿](/blog/hugo-blog-3/#게시글-항목-템플릿-추가)에서
이미 사용하고 있으므로 `book-cover` 라고 이름지었습니다.

커버 이미지를 적용하고 동일한 게시글에 들어가보면 헤더 아래에
큼지막하게 커버 이미지가 노출됩니다.

![본문 커버 이미지 - Getting Started with Hugo](https://dl.dropboxusercontent.com/scl/fi/x65dvdgm2mnwhjzh8uipl/hugo-53-book-cover.webp?rlkey=m9d06tpw6dkt0wnbbp7lullmf&raw=1)

## 푸터 영역 파악하기

Book 테마의 기본 푸터 영역은 아래 이미지처럼 카피라이트 외에 보여지는 것이 없습니다.

![Hugo Book 푸터 영역](https://dl.dropboxusercontent.com/scl/fi/ac4payhh900vfomy0gxgi/hugo-54-book-footer.webp?rlkey=m5t5x8xmgmqb0btay7nmjzshc&raw=1)

다시, 가장 기본이 되는 `baseof.html` 파일로 돌아가보겠습니다.

```html
<!-- layouts/baseof.html -->

<body>
    <!-- ... -->
    <div class="book-page">
      <!-- ... -->
      {{ partial "docs/inject/content-before" . }}
      {{ template "main" . }} <!-- Page Content -->
      {{ partial "docs/inject/content-after" . }}

      <footer class="book-footer">
        {{ template "footer" . }} <!-- Footer under page content -->
        {{ template "comments" . }} <!-- Comments block -->
        {{ partial "docs/inject/footer" . }}
        {{ template "copyright" . }} <!-- Copyright block -->
      </footer>
<!-- ... -->
</body>
```

`main` 템플릿 아래에 `book-footer` 영역이 위치해있습니다.
푸터 영역은 순서대로 `footer`, `comments`, `docs/inject/footer`, `copyright`
템플릿이 배치됩니다.

### footer 템플릿

푸터 영역에서 가장 상단에 있는 `footer` 템플릿은 두 가지 링크로 구성되어 있습니다.

각각 `BookLastChangeLink` 변수가 `true` 로 설정되어 있을 경우 표시되는 "커밋 링크"와,
`BookEditLink` 변수가 `true` 로 설정되어 있을 경우 표시되는 "수정하기 링크"입니다.
개인적으로 글 작성은 에디터에서 하기 때문에 이 기능을 사용할 일은 없을 것 같습니다.

```html
<!-- layouts/_partials/docs/footer.html -->

<div class="flex flex-wrap justify-between">

<div>
{{ if and .GitInfo .Site.Params.BookLastChangeLink }}
  {{- $date := partial "docs/date" (dict "Date" .Lastmod "Format" .Site.Params.BookDateFormat) -}}
  <a class="flex align-center" href="{{ partial "docs/links/commit" . }}" title='{{ partial "docs/text/i18n" "Last modified by" }} {{ .GitInfo.AuthorName }} | {{ $date }}' target="_blank" rel="noopener">
    <img src="{{ partial "docs/icon" "calendar" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Calendar" }}" />
    <span>{{ $date }}</span>
  </a>
{{ end }}
</div>

<div>
{{ if and .File .Site.Params.BookEditLink }}
  <a class="flex align-center" href="{{ partial "docs/links/edit" . }}" target="_blank" rel="noopener edit">
    <img src="{{ partial "docs/icon" "edit" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Edit" }}" />
    <span>{{ partial "docs/text/i18n" "Edit this page" }}</span>
  </a>
{{ end }}
</div>

</div>

{{ partial "docs/prev-next" . }}
```

추가로, `footer` 템플릿 하단에 `docs/prev-next` 템플릿을 연쇄적으로 호출하는데,
이전/다음 페이지로 이동하는 기능은 이후에 별도로 알아보겠습니다.

`baseof` 에서 `footer` 템플릿 다음으로 이어지는 `comments` 템플릿 또한
댓글 기능이 구현되어 있지 않기 때문에 별도로 설명드릴 예정입니다.
그리고, `comments` 템플릿 다음 순서인 `docs/inject/footer` 영역은 마찬가지로 비어있고
이번에 사용하지는 않습니다.

### copyright 템플릿

현재 푸터 영역에서 유일하게 보여지고 있는 `copyright` 템플릿은 한 줄로 구성된 단순한 파일입니다.

```html
<!-- layouts/_partials/docs/copyright.html -->

<small>{{ .Site.Title }} - {{ .Site.Copyright | .RenderString }}</small>
```

Hugo 설정에서 `title` 과 `copyright` 값을 읽어서 `<small>` 텍스트로 표시합니다.
카피라이트 값은 Book 테마의 ExampleSite에서 그대로 가져왔습니다.

```yaml
copyright: "[© CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode)"
```

## 본문 푸터 개선하기

### 이전, 다음 게시글 링크 추가하기

Velog와 같은 일반적인 블로그 플랫폼에서는 아래 이미지처럼 이전, 다음 게시글로
이동하는 링크를 제공하여 현재 게시글에 관심있는 독자들이 다른 게시글을 연속해서 볼 수 있도록
지원합니다.

![Velog 이전, 다음 게시글 링크](https://dl.dropboxusercontent.com/scl/fi/ds1q718dur3j1k12fof7t/hugo-55-velog-prev-next.webp?rlkey=eexbteixibselrr653yy3qorw&raw=1)

Book 테마의 푸터에서는 그러한 바로가기 링크가 보이지 않는데,
이전에 `footer` 템플릿 하단에서 `docs/prev-next` 템플릿을 호출하던걸 보면
이전, 다음 게시글 링크가 구현은 되어 있는 것 같습니다.
해당 템플릿이 어떤 내용을 가지고 있는지 확인해보았습니다.

```html
<!-- layouts/_partials/docs/prev-next.html -->

<div class="flex flex-wrap justify-between">
  <div>
  {{ with .NextInSection }}
    <a href="{{ .RelPermalink }}" class="flex align-center">
      <img src="{{ partial "docs/icon" "backward" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Backward" }}" />
      <span>{{ partial "docs/title" . }}</span>
    </a>
  {{ end }}
  </div>
  <div>
  {{ with .PrevInSection }}
    <a href="{{ .RelPermalink }}" class="flex align-center">
      <span>{{ partial "docs/title" . }}</span>
      <img src="{{ partial "docs/icon" "forward" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Forward" }}" />
    </a>
  {{ end }}
  </div>
</div>
```

`NextInSection`, `PrevInSection` 이 있을 경우에 바로가기 링크가 나타나는 것 같습니다.
해당 기능과 관련해서는 아래 공식문서를 참고할 수 있는데,
개인적으로 원하는건 모든 게시글 중에서 이전, 다음 게시글을 보여주는게 아니라
같은 자식 카테고리에 포함되는 게시글끼리 구분해서 이전, 다음 게시글을 보여주고 싶습니다.

{{< bookmark "https://gohugo.io/methods/page/nextinsection/" >}}

따라서, `NextInSection` 기능에 대해 알아보지 않고 직접 템플릿을 만들어보겠습니다.

Book 테마에서는 위에 `prev-next` 템플릿 외에 `post-prev-next` 템플릿도 있는데
내용은 비슷합니다. 이전, 다음 게시글 링크로는 `post-prev-next` 라는 명칭이 더 적절한 것 같아서
`prev-next` 템플릿 대신에 `post-prev-next` 템플릿을 사용하겠습니다.

{{% tabs "post-prev-next" %}}

{{% tab "HTML1" %}}
```go
/* layouts/_partials/docs/post-prev-next.html */

{{ $currentCategories := partial "categories/value" .Params.categories }}
{{ $currentPage := . }}

{{/* 카테고리와 매칭되는 페이지를 분류하기 위한 빈 배열 선언 */}}
{{ $pages := slice }}

{{ range where .Site.RegularPages "Section" .Section }}
  {{ $pageCategories := partial "categories/value" .Params.categories }}

  {{/* 카테고리와 매칭되는 페이지를 `$pages` 배열에 추가 */}}
  {{ if eq $currentCategories $pageCategories }}
    {{ $pages = $pages | append . }}
  {{ end }}
{{ end }}

{{/* 이전, 다음 페이지 초기화 */}}
{{ $prev := "" }}
{{ $next := "" }}
{{ $matches := false }}

{{/* 인접 페이지를 구하기 위해 현재 페이지의 위치를 탐색 */}}
{{ range $index, $page := $pages }}
  {{ if eq $page.RelPermalink $currentPage.RelPermalink }}
    {{ $matches = true }}

    {{/* 현재 페이지가 배열의 시작이 아니라면 `$prev` 에 이전 페이지 객체를 할당 */}}
    {{ if lt $index (sub (len $pages) 1) }}
      {{ $prev = index $pages (add $index 1) }}
    {{ end }}

    {{/* 현재 페이지가 배열의 끝이 아니라면 `$next` 에 다음 페이지 객체를 할당 */}}
    {{ if gt $index 0 }}
      {{ $next = index $pages (sub $index 1) }}
    {{ end }}
  {{ end }}
{{ end }}
/* HTML2 */
```
{{% /tab %}}

{{% tab "HTML2" %}}
```html
<!-- layouts/_partials/docs/post-prev-next.html -->

<!-- HTML1 -->
<div class="post-navigation">
  {{ with $prev }}
  <a href="{{ .RelPermalink }}" class="post-nav-link post-nav-prev">
    <span class="post-nav-direction"><i class="fa-solid fa-backward"></i> PREV</span>
    <span class="post-nav-title">{{ partial "docs/title" . }}</span>
  </a>
  {{ else }}
  <a href="" class="post-nav-link post-nav-prev post-nav-disabled">
    <span class="post-nav-direction"><i class="fa-solid fa-backward"></i> PREV</span>
    <span class="post-nav-title">이전 게시글이 없습니다</span>
  </a>
  {{ end }}

  {{ with $next }}
  <a href="{{ .RelPermalink }}" class="post-nav-link post-nav-next">
    <span class="post-nav-direction">NEXT <i class="fa-solid fa-forward"></i></span>
    <span class="post-nav-title">{{ partial "docs/title" . }}</span>
  </a>
  {{ else }}
  <a href="" class="post-nav-link post-nav-next post-nav-disabled">
    <span class="post-nav-direction">NEXT <i class="fa-solid fa-forward"></i></span>
    <span class="post-nav-title">다음 게시글이 없습니다</span>
  </a>
  {{ end }}
</div>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

$narrow-breakpoint: ($body-min-width + $body-max-width) / 2;

.post-navigation {
  display: flex;
  justify-content: space-between;
  gap: 0;
  margin-top: $padding-24;
  padding-top: $padding-24;
  border-top: 1px solid var(--gray-200);
  overflow: hidden;

  @media screen and (max-width: $narrow-breakpoint) {
    flex-direction: column;
  }

  .post-nav-link {
    display: block;
    background: var(--gray-100);
    padding: $padding-12;
    text-decoration: none;
    transition: background-color 0.2s ease;
    flex: 1;
    max-width: 50%;

    &:hover {
      background: var(--link-background);
    }

    @media screen and (max-width: $narrow-breakpoint) {
      max-width: 100%;
    }
  }

  .post-nav-prev {
    text-align: left;
    border-radius: 8px 0 0 8px;

    @media screen and (max-width: $narrow-breakpoint) {
      border-radius: 8px;
    }
  }

  .post-nav-next {
    text-align: right;
    border-radius: 0 8px 8px 0;

    @media screen and (max-width: $narrow-breakpoint) {
      border-radius: 8px;
    }
  }

  .post-nav-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  .post-nav-direction {
    display: block;
    color: var(--gray-500);
    font-size: $font-size-14;
    font-weight: 600;
    margin-bottom: $padding-8;

    .fa-backward, .fa-forward {
      font-size: $font-size-14;
    }
  }

  .post-nav-title {
    display: block;
    color: var(--body-font-color);
    font-size: $font-size-16;
    font-weight: 400;
    line-height: 1.5;

    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
```
{{% /tab %}}

{{% /tabs %}}

`post-prev-next` 템플릿 내용이 길어서 HTML1, HTML2 탭으로 분리했습니다.
템플릿의 상단인 HTML1 탭에서는 Hugo 문법을 사용해서 이전, 다음 페이지 객체를 구하고,
하단인 HTML2 탭에서는 페이지 객체로부터 바로가기 링크를 만듧니다.

CSS 스타일에서 신경쓴 부분은 이전 게시글 링크 `.post-nav-prev` 요소는
왼쪽만 둥근 사각형 형태로 만들고, 다음 게시글 링크 `.post-nav-next` 요소는
오른쪽만 둥근 사각형 형태로 만들어서 두 사각형을 자연스럽게 연결한 것입니다.

그리고, `footer` 템플릿에서 `docs/prev-next` 템플릿을 호출하는 부분을
`docs/post-prev-next` 템플릿을 호출하도록 수정하면
아래 이미지처럼 이전, 다음 게시글 링크가 표시됩니다.

![NEXT >> (Hu)go Template Primer](https://dl.dropboxusercontent.com/scl/fi/6ujyg43trd2utnd18c6n4/hugo-56-post-next.webp?rlkey=el8enizgyonqoxi2jux2wl48y&raw=1)
![Getting Started with Hugo << PREV](https://dl.dropboxusercontent.com/scl/fi/xj13r3jedux66nhgajd4j/hugo-57-post-prev.webp?rlkey=mfi2yeoftoe9ee9yb1grs2ikn&raw=1)

만약 이전 게시글이 없다면 "이전 게시글이 없습니다" 안내 문구와 함께 링크가 비활성화되고
다음 게시글이 없다면 마찬가지로 링크가 비활성화됩니다.
이전, 다음 게시글이 둘 다 있으면 양쪽 링크가 모두 활성화됩니다.

### 태그 목록 표시하기

본문 헤더에 카테고리는 표시했지만 태그는 아직 추가하지 않았습니다.
태그 목록은 헤더에 있는 경우도 있고 푸터에 있는 경우도 있는데,
헤더는 이미 제목과 커버 이미지만으로 꽉찬데다 태그가 얼마나 길어질수도 예측할 수 없어서
푸터에 두는게 적절하다고 판단했습니다.

태그 목록의 위치는 앞에서 추가한 이전, 다음 게시글 링크의 위쪽이 적절해보입니다.
태그 목록은 내용이 별로 길지는 않지만 `footer` 템플릿에서 태그의 깊이가 깊어지는걸 피하고 싶어서
`docs/post-tags` 템플릿이라는 별도의 템플릿으로 분리하겠습니다.

```html
<!-- layouts/_partials/docs/post-tags.html -->

<div class="post-tags">
  {{ range .Params.tags }}
  <a href="{{ "/tags/" | relURL }}{{ . | urlize }}/" class="tag">#{{ . }}</a>
  {{ end }}
</div>
```

그리고, `footer` 템플릿에서 `tags` 가 있는 경우만 `post-tags` 템플릿을
호출하는 구문을 `post-prev-next` 위에 배치시킵니다.

```html
<!-- layouts/_partials/docs/footer.html -->

{{ if .Params.tags }}
  {{ partial "docs/post-tags" . }}
{{ end }}
{{ partial "docs/post-prev-next" . }}
```

태그가 있는 게시글에서 보면 아래 이미지처럼 칩 형태의 태그 목록이 나타납니다.
`post-item` 템플릿에서 사용된 스타일을 그대로 사용하기 때문에 별도로
CSS 스타일을 추가해줄 필요는 없습니다.
태그 칩을 클릭하면 태그 페이지로 이동하는 것도 동일합니다.

![태그 목록 [#go, #golang, #hugo, #development]](https://dl.dropboxusercontent.com/scl/fi/1emh4l8qibucohh08ws02/hugo-58-post-tags.webp?rlkey=44kcyrh2fkzdq4kcrsoi6lvib&raw=1)

### 댓글 기능 추가하기 (Disqus)

과거 3년 전에 Hugo 블로그를 만들면서 Utterances 앱을 활용한 댓글 기능을 추가한적이 있습니다.
관련 게시글은 [링크](/blog/hugo-blog-old-2/)를 참고해주세요.

Utterances는 Github 이슈를 데이터베이스처럼 사용하여 댓글을 관리하는 기능입니다.
댓글을 작성하려면 Github 계정이 있어야하는 단점이 있지만
어차피 이런 기술 블로그에 들어오는 사람이라면 Github 계정이 있는건
당연하기에 댓글을 쓰는데 있어서 불편함이 있을거라 생각하진 않습니다.

하지만, 최근에 블로그를 개편하면서 블로그 리포지토리를 갈아엎은적이 있었는데,
Github 이슈도 같이 날아가버려서 이런 식으로 관리하는데는 한계가 있을 것이라 생각했습니다.

마침 Book 테마에서 기본 댓글 기능으로 Disqus를 권장하고 있고
유료 서비스인만큼 관리가 잘될 것을 기대하여 이번에 이용해보기로 했습니다.
(유료 플랜이 있다는것 뿐이고 해당 블로그는 규모가 크지 않아서 무료 플랜을 사용합니다.)

Disqus는 소셜 미디어 계정을 통해서 댓글이나 좋아요와 같이 게시글에 반응할 수 있는
기능을 제공합니다. 어드민 페이지도 따로 제공하여 어떤 페이지에서 댓글이 달렸는지 확인하고,
필요하면 삭제할 수 있는 기능까지 제공합니다.

Disqus의 장단점을 설명하는게 목적은 아니기에 자세한건 다른 게시글을 참고해주시기 바랍니다.

{{< bookmark "https://muhanstory.tistory.com/902" >}}

Disqus를 사용하려면 먼저 Disqus 사이트에 방문하여 요금제를 선택합니다.
(이미지를 클릭하면 이동합니다.)

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/r50aiy2tpou104i9dwm5v/hugo-59-disqus-pricing.webp?rlkey=toy12an5lob6o0zd5cungv4iz&raw=1"
  alt="Disqus Pricing"
  href="https://disqus.com/pricing/" >}}

물론, 밑으로 조금 내리면 무료 플랜을 선택할 수 있습니다.

![Disqus - We offer a free, ad-supported version of Disqus Comments to eligible publishers.](https://dl.dropboxusercontent.com/scl/fi/0dfmqyta1jummihk82zgd/hugo-60-disqus-free.webp?rlkey=qdhlrvjq2f2l0kegmuge4jnp9&raw=1)

계정을 만들고 로그인하면 새로운 사이트를 만들 수 있는 페이지로 이동합니다.
사이트명은 기본적으로 어드민 페이지의 URL로 사용되는데 원한다면 URL만 수정할 수도 있습니다.

![Disqus - Create a new site](https://dl.dropboxusercontent.com/scl/fi/xglt6xwvt1xge1b9hrf55/hugo-61-disqus-new-site.webp?rlkey=lqnvnxs7jjs5zq3gkr04872d3&raw=1)

카테고리는 아무거나 선택해서 다음으로 넘어가면 플랫폼을 선택하는 페이지가 나타납니다.
아쉽게도 Jekyll은 있는데 Hugo가 없네요. 맨 아래에 `Install manually` 부분을 클릭해줍니다.

![Disqus - What platform is your site on?](https://dl.dropboxusercontent.com/scl/fi/0gamdvt43dkf9rl9fjk2c/hugo-62-disqus-platform.webp?rlkey=o81ph3mded67j89w76gko924y&raw=1)

그러면 웹사이트에 Disqus를 직접 추가할 수 있는 스크립트를 제공해줍니다.   
(아래 스크립트를 그대로 가져다 쓰면 안되고 `<site-name>` 에 알맞은 URL이 들어가야 합니다.)

```html
<div id="disqus_thread"></div>
<script>
    /**
    *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
    *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables    */
    /*
    var disqus_config = function () {
    this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
    this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
    };
    */
    (function() { // DON'T EDIT BELOW THIS LINE
    var d = document, s = d.createElement('script');
    s.src = 'https://<site-name>.disqus.com/embed.js';
    s.setAttribute('data-timestamp', +new Date());
    (d.head || d.body).appendChild(s);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
```

이것을 `layouts/_partials/docs/comments.html` 템플릿 파일에 그대로 넣어줍니다.   
(기존에 `disqus` 템플릿을 호출하는건 무시하고 덮어씌워도 됩니다.)

그러면 아래 이미지처럼 푸터 영역에 Disqus UI가 나타납니다.

![Disqus - What do you think? 0 Responses](https://dl.dropboxusercontent.com/scl/fi/wd9gveaxjkpln3grb4gv2/hugo-63-disqus-thread.webp?rlkey=m7d1fn0aadrrxx0rpsv37plok&raw=1)

만약 Disqus 댓글창이 바로 위에 있는 이전, 다음 게시글 링크와 너무 붙어있다고 생각된다면
`#disqus_thread` 영역을 대상으로 `margin` 스타일을 추가할 수 있습니다.

`color-scheme` 이라는 색상 테마도 있긴한데, 이후에 다크모드를 만들 때 이 속성 때문에
댓글창만 색상이 고정되어버리는 문제 때문에 `none` 값을 주어 없앴습니다.

```scss
#disqus_thread {
  color-scheme: none;
  margin-top: $padding-40;
}
```

## 기타 기능 추가하기

본문 레이아웃을 개선하는 과정은 여기까지로 마무리되었습니다.

이제부터는 별도의 게시글로 담아낼만큼 분량이 안나오는 자잘한 기능들을
따로 모아서 구현하는 과정을 전달드리겠습니다.

### 스크롤 진행도 표시하기

블로그나 뉴스 사이트를 보다 보면 일부 사이트에서 스크롤 위치에 따라 상단 또는 하단에
눈에 띄는 색상의 진행도를 표시하는 모습을 보입니다.
개인적으로 느끼기에 매우 유용한 기능인 것 같아서 코파일럿에게 구현을 요청했습니다.

생각보다 원리는 간단합니다.

{{% tabs "scroll-progress" %}}

{{% tab "JavaScript" %}}
```js
// assets/scroll-progress.js

document.addEventListener('DOMContentLoaded', function() {
  const progressBar = document.querySelector('.scroll-progress-bar');
  
  if (!progressBar) return;
  
  function updateScrollProgress() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollProgress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
    progressBar.style.width = scrollProgress + '%';
  }

  window.addEventListener('scroll', updateScrollProgress, { passive: true });
  updateScrollProgress();
});
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 9999;
  pointer-events: none;
}

.scroll-progress-bar {
  height: 100%;
  background: #1e6ef4;
}
```
{{% /tab %}}

{{% /tabs %}}

모든 페이지에 `scroll-progress-bar` 라는 클래스를 포함하는 요소를 두고
이 요소의 가로 길이를 스크롤 위치에 맞춰서 제어합니다.
이 요소에 배경색을 부여하고 세로 길이로 진행도의 굵기를 표현하면
눈에 띄는 스크롤 진행도를 표시할 수 있습니다.

```html
<!-- baseof.html -->

<body>
  <div class="scroll-progress">
    <div class="scroll-progress-bar"></div>
  </div>
```

모든 페이지에 `scroll-progress-bar` 요소를 둘만한 템플릿을 결정해야 하는데,
어렵게 생각할 필요없이 모든 페이지에서 공통으로 참조하는 `baseof` 의 `<body>` 태그 내
최상단에 배치하면 다른 영역들과 겹치는 것을 고려하지 않아도 됩니다.

게시글에 접속해서 스크롤을 조금 내리면 아래 이미지처럼 진행도가 표시됩니다.
스크롤 위치에 따라 왼쪽에서 시작해 오른쪽까지 파란색 진행도가 자연스럽게 채워집니다.

![스크롤 진행도 표시](https://dl.dropboxusercontent.com/scl/fi/vatf7headlxbgwetyxdfk/hugo-64-scroll-progress.webp?rlkey=0t0kjbwzcr1k3a389rqv5e9wi&raw=1)

### 최신글 표시하기

왼쪽 사이드 메뉴에서 최신글 목록을 표시하면 유입된 독자들을
다른 게시글로 전환시키는데 효과적일 것이라 생각하여 관련 템플릿을 만들어보았습니다.

{{% tabs "recent-posts" %}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/recent-posts.html -->

<!-- ExampleSite 기준, 섹션이 다르다면 변경해줘야 합니다. -->
{{ $recentPosts := where .Site.RegularPages "Section" "post" | first 5 }}
{{ if $recentPosts }}
<div class="recent-posts">
  <div class="recent-posts-header">
    <i class="fa-solid fa-clock"></i>
    <span>최신글</span>
  </div>

  <ul class="recent-posts-list">
    {{ range $recentPosts }}
    <li class="recent-post-item">
      <a href="{{ .RelPermalink }}" title="{{ .Title }}">
        <div class="recent-post-title">{{ .Title }}</div>
        <div class="recent-post-date">
          <time datetime="{{ .Date.Format "2006-01-02" }}">
            {{ .Date.Format "2006.01.02" }}
          </time>
        </div>
      </a>
    </li>
    {{ end }}
  </ul>
</div>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/custom.scss

.recent-posts {
  margin: $padding-16 0;
  padding-bottom: $padding-16;
  border-bottom: 1px solid var(--gray-500);

  .recent-posts-header {
    margin-bottom: $padding-8;
    padding: $padding-4 $padding-8;
    font-weight: 500;
    color: var(--body-font-color);

    .fa-clock {
      font-size: $font-size-14;
      color: var(--color-link);
    }
  }

  .recent-posts-list {
    list-style: none;
    padding: 0;
    margin: 0;

    .recent-post-item {
      a {
        display: block;
        padding: $padding-8;
        color: var(--body-font-color);
        border-radius: $border-radius;
        text-decoration: none;

        &:hover {
          color: var(--color-link);
          background-color: var(--link-background);
        }
      }

      .recent-post-title {
        font-size: $font-size-14;
        font-weight: 400;
        margin-bottom: $padding-4;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .recent-post-date {
        font-size: $font-size-12;
        color: var(--gray-500);

        time {
          font-family: monospace;
        }
      }
    }
  }
}
```
{{% /tab %}}

{{% /tabs %}}

최신글 템플릿이 추가되는 위치는 사이드 메뉴에서 카테고리 목록 아래가 적절해보입니다.
`docs/menu` 템플릿에서 `docs/recent-posts` 템플릿을 불러오면 되는데,
Hugo 설정에서 `BookMenu.recentPosts` 가 `true` 일 경우에만 표시되도록 제어했습니다.

```html
<!-- layouts/_partials/docs/menu.html -->

<nav>
{{ partial "docs/brand" . }}
{{ partial "docs/search" . }}
{{ partial "categories/menu" . }}
{{ if default false .Site.Params.BookMenu.recentPosts }}
  {{ partial "docs/recent-posts" . }}
{{ end }}
<!-- ... -->
</nav>
```

`config.yaml` 과 같은 설정 파일에서 `BookMenu.recentPosts` 키값을 추가하면
아래 이미지와 같이 카테고리 목록 아래에 최신글 목록이 최대 5개까지 표시됩니다.

![최신글](https://dl.dropboxusercontent.com/scl/fi/8s3vk9617fzi4ljcxrl48/hugo-65-recent-posts.webp?rlkey=wis8xi2x2fw7jn5tj2oujo4rt&raw=1)

## 마치며

블로그를 구성하는 주요 레이아웃들은 여기까지의 과정을 통해 완성되었습니다.
앞으로 다크모드, 코드블럭, 검색엔진 등록, 이미지 업로드 등의 개선 과정이
남아있지만, 순차적으로 진행해야 하는 과정은 이 글이 마지막입니다.
이어지는 게시글에서는 더 이상 "Hugo 블로그 만들기" 제목과 순번이 붙지 않으며
각각의 독립적인 게시글로 작성될 것입니다.

이번 시리즈가 개인 블로그를 만드는데 도움이 되었다면 좋겠습니다.
만약 이번 시리즈를 보고 개인 블로그를 개성있게 커스터마이징했다면
댓글로 주소를 알려주시기 바랍니다. 관심있게 둘러보겠습니다.
또한, 추가로 만들면 좋겠다 싶은 기능이 있으면 마찬가지로 댓글로
작성해주셔도 좋겠습니다. 감사합니다.
