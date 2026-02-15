---
title: "Hugo 정적 페이지 경량화 - JS 기반 동적 렌더링 검색 구현"
date: "2026-02-15T14:07:18+09:00"
layout: "post"
description: >
  Hugo 서택스(SeoTax) 테마의 핵심 기능인 동적 검색 페이지 구현 과정을 상세히 다룹니다.
  Taxonomies로 인한 정적 페이지 증가 문제를 해결하고, Fuse.js와 Vanilla JS를 활용한
  고급 검색 필터(카테고리, 태그) 구현 방법을 코드 예제와 함께 설명합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/akc9netlwqqnmvzdwx9fj/seotax-20-cover-search.webp?rlkey=7y56r86rjd3hkfdufvbfu4tq1&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/373ci1c9iozdc8aoi94ka/logo-seotax.webp?rlkey=wsjupt9pphj6gf1fs2zy82fcc&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "서택스 테마", "Fuse.js", "동적 렌더링", "Hugo 검색", "Taxonomies", "정적 페이지 최적화", "Vanilla JS", "카테고리 검색", "태그 검색"]
series: ["Hugo 테마 만들기"]
---
<style>
.screenshot-image { border: 3px solid var(--gray-200); }
pre.mermaid {
  display: flex;
  justify-content: center;
}
</style>

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo 서택스(SeoTax) 테마의 핵심 기능인 동적 검색 페이지 구현 과정을 다룹니다.
Taxonomies로 인한 정적 페이지 증가 문제를 분석하고, Fuse.js와 Vanilla JS를 활용해
단일 검색 페이지에서 카테고리/태그 필터까지 제공하는 방법을 코드와 함께 설명합니다.

- **[경량화 고민](#경량화-왜-고민하게-됐을까)**: Taxonomies로 생성되는 수백 개의 term 페이지 문제와 장기적 영향 분석
- **[term 페이지 대체](#어떻게-term-페이지를-줄일까)**: 정적 페이지를 동적 렌더링으로 대체하는 설계 전략
- **[기존 검색 기능](#기존-검색-페이지의-기능)**: Fuse.js 검색, 전체 글 목록 미리 생성, 헤더 동적 변경 원리
- **[검색/term 페이지 통합](#검색-페이지와-term-페이지-합치기)**: GET 파라미터 파싱부터 5가지 검색 유형별 헤더/필터 구현까지
- **[검색 결과 표시](#검색-결과-표시하기)**: JSON 데이터를 활용한 효율적인 카테고리/태그 필터링과 가상 DOM 렌더링
{{% /hint %}}

Hugo 서택스(SeoTax) 테마를 만들게 된 계기이자 가장 중요하게 생각하는 기능은 검색 입니다.

물론, 많아야 몇백 개 정도의 게시글에서 검색 속도의 향상을 바라진 않습니다.
저는 방문자들이 블로그 내 게시글을 탐색하는 경험에 집중하여,
최대한 다양한 필터를 제공하고 연속적인 검색이 가능하게끔 지원하는
UI/UX의 개선을 주로 다뤘습니다.

## 경량화, 왜 고민하게 됐을까?

Hugo 서택스 테마를 만들기 전에 Hugo Book 테마를 커스터마이징해서 사용한 적이 있습니다.

이 과정에서 Hugo 정적 페이지 생성기의 단점을 느끼고 현재 경량화 시도까지 이르게 된
것을 아래 2개 게시글을 통해 설명드릴 수 있습니다.
이 글에서도 과거의 경험을 뒷받침 자료로 설명드릴 것이기 때문에 반드시 봐야할 필요는 없지만,
혹시라도 설명이 부족할 경우엔 과거 게시글을 참고해주시기 바랍니다.

{{< bookmark "https://minyeamer.github.io/blog/hugo-blog-3/" >}}

{{< bookmark "https://minyeamer.github.io/blog/hugo-blog-4/" >}}

### Taxonomies 문제점

Hugo는 카테고리, 태그와 같은 분류 기능들을 `Taxonomies` 라 정의합니다.

기본적으로 `Taxonomies` 는 활성화되어 있는데,
마크다운 컨텐츠 상단의 프론트매터(front matter)에 `categories` 또는 `tags` 필드를 추가하면
각각의 카테고리 및 태그에 대한 `term` 정적 페이지가 생성됩니다.

문제는 여기에 있습니다. 카테고리가 많아질수록, 태그가 많아질수록 `term` 정적 페이지가 비례해서 생성됩니다.
카테고리가 100개, 태그가 100개라면 정적 페이지는 최소 200개가 만들어지고,
페이지네이션을 통해 여러 페이지로 나눠져 있다면 그 배수만큼 더 늘어날 수 있습니다.

{{% columns %}}
```yaml
---
categories:
- Category A
- Category B
tags:
- Tag A
- Tag B
title: Example
---
```
<--->
```bash
public/
├── categories/
│   ├── Category A/
│   │   ├── index.html
│   │   ├── index.xml
│   │   └── page/
│   │       └── 1/
│   │           └── index.html
│   ├── index.html
│   └── index.xml
├── tags/
│   ├── Tag A/
│   │   ├── index.html
│   │   ├── index.xml
│   │   └── page/
│   │       └── 1/
│   │           └── index.html
│   ├── index.html
│   └── index.xml
└── ...
```
{{% /columns %}}

### `term` 정적 페이지에 대한 걱정

(단기적으로 정적 페이지를 이용하는데는 전혀 문제가 없기 때문에
진지하게 받아들이실 필요는 없습니다. 단순히 제 걱정입니다.)

40개 글을 작성하고 7개의 부모 카테고리, 12개의 자식 카테고리, 237개의 태그를 생성한 시점에서
실제 블로그 문서를 구성하는 `public/` 경로에서 카테고리 페이지는 총 69개 및 2.5MB를 차지하고,
태그 페이지는 594개 및 11.7MB 용량을 차지합니다.

단순 연산으로 페이지 당 `term` 페이지 수와 용량 계산식으로 정의하면 다음과 같습니다:
(카테고리 수 = `c`, 태그 수 = `t`)

```katex
\begin{align}
\mathrm{Count}(c, t) &= 3.6c + 2.2t \\
\mathrm{Size}(c, t)\ &= (131c + 49t) \mathrm{KB}
\end{align}
```

하나의 글은 2개의 카테고리(부모+자식)과 평균 10개의 태그를 가지며,
제 글쓰기 스타일을 참고했을 때 겹치지 않는 태그는 글 하나에 평균 9개 정도라고 볼 수 있습니다.
하지만, 글이 추가된다고 카테고리가 반드시 추가되는건 아니고
페이지네이션에 의해 10개 글마다 1개의 정적 페이지가 추가되는건 큰 영향이 없어 무시합니다.

태그에 의한 페이지 수 및 용량만 따졌을 때,
글 1개 추가 시 18개의 정적 페이지가 새로 생성되고 441KB의 용량이 추가된다고 예상할 수 있습니다.
약 1~2년 뒤에 제 희망으로 글이 400개까지, 현재에서 360개의 게시글이 추가로 작성된다고 가정하면,
6,480개의 정적 페이지와 158MB의 페이지 용량이 추가된다고 볼 수 있습니다.

{{< mermaid >}}
graph LR
    A[현재: 40개 글<br>태그 페이지 수 594개<br>태그 페이지 용량 11.7MB]
    --> B[미래: 400개 글<br>태그 페이지 수 7,074개<br>태그 페이지 용량 169.7MB]
{{< /mermaid >}}

테마에서 공통된 레이아웃 스타일 하나만 변경해도 `public/` 경로 내 대부분의 파일이 변경되며,
이를 호스팅 중인 블로그에 반영하기 위해 Github에 올릴 때마다 속도가 느려질 것을 생각하면
동적 렌더링을 통해 정적 페이지를 절약해서 나쁠건 없다고 생각합니다.

그리고, 블로그를 구글 검색 엔진 및 GA4에 등록했을 때도
크롤러가 카테고리 및 태그 페이지 하나하나를 전부 수집해 통계를 산출하는데,
이런 페이지에서 발생하는 통계가 몇천 개의 정적 페이지로 쪼개져서 보여지는 것
또한 대단히 불편할 것으로 생각됩니다.

## 어떻게 `term` 페이지를 줄일까?

그렇다면, `term` 페이지 수를 줄이기 위한 방법은 무엇이 있을까요?

프로그래밍에서 반복되는 기능을 하나의 함수로 만들듯
`term` 페이지에서 공통되는 요소를 하나의 페이지 레이아웃으로 만들고
일부 텍스트만 동적으로 변경하면 됩니다.

### `term` 페이지의 공통된 요소

`Taxonomies` 에 대한 `term` 정적 페이지는 아래 이미지와 같은 레이아웃을 가집니다.
상단에 어떤 태그 페이지인지 알리는 제목과 관련 게시글 수, 그리고 게시글 목록을 동적으로 변경하고
나머지들이 공통된 요소라고 볼 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/7phkjfv89kr8coyrjtde8/seotax-21-term-example.webp?rlkey=0q2l90milz38o74stx4q2q7b3&raw=1"
  alt="term 페이지 예시 - 'Hugo' 태그"
  caption="term 페이지 - 'Hugo' 태그"
  class="screenshot-image" >}}

그렇다면, `/tag/` 라는 단일 경로로 연결되는 레이아웃을 만들고,
`/tag/?t=Hugo` 처럼 GET 요청 시 태그 값을 파라미터로 전달하며
일부 요소만 동적으로 변경하면 어떨까요?

그것도 괜찮은 방법이지만, 저는 한번 더 개선해보려 합니다.

### 검색 페이지를 활용하는 방법

다음은 검색 결과를 표시하는 검색 페이지입니다.   
(Book 테마를 커스터마이징하여 사용하던 시절의 UI라서 검색창은 없습니다.)

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/kzu3pb3ho5wbyp96pmy92/seotax-22-search-example.webp?rlkey=c0vhbmjtnw0bzh9qrrtxjcoze&raw=1"
  alt="검색 페이지 예시 - 'Hugo' 검색 결과"
  caption="검색 페이지 - 'Hugo' 검색 결과"
  class="screenshot-image" >}}

`term` 페이지와 검색 페이지를 비교해보면 제목과 게시글 수를 포함한 `헤더` 와,
게시글 목록을 포함한 `본문` 영역으로 구분되었다는 공통점을 발견할 수 있습니다.
물론, 이 공통점은 `term` 페이지와 검색 페이지를 설계할 때
CSS 스타일을 공유하기 위해서 의도적으로 맞춘 것입니다.

두 페이지 레이아웃이 공통된 구조를 가졌다면,
`/search/` 라는 경로로 연결되는 레이아웃 하나만 유지하고
`?query=테마&tags=블로그` 같이 검색어와 태그를 동시에 파라미터로 전달하면
정적 페이지를 더 줄일 수 있습니다.

그리고, 이렇게 구성했을 때의 또다른 장점은 더 세분화된 검색이 가능해진다는 것입니다.
기존에는 검색어만 활용할 수 있었지만, 태그 그리고 카테고리를 추가로 활용하여
더 세분화된 검색 결과를 도출할 수 있습니다. 현재 40개 수준의 게시글에서는
활용도가 낮을 수 있지만 앞으로 게시글이 몇백 개까지 추가된다고 예상한다면
독자들이 블로그를 탐색하는데 큰 도움을 줄 것입니다.

## 기존 검색 페이지의 기능

기존에 구현했던 검색 페이지의 기능을 간략하게 설명할건데,
자세한 구현 과정 및 JS 코드를 보고 싶으시다면 아래 게시글을 참고해주세요.

{{< bookmark "https://minyeamer.github.io/blog/hugo-blog-4/" >}}

기존의 검색 페이지를 구현하는데 활용한 핵심기술은 다음 3가지 입니다:

{{% hint %}}
1. `Fuse.js` 를 활용하여 글 제목과 내용에 기반해 가볍고 강력한 유사 검색 구현
2. Hugo 템플릿으로 전체 게시글 목록을 미리 만들어두고 검색 결과에 해당하는 항목만 사용자에게 표시
3. 헤더의 `"${검색어}" 검색 결과 ${개수}` 라벨 값을 동적으로 변경
{{% /hint %}}

### `Fuse.js` 검색

1번 기능 `Fuse.js` 와 관련하여 간략하게 설명하자면,
Hugo 렌더링 시에 모든 글 제목과 내용 배열을 하나의 JSON 파일로 만들어두고
최초로 검색이 실행되면 GET 요청으로 JSON 파일을 가져옵니다.
이 데이터를 `Fuse.js` 를 생성하는 `new Fuse(data, options)` 에 전달하여
`Fuse` 인스턴스를 생성합니다. `Fuse` 인스턴스의 `search` 메서드에 검색어를 전달하면
유사한 글이 배열로 반환됩니다.

저는 `window.siteSearch.index` 라는 `Fuse` 전역 객체를 만들어뒀고,
사용자의 검색 요청으로 `search()` 메서드가 호출되면
아래와 같이 `score` 라는 0 부터 1 사이의 범위를 가지는 점수를 포함한 검색 결과를 반환합니다.
0에 가까울수록 유사도가 높다는 것을 의미하며, 검색 결과는 점수의 오름차순으로 정렬되어 있습니다.

```js
> window.siteSearch.index.search('Hugo');
0: {item: {…}, refIndex: 4, score: 0.3243396173493493}
1: {item: {…}, refIndex: 6, score: 0.3599979270433567}
2: {item: {…}, refIndex: 5, score: 0.3607447338641917}
3: {item: {…}, refIndex: 1, score: 0.3927353556467251}
4: {item: {…}, refIndex: 2, score: 0.3935500754557775}
5: {item: {…}, refIndex: 3, score: 0.3935500754557775}
6: {item: {…}, refIndex: 0, score: 0.4453485062698579}
7: {item: {…}, refIndex: 33, score: 0.9774622640495892}
8: {item: {…}, refIndex: 32, score: 0.9876430227771064}
9: {item: {…}, refIndex: 34, score: 0.9896918638691029}
```

검색 결과에서 `item` 은 `Fuse` 객체를 만들 때 전달한 데이터로,
`id`, `href`, `title`, `content` 항목으로 구성되어 있습니다:
- `id` 는 작성일 내림차순으로 정렬된 0부터 시작하는 순번입니다.   
  이어지는 2번 기능 전체 글 목록으로부터 검색 결과에 해당하는 글 목록만 추출할 때 키로 활용합니다.
- `href` 는 이름 그대로 글 경로고, 글에 대한 바로가기 링크를 만들어야 할 때 `href` 속성값으로 사용됩니다.
- `title`, `content` 는 검색에 사용되는 글 제목과 내용입니다. 검색 결과 미리보기를 생성할 때도 사용됩니다.

```js
> window.siteSearch.index.search('Hugo');
(10) [{…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}]
0:
  item:
    id: 4
    href: "/blog/hugo-blog-3/"
    title: "Hugo 분류(Taxonomies) 커스터마이징 - 태그/카테고리 템플릿 구현"
    content: " Hugo 블로그 만들기 1. Hugo 블로그 만들기 - Git Submodule로 구성..."
  refIndex: 4
  score: 0.3243396173493493
```

### 전체 글 목록 미리 생성

2번 기능, 전체 글 목록을 설명하기 위해 검색 페이지를 구성하는 HTML 코드를 참고해 봅니다.

```html
{{ define "content" }}
<article class="content-wrap markdown">
  <div class="list-header" id="list-header"></div>
  <div class="taxonomy-section hidden" id="taxonomy-section"></div>

  <div class="search-data hidden" id="search-data">
    {{- range $index, $page := partialCached "pages/search" . "search" -}}
      <div class="search-item" data-id="{{ $index }}">
        {{ partial "post-item.html" . }}
      </div>
    {{- end -}}
  </div>

  <div class="search-no-results hidden" id="search-no-results">
    <p data-i18n-id="search.results.empty" data-i18n-text>
      {{- i18n "search.results.empty" | default "No results found." -}}
    </p>
  </div>

  <div class="post-list hidden" id="search-results"></div>

  <div id="pagination-anchor"></div>
  <nav class="pagination hidden" id="pagination"></nav>
</article>
{{ end }}
```

HTML 중간에 `#search-data` 영역을 보면,
`pages/search` 템플릿을 호출해 검색 대상인 모든 `Page` 객체를 가져오고
각각의 객체를 `post-item` 템플릿에 전달해 아래 이미지와 같은 `.post-item` 요소를 만들어냅니다.
`.post-item` 요소들을 담고 있는 `#search-data` 영역은
`display: hidden;` 스타일이 적용되어 사용자에게 보이지 않으므로
HTML 코드 내에 전체 글 목록이 숨겨져 있게 됩니다.

검색 결과를 표시할 때는 전체 글 목록에서 `id` 를 인덱스로 참조하여
`.post-item` 요소를 특정하고 `.post-list` 영역으로 복사합니다.
(글 목록 복사 과정에서 가상 DOM을 활용하여 실제 DOM의 변경 비용은 최소화했습니다.)
`.post-list` 영역에서 `hidden` 클래스를 떼면 최종적으로
검색 결과가 사용자에게 보여지는 원리입니다.

{{< tabs "post-item" >}}

{{% tab "View" %}}
![post-item 템플릿](https://dl.dropboxusercontent.com/scl/fi/r1x5j52f7p1hrtg9lk2rx/seotax-23-post-item.webp?rlkey=dfquj57ra11sggz71qp18vl5t&dl=0)
{{% /tab %}}

{{% tab "HTML" %}}
```html
<article class="post-item">
  <div class="post-meta">
    <time datetime="2025-12-14">2025년 12월 14일</time>
    <div class="post-categories">
      <a href="/categories/frontend/" class="category"><i class="icon-folder"></i>Frontend</a>
      <a href="/categories/frontend/blog/" class="category"><i class="icon-file"></i> Blog</a>
    </div>
  </div>
  <div class="post-content-area has-cover">
    <div class="post-cover-mobile">
      <img src="https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&amp;dl=0" alt="Cover Image" class="post-cover-mobile-img">
    </div>
    <div class="post-text-area">
      <h2 class="post-title"><a href="/blog/hugo-blog-4/">Hugo 블로그 만들기 (4) - 검색 기능 개선 및 검색 페이지 구현 (Fuse.js)</a></h2>
      <div class="post-summary">Hugo Book 테마에서 Fuse.js 기반 검색 인덱스를 분석하고 검색 UI를 개선하는 과정을 소개합니다. 검색 페이지를 구현하면서 검색 성능을 최적화하고 템플릿 일관성을 보장하기 위한 방식을 알아봅니다.</div>
      <div class="post-tags">
        <a href="/tags/hugo/" class="tag">#Hugo</a>
        <a href="/tags/fusejs/" class="tag">#Fusejs</a>
        <a href="/tags/%EA%B2%80%EC%83%89-%EC%9D%B8%EB%8D%B1%EC%8A%A4/" class="tag">#검색 인덱스</a>
        <a href="/tags/%EA%B2%80%EC%83%89-%ED%8E%98%EC%9D%B4%EC%A7%80/" class="tag">#검색 페이지</a>
        <a href="/tags/hugo-%EA%B2%80%EC%83%89/" class="tag">#Hugo 검색</a>
      </div>
    </div>
    <div class="post-cover">
      <img src="https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&amp;dl=0" alt="Cover Image" class="post-cover-img">
    </div>
  </div>
</article>
```
{{% /tab %}}

{{< /tabs >}}

`.post-item` 요소를 JavaScript로 동적 생성하지 않고 이렇게 HTML 코드 내에 숨겨진 요소로
만들어둔 이유는, `post-item` 템플릿을 이미 다른 곳에서도 사용하고 있었기 때문에
유지보수 편의성을 위해 재활용한 것입니다.
장기적으로 작성글이 계속 늘어날 것을 생각하면 언젠가는 동적 생성하는 방식으로 바꿀 수도 있겠습니다.

### 헤더 라벨 동적 변경

3번 기능, 검색 페이지 헤더 영역의 라벨을 동적으로 변경하는건 앞선 기능들 대비 단순한 편입니다.
위 HTML 코드 내에 비어있는 `#list-header` 및 `#taxonomy-section` 영역이 동적 변경 대상입니다.

기존 검색 페이지에서는 공통되는 텍스트를 포함한 라벨 요소가 이 영역 안에 미리 만들어져 있고,
동적으로 변경할 대상을 `id` 로 특정해 HTML을 대체했습니다.

```js
displayElement.innerHTML = `"${query}" 검색 결과 <em class="list-count" id="search-count">0</em>`;
...
document.getElementById('search-count').textContent = matchedItems.length;
```

## 검색 페이지와 `term` 페이지 합치기

기존 검색 페이지의 원리와 구성 요소를 파악했으니 본격적으로
`term` 페이지를 검색 페이지와 합쳐 보겠습니다.

완성된 검색 페이지는 Github에 올린 JS 파일을 확인하시면 됩니다.

{{< bookmark "https://github.com/minyeamer/hugo-seotax/blob/main/assets/js/search/list.js" >}}

### GET 파라미터 파싱

검색 페이지는 `/search/` 라는 단일 URL로 접근하며,
`query` 라는 검색어 파라미터를 입력받아 검색 결과를 생성했습니다.
검색 페이지에서 `term` 페이지의 기능도 병행하기 위해서는
카테고리와 태그를 추가로 입력으로 받을 수 있어야 합니다.

```js
const params = new URLSearchParams(window.location.search);
const state = {
  query: params.get('query') || '',
  category1: params.get('category1') || '',
  category2: params.get('category2') || '',
  tags: (params.get('tags')
    ? [...new Set(params.get('tags').split(',').map(tag => tag.trim()).filter(tag => tag))]
    : []),
  tagsOp: params.get('tagsOp') || 'and',
  page: Math.max(1, parseInt(params.get('page')) || 1),
  pageSize: Math.max(1, parseInt(params.get('pageSize')) || 10)
};
```

검색 페이지 요청 시 Taxomomies를 추가적인 파라미터로 받아서
`state` 라는 이름의 상태 객체로 저장합니다.

`state` 객체를 만들 때 검색어나 카테고리는 단일 값이기 때문에 그대로 받지만,
태그는 목록으로 받기 때문에 전달받은 값을 구분자 `,` 로 나눠서 배열로 저장합니다.
그리고, 목록으로 전달된 태그를 AND 조건으로 필터할지, OR 조건으로 필터할지 여부를
결정하는 `tagsOp` 파라미터를 추가로 입력받습니다.

### 검색 유형 파악하기

상태 객체 `state` 가 만들어졌다면 이 객체의 값을 참고하여
어떠한 유형의 검색 페이지를 만들면 되는지 미리 파악합니다.

```js
function getSearchType(state) {
  const hasQuery = (state.query.length > 0);
  const hasCategory1 = (state.category1.length > 0);
  const hasCategory2 = (state.category2.length > 0);
  const hasTags = (state.tags.length > 0);

  if (hasQuery) {
    if (hasCategory1 | hasTags) return 'combined';
    else return 'search';
  } else {
    if (hasCategory1) return hasCategory2 ? 'category2' : 'category1';
    else if (hasTags) return 'tags';
    else return 'search';
  }
}

const searchType = getSearchType(state);
```

검색 페이지 유형에는 `search`, `category1`, `category2`, `tags`, `combined` 5가지가 있습니다.
- `search`: 검색어에 대한 검색 결과를 표시하는 기존 검색 페이지
- `category1`: 부모 카테고리 필터만 제공되는 경우 전용 헤더를 포함한 `term` 페이지
- `category2`: 부모와 자식 카테고리 필터가 제공되는 경우 전용 헤더를 포함한 `term` 페이지
- `tags`: 태그 필터가 제공되는 경우 전용 헤더를 포함한 `term` 페이지
- `combined`: 검색어, 카테고리, 태그 중 2가지 이상의 복합적인 필터가 제공되는 경우의 결과 페이지

검색 유형 `searchType` 은 검색 페이지의 헤더를 구성할 때와
검색 결과(페이지네이션 포함)를 구성하는 두 가지 경우에 사용됩니다.
이 조건문은 다음의 `switch` 구문으로 구성됩니다.

{{< tabs "search-type" >}}

{{% tab "조건 하나만 보기" %}}
```js
switch (searchType) {

  case 'search':
    Promise.all([
      window.siteSearch.initIndex(),
      window.siteSearch.initCategories(),
      window.siteSearch.initTags()
    ]).then(() => {
      const ids = searchQuery(state, true);
      displayResults(ids, state);
    });
    break;
  ...
}
```
{{% /tab %}}

{{% tab "전체 조건문 보기" %}}
```js
switch (searchType) {

  case 'search':
    Promise.all([
      window.siteSearch.initIndex(),
      window.siteSearch.initCategories(),
      window.siteSearch.initTags()
    ]).then(() => {
      const ids = searchQuery(state, true);
      displayResults(ids, state);
    });
    break;

  case 'category1':
    window.siteSearch.initCategories().then(() => {
      const ids = searchCategory1(state, true);
      displayResults(ids, state);
    });
    break;

  case 'category2':
    window.siteSearch.initCategories().then(() => {
      const ids = searchCategory2(state, true);
      displayResults(ids, state);
    });
    break;

  case 'tags':
    window.siteSearch.initTags().then(() => {
      const ids = searchTags(state, true);
      displayResults(ids, state);
    });
    break;

  case 'combined':
    Promise.all([
      window.siteSearch.initIndex(),
      window.siteSearch.initCategories(),
      window.siteSearch.initTags()
    ]).then(() => {
      const ids = searchCombined(state, true);
      displayResults(ids, state);
    });
    break;

  default:
    Promise.all([
      window.siteSearch.initIndex(),
      window.siteSearch.initCategories(),
      window.siteSearch.initTags()
    ]).then(() => {
      clearHeader();
      createListHeader({i18nId: 'search.results.title', icon: 'icon-file-lines'}, 0, '');
      displayResults(new Set());
    });
    break;
}
```
{{% /tab %}}

{{< /tabs >}}
각 함수에 대해서는 이어지는 문단에서 설명드릴 것이지만, 간단하게 다음 표로 정리할 수 있습니다.

|함수|설명|
|---|---|
|`initIndex()`|검색어를 통해 검색 결과를 도출하는데 필요한 `Fuse.js` 인덱스를 초기화 (전역 함수)|
|`initCategories()`|카테고리별 관련 게시글 번호가 배열로 정리된 데이터를 초기화 (전역 함수)|
|`initTags()`|태그별 관련 게시글 번호가 배열로 정리된 데이터를 초기화 (전역 함수)|
|`searchQuery(state, appendHeader)`|검색 결과를 구하고, 동시에 헤더를 생성하여 DOM에 적용|
|`displayResults(ids, state)`|검색 결과에 해당되는 글 목록을 추출하여 DOM에 표시하고 페이지네이션을 계산|

### 검색 페이지 헤더 동적 생성

`search` 유형의 기본 검색 페이지 헤더는 아래 이미지와 같이 구성됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/llja2m7ni7anbpaqvzk6b/seotax-24-search-header.webp?rlkey=y7izyn4c4xucm5thv72mv8coz&raw=1"
  alt="검색 페이지 헤더"
  class="screenshot-image" >}}

헤더는 위에서부터 순서대로 제목, 라벨, 검색 필터 영역으로 구성됩니다.

이 중에서 제목은 검색 유형에 따라 다음과 같은 형식으로 만들어집니다.
- `category1` 유형에서는 <code><i class="icon-folder"></i> 부모 카테고리</code>
- `category2` 유형에서는 <code><i class="icon-file"></i> 자식 카테고리</code>
- `tags` 유형 중 단일 태그 검색 시에는 <code><i class="icon-tag"></i> 태그</code>
- 그 외의 경우에는 <code><i class="icon-file-text"></i> 검색 결과</code>

그리고, 제목 아래에 검색 결과 수를 표시하는 라벨은 다음 두 가지 경우의 수가 있습니다.
- 검색어가 있는 경우 `"검색어" 검색 결과 %d`
- 검색어가 없는 경우 `전체 글 %d`

이러한 논리를 가지고 생성한 함수 `createListHeader()` 는
각각의 검색 유형에 대해 아래처럼 호출할 수 있습니다.
함수의 본문도 탭을 클릭하면 볼 수 있지만, 다국어 번역 등 이번 주제와는 무관한
코드가 많아서 코드에 대한 설명은 생략합니다.

{{< tabs "list-header" >}}

{{% tab "헤더 생성 함수 호출" %}}
```js
function createListHeader(titleInfo, pageCount, query = '') { ... }

// case 'search' + 'combined':
createListHeader({i18nId: 'search.results.title', icon: 'icon-file-text'}, searchPosts.size, state.query);
// case 'category1':
createListHeader({text: category1Name, icon: 'icon-folder'}, category1Posts.length);
// case 'category2':
createListHeader({text: category2Name, icon: 'icon-file'}, category2Posts.length);
// case 'tags':
createListHeader({text: tagNames[0], icon: 'icon-tag'}, tagPosts.size);
```
{{% /tab %}}

{{% tab "헤더 생성 함수 본문" %}}
```js
function createListHeader(titleInfo, pageCount, query = '') {
  const fragment = document.createDocumentFragment();

  const title = createElement('h1');
  if (titleInfo.icon) {
    title.appendChild(createElement('i', {className: `${titleInfo.icon}`}))
    title.appendChild(document.createTextNode(' '));
  }
  if (titleInfo.i18nId) {
    title.appendChild(createElement('span', {
      text: translate(titleInfo.i18nId),
      dataset: {i18nId: titleInfo.i18nId, i18nText: ''}
    }));
  } else {
    title.appendChild(createElement('span', {text: titleInfo.text || ''}));
  }
  fragment.appendChild(title);

  const subtitleI18nId = query ? 'search.count.label' : 'list.count.label';
  const subtitleI18nParams = query ? `{"%q": "${query}", "%s": "$.list-count"}` : '{"%s": "$.list-count"}';
  const countLabel = translate(subtitleI18nId);
  const listCount = `<em class="list-count">${pageCount}</em>`;
  fragment.appendChild(createElement('p', {
    html: (query ? countLabel.replace('%q', query) : countLabel).replace('%s', listCount),
    dataset: {i18nId: subtitleI18nId, i18nText: subtitleI18nParams}
  }));

  listHeader.appendChild(fragment);
}
```
{{% /tab %}}

{{< /tabs >}}

각각의 검색 유형별 검색 페이지를 요청해보면 아래 탭으로 구분된 이미지처럼
헤더의 일부분이 동적으로 변경됨을 볼 수 있습니다.

{{< tabs "search-header" >}}

{{< tab "부모 카테고리" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/p9wc48zxgnq53nsk2r32v/seotax-25-search-header-category1.webp?rlkey=5phc0zuj4u1tfmkmezvm4eyg6&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< tab "자식 카테고리" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/2ln3dh6jajeqet7jq9e0k/seotax-26-search-header-category2.webp?rlkey=wd5n5g33g8w47e05an3j00ai4&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< tab "태그 1개" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/6j1d8rjgjdbek7nj05gas/seotax-27-search-header-tag.webp?rlkey=d3nbyesliw62eca8054gn643z&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< tab "태그 여러 개" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/c7jypqw0mero5h7n1wfzt/seotax-28-search-header-tags.webp?rlkey=fnjazs5n6026dktvbuxchwfei&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< /tabs >}}

### 검색 필터 동적 생성

위에 탭으로 구분된 이미지를 보면 헤더의 제목과 라벨 아래에 공통적으로 검색 필터 영역이
표시되는 것을 알 수 있습니다.

검색 필터 영역은 `createListHeader()` 함수로 헤더의 제목과 라벨을 생성한 후
아래 `createSearchFilter()` 함수를 호출하여 생성합니다.
검색 필터 영역은 2개 행으로 나눠져 있는데, 검색어를 입력하는 긴 검색창이 첫 번째 행에,
나머지 카테고리 및 태그를 선택하는 드롭박스 필터들이 두 번째 행에 배치됩니다.
두 번째 행, 고급 필터는 토글 버튼을 클릭해 숨기거나 펼칠 수 있습니다.

`createListHeader()` 함수를 간략하게 다음과 같이 표현할 수 있습니다.

```js
function createSearchFilter(ids, isExpanded=null) {
  const fragment = document.createDocumentFragment();
  const searchFilter = createElement('div', {className: 'search-filter'});

  const queryFilter = createQueryFilter(state.query);
  ...
  const taxonomiesRow = createElement('div', {className: 'search-taxonomies-row'});
  ...
  const categoriesFilter = createElement('div', {className: 'search-categories-filter'});
  ...
  const tagsFilter = createElement('div', {className: 'search-tags-filter'});
  ...

  setupQueryFilterEvents(false);
  setupFilterToggle(isExpanded);
  setupTaxonomyFilterEvents(ids);
  initFiltersFromState();
}
```

검색 필터 영역을 생성한 후 밑에 4개의 함수는 검색 필터에 대한 편의성을 제공하거나,
검색 결과에 맞춰서 드롭다운 필터의 내용을 동적으로 변경하는 기능을 합니다.
함수 본문은 길어서 Github 저장소를 참고해주시고, 주석으로 설명을 대체합니다.

```js
function setupQueryFilterEvents(preserveTaxonomy = false) {
  // 검색창에서 엔터키를 누르거나 검색 버튼을 클릭하면 검색이 실행되는 이벤트 리스너를 등록합니다.
}
function setupFilterToggle(isExpanded=null) {
  // 고급 필터의 기본 펼침/접힘 상태를 설정합니다.
}
function setupTaxonomyFilterEvents(ids) {
  // 고급 필터 영역에서 입력창을 조작하거나 드롭다운 항목을 클릭할 때 검색이 실행되는 이벤트 리스너를 등록합니다.
}
function initFiltersFromState() {
  // 검색 페이지로 이동할 때 전달된 파라미터를 조회하여 필터 항목을 선택된 상태로 초기화합니다.
}
```

### Taxonomies 영역 동적 생성

다시 위에서 봤던 이미지를 가져오겠습니다.
헤더 영역에서 구분선을 긋고 그 아래 있는 영역이 Taxonomies 영역입니다.

기본 검색 페이지에서는 이 영역이 없지만,
`term` 페이지와 검색 페이지를 합치면서 이 영역도 그대로 가져왔습니다.

{{< tabs "search-header2" >}}

{{< tab "부모 카테고리" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/p9wc48zxgnq53nsk2r32v/seotax-25-search-header-category1.webp?rlkey=5phc0zuj4u1tfmkmezvm4eyg6&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< tab "자식 카테고리" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/2ln3dh6jajeqet7jq9e0k/seotax-26-search-header-category2.webp?rlkey=wd5n5g33g8w47e05an3j00ai4&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< tab "태그 여러 개" >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/c7jypqw0mero5h7n1wfzt/seotax-28-search-header-tags.webp?rlkey=fnjazs5n6026dktvbuxchwfei&raw=1"
  alt="검색 페이지 헤더 - 부모 카테고리"
  class="screenshot-image" >}}
{{< /tab >}}

{{< /tabs >}}

Taxonomies 영역의 종류는 3가지로,
1. `부모 카테고리` 검색 유형에서는 하위의 자식 카테고리 목록을 칩 형태로 보여줍니다.
2. `자식 카테고리` 검색 유형에서는 상위 부모 카테고리 링크 하나를 칩 형태로 보여줍니다.
3. 태그가 1개일 때는 이 영역이 없지만, `태그가 여러 개` 라면 단일 태그 검색 유형으로 이동할 수 있는 태그 칩 목록을 보여줍니다.

Taxonomies 영역을 생성하는 `createTaxonomySection()` 는
제목 및 칩 목록을 생성하는 동작을 합니다. 칩 요소를 생성하는 `createTaxonomyChip()`
함수에서는 `.taxonomy-chip` 클래스가 부여된 `div` 요소를 만들어 반환합니다.

이 칩 요소들은 `display: flex;` 스타일이 적용된 `.taxonomy-chips` 영역에 추가되어,
여러 개의 칩이 있다면 가로로 나열됩니다.

```js
function createTaxonomySection(i18nId, taxonomies) {
  ...
  const label = createElement('h2', {
    text: translate(i18nId),
    dataset: {i18nId: i18nId, i18nText: ''}
  });
  const chips = createElement('div', {className: 'taxonomy-chips'});
  taxonomies.forEach(taxonomy => {
    chips.appendChild(createTaxonomyChip(taxonomy));
  });
  ...
}
```

### 검색 결과 표시하기

검색 결과 표시 방식으로는 기존 검색 페이지에서 [전체 글 목록](#전체-글-목록-미리-생성)을
미리 보이지 않는 영역에 생성해두고, 결과에 해당하는 글들만 골라서 사용자에게 보이는 영역으로
옮기는 방식을 그대로 사용했습니다.

```
[실제 DOM]                         [메모리]                             [실제 DOM]
┌─────────────────┐              ┌───────────────────┐              ┌──────────────────┐
│ #search-data    │              │  DocumentFragment │              │  #search-results │
│ ├─ post-item 1  │              │  ├─ post-item 1   │              │  ├─ post-item 1  │
│ ├─ post-item 2  │  ─────────►  │  ├─ post-item 3   │  ─────────►  │  ├─ post-item 3  │
│ ├─ post-item 3  │  appendChild │  └─ post-item 5   │  appendChild │  └─ post-item 5  │
│ ├─ post-item 4  │              └───────────────────┘              └──────────────────┘
│ └─ post-item 5  │
└─────────────────┘
```

저에게는 가장 편리한 검색 결과 표시 방식이지만, 카테고리 및 태그 검색을 추가하면서
복합적인 검색을 어떻게 구현할지 고민이 있었습니다.

`.post-item` 요소에서 카테고리 및 태그 속성을 추출해서 파라미터 값과 비교하는 방식도 있을 수 있겠지만,
그러면 매 검색 시마다 모든 글 목록을 하나씩 파싱하면서 검색 조건을 확인해야 하고,
태그는 상위 5개 태그만 미리보기로 추가하기 때문에 정확한 검색을 수행할 수도 없습니다.

제가 생각한 해결책은 각각의 카테고리 및 태그가 어떤 글 `id` 와 연관되는지 배열로 저장해놓는 것입니다.

기존 검색 페이지에서 검색어를 기반으로 [`Fuse.js` 검색](#fusejs-검색)을 수행할 때
글 정보에 `id` 라는 항목이 있었던 것을 아실 것입니다. `id` 는 글을 등록일 기준으로
내림차순 정렬했을 때 순번입니다. `.post-item` 요소도 마찬가지로 등록일 내림차순 정렬되어 있어
따로 속성 값을 파싱할 필요없이 `id` 를 가지고 글 목록 배열에 인덱싱 조회하는 단순한 연산으로
검색 결과를 추출할 수 있습니다.

카테고리와 태그도 다음과 같이 소문자 변환된 카테고리 값을 맵에서 키로 조회했을 때
연관 글 `id` 배열을 반환할 수 있도록 JSON 데이터를 만들었습니다.
카테고리 또는 태그 검색 수행 시 이 데이터를 HTTP 요청해서 가져오거나, 전역 객체에서
참조하여 검색 결과와 카테고리/태그의 원본 값을 조회할 수 있습니다.

이 방식의 장점은, 우선 검색 시 대소문자를 구분하지 않습니다.
키는 모두 소문자로 되어 있으므로 사용자의 파라미터로 전부 소문자로 변환됩니다.
하지만, 그러면 원본 카테고리 값을 알기 어려워지는데, 이를 위해 `name` 이라는 키값을 남겨뒀습니다.

두 번째 장점은 검색 수행을 위한 비용이 매우 저렴합니다.
일반적으로 부모-자식 카테고리 검색을 수행하려 한다면 모든 글 목록에서
부모 카테고리와 자식 카테고리라는 두 가지 속성 값을 비교해야 하지만,
미리 만들어진 JSON 데이터를 활용하면 2번의 키 조회만으로 검색 결과를 얻을 수 있습니다.

{{< tabs "categories.json" >}}

{{% tab "카테고리 검색 결과" %}}
```js
> window.siteSearch.categories["data engineering"];
{A: {…}, apache_airflow: {…}, apache_spark: {…}, crawling: {…}}
A:
  ids: (19) [9, 12, 13, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
  name: "Data Engineering"
apache_airflow:
  ids: (7) [21, 22, 23, 24, 25, 26, 27]
  name: "Apache Airflow"
apache_spark:
  ids: (8) [12, 13, 15, 17, 18, 19, 20, 9]
  name: "Apache Spark"
crawling:
  ids: (4) [28, 29, 30, 31]
  name: "Crawling"
```
{{% /tab %}}

{{% tab "categories.json 구현" %}}
```json
{{- $json := dict -}}
{{- $pages := partialCached "pages/search" . "search" -}}
{{- $treeL1 := partialCached "categories/tree" . "categories" -}}
{{- /* 부모-자식 카테고리 맵 생성 */ -}}
{{- range $key1 := (partial "keys" $treeL1) -}}
  {{- $ids1 := slice -}}
  {{- $pagesL1 := dict -}}
  {{- range $id1, $page1 := $pages -}}
    {{- if eq (partial "categories/level1" $page1.Params.categories | default "") $key1 -}}
      {{- $ids1 = $ids1 | append $id1 -}}
      {{- $pagesL1 = $pagesL1 | merge (dict (string $id1) $page1) -}}
    {{- end -}}
  {{- end -}}
  {{- /* 부모 카테고리를 맵에 추가 */ -}}
  {{- $category1 := dict "A" (dict "name" $key1 "ids" $ids1) -}}
  {{- /* 자식 카테고리 맵 생성 */ -}}
  {{- $treeL2 := index $treeL1 $key1 -}}
  {{- if $treeL2 -}}
    {{- $category2 := dict -}}
    {{- range $key2 := (partial "keys" $treeL2) -}}
      {{- $ids2 := slice -}}
      {{- range $id2, $page2 := $pagesL1 -}}
        {{- if eq (partial "categories/level2" $page2.Params.categories | default "") $key2 -}}
          {{- $ids2 = $ids2 | append (int $id2) -}}
        {{- end -}}
      {{- end -}}
      {{- $category2 = $category2 | merge (dict (lower $key2) (dict "name" $key2 "ids" $ids2)) -}}
    {{- end -}}
    {{- /* 자식 카테고리 맵을 부모-자식 카테고리 맵에 병합 */ -}}
    {{- $category1 = $category1 | merge $category2 -}}
  {{- end -}}
  {{- /* 부모-자식 카테고리 맵을 전체 카테고리 맵에 병합 */ -}}
  {{- $json = $json | merge (dict (lower $key1) $category1) -}}
{{- end -}}
{{- /* 전체 카테고리 맵을 JSON 형식으로 반환(생성) */ -}}
{{- $json | jsonify -}}
```
{{% /tab %}}

{{< /tabs >}}

카테고리 검색의 경우 자식 카테고리 없이 부모 카테고리에 연관된 글 목록만 검색하는 경우도 있어서
아래 태그와 구조가 다릅니다. 부모 카테고리 하위에 자식 카테고리 키값 말고도 `A` 라는 키값이 하나 더 있습니다.
이것이 부모 카테고리 자체에 대한 검색 결과 및 원본 카테고리명입니다.

{{< tabs "tags.json" >}}

{{% tab "태그 검색 결과" %}}
```js
> window.siteSearch.tags["hugo"];
{ids: Array(10), name: 'Hugo'}
ids: (10) [0, 1, 2, 3, 4, 5, 6, 32, 33, 34]
name: "Hugo"
```
{{% /tab %}}

{{% tab "tags.json 구현" %}}
```json
{{- $json := dict -}}
{{- $pages := partialCached "pages/search" . "search" -}}
{{- /* 태그 목록 가져오기 */ -}}
{{- $tags := slice -}}
{{- range $page := $pages -}}
  {{- range $page.Params.tags -}}
    {{- $tags = $tags | append . -}}
  {{- end -}}
{{- end -}}
{{- /* 전체 태그 맵 생성 */ -}}
{{- range $t := sort (uniq $tags) -}}
  {{- $ids := slice -}}
  {{- range $id, $page := $pages -}}
    {{- if in $page.Params.tags $t -}}
      {{- $ids = $ids | append $id -}}
    {{- end -}}
  {{- end -}}
  {{- $tag := dict "name" $t "ids" $ids -}}
  {{- $json = $json | merge (dict (lower $t) $tag) -}}
{{- end -}}
{{- /* 전체 태그 맵을 JSON 형식으로 반환(생성) */ -}}
{{- $json | jsonify -}}
```
{{% /tab %}}

{{< /tabs >}}

[검색 유형](#검색-유형-파악하기)에 따라 `switch` 조건문을 거쳐 호출되는
함수 `searchQuery()` 등에서는 위 데이터에 따라 검색 결과 `id` 의 배열을 도출하고
검색 페이지의 헤더를 생성합니다.
`id` 의 배열은 `ids` 로 반환됩니다. `ids` 는 `displayResults()` 함수에
전달되어 검색 결과를 표시하는데 활용됩니다.

```js
switch (searchType) {
  case 'search':
    const ids = searchQuery(state, true);
  case 'category1':
    const ids = searchCategory1(state, true);
  case 'category2':
    const ids = searchCategory2(state, true);
  case 'tags':
    const ids = searchTags(state, true);
  case 'combined':
    const ids = searchCombined(state, true);
  displayResults(ids, state);
}
```

`displayResults()` 함수의 동작은 이 문단의 초반에서 그린 [그래프](#검색-결과-표시하기)를
그대로 구현했습니다. 먼저, `#search-data` 영역에 있는 글 요소 `.search-item` 를
`searchItems` 배열로 추출합니다. 이후, 페이지네이션 설정(기본값은 1페이지 = 10개 글)에
따라 실제 표시할 `ids` 범위만 계산하고, 해당 범위의 `.search-item` 을 인덱스 조회하여
가상 DOM `fragment` 에 하나씩 추가합니다. 가상 DOM에 모든 요소가 추가되면
`#search-results` 영역으로 옮김으로써 실제 DOM의 변화를 최소화하면서 검색 결과를 사용자에게 표시합니다.

```js
const searchData = document.querySelector('#search-data');
const searchResults = document.querySelector('#search-results');

function displayResults(ids, state) {
  ...
  const fragment = document.createDocumentFragment();
  const sortedIds = Array.from(ids).toSorted((a, b) => a - b);
  const searchItems = searchData.querySelectorAll('.search-item');
  ...
  const startIndex = (state.page - 1) * state.pageSize;
  const endIndex = Math.min(startIndex + state.pageSize, totalPosts);

  for (let i = startIndex; i < endIndex; i++) {
    const curIndex = sortedIds[i];
    fragment.appendChild(searchItems[curIndex].cloneNode(true));
  }
  ...
  searchResults.appendChild(fragment);
}
```

### `term` 페이지 비활성화

더 이상 `term` 페이지가 필요하지 않으니 이 페이지들이 자동으로 만들어지지 못하게 하겠습니다.

Hugo 프로젝트 루트 경로에 있는 설정 파일에서 다음과 같이 `disableKinds` 항목에 `term` 값을 추가합니다.

```yaml
disableKinds: ["term"]
```

추가로, `taxonomy` 값을 여기에 추가하면 `/categories/`, `/tags/` 경로에 페이지가 만들어지는 것을
비활성화할 수도 있지만, 저는 이 페이지를 사용하기 때문에 `disableKinds` 에 넣지 않았습니다.

```bash
public/
├── ...
├── categories
│   ├── index.html
│   └── index.xml
├── ...
├── tags
│   ├── index.html
│   └── index.xml
└── ...
```

설정을 적용하고 나면 정적 페이지 렌더링 결과의 모음인 `public/` 경로에서
`term` 페이지들이 사라져 훨씬 깔끔해졌습니다.

## 검색 페이지 개선 계획

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/llja2m7ni7anbpaqvzk6b/seotax-24-search-header.webp?rlkey=y7izyn4c4xucm5thv72mv8coz&raw=1"
  alt="검색 페이지 헤더"
  class="screenshot-image" >}}

현재 검색 페이지는 검색어, 카테고리, 태그 검색을 지원합니다.
당장에 검색 조건은 이 정도로 충분해 보이지만, 글이 많아지고 검색 결과도 그만큼 늘어난다면
추가적인 검색 조건이 필요해질 것입니다.

### 기간 필터

검색하면 일반적으로 생각할 수 있는 구글 검색 페이지에서 제가 자주 사용하는 검색 조건이 있습니다.

![구글 검색 페이지](https://dl.dropboxusercontent.com/scl/fi/fqvk7f9ft0hz3qj76b59w/seotax-29-google-search.webp?rlkey=l5rh7vctf4wyvukv0p6gu7331&raw=1)

검색 결과가 너무 많을 경우에 특정 기간의 글만 필터해서 볼 수 있다면
검색 결과를 골라내기 더 편해질 것입니다.

### 정렬 기능

또한, 현재는 등록일 내림차순으로 글이 자동 정렬되어서 표시되지만,
마찬가지로 글이 많아지면 연관성 없는 글이 상위에 표시될 수도 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/mbhnbkjj4757xhzuia0vm/seotax-30-naver-search.webp?rlkey=n259nz3ei8fasv0ncy6pw7wuu&raw=1"
  alt="네이버 검색 페이지"
  max-width="691px"
  align="center" >}}

네이버 검색에서는 검색 결과에 대해 관련도순, 최신순 정렬을 지원하는데,
서택스 테마의 검색 페이지에서도 두 가지 정렬 기능을 지원할 수 있으면
독자들의 입맛에 맞는 검색 결과를 보여주는데 도움이 될 것입니다.
