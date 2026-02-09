---
title: "Hugo 분류(Taxonomies) 커스터마이징 - 태그/카테고리 템플릿 구현"
date: "2025-11-22T23:04:47+09:00"
layout: "post"
description: >
  Hugo의 taxonomies 기능을 활용하여 태그와 카테고리 페이지를 커스터마이징하는 방법을 소개합니다.
  게시글 목록 템플릿과 페이지네이션 구현, 태그 및 카테고리 페이지 추가, 메뉴에 카테고리를 통합하는 과정을 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Taxonomies", "태그", "카테고리", "Hugo 분류", "휴고 테마", "Blog", "HTML", "CSS", "JavaScript", "Hugo Book", "블로그 태그", "블로그 카테고리"]
series: ["Hugo 블로그 만들기"]
---

{{< series "Hugo 블로그 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo가 기본으로 제공하는 기능을 넘어, 블로그의 전문성을 높여주는 **Taxonomy 커스터마이징** 노하우를 공유합니다.
반복되는 게시글 목록과 복잡한 카테고리 트리 구조를 독립된 **템플릿으로 모듈화**하여,
단 한 번의 설계만으로 모든 페이지에서 완벽한 일관성과 압도적인 **재사용성**을 확보해 보세요.

- **[Taxonomies 이해](#taxonomies)**: 콘텐츠를 그룹화하는 Taxonomy, Term의 핵심 개념 파악
- **[게시글 목록 모듈화](#게시글-목록-템플릿-추가)**: 카드뉴스 스타일의 게시글 항목과 효율적인 **[페이지네이션](#페이지네이션-템플릿-추가)** 구현
- **[태그 템플릿 개선](#태그-페이지-추가)**: 모든 태그를 칩(Chip) 스타일로 나열한 태그 목록 페이지 제작
- **[계층형 카테고리 설계](#카테고리-페이지-추가)**: 부모-자식 관계의 2단계 구조 설계 및 **[접이식 카테고리 메뉴](#메뉴에-카테고리-추가)** 추가
{{% /hint %}}

[앞선 게시글](/blog/hugo-blog-2/)에서 Book 테마의 메인 레이아웃인 메뉴, 목차, 헤더를 개선해보았습니다.   
앞에서의 과정을 거쳤다면 프로필 사진, 소셜 링크, 스크롤 이동 버튼 등이 블로그에 추가되었을 것입니다.

이번 게시글에서는 Hugo의 `taxonomies` 기능을 활용하여 카테고리와 태그를 커스터마이징하는 방법을 알아보겠습니다.

## Taxonomies

Hugo는 `taxonomies` 라고 하는 콘텐츠 그룹화 기능을 제공합니다.
해당 기능은 게시글과 같은 콘텐츠를 사용자가 직접 정의하여 분류하기 위해 사용할 수 있는데,
대표적으로 카테고리와 태그가 있습니다.

{{< bookmark "https://gohugo.io/content-management/taxonomies/" >}}

### Taxonomy 구성 요소

Hugo에서 Taxonomy는 다음 세 가지 요소로 구성됩니다.

- **Taxonomy**: 콘텐츠를 분류하는 데 사용할 수 있는 카테고리 체계 (예: `tags`, `categories`)
- **Term**: Taxonomy 내의 개별 항목 (예: `Hugo`, `Blog`, `Frontend`)
- **Value**: Term에 할당된 콘텐츠 (예: 특정 태그가 지정된 게시글)

예를 들어, 이 블로그의 현재 게시글은 다음과 같은 taxonomies를 가지고 있습니다.

```yaml
categories: ["Frontend", "Blog"]
tags: ["Hugo", "태그", "카테고리"]
```

여기서 `categories`와 `tags`는 **Taxonomy**이고, `Frontend`, `Blog`, `Hugo` 등은 **Term**입니다.

그리고 이 게시글 자체가 이러한 **Term**들의 **Value**가 됩니다.

### Taxonomy 할당 방법

Hugo는 기본적으로 `categories` 와 `tags` 두 가지 taxonomy를 제공합니다.

게시글의 `front matter` 에 태그나 카테고리를 추가하면, Hugo는 자동으로 다음과 같은 페이지들을 생성합니다.   
([front matter](https://gohugo.io/content-management/front-matter/)에 대해서는 따로 설명하지 않았는데,
게시글의 최상단에 YAML, TOML 등 형식으로 입력하는 메타데이터 입니다.)

- 모든 태그/카테고리를 나열하는 목록 페이지 (예: `/categories/`, `/tags/`)
- 각 태그/카테고리별 게시글 목록 페이지 (예: `/categories/blog/`, `/tags/hugo/`)

실제로 Hugo 정적 웹페이지를 만들면 아래와 같은 경로들이 생성되는 것을 확인할 수 있습니다.

```bash
public/
├── asciinema/
├── categories/
├── docs/
├── icons/
├── katex/
├── posts/
├── showcases/
└── tags/
```

여기서 `categories/` 와 `tags/` 경로가 `taxonomy.html` 및 `terms.html` 템플릿에 의해 만들어진 결과입니다.   
(Book 테마에서는 두 경로에 대한 레이아웃을 만들지 않았으므로 해당 페이지의 내용은 비어있습니다.)

Hugo에서 이러한 기능을 제공해준다면 그대로 사용해도 되지 않을까 싶지만,
안타깝게도 Hugo는 카테고리와 태그를 1차원적으로밖에 인식하지 못합니다.
태그는 단순히 1차원 배열로 봐도 괜찮지만, 카테고리는 최소 2단계 이상의 깊이가 있는 구조를 지향하므로
직접 커스터마이징할 필요가 있습니다.

## 게시글 목록 템플릿 추가

카테고리와 태그 페이지는 두 종류로 나눠집니다.
하나는 전체 카테고리 및 태그 목록을 보는 페이지(이하 taxonomy 페이지)이고,
다른 하나는 단일 카테고리 또는 태그에 속하는 게시글 목록을 보여주는 페이지(이하 terms 페이지)입니다.

이 중 게시글 목록을 보여주는 taxonomy 페이지에서 공통적인 기능과 외관을 가진 부분이 있는데,
해당 부분을 별도의 템플릿으로 구성하고자 합니다.

### 게시글 목록 구상하기

일반적인 블로그 플랫폼에서 게시글 목록은 세로로 나열됩니다.
아래 이미지는 티스토리에서 볼 수 있는 게시글 목록의 한 부분인데,
게시글 제목, 작성일, 요약과 같은 메타데이터가 좌측에 보여지고 커버 이미지가 우측에 표시됩니다.

![티스토리 페이지 목록](https://dl.dropboxusercontent.com/scl/fi/ikiuvlhm3qhzedbo70lq2/hugo-26-tistory-list.webp?rlkey=1wxkesjmx7ukcemg2edd107g3&raw=1)

티스토리 블로그에서는 게시글 목록에서 태그를 보여주지 않지만,
이번에 만들 taxonomy 페이지에서는 각 게시글 항목마다 태그를 보여주고
태그를 클릭하면 terms 페이지로 이동하도록 구성할 예정입니다. (카테고리도 마찬가지 입니다.)

### 게시글 항목 템플릿 추가

Book 테마는 `layouts/_partials/docs` 경로에 partial 템플릿이 위치해 있습니다.

게시글 목록에서 단일 게시글 항목은 partial 템플릿으로 분류된다 생각하여 해당 경로에
`post-item.html` 이라는 템플릿을 추가했습니다.
커버 이미지의 위치를 조정하는 등의 CSS 스타일은 `assets/_custom.scss` 에 적용해줍니다.
(CSS 스타일이 상대적으로 길어 주석으로 설명을 대체합니다.)

{{< tabs "post-item-draft" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/post-item.html -->

<article class="post-item">

  <div class="post-meta">
    <!-- 게시글 작성일 -->
    <time datetime="{{ .Date.Format "2006-01-02" }}">
      {{ .Date.Format "2006년 01월 02일" }}
    </time>
    <!-- 카테고리 목록이 추가될 위치 -->
  </div>

  <div class="post-content-area{{ if .Params.cover }} has-cover{{ end }}">
    <div class="post-text-area">
      <!-- 게시글 제목 -->
      <h2 class="post-title">
        <a href="{{ .RelPermalink }}">{{ .Title }}</a>
      </h2>

      <!-- 게시글 요약 -->
      {{ $summary := cond .Description .Description (cond .Summary .Summary "") }}
      {{ if $summary }}
      <div class="post-summary">
        {{ $summary | plainify | truncate 148 }}
      </div>
      <div class="post-summary-mobile">
        {{ $summary | plainify | truncate 72 }}
      </div>
      {{ end }}

      <!-- 태그 목록이 추가될 위치 -->
    </div>

    <!-- 커버 이미지 -->
    {{ if .Params.cover }}
    <div class="post-cover">
      <img src="{{ .Params.cover | absURL }}" alt="Cover Image" class="post-cover-img">
    </div>
    {{ end }}
  </div>

</article>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.post-item {
  // `post-item` 영역을 명확하게 구분하기 위해 테두리를 추가
  border: 1px solid var(--gray-200);
  border-radius: 8px;
  padding: $padding-24;
  background: var(--body-background);
  transition: box-shadow 0.3s ease, border-color 0.3s ease;

  &:hover {
    // `post-item` 영역에 마우스를 올리면 테두리를 링크 색상(파란색)으로 변경
    box-shadow: 0 4px 12px var(--box-shadow);
    border-color: var(--color-link);
  }
}

.post-meta {
  // `post-meta` 영역 내 항목(작성일 및 카테고리)을 정렬하고 연한 글씨색 적용
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--gray-500);
  flex-wrap: wrap;
  gap: 0.5rem;
  font-size: 0.9rem;
  margin-bottom: 0.9rem;

  time {
    font-weight: 500;
  }
}

.post-content-area {
  // `post-content-area` 영역 내 항목(제목, 요약 텍스트 및 커버 이미지)을 정렬
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;

  &.has-cover .post-text-area {
    // 게시글이 커버 이미지를 가질 경우 텍스트 영역의 세로 길이를 이미지 높이만큼 고정
    // (태그 목록을 영역 하단에 고정시키기 위한 목적)
    min-height: $preview-height; // 170px;
  }
}

.post-text-area {
  // 제목 텍스트, 요약 텍스트, 태그 목록 요소들을 정렬
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;

  h2.post-title {
    margin-top: 0;
    margin-bottom: $padding-8;
    line-height: 1.4;
  }
}

.post-title {
  // 제목 텍스트의 스타일을 적용
  font-size: $font-size-24;
  line-height: 1.3;

  a {
    color: var(--body-font-color);
    text-decoration: none;
    transition: color 0.3s ease;

    &:hover {
      color: var(--color-link);
    }
  }
}

.markdown .post-title {
  // 마크다운 H2 헤더에 기본으로 적용되는 마진을 무시 (여백 줄이기)
  margin-top: $padding-20;
}

.post-summary, .post-summary-mobile {
  // 요약 텍스트의 스타일을 적용
  color: var(--gray-800);
  line-height: 1.6;
  margin-bottom: 1rem;
  overflow: hidden;
  word-wrap: break-word;
  flex: 1;
}

.post-summary-mobile {
  // 기본적으로는 모바일 전용 요약 텍스트를 숨기기
  display: none;
}

.post-cover {
  // 커버 이미지의 가로, 세로 길이를 고정
  width: $preview-width; // 200px;
  height: $preview-height; // 170px;
  border-radius: 8px;
  overflow: hidden;

  .post-cover-img {
    // 커버 이미지가 고정된 길이를 넘으면 가운데만 잘라서 표시하기
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }
}

@media (max-width: $body-max-width) {
  .post-title {
    font-size: $font-size-20; // 모바일 사이즈에서 제목 텍스트 크기를 줄이기
  }

  .post-summary {
    display: none; // 모바일 사이즈에서 기본 요약 텍스트를 숨기기
  }

  .post-summary-mobile {
    display: block; // 모바일 사이즈에서 모바일 전용 요약 텍스트를 표시하기
  }

  .post-content-area.has-cover {
    // 모바일 사이즈에서 커버 이미지 크기를 줄이고 정사각형 비율로 변경
    .post-cover {
      width: $preview-mobile-width; // 160px;
      height: $preview-mobile-height; // 160px;
    }

    .post-text-area {
      min-height: $preview-mobile-height; // 160px;
    }
  }
}
```
{{% /tab %}}

{{< /tabs >}}

하나의 게시글 항목은 게시글 작성일, 제목, 요약, 커버 이미지로만 구성되어 있습니다.

아직 게시글 항목을 볼 수 있는 페이지를 만들지 않아서 해당 템플릿을 직접 확인하기 어려울 것이기에
실제로 템플릿을 렌더링한 결과를 보여드립니다. (커버 이미지는 해당 게시글의 커버 이미지를 첨부했습니다.)

![스타일이 적용된 게시글 항목](https://dl.dropboxusercontent.com/scl/fi/5wp1ijnpa7wsiiidjqx90/hugo-29-post-item-with-style.webp?rlkey=xpi059pig9wnpki1t6x2hemvk&raw=1)

간단하게 설명하자면, 게시글 요약은 게시글이 가진 `Description` 또는 `Summary` 를 가져와
일정 글자 수까지 잘라서 표시합니다. `Description` 은 front matter에서 작성하는
게시글에 대한 설명문이고, `Summary` 는 마찬가지로 front matter에서 지정할 수도 있지만
따로 지정하지 않으면 게시글의 본문 텍스트를 일정 글자 수까지 제공합니다.

게시글 요약에 표시할 글자 수의 경우 여러가지 숫자를 넣어봤을 때 148자가 적절했고,
모바일의 경우 그보다 더 적은 72자 정도가 적절했습니다.
이어지는 CSS 설정에서 볼 수 있는데, 화면의 너비에 따라 일정 크기를 초과하면 `post-summary` 요소만 표시하고
일정 크기 이하로 줄어들면 `post-summary-mobile` 요소만 표시하는 원리입니다.

커버 이미지를 불러오는 부분은 Hugo에서 이미지가 문자열로 전달되는 경우와 맵 형태로 전달되는 경우를 고려하여 작성되었습니다.
특별히 맵 형태의 이미지를 의식한 것은 아니고, Book 테마의 다른 템플릿에서 이런식으로 커버 이미지를 불러와서 그대로 가져다 썼습니다.
front matter에서 커버 이미지에 대한 주소를 작성하면 `img.post-cover-img` 요소의 `src` 속성으로 해당 이미지 주소가 전달됩니다.

이후에 카테고리와 태그 페이지를 추가하면서
게시글 항목의 우측 상단인 커버 이미지 위에 카테고리 목록을,
좌측 하단인 요약 텍스트 아래에 태그 목록을 추가할 예정입니다.

## 페이지네이션 템플릿 추가

또 하나로 고려해야 할 것은 페이지네이션 입니다.
앞으로 게시글들이 계속 추가될건데, 그 많은 게시글들을 하나의 페이지에서 모두 보여주게 되면
보기도 불편할 것이며 장기적으로 게시글들을 불러오는 속도를 감당하지 못할 것입니다.
페이지네이션은 이런 문제를 개선하기 위해 게시글들을 여러 페이지로 나눠서 일정 개수만 표시하는 방식입니다.

### 페이지네이션 구상하기

마찬가지로 티스토리 블로그를 보면 아래 이미지와 같이 페이지네이션 기능을 제공합니다.

![티스토리 페이지네이션](https://dl.dropboxusercontent.com/scl/fi/ovln0vmu7bnazbz1xcuel/hugo-27-tistory-pagination.webp?rlkey=znhs90atgjp8rpfhcwqvcsjk5&raw=1)

일반적인 게시판 페이지에서는 10개 단위로 페이지를 표시하는데
티스토리 블로그는 현재 페이지에서 앞뒤로 3개의 페이지만 보여줍니다.
이번에 만들 taxonomy 페이지에서는 일반적인 게시판처럼 10개 단위로 페이지를 표시할 것입니다.

### 페이지네이션 템플릿 추가

Book 테마에서는 기본적으로 `pagination.html` 템플릿을 제공하고
해당 템플릿은 Hugo의 [Paginator](https://gohugo.io/methods/page/paginator/)라는 기능을 사용합니다.

```html
<!-- layouts/_partials/docs/pagination.html -->

{{- if .Paginator -}}
<!-- ... -->
{{- end -}}
```

하지만, Paginator 기능에 대한 [공식문서](https://gohugo.io/methods/page/paginator/)를 보면 다음과 같은 제약사항을 안내하고 있습니다.

{{< hint info >}}
<p>
Although simple to invoke, with the Paginator method you can neither filter nor sort the page collection.
It acts upon the page collection received in context.
</p>
<p>
The Paginate method is more flexible, and strongly recommended.
</p>
{{< /hint >}}

페이지 컬렉션, 즉 게시글 목록을 필터하거나 정렬할 수 없다는건데 카테고리 또는 태그 관련 게시글을
페이지 단위로 나열할 때는 전체 게시글 중 관련된 일부 게시글만 필터할 필요가 있어서
[Paginate](https://gohugo.io/methods/page/paginate/)라는 다른 기능을 사용할 것입니다.

다음과 같이 `paginate.html` 템플릿을 변경해줍니다.
(CSS 스타일도 `assets/_custom.scss` 에 추가해줍니다.)

{{< tabs "pagination" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/pagination.html -->

{{ $paginate := . }}
{{ if gt $paginate.TotalPages 1 }}
<div id="pagination-anchor"></div>
<nav class="pagination">
  {{ $currentPage := $paginate.PageNumber }}
  {{ $totalPages := $paginate.TotalPages }}

  <!-- 10개 게시글 단위로 페이지를 그룹화 -->
  {{ $groupNumber := div (sub $currentPage 1) 10 }}
  {{ $groupStart := add (mul $groupNumber 10) 1 }}
  {{ $groupEnd := add $groupStart 9 }}
  {{ if gt $groupEnd $totalPages }}
    {{ $groupEnd = $totalPages }}
  {{ end }}

  <!-- 이전 및 다음 페이지 그룹을 계산 -->
  {{ $prevGroupPage := sub $groupStart 10 }}
  {{ $nextGroupPage := add $groupEnd 1 }}

  <!-- 이전 페이지 그룹으로 이동하는 링크 -->
  {{ if gt $groupStart 1 }}
  <a href="{{ $paginate.First.URL }}{{ if gt $prevGroupPage 1 }}page/{{ $prevGroupPage }}/{{ end }}#pagination-anchor" class="pagination-nav pagination-link">
    <i class="fa-solid fa-backward"></i> 이전
  </a>
  {{ else }}
  <span class="pagination-nav disabled">
    <i class="fa-solid fa-backward"></i> 이전
  </span>
  {{ end }}

  <!-- 현재 페이지 그룹의 페이지로 이동하는 링크 -->
  <div class="pagination-pages">
    {{ range $i := seq $groupStart $groupEnd }}
      {{ if eq $i $currentPage }}
      <span class="pagination-page current" id="current-page">{{ $i }}</span>
      {{ else }}
      <a href="{{ $paginate.First.URL }}{{ if gt $i 1 }}page/{{ $i }}/{{ end }}#pagination-anchor" class="pagination-page pagination-link">
        {{ $i }}
      </a>
      {{ end }}
    {{ end }}
  </div>

  <!-- 다음 페이지 그룹으로 이동하는 링크 -->
  {{ if le $nextGroupPage $totalPages }}
  <a href="{{ $paginate.First.URL }}page/{{ $nextGroupPage }}/#pagination-anchor" class="pagination-nav pagination-link">
    다음 <i class="fa-solid fa-forward"></i>
  </a>
  {{ else }}
  <span class="pagination-nav disabled">
    다음 <i class="fa-solid fa-forward"></i>
  </span>
  {{ end }}

</nav>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.pagination {
  // 이전 버튼, 페이지 링크, 다음 버튼을 정렬
  display: flex;
  justify-content: center;
  align-items: center;
  gap: $padding-4;

  padding: 2rem 0;
  margin-top: 2rem;
  border-top: 1px solid var(--gray-200);
  max-width: 100%;

  .pagination-nav, .pagination-page {
    // 각각의 페이지 링크에 대한 스타일을 적용
    // (페이지 번호를 모서리가 둥근 사각형 테두리로 감싸기)
    padding: $padding-8;
    border: 1px solid var(--gray-200);
    border-radius: 4px;

    flex-grow: 0;
    flex-shrink: 0;
    text-align: center;
    white-space: nowrap;

    &:hover {
      background: var(--gray-200);
      border-color: var(--color-link);
    }
  }
}

.markdown {
  // 마크다운 a 태그에 기본으로 적용되는 색상을 무시
  a[href].pagination-link {
    color: var(--body-font-color);
    text-decoration: none;
  }

  a[href]:hover.pagination-link {
    color: var(--body-font-color);
    text-decoration: none;
  }

  a[href]:visited.pagination-link {
    color: var(--body-font-color);
    text-decoration: none;
  }
}

.pagination-nav {
  width: 4rem;

  &.disabled {
    // 이전, 다음 페이지 그룹이 없으면 버튼을 비활성화
    border: 1px solid var(--gray-200);
    color: var(--gray-500);
    cursor: not-allowed;
  }

  i {
    // 이전, 다음 버튼의 아이콘 크기 설정
    font-size: $font-size-12;
  }
}

.pagination-pages {
  // 페이지 링크들을 정렬
  display: flex;
  gap: $padding-4;

  .pagination-page {
    min-width: 2.5rem;

    &.current {
      // 현재 페이지에 대한 링크를 강조
      background: var(--color-page-link);
      border-color: var(--color-link);
      cursor: default;
    }
  }
}

#pagination-anchor {
  // 페이지 이동 후 스크롤을 유지하기 위한 앵커 요소 숨기기
  position: relative;
  top: -100px;
  visibility: hidden;
}

@media (max-width: $body-max-width) {
  // 모바일 사이즈에서는 이전, 다음 버튼을 페이지 링크 아래로 배치
  .pagination {
    flex-wrap: wrap;
    gap: $padding-8;
  }

  .pagination-pages {
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
  }

  .pagination-nav {
    order: 2;
  }
}
```
{{% /tab %}}

{{< /tabs >}}

페이지네이션 템플릿을 렌더링하면 아래 이미지처럼 보입니다.

![스타일이 적용된 페이지네이션](https://dl.dropboxusercontent.com/scl/fi/ese1anj2erz20tjsy4zd3/hugo-32-pagination-with-style.webp?rlkey=lpaiva9puxov3agnsyh0cget1&raw=1)

페이지네이션 템플릿은 이전 버튼, 페이지 링크 10개, 다음 버튼이 순서대로 나열되어 있습니다.

페이지를 이동하는건 현재 경로 뒤에 `/page/{페이지}` 를 붙이면 됩니다.   
(`Paginate` 기능을 사용했다면 렌더링 시에 각 페이지별 정적 페이지가 만들어집니다.)

페이지 링크는 이를 이용해 특정 페이지에 대한 경로로 이동할 수 있는 링크를 제공합니다.
또한, 다른 페이지로 이동한 후에도 스크롤 위치를 유지하도록 페이지네이션 영역에 대한 앵커 링크 `#pagination-anchor` 를
추가했습니다.

이전 버튼과 다음 버튼은 직전, 직후 페이지로 이동하는게 아니라 이전, 다음 페이지 그룹으로 이동하는 링크를 제공합니다.
페이지 그룹은 10개 페이지 단위로 구성되어 있으며, 해당 버튼은 페이지 그룹의 첫 번째 페이지로 연결됩니다.

## Taxonomy 템플릿 경로

필요한 partial 템플릿들을 만들었으니 본격적으로 taxonomy 및 terms 템플릿을 만들겠습니다.   
그전에, 어디에 템플릿을 만들어야 하는지 알아보겠습니다.

{{< bookmark
  url="https://gohugobrasil.netlify.app/templates/taxonomy-templates/#taxonomy-list-templates"
  image="https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&raw=1" >}}

위 Hugo 공식문서를 참고해보면 다음과 같은 우선순위로 taxonomy 템플릿을 탐색한다는 것을 알 수 있습니다.

{{< hint info >}}
<ol>
<li>layouts/taxonomy/&lt;SINGULAR&gt;.html</li>
<li>layouts/_default/taxonomy.html</li>
<li>layouts/_default/list.html</li>
<ol>
{{< /hint >}}

동일하게, terms 템플릿은 다음과 같은 우선순위로 탐색합니다.

{{< hint info >}}
<ol>
<li>layouts/taxonomy/&lt;SINGULAR&gt;.terms.html</li>
<li>layouts/_default/terms.html</li>
<ol>
{{< /hint >}}

Book 테마에서 terms 템플릿은 제공되지 않지만 taxonomy 템플릿은
`layouts/_partials/docs/taxonomy.html` 경로에서 제공됩니다.
해당 taxonomy 템플릿은 태그와 카테고리에 공통적으로 적용됩니다.

하지만, 태그와 카테고리에 대한 페이지 구성에 차이가 있어서 전용 템플릿을 만들어야 합니다.
이 경우에는 `layouts/tags/` 및 `layouts/categories/` 경로를 활용할 수 있습니다.

## 태그 페이지 추가

태그 페이지는 taxonomy 템플릿을 먼저 만들고 terms 템플릿을 만들겠습니다.   
태그 전용 템플릿을 만들기 위해 `layouts/tags/` 경로 아래에 두 개의 템플릿 파일을 추가하면 됩니다.

### taxonomy 템플릿 추가

먼저, `layouts/tags/list.html` 파일을 추가하여 특정 태그를 포함하는 게시글 목록을 보여주는
템플릿을 만들어보겠습니다.

{{< tabs "tags-list" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/tags/list.html -->

{{ define "main" }}
<article class="markdown book-article">
  <div class="list-header">
    <h1><i class="fa-solid fa-tag"></i> {{ .Title }}</h1>
    <p>전체 글 <em class="list-count">{{ len .Pages }}</em></p>
  </div>

  {{ $paginator := .Paginate .Pages 10 }}

  <div class="post-list">
    {{ range $paginator.Pages }}
      {{ partial "docs/post-item.html" . }}
    {{ end }}
  </div>

  {{ partial "docs/pagination.html" $paginator }}
</article>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.list-header {
  // 헤더 영역의 요소들을 가운데 정렬
  text-align: center;
  padding-bottom: $padding-16;
  margin-bottom: $padding-48;
  border-bottom: 1px solid var(--body-font-color);

  h1 {
    font-size: $font-size-40;
    margin-bottom: $padding-8;

    i {
      font-size: $font-size-40;
    }
  }

  p {
    font-size: $font-size-20;
  }
}

.list-count {
  // 관련 게시글 수를 파란색으로 강조 표현
  font-style: normal;
  font-weight: bold;
  color: var(--color-link);
}

.post-list {
  // 게시글 목록 간의 간격을 조절하고 footer와의 여백도 추가
  display: flex;
  flex-direction: column;
  gap: $padding-24;
  margin-bottom: $padding-48;
}
```
{{% /tab %}}

{{< /tabs >}}

앞에서 게시글 목록과 페이지네이션 템플릿을 미리 만들어뒀기 때문에 taxonomy 템플릿은 단순합니다.

템플릿에서 사용되는 [Pages](https://gohugo.io/methods/page/pages/) 기능은
모든 `Page` 객체를 목록으로 반환하는데, taxonomy 레이아웃에서는
해당 taxonomy, 즉 태그를 포함하는 `Page` 객체들만 반환합니다.

상단의 `list-header` 영역에서는 단순히 `Pages` 를 호출하고
그 개수를 세어 전체 몇 개의 게시글이 있는지 알려줍니다.

헤더 아래 본문인 `post-list` 영역에서는 각각의 `Page` 객체에 대한
메타데이터를 목록으로 나타내는데, 한번에 10개 페이지씩 나눠서 보여주기 위해
`Pages` 를 [Paginate](https://gohugo.io/methods/page/paginate/)로 감쌉니다.

반복문을 통해 현재 페이지에 할당된 모든 `Page` 객체를
`layouts/_partials/docs/post-item.html` 템플릿을 사용해 보여주고,
본문 아래에는 `layouts/_partials/docs/pagination.html` 템플릿을 사용해
페이지 이동 링크를 나타냅니다.

보기 좋게 CSS 스타일도 추가했습니다.
`list-header` 및 `post-list` 클래스는 카테고리의 taxonomy 템플릿에서도 사용되므로
taxonomy 유형의 템플릿에서 공통으로 적용되는 스타일입니다.

렌더링하고 Example Site의 태그 중 `Development` 에 대한 taxonomy 페이지를 접속하면
아래와 같이 관련 게시글 목록을 볼 수 있습니다.
관련 게시글이 2개 밖에 없어 페이지네이션은 안보이는데 관련 게시글을 10개 이상 추가하면 나타납니다.

![태그와 연관된 게시글 목록을 보여주는 페이지](https://dl.dropboxusercontent.com/scl/fi/ltozvebtxa8syiz53kleq/hugo-33-tags-list.webp?rlkey=3u1ppcgqz9t7nrrls2yf31bql&raw=1)

### terms 템플릿 추가

모든 태그 목록을 보여주는 페이지가 있다면 블로그에 처음 들어오는 사람들이
블로그의 정체성을 이해하기 쉬울 것입니다.

`layouts/tags/terms.html` 파일을 추가하여 모든 태그 목록을 보여주는
템플릿을 만들어보겠습니다.

{{< tabs "tags-terms" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/tags/terms.html -->

{{ define "main" }}
<article class="markdown book-article">
  <div class="list-header">
    <h1><i class="fa-solid fa-tags"></i> Tags</h1>
    <p>전체 태그 <em class="list-count">{{ len .Data.Terms }}</em></p>
  </div>

  <div class="tag-chips">
    {{ range .Data.Terms.ByCount }}
    <div class="tag-item">
      <a href="{{ .Page.RelPermalink }}" class="tag-link">
        <span class="tag-name">{{ .Page.Title }}</span>
        <span class="tag-count">({{ .Count }})</span>
      </a>
    </div>
    {{ end }}
  </div>
</article>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.tag-chips {
  display: flex;
  flex-wrap: wrap;
  gap: $padding-8;

  .tag-link {
    display: flex;
    align-items: center;
    gap: $padding-4;
    padding: $padding-8 $padding-12;

    .tag-name {
      font-weight: 500;
    }

    .tag-count {
      font-size: $font-size-12;
      opacity: 0.7;
    }
  }
}
```
{{% /tab %}}

{{< /tabs >}}

terms 템플릿은 단순히 태그 목록을 나열하는 것뿐이라서 내용은 단순합니다.

`.Data.Terms` 방식으로 taxonomies를 가져오는 것은
[Taxonomies 문서](https://gohugo.io/content-management/taxonomies/)에 안내되어 있습니다.
이렇게 가져온 taxonomies, 즉 태그 목록에서 각 태그마다 관련된 게시글의 수를 세어서
`태그 (개수)` 형식으로 보여줄 것입니다.

하지만, 이렇게하면 태그가 하나에 한줄씩 세로로 나열되어 보기에 좋지 않습니다.
단순한 텍스트인 각각의 태그를 칩 형태로 바꾸고 가로로 나열하는 CSS 스타일도 적용했습니다.

![스타일이 적용된 태그 목록](https://dl.dropboxusercontent.com/scl/fi/d2d796n8c5mvv01s566t5/hugo-35-tags-terms-with-style.webp?rlkey=2nncbcugjb28gv45disvkab1m&raw=1)

`{baseURL}/tags` 경로를 통해 terms 페이지에 접근할 수 있는데,
좌측 메뉴에 해당 페이지에 대한 바로가기 버튼도 추가하면 누구나 찾아갈 수 있습니다.
다음과 같이 소셜 링크 영역에서 안쓰는 링크 하나를 태그 페이지로 연결시켰습니다.

```html
<!-- layouts/_partials/docs/brand.html -->

<div class="sidebar-profile">
  <div class="sidebar-social">
    <!-- ... -->
    <a href="{{ "/tags/" | relURL }}" title="Tags">
      <i class="fa-solid fa-tags"></i>
    </a>
    <!-- ... -->
  </div>
</div>
```

## 카테고리 페이지 추가

카테고리는 단순히 키워드들을 1차원적으로 나열한 태그와 다르게 2단계로 구성할 것입니다.
따라서, 저는 카테고리를 일반적인 taxonomies처럼 다루지 않고 첫 번째 원소가 부모 카테고리,
두 번째 원소가 자식 카테고리인 길이가 2인 배열의 형태로 정의했습니다.

이 게시글은 다음과 같이 카테고리를 지정하고 있습니다.

```yaml
categories: ["Frontend", "Blog"]
```

여기서 첫 번째 원소인 "Frontend"가 부모 카테고리가 되고,
두 번째 원소인 "Blog"는 자식 카테고리가 됩니다.

### 카테고리 파싱 템플릿 추가

이어서 만들 taxonomy 템플릿 뿐 아니라
카테고리를 활용하는 모든 템플릿에서 부모/자식 카테고리를 추출해 사용하게 될건데,
해당 코드가 짧은 편이 아니라서 별도의 템플릿으로 만들려고 합니다.

`layouts/_partials/` 경로 아래에 임의의 템플릿 파일을 추가하면 되지만,
비슷한 유형의 템플릿을 3개 정도 만들 것이므로 `categories` 라는 폴더로 묶어주겠습니다.

첫 번째 템플릿은 `.Params.categories` 를 파라미터로 받아서
첫 번째 카테고리 값을 꺼내는 `value-first` 템플릿입니다.
카테고리는 기본적으로 배열 형태지만,
빈 배열 또는 단일 문자열이 지정될 경우도 고려하여 몇 가지 예외처리를 했습니다.

```html
<!-- layouts/_partials/categories/value-first.html -->

{{ $categories := . }}
{{ if reflect.IsSlice $categories }}
  {{- cond (gt (len $categories) 0) (index $categories 0 | string) "" -}}
{{ else if eq (printf "%T" $categories) "string" }}
  {{- $categories -}}
{{ else }}
  ""
{{ end }}
```

두 번째 템플릿은 `.Params.categories` 를 파라미터로 받아서
두 번째 카테고리 값을 꺼내는 `value-second` 템플릿입니다.
카테고리가 단일 문자열인 경우 부모 카테고리만 있다고 판단하기 때문에,
카테고리의 길이가 2 이상인 배열로 제공될 조건만 고려하면 됩니다.

```html
<!-- layouts/_partials/categories/value-second.html -->

{{ $categories := . }}
{{- cond (and (reflect.IsSlice $categories) (gt (len $categories) 1)) (index $categories 1 | string) "" -}}
```

세 번째 템플릿은 `.Params.categories` 를 파라미터로 받아서
`/` 로 구분된 전체 카테고리 문자열을 반환하는 `value` 템플릿입니다.
현재는 2단계 카테고리까지만 지원하기 때문에 배열에 길이 제한을 걸면 디테일을 살릴 수 있지만,
이것이 딱히 오류가 발생하는 것도 아니고 향후 카테고리 단계를 더 늘릴 수도 있기 때문에 단순하게 만들었습니다.

```html
<!-- layouts/_partials/categories/value.html -->

{{ $categories := . }}
{{ if reflect.IsSlice $categories }}
  {{- delimit $categories "/" -}}
{{ else if eq (printf "%T" $categories) "string" }}
  {{- $categories -}}
{{ else }}
  ""
{{ end }}
```

### 부모 카테고리 템플릿 추가

태그에서는 하나의 taxonomy 템플릿을 만들었지만,
카테고리는 부모와 자식 카테고리의 구성이 달라서 2개의 템플릿으로 분리할 것입니다.
태그에서 `layouts/tags/` 경로 아래에 템플릿을 추가한 것처럼
카테고리도 `layouts/categories/` 경로 아래에 템플릿을 추가하겠습니다.

{{< tabs "categories-parent" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/categories/parent.html -->

{{ define "main" }}
<article class="markdown book-article">

  <!-- 제목을 부모 카테고리 명칭으로 인식 -->
  {{ $currentCategory := partial "categories/value-first" (slice .Title) }}
  {{ $pages := slice }}
  {{ $subCategories := slice }}

  <!-- 모든 "posts" 경로의 게시글들을 순회하면서 -->
  {{ range where .Site.RegularPages "Section" "posts" }}
    {{ $pageCategory := partial "categories/value-first" .Params.categories }}

    <!-- 게시글의 첫 번째 카테고리가 현재 부모 카테고리와 같으면 `$pages` 배열에 추가 -->
    {{ if eq $currentCategory $pageCategory }}
      {{ $pages = $pages | append . }}
      {{ $subCategory := partial "categories/value-second" .Params.categories }}
      <!-- 게시글의 두 번째 카테고리가 하위 카테고리 목록에 없으면 `$subCategories` 배열에 추가 -->
      {{ if not (in $subCategories $subCategory) }}
        {{ $subCategories = $subCategories | append $subCategory }}
      {{ end }}
    {{ end }}
  {{ end }}

  <div class="list-header">
    <h1><i class="fa-solid fa-folder"></i> {{ .Title }}</h1>
    <p>전체 글 <em class="list-count">{{ len $pages }}</em></p>
  </div>

  <!-- 모든 하위 카테고리들에 대한 바로가기 링크를 나열 -->
  {{ if $subCategories }}
  <div class="categories-section">
    <h2>하위 카테고리</h2>
    <div class="category-chips">
      {{ range $subCategory := $subCategories }}
      <div class="category-item">
        <a href="{{ "/categories/" | relURL }}{{ $currentCategory | urlize }}/{{ $subCategory | urlize }}" class="category-link">
          <span class="category-name"><i class="fa-solid fa-file"></i> {{ $subCategory }}</span>
        </a>
      </div>
      {{ end }}
    </div>
  </div>
  {{ end }}

  {{ if $pages }}
  <div class="post-list">
    {{ $paginate := .Paginate $pages 10 }}
    <div class="post-list">
      {{ range $paginate.Pages }}
        {{ partial "docs/post-item.html" . }}
      {{ end }}
    </div>

    {{ partial "docs/pagination.html" $paginate }}
  </div>
  {{ else }}
  <div class="post-list empty-list">
    <p>이 카테고리에 게시글이 없습니다.</p>
  </div>
  {{ end }}

</article>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.categories-section {
  margin-bottom: $padding-40;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: $padding-8;

  .category-link {
    display: flex;
    align-items: center;
    gap: $padding-4;
    padding: $padding-8 $padding-12;

    .category-name {
      font-weight: 500;

      .fa-file, .fa-folder, .fa-folder-open {
        font-size: $font-size-base;
      }
    }
  }
}

.empty-list p {
  text-align: center;
}
```
{{% /tab %}}

{{< /tabs >}}

템플릿의 상단에서 부모 카테고리와 연관된 게시글들을 걸러내는 부분을 제외하면
태그의 taxonomy 템플릿과 유사합니다.

해당 템플릿도 taxonomy 템플릿이기 때문에 `Pages` 를 직접 호출할 수도 있지만,
Hugo에서 taxonomy엔 순서가 없기 때문에 부모 카테고리가 카테고리 배열에서 첫 번째 값인 조건을 만족시키기 위해
직접 `Page` 배열을 만들었습니다.

태그의 taxonomy 템플릿과의 가장 큰 차이점은 헤더 아래에 하위 카테고리들에 대한 바로가기 링크를 표시한다는 것입니다.
부모-자식 카테고리 간에 이동을 용이하게 하기 위해 이와 같은 바로가기 링크를 추가했고,
이것이 폴더-파일 관계와 유사하다 생각해 그러한 아이콘으로 직관성을 더했습니다.

렌더링하기 전에 한가지 유의할 점은,
`parent` 라는 임의의 명칭을 사용하는 해당 템플릿은 자동으로 카테고리 페이지들을 만들어내지 않습니다.
게시글이 있는 `content/` 폴더에서 모든 카테고리에 대한 인덱스 페이지를 만들어줘야 합니다.

Example Site에서도 기본적으로 `["Development", "golang"]` 카테고리가 지정되어 있습니다.
부모 카테고리인 `Development` 에 대한 인덱스 페이지를 아래처럼 생성했습니다.

```yaml
# content/categories/Development/_index.md

---
title: "Development"
type: "categories"
layout: "parent"
---
```

제목은 카테고리 명칭과 동일해야 하고, `layout` 를 `parent` 로 지정하면 부모 카테고리 페이지로 렌더링됩니다.
그 결과는 아래 이미지처럼 보입니다. (jekyll 카테고리는 임의로 추가했습니다.)

![부모 카테고리와 연관된 게시글 목록을 보여주는 페이지](https://dl.dropboxusercontent.com/scl/fi/90dwwoc6j18ggg3o79c8v/hugo-36-categories-parent.webp?rlkey=87fe1su96x9jfkr4d89conlh0&raw=1)

### 자식 카테고리 템플릿 추가

자식 카테고리 템플릿은 동일하게 `layouts/categories/` 경로 아래에 추가합니다.
CSS 스타일은 부모 카테고리 템플릿과 동일한 설정을 공유합니다.

```html
<!-- layouts/categories/child.html -->

{{ define "main" }}
<article class="markdown book-article">

  <!-- front matter에서 `parent` 파라미터를 부모 카테고리 명칭으로, 제목을 자식 카테고리 명칭으로 인식 -->
  {{ $currentCategories := partial "categories/value" (slice .Params.parent .Title) }}
  {{ $pages := slice }}

  <!-- 모든 "posts" 경로의 게시글들을 순회하면서 -->
  {{ range where .Site.RegularPages "Section" "posts" }}
    {{ $pageCategories := partial "categories/value" .Params.categories }}

    <!-- 게시글의 전체 카테고리가 현재 카테고리와 같으면 `$pages` 배열에 추가 -->
    {{ if eq $currentCategories $pageCategories }}
      {{ $pages = $pages | append . }}
    {{ end }}
  {{ end }}

  <div class="list-header">
    <h1><i class="fa-solid fa-file"></i> {{ .Title }}</h1>
    <p>전체 글 <em class="list-count">{{ len $pages }}</em></p>
  </div>

  <!-- 부모 카테고리를 가리키는 `parent` 파라미터로 바로가기 링크를 생성 -->
  {{ if .Params.parent }}
  <div class="categories-section">
    <h2>상위 카테고리</h2>
    <div class="category-chips">
      <div class="category-item">
        <a href="{{ "/categories/" | relURL }}{{ .Params.parent | urlize }}/" class="category-link">
          <span class="category-name"><i class="fa-solid fa-folder-open"></i> {{ .Params.parent }}</span>
        </a>
      </div>
    </div>
  </div>
  {{ end }}

  {{ if $pages }}
  <div class="post-list">
    {{ $paginate := .Paginate $pages 10 }}
    <div class="post-list">
      {{ range $paginate.Pages }}
        {{ partial "docs/post-item.html" . }}
      {{ end }}
    </div>

    {{ partial "docs/pagination.html" $paginate }}
  </div>
  {{ else }}
  <div class="post-list empty-list">
    <p>이 카테고리에 게시글이 없습니다.</p>
  </div>
  {{ end }}

</article>
{{ end }}
```

자식 카테고리와 연관된 페이지들을 탐색하는 동작을 제외하면 부모 카테고리 템플릿과 동일합니다.
배열 형태의 `categories` 를 `/` 로 구분된 문자열로 만들어서 비교합니다.

스타일은 부모 카테고리와 동일하므로 별도로 추가할건 없고, 자식 카테고리에 대한 인덱스 페이지들을 만들어줘야 합니다.
아래처럼 부모 카테고리의 인덱스 페이지와 동일한 경로에 자식 카테고리 폴더를 만들고 인덱스 페이지를 추가합니다.

```bash
content/categories/
└── Development/
    ├── _index.md
    ├── golang/
    │   └── _index.md
    └── jekyll/
        └── _index.md
```

자식 카테고리의 인덱스 페이지 내용은 부모 카테고리처럼 front matter를 작성하는데,
부모 카테고리 명칭을 `parent` 파라미터로 추가합니다.

```yaml
---
title: "golang"
type: "categories"
layout: "child"
parent: "Development"
---
```

렌더링하면 이렇게 보입니다.

![자식 카테고리와 연관된 게시글 목록을 보여주는 페이지](https://dl.dropboxusercontent.com/scl/fi/epkvj6f0d695go7gano4w/hugo-37-categories-child.webp?rlkey=i6kkniqxp0r9ksesrlrge7ezd&raw=1)

### 카테고리 목록 템플릿 추가

카테고리 목록을 보여주는 페이지는 결론부터 보여드리면 아래 이미지와 같습니다.

![카테고리 목록](https://dl.dropboxusercontent.com/scl/fi/p7p85k9q39czms9krzof8/hugo-38-categories-terms.webp?rlkey=1uyijv1rprc6fvekpxu1zb27l&raw=1)

트리처럼 카테고리를 단계적으로 보여주고 자식 카테고리 하위에는 관련 게시글을 최대 3개까지 표시합니다.

과거 PaperMod 테마를 커스터마이징 시도할 때 다른 테마 사용자로부터 전달받은
소스코드를 코파일럿 Grok Code Fast 1 모델의 도움을 받아 가공했지만 코드 길이가 길어서 링크로 대체합니다.

{{< bookmark "https://github.com/minyeamer/hugo-book-custom/blob/master/layouts/categories/root.html" >}}

{{< bookmark "https://github.com/minyeamer/hugo-book-custom/blob/master/assets/_custom.scss" >}}

첫 번째 링크는 `layouts/categories/root.html` 경로에 추가하는 파일로 terms 템플릿입니다.   
두 번째 링크는 `assets/_custom.scss` 파일인데, 중간에 `/* Categories List */` 주석으로
시작하는 부분을 참고하면 됩니다.

그리고, terms 템플릿으로 분류했지만 템플릿 명칭은 `root` 이므로 Hugo가 자동으로 인식하지 못합니다.
`content/categories/` 경로 아래에 인덱스 페이지를 추가해줘야 합니다.

```yaml
# content/categories/_index.md

---
title: "Categories"
type: "categories"
layout: "root"
---
```

`{baseURL}/categories` 경로를 통해 카테고리 terms 페이지에 접근할 수 있는데,
태그 terms 페이지처럼 소셜 링크 영역에서 안쓰는 링크 하나 대신에 카테고리 링크를 추가하겠습니다.

```html
<!-- layouts/_partials/docs/brand.html -->

<div class="sidebar-profile">
  <div class="sidebar-social">
    <!-- ... -->
    <a href="{{ "/categories/" | relURL }}" title="Categories">
      <i class="fa-solid fa-folder"></i>
    </a>
    <!-- ... -->
  </div>
</div>
```

### 메뉴에 카테고리 추가

카테고리 terms 페이지에서 전체 카테고리 목록을 파악할 수 있지만,
카테고리는 아무래도 어느 위치에서나 볼 수 있는 메뉴 영역에서 보여지는게
블로그 독자들의 이목을 끌기에 좋을 것입니다.

Book 테마에서 메뉴를 표현하는 템플릿은 `layouts/_partials/docs/menu.html` 입니다.
여기서 카테고리 목록에 대한 템플릿을 호출할 것입니다.

새로운 템플릿의 위치는 앞에서 카테고리 파싱 템플릿을 추가했던 `layouts/_partials/categories/`
경로가 적절해보입니다. 여기에 `menu.html` 템플릿을 추가하겠습니다.

{{< tabs "categories-menu" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/categories/menu.html -->

{{ if .Site.Taxonomies.categories }}
<div class="book-categories">
  <input type="checkbox" class="hidden toggle" id="categories-control" checked />
  <label for="categories-control" class="categories-toggle categories-link">
    <!-- `전체` 카테고리 링크 -> 카테고리 terms 페이지로 연결 -->
    <a href="/categories/">
      <i class="fa-solid fa-folder"></i>
      <span>{{ default "Categories" .Site.Params.BookMenu.categoriesLabel }}</span>
      <span class="category-count">({{ len (where .Site.RegularPages "Section" "posts") }})</span>
    </a>
    <i class="fa-solid fa-chevron-down categories-arrow"></i>
  </label>

  <ul class="categories-menu" id="categories-menu">
    <!-- 부모-자식 카테고리 트리 구성 -->
    {{ $categoryTree := dict }}
    {{ range (where .Site.RegularPages "Section" "posts") }}
      {{ if .Params.categories }}
        {{ $parent := partial "categories/value-first" .Params.categories | string }}
        {{ if $parent }}
          <!-- 부모 카테고리 목록 구성 -->
          {{ if not (index $categoryTree $parent) }}
            {{ $categoryTree = $categoryTree | merge (dict $parent dict) }}
          {{ end }}

          {{ $child := partial "categories/value-second" .Params.categories | string }}
          {{ if $child }}
            <!-- 부모 카테고리에 대한 자식 카테고리 목록 구성 -->
            {{ $children := index $categoryTree $parent }}
            {{ if not (index $children $child) }}
              {{ $children = $children | merge (dict $child dict) }}
              {{ $categoryTree = $categoryTree | merge (dict $parent $children) }}
            {{ end }}
          {{ end }}
        {{ end }}
      {{ end }}
    {{ end }}

    {{ range $parent, $children := $categoryTree }}

    <!-- 부모 카테고리와 연관된 게시글 수를 카운팅 -->
    {{ $parentCount := 0 }}
    {{ range (where $.Site.RegularPages "Section" "posts") }}
      {{ if .Params.categories }}
        {{ if eq $parent (partial "categories/value-first" .Params.categories | string) }}
          {{ $parentCount = add $parentCount 1 }}
        {{ end }}
      {{ end }}
    {{ end }}

    <li>
      {{ if $children }}
      <input type="checkbox" class="hidden toggle" id="cat-{{ $parent | urlize }}" />
      <label for="cat-{{ $parent | urlize }}" class="categories-toggle categories-link">
        <a href="/categories/{{ $parent | urlize }}/">
          <i class="fa-solid fa-folder"></i>
          {{ $parent }}
          <span class="category-count">({{ $parentCount }})</span>
        </a>
        <i class="fa-solid fa-chevron-down categories-arrow"></i>
      </label>
      <ul>
        {{ range $child, $_ := $children }}

        <!-- 자식 카테고리와 연관된 게시글 수를 카운팅 -->
        {{ $childCount := 0 }}
        {{ range (where $.Site.RegularPages "Section" "posts") }}
          {{ if .Params.categories }}
            {{ if eq (printf "%s/%s" $parent $child) (partial "categories/value" .Params.categories | string) }}
              {{ $childCount = add $childCount 1 }}
            {{ end }}
          {{ end }}
        {{ end }}

        <li class="categories-link">
          <a href="/categories/{{ $parent | urlize }}/{{ $child | urlize }}/">
            <i class="fa-solid fa-file"></i>
            {{ $child }}
            <span class="category-count">({{ $childCount }})</span>
          </a>
        </li>
        {{ end }}
      </ul>
      {{ else }}
      <a href="/categories/{{ $parent | urlize }}/">
        <i class="fa-solid fa-file"></i>
        {{ $parent }}
        <span class="category-count">({{ $parentCount }})</span>
      </a>
      {{ end }}
    </li>
    {{ end }}
  </ul>
</div>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
.book-categories {
  margin: $padding-16 0;
  padding-bottom: $padding-16;
  border-bottom: 1px solid var(--gray-500);
  position: relative;
  z-index: 1;

  i.fa-file, i.fa-folder, i.fa-chevron-down, i.fa-chevron-up {
    font-size: $font-size-14;
    transition: transform 0.2s ease;
    max-width: $font-size-18;
  }

  .category-count {
    font-size: $font-size-12;
    color: var(--gray-500);
    white-space: nowrap;
    text-align: left;
    margin: 0;
  }

  .categories-toggle {
    display: flex;
    align-items: center;
    padding: $padding-4 $padding-8;
    min-height: 2.381rem;
    font-weight: 500;
    cursor: pointer;
  }

  .categories-link:hover {
    color: var(--color-link);
    background-color: var(--link-background);
  }

  // `전체` 카테고리 펼치기/접기
  #categories-control:checked + .categories-toggle .categories-arrow {
    transform: rotate(180deg);
  }

  #categories-control:checked ~ .categories-menu {
    max-height: 1000px;
  }

  // 부모-자식 카테고리 펼치기/접기
  input[id^="cat-"]:checked + .categories-toggle .categories-arrow {
    transform: rotate(180deg);
  }
}
```
{{% /tab %}}

{{< /tabs >}}

메뉴 카테고리의 핵심 기능은 카테고리를 펼치고 접을 수 있는 기능과
카테고리와 연관된 게시글의 수를 카운팅하여 표시하는 것입니다.

첫 번째, 카테고리를 펼치고 접는 기능은 체크박스를 통해 이루어집니다.
기능상 체크박스지만 스타일을 적용하게 되면 화살표로 보이는데,
체크박스를 클릭하면 하위 카테고리가 펼쳐지게 됩니다.

두 번째, 카테고리와 연관된 게시글의 수를 카운팅하는 방식은
처음에 `categoryCount` 라는 맵을 만들고 카테고리 트리를 만들 때
카운팅도 같이 하려고 했지만, Hugo에서 맵은 불변성을 가져서
아무리 카운팅해도 1 이상으로 올라가지 않았습니다.
그래서, 완성된 카테고리 트리를 순회하는 과정에서 매번 모든 게시글 목록을 가져와
현재 카테고리와 연관된 게시글의 수를 세는 방식을 채택했습니다.

마지막으로, `layouts/_partials/docs/menu.html` 템플릿으로 돌아가서
검색창 아래에 방금 추가한 템플릿을 호출해주면 메뉴 영역에 카테고리 트리가 나타납니다.

```html
<!-- layouts/_partials/docs/menu.html -->

<nav>
{{ partial "docs/brand" . }}
{{ partial "docs/search" . }}
{{ partial "categories/menu" . }}
<!-- ... -->
```

여기까지 적용했다면 아래 이미지와 같이 메뉴에 카테고리 트리가 보여집니다.

![메뉴에서 보이는 카테고리 트리](https://dl.dropboxusercontent.com/scl/fi/dfuwpvpv27nzbn8drlfs9/hugo-39-categories-menu.webp?rlkey=gg0qotqspkfblua4gv7454c2h&raw=1)

## 게시글 항목 개선하기

태그와 카테고리 페이지를 추가했으니 처음에 만들다만 게시글 항목 템플릿을 완성시켜보겠습니다.

{{< tabs "post-item-complete" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/post-item.html -->

<article class="post-item">

  <div class="post-meta">
    <time datetime="{{ .Date.Format "2006-01-02" }}">
      {{ .Date.Format "2006년 01월 02일" }}
    </time>
    <!-- 게시글이 가진 부모-자식 카테고리 속성을 표시 -->
    {{ if .Params.categories }}
    <div class="post-categories">
      {{ $parentCategory := partial "categories/value-first" .Params.categories }}
      {{- if $parentCategory -}}
        <a href="{{ "/categories/" | relURL }}{{ $parentCategory | urlize }}/" class="category">
          <i class="fa-solid fa-folder"></i> {{ $parentCategory }}
        </a>

        {{ $childCategory := partial "categories/value-second" .Params.categories }}
        {{- if $childCategory -}}
        <a href="{{ "/categories/" | relURL }}{{ $parentCategory | urlize }}/{{ $childCategory | urlize }}/" class="category">
        <i class="fa-solid fa-file"></i> {{ $childCategory }}
        </a>
        {{- end -}}
      {{- end -}}
    </div>
    {{ end }}
  </div>

  <div class="post-content-area{{ if .Params.cover }} has-cover{{ end }}">
    <div class="post-text-area">
      <h2 class="post-title">
        <a href="{{ .RelPermalink }}">{{ .Title }}</a>
      </h2>

      {{- $summary := cond .Description .Description (cond .Summary .Summary "") -}}
      {{ if $summary }}
      <div class="post-summary">
        {{ $summary | plainify | truncate 148 }}
      </div>
      <div class="post-summary-mobile">
        {{ $summary | plainify | truncate 72 }}
      </div>
      {{ end }}

      <!-- 게시글이 가진 태그 속성을 표시 -->
      {{ if .Params.tags }}
      <div class="post-tags">
        {{ range first 5 .Params.tags }}
        <a href="{{ "/tags/" | relURL }}{{ . | urlize }}/" class="tag">#{{ . }}</a>
        {{ end }}
      </div>
      {{ end }}
    </div>

    {{ if .Params.cover }}
    <div class="post-cover">
      <img src="{{ .Params.cover | absURL }}" alt="Cover Image" class="post-cover-img">
    </div>
    {{ end }}
  </div>

</article>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
.post-categories {
  display: flex;
  gap: 0.5rem;

  .category {
    background: var(--gray-200);
    color: var(--body-font-color);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;

    .fa-file, .fa-folder {
      font-size: 0.8rem;
    }
  }
}

.post-tags {
  display: flex;
  flex-wrap: nowrap;
  gap: $padding-8;
  overflow: hidden;
  white-space: nowrap;

  .tag {
    display: inline-block;
    flex: none;
    background: var(--gray-100);
    color: var(--body-font-color);
    padding: $padding-4 $padding-8;
    font-size: $font-size-14;
    border: 1px solid var(--gray-200);
    border-radius: 4px;
  }
}

.book-footer .post-tags {
  line-height: 1.6;
}

.markdown .category,
.markdown .category-link,
.markdown .tag,
.markdown .tag-link,
.book-footer .tag {

  &[href] {
    color: var(--body-font-color);
    background: var(--gray-200);
    border-radius: $border-radius;
  }

  &[href]:visited {
    color: var(--body-font-color);
  }

  &[href]:hover {
    background: var(--color-page-link);
    color: var(--body-font-color);
    text-decoration: none;
  }
}
```
{{% /tab %}}

{{< /tabs >}}

[게시글 항목 템플릿 추가](#게시글-항목-템플릿-추가) 시에 만들었던 `post-item` 템플릿 중간에
`post-categories` 및 `post-tags` 요소를 칩 형태로 추가했습니다.

![태그와 카테고리를 추가하여 완성된 게시글 항목](https://dl.dropboxusercontent.com/scl/fi/wgpcod2e86fb6kpnq6cnd/hugo-40-post-item-complete.webp?rlkey=tqzyqvdn0j5c4r81cg96ukpuq&raw=1)

태그와 카테고리 페이지와 관련된 모든 구현 과정이 종료되었습니다.

태그와 카테고리 페이지를 구성하는 과정은 각각의 컨텐츠로 나눠도 긴 내용이라서
2개의 글로 나눌지 고민했지만, `taxonomies` 나 게시글 목록 템플릿 등
서로 간에 공통으로 설명해야 할 부분이 많아서 하나의 글로 합치게 되었습니다.

다음 게시글에서는 검색 페이지를 추가하고 기본 검색 기능을 개선하는 과정을 진행하겠습니다.
