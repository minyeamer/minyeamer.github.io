---
title: "Hugo 블로그 만들기 (4) - 검색 기능 개선 및 검색 페이지 구현 (Fuse.js)"
date: "2025-12-14T12:40:13+09:00"
layout: "post"
description: >
  Hugo Book 테마에서 Fuse.js 기반 검색 인덱스를 분석하고 검색 UI를 개선하는 과정을 소개합니다.
  검색 페이지를 구현하면서 검색 성능을 최적화하고 템플릿 일관성을 보장하기 위한 방식을 알아봅니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Fusejs", "검색 인덱스", "검색 페이지", "Hugo 검색", "휴고 테마", "EventListener", "window", "DocumentFragment", "JavaScript", "Blog", "Hugo Book"]
series: ["Hugo 블로그 만들기"]
---

{{< series "Hugo 블로그 만들기" "Hugo 블로그 만들기 \([0-9]+\) - " >}}

{{% hint info %}}
<i class="fa-solid fa-circle-info"></i> 대상 독자
- 마크다운으로 작성할 수 있는 나만의 블로그를 만들고 싶은 분들
- 블로그를 기능적으로 또는 시각적으로 커스터마이징 하고 싶은 분들
- Fuse.js를 활용한 클라이언트 사이드 검색을 구현하려는 분들
- 자바스크립트 이벤트 리스너와 가상 DOM을 활용한 사례를 찾고 있는 분들
{{% /hint %}}

{{% hint success %}}
<i class="fa-solid fa-lightbulb"></i> 주요 내용
- Book 테마 검색 프로세스 분석 ([Book 테마 검색 프로세스 분석](#book-테마-검색-프로세스-분석))
- Book 테마 검색창의 UI 및 기능 개선 ([검색 기능 개선](#검색-기능-개선))
- 템플릿 구조 재설계 및 window 전역 객체 활용 ([검색 기능 파일 구조 재설계](#검색-기능-파일-구조-재설계))
- 검색 결과를 표시하기 위한 DOM 조작 최적화 ([검색 수행 및 결과 필터링](#검색-수행-및-결과-필터링))
{{% /hint %}}

[앞선 게시글](/blog/hugo-blog-3/)에서 Book 테마의 태그와 카테고리 페이지를 구성하기 위한
Taxonomies 기능에 대해 알아보았습니다.

앞에서의 과정을 거쳤다면 태그와 카테고리 페이지가 블로그에 추가되고,
여기서 공통적으로 사용되는 게시글 항목 및 페이지네이션 템플릿을 만들었을 것입니다.

이번 게시글에서는 Hugo Book 테마에서 구현된 검색 프로세스를 분석하고
실제로 검색 페이지를 구현하면서 검색 성능을 최적화하고 템플릿 일관성을 보장하기 위한 방식을 알아보겠습니다.

---

## Book 테마 검색 프로세스 분석

Hugo는 기본적으로 내장된 검색 기능을 지원하지 않습니다.
하지만, 아래 공식문서에 따르면 `Pagefind`, `Lunr.js`, `Fuse.js` 등의
오픈소스 검색 기능을 지원합니다.

{{< bookmark "https://gohugo.io/tools/search/" >}}

이런 기능에 익숙하지 않은 저와 같은 사람이 직접 문서를 찾아가며 검색 기능을 도입하려 했다면
꽤나 머리 아프고 오랜 시간이 걸렸을 수 있지만,
다행히 Book 테마는 검색 기능을 지원해줘서 중간중간 로그를 찍어보면서 검색 과정을 이해할 수 있었습니다.

### 검색 템플릿 분석

Book 테마의 검색창은 `book-menu` 영역에 있으므로
우선 `layouts/_partials/docs/menu.html` 템플릿을 찾아봤습니다.

```html
<!-- layouts/_partials/docs/menu.html -->

<nav>
{{ partial "docs/brand" . }}
{{ partial "docs/search" . }}
<!-- ... -->
</nav>
```

`docs/brand` 는 [메인 레이아웃을 커스터마이징](/blog/hugo-blog-2/)할 때
프로필 사진이나 소셜 링크를 구현했던 템플릿입니다.
검색창은 바로 밑에 있으므로, 그리고 템플릿 명칭 자체가 직관적으로 "검색"을 가리키므로
`layouts/_partials/docs/search.html` 템플릿의 내용을 확인해보았습니다.

```html
<!-- layouts/_partials/docs/search.html -->

{{ if default true .Site.Params.BookSearch }}
<div class="book-search hidden">
  <input id="book-search-input" type="text" 
    placeholder="{{ i18n "Search" }}" aria-label="{{ i18n "Search" }}"
    maxlength="64" data-hotkeys="s/" />
  <div class="book-search-spinner hidden"></div>
  <ul id="book-search-results"></ul>
</div>
<script>document.querySelector(".book-search").classList.remove("hidden")</script>
{{ end }}
```

`docs/search` 템플릿의 내용 자체는 `input` 요소 하나만 있고 특별한건 없습니다.
설정 내 파라미터(`params`) 아래서 `BookSearch` 값을 할당하여
검색창을 활성화/비활성화할 수 있다는 것 정도만 알 수 있습니다.

### 자바스크립트 분석

그렇다면 검색 기능을 자바스크립트로 구현되어 있을 것이므로 템플릿과 별개의
`assets/` 경로를 탐색하여 `search.js` 라는 직관적인 이름의 파일을 발견했습니다.

파일이 한 페이지에 들어오지 않아 부분적으로 나눠서 알아보겠습니다.

```js
// assets/search.js

'use strict';

{{ $searchDataFile := printf "%s.search-data.json" .Language.Lang }}
{{ $searchData := resources.Get "search-data.json" | resources.ExecuteAsTemplate $searchDataFile . | resources.Minify | resources.Fingerprint }}
{{ $searchConfig := i18n "bookSearchConfig" | default "{}" }}

(function () {
  const searchDataURL = '{{ partial "docs/links/resource-precache" $searchData }}';
  // ...
})();
```

먼저, 스크립트의 시작 부분에는 `$searchData` 변수에 할당된 파일을 가져와 읽어오고 있습니다.
이 변수를 `console.log()` 에 넣어보면 `/search-data.json` 값이 출력됩니다.

### 검색 코퍼스 분석

아마 자바스크립트 파일과 동일한 경로에 있는 `search-data.json` 파일을 가리키는 것 같아서
내용을 확인해보았습니다.

```json
[
{{- $pages := where .Site.Pages "Kind" "in" (slice "page" "section") -}}
{{- $pages = where $pages "Params.bookSearchExclude" "!=" true -}}
{{/* Remove until we know why it does not work, see https://github.com/alex-shpak/hugo-book/issues/528 */}}
{{/*- $pages = where $pages "Content" "not in" (slice nil "") -*/}}
{{- $pages = where $pages "Content" "!=" "" -}}

{{ range $index, $page := $pages }}
{{ if gt $index 0}},{{end}} {
    "id": {{ $index }},
    "href": "{{ $page.RelPermalink }}",
    "title": {{ (partial "docs/title" $page) | jsonify }},
    "section": {{ (partial "docs/title" $page.Parent) | default $.Site.Title | jsonify }},
    "content": {{ $page.Plain | jsonify }}
}
{{- end -}}
]
```

익숙한 Go 템플릿을 사용하여 모든 페이지에 대해
`id`, `href`, `title`, `section`, `content` 로 구성된 객체의 배열을 만들어내는 것 같습니다.
이는 일종의 검색 인덱스라고 볼 수 있을 것 같은데, 게시글의 내용 전문을 포함하고 있어서
검색 코퍼스라고 부르는게 적절할지도 모르겠습니다.

> 이하 내용에서 `search-data.json` 의 내용을 `검색 코퍼스` 라 부르겠습니다.

Hugo로 만들어지는 웹사이트는 정적 페이지로만 구성되므로,
검색 인덱스도 아마 `public/` 경로를 찾아보면 관련된 파일이 있을 것입니다.
역시나 직관적으로 알 수 있는 JSON 파일 하나가 `public` 경로 아래에 있습니다.

```bash
public % tree -L 1 
.
├── ...
├── en.search-data.min.eab6c7b9001273416ee00669c84e2e15e0c20a277354e60f930fbf616c3450cd.json
├── ...
```

만약 Hugo 빌드를 여러 번 했다면 (동시에 이전 빌드에서 만들어진 파일을 지우지 않았다면) `search-data.json` 파일이 여러 개
만들어졌을건데, 어떤 파일을 봐야할지 모르겠다면 위 자바스크립트에서 `searchDataURL` 변수를 출력해보면 알 수 있습니다.
(`searchDataURL` 변수를 선언하는 라인 아래에 `console.log()` 를 실행하면 빌드 직후에 콘솔에 출력됩니다.)

![/search-data.json | en.search-data.min.eab6c7b9001273416ee00669c84e2e15e0c20a277354e60f930fbf616c3450cd.json](https://dl.dropboxusercontent.com/scl/fi/sm2svkm72ba0mylhjxn4m/hugo-41-search-data-log.webp?rlkey=enpd7cb3550b5mrvdjnxdu21f&raw=1)

`public/` 경로에서 보았던 `en.search-data.min.eab6c7b9001273416ee00669c84e2e15e0c20a277354e60f930fbf616c3450cd.json`
파일이 그대로 출력되었습니다.

> 파일명이 왜 이렇게 되었는가는, 우선 `$searchData` 변수를 할당하는 라인에서
`resources.Minify` 기능으로 파일을 축소하면서 뒤에 `.min` 이 붙고,
`resources.Fingerprint` 기능으로 파일명에 해시까지 추가되면서
이런 명칭으로 변환된 것입니다.

브라우저에서 이 파일의 경로로 접속하면 아래와 같은 내용을 볼 수 있습니다.

![{"id": 0, "href": "/docs/example/", "title": "Example Site", "section": "Docs", "content": "Introduction..."}](https://dl.dropboxusercontent.com/scl/fi/6euzxfwdwi9xilagnp270/hugo-42-search-data-json.webp?rlkey=7qdw7qra5i2cs9m8mqg5gdmvv&raw=1)

이 파일은 ExampleSite 기준으로 100 KB,
현재 40개 글이 있는 제 블로그 기준으로는 600 KB 정도의 용량이 되는데
앞으로 게시글이 추가될 때마다 무식하게 커지는 이 파일을 검색할 때마다 가져온다고 생각하니
장기적인 관점에서 걱정이 됩니다.

아무튼, 이 파일만 봤을 때 자바스크립트의 이후 동작은 검색 코퍼스에서
입력 쿼리를 포함하는 페이지를 필터할 것이라 예상할 수 있습니다.

### 이벤트 리스너 분석

구체적인 검색 과정을 확인하기 위해 자바스크립트의 내용을 이어서 보겠습니다.

```js
(function () {
  const searchDataURL = '{{ partial "docs/links/resource-precache" $searchData }}';
  // ...

  const input = document.querySelector('#book-search-input');
  const results = document.querySelector('#book-search-results');

  if (!input) {
    return
  }

  input.addEventListener('focus', init);
  input.addEventListener('keyup', search);

  document.addEventListener('keypress', focusSearchFieldOnKeyPress);
  // ...
})();
```

아래에는 함수들이 정의되어 있는데, 이벤트 리스너에 할당되는
`init`, `search`, `focusSearchFieldOnKeyPress` 가 각각 이 함수들입니다.

`input` 요소인 검색창이 포커스되면 `init()` 함수가 실행되고, 입력을 마치면 `search()` 함수가 실행됩니다.

`focusSearchFieldOnKeyPress()` 함수는 단축키가 눌렸는지 감시하는 함수인데,
`input#book-search-input` 요소의 `data-hotkeys` 속성에 지정된 단축키가 눌리면
바로 검색창에 포커스되는 기능을 합니다. (단축키는 `s`, `/` 가 지정되어 있습니다.)

### 초기화 함수 분석

`init()` 함수는 검색창에 포커스될 때 실행됩니다.

```js
(function () {
  // ...
  function init() {
    input.removeEventListener('focus', init); // init once
    input.required = true;

    fetch(searchDataURL)
      .then(pages => pages.json())
      .then(pages => {
        window.bookSearchIndex = new Fuse(pages, indexConfig);
      })
      .then(() => input.required = false)
      .then(search);
  }
  // ...
})();
```

함수의 첫줄부터 이벤트 리스너에서 제거합니다. 초기화 함수다보니 한 번만 실행하면 되는 것 같은데 내용을 이어서 보자면,
`searchDataURL` 경로, 즉 `search-data.json` 을 요청한다는 것을 알 수 있습니다.

그리고, 가져온 검색 코퍼스를 `Fuse(pages, indexConfig)` 함수에 전달해서
Fuse 인덱스를 생성하는 것을 보니 `Fuse.js` 를 사용한다는 것을 알 수 있습니다.
향후 검색 시에 Fuse 인덱스를 재사용하기 때문에 초기화 함수를 한 번만 실행하는 이유를 이해할 수 있습니다.

### 검색 함수 분석

`search()` 함수는 키를 떼었을 때, 즉 문자를 하나하나 입력할 때마다 실행됩니다.   
(검색 결과를 보기 위해 따로 엔터 키를 눌러야 할 필요는 없습니다.)

```js
(function () {
  // ...
  function search() {
    while (results.firstChild) {
      results.removeChild(results.firstChild);
    }

    if (!input.value) {
      return;
    }

    const searchHits = window.bookSearchIndex.search(input.value).slice(0,10);
    searchHits.forEach(function (page) {
      const li = element('<li><a href></a><small></small></li>');
      const a = li.querySelector('a'), small = li.querySelector('small');

      a.href = page.item.href;
      a.textContent = page.item.title;
      small.textContent = page.item.section;

      results.appendChild(li);
    });
  }
  // ...
})();
```

`Fuse.js` 의 내부 동작까지는 다룰 수는 없고, 이 함수의 동작만 보자면
기존 검색 결과인 `results` 를 초기화하고 검색 결과에서 최대 10개 페이지의 정보를
`li` 요소로 변환하여 다시 `results` 에 추가하는 동작을 합니다.

`results` 의 내용은 즉시 `ul#book-search-results` 요소 내부에 표시됩니다.
해당 요소는 검색창 바로 아래 있어서 검색 결과가 검색창 아래에 (카테고리 목록을 아래로 밀어내고) 출력됩니다.

![Hugo 검색 > Getting Started with Hugo, ...](https://dl.dropboxusercontent.com/scl/fi/0idnsek7m85h1e3c22q27/hugo-43-search-results.webp?rlkey=yac3gdsry1p95r5it9xjf2nyr&raw=1)

여기까지 봤다면 Book 테마에서 검색을 어떻게 구현했는지 이해할 수 있습니다.

## 검색 기능 개선

바로 위 이미지를 보자마자 개선해야 할 부분이 보였습니다.

### 검색 아이콘 추가

가장 먼저 느낀 문제점은 검색창의 UI가 입력창 하나만 덩그러니 있어서
검색을 위한 입력창인지 다른 목적인지 직관적으로 이해하기 어렵다고 느꼈습니다.

그래서, 입력창 오른쪽에 검색 아이콘을 하나 추가하고자 합니다.

{{< tabs "search-button" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/search.html -->

<div class="book-search hidden">
  <div class="search-input-container">
    <input ... />
    <button type="button" id="book-search-button" class="book-search-btn" onclick="goToSearchPage()">
      <i class="fa-solid fa-magnifying-glass"></i>
    </button>
  </div>
  <!-- ... -->
</div>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.book-search {
  position: relative;
  margin: $padding-8 0;

  .search-input-container {
    // 입력창과 검색 아이콘을 가로로 나란히 나열
    position: relative;
    display: flex;
    align-items: center;
  }

  input {
    width: 100%;
    padding: $padding-8;
    margin: 0 $padding-8 0 0; // 검색 아이콘과 간격 두기

    // 입력창에 테두리 적용
    border: 1px solid var(--gray-500);
    border-radius: $border-radius;

    background: var(--gray-300);
    color: var(--body-font-color);

    &:required + .book-search-spinner {
      display: block;
    }
  }

  .book-search-btn {
    // 검색 아이콘에 대한 스타일을 적용
    background: transparent;
    border: none;
    color: var(--body-font-color);
    cursor: pointer;

    &:hover {
      color: var(--color-link);
    }

    i {
      font-size: $font-size-24;
    }
  }
  // ...
}
```
{{% /tab %}}

{{< /tabs >}}

정확히는 검색 버튼의 역할이지만, 아직 검색 페이지 및 리다이렉트 기능을 구현하지는 않았으므로
검색 아이콘이라고 부르겠습니다.

![검색창 오른쪽에 검색 아이콘 추가](https://dl.dropboxusercontent.com/scl/fi/ex7a0jo1tl2g9o97awx8p/hugo-44-search-icon.webp?rlkey=u8pwtm314swdts5chgxobypen&raw=1)

아직 검색 아이콘에 특별한 기능은 없지만,
입력창이 검색 기능을 한다는 것은 직관적으로 인식하게 되었습니다.

### 검색 결과 위치 고정

가장 먼저 느낀 문제점은 검색 결과가 카테고리 목록을 밀어내고 보여진다는 것입니다.
개인적으로 이러한 동작은 선호하지 않습니다.
검색 결과는 카테고리 목록의 위치를 옮기지 않고 그 위에 겹쳐서 나타나는 것이 가장 이상적입니다.

{{< tabs "search-results" >}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.book-search {
  // ...
  #book-search-results {
    position: absolute;
    background: var(--gray-100);
    border: 1px solid var(--gray-200);
    border-radius: $border-radius;
    z-index: 11;
  }
}
```
{{% /tab %}}

{{% tab "JavaScript" %}}
```js
// assets/search.js

(function () {
  // ...
  function search() {
    // ...
    searchHits.forEach(function (page) {
      const li = element('<li><a href></a><small></small></li>');
      const a = li.querySelector('a');
      // small = li.querySelector('small'); << 제거

      a.href = page.item.href;
      a.textContent = page.item.title;
      // small.textContent = page.item.section; << 제거

      results.appendChild(li);
    });
  }
  // ...
})();
```
{{% /tab %}}

{{< /tabs >}}

이것은 검색 결과를 보여주는 요소의 위치를 고정시키면 됩니다.
CSS 파일에서 `position: absolute;` 를 적용하면 위치를 고정할 수 있고,
카테고리 목록인 `.book-categories` 요소보다 큰 `z-index` 를 부여하면
카테고리 목록 위에 검색 결과가 나타납니다.

추가로, 검색 결과에는 `section` 정보를 제목 밑에 같이 보여주고 있는데,
해당 블로그에서는 `section` 을 여러 개 사용할 일이 없으므로 없애는게 더 깔끔합니다.
이에 해당하는 `<small>` 태그는 자바스크립트에서 동적으로 생성하므로 이 부분을 제거했습니다.

![카테고리 목록 위에 검색 결과를 표시](https://dl.dropboxusercontent.com/scl/fi/yjojly1wmx3ltbmw3b6qm/hugo-45-search-results-absolute.webp?rlkey=43mp7431jni6p59i6t95f43zi&raw=1)

### 검색 결과에 더보기 링크 추가

Book 테마에서는 검색 결과를 최대 10개까지만 보여줍니다.
하지만, 제목이 여러줄에 달하는 게시글들을 10개만 나열해도
해상도에 따라 검색 결과가 화면 끝에 닿거나 한 화면에 다 보이지 않을 수 있습니다.

이런 사유로 검색 페이지를 만들려고 하지만 검색 페이지에 대한건 다음 문단에서 서술하고,
일단 검색 결과를 요약해서 보여주기 위한 더보기 링크를 표시하겠습니다.

{{< tabs "search-more" >}}

{{% tab "JavaScript" %}}
```js
// assets/search.js

(function () {
  // ...
  function search() {
    // ...
    const searchHits = window.bookSearchIndex.search(input.value); // 실제 검색 결과
    const searchPreview = searchHits.slice(0, 3); // 사용자에게 보여줄 검색 결과 (미리보기 3개)

    searchPreview.forEach(function (page) {
      const li = element('<li><a href></a><small></small></li>');
      const a = li.querySelector('a');

      a.href = page.item.href;
      a.textContent = page.item.title;

      results.appendChild(li);
    });

    if (searchHits.length > 3) {
      // 검색 결과가 3개를 초과할 경우 더보기 링크를 추가 (+ 검색 결과가 몇 개 있는지 카운팅하여 표시)
      const moreLink = element('<li class="book-search-more"><a href></a></li>');
      const a = moreLink.querySelector('a');
      a.textContent = '더보기 (총 ' + searchHits.length + '개)';
      results.appendChild(moreLink);
    }
  }
  // ...
})();
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.book-search {
  // ...
  .book-search-more {
    border-top: 1px solid var(--gray-200);

    a {
      color: var(--color-link);
      font-size: $font-size-12;
      font-weight: 500;
    }
  }
}
```
{{% /tab %}}

{{< /tabs >}}

더보기 링크의 역할은 검색 버튼과 마찬가지로 검색 페이지가 만들어져야 제 기능을 하지만
일단 구색만 갖췄습니다.

![검색 결과가 3개를 초과하면 더보기 표시](https://dl.dropboxusercontent.com/scl/fi/nw82ytf7boi8ljjif0heu/hugo-46-search-results-more.webp?rlkey=41wze58zpc55q7idbo2fgb4ga&raw=1)

이전 결과에서는 최대 10개 게시글만 보여주고
전체 몇 개 글이 있는지는 알 수 없었는데, 이 점을 개선했다는데에 의미가 있습니다.

### 검색 결과 초기화 기능 추가

Book 테마에서는 검색 결과를 표시하는 기능만 있고
검색 결과를 초기화하는 기능이 구현되어 있지 않습니다.

검색 결과를 팝업처럼 나타나게 하기 전에는 굳이 없어도 문제 없었겠지만,
변경 후 검색 결과가 카테고리 목록을 가려버리면서 검색 결과를 없애는 기능이 필요하다고 느꼈습니다.

이미 검색창으로 이동하는 단축키를 이벤트 리스너로 구현한 사례를 봤기 때문에
검색 결과 초기화 기능도 이벤트 리스너를 사용하면 동작을 구현할 수 있습니다.

```js
(function () {
  // ..
  input.addEventListener('focus', init);
  input.addEventListener('keyup', search);
  input.addEventListener('keydown', handleEscape);
  input.addEventListener('blur', clearResults);
  // ...

  /**
   * @param {KeyboardEvent} event
   */
  function handleEscape(event) {
    if (event.key === 'Escape') {
      clearResults();
      input.blur();
    }
  }

  function clearResults() {
    while (results.firstChild) {
      results.removeChild(results.firstChild);
    }
  }
  // ...
})();
```

## 검색 페이지 추가

사이드 메뉴라는 작은 영역에서 검색 결과를 표시하는데는 한계가 있습니다.
일반적인 블로그 플랫폼에서는 검색창에 입력한 결과를 하나의 페이지로 보여주는데
커스텀 테마에도 검색 페이지 템플릿을 추가해보겠습니다.

{{% hint danger %}}
💡 검색 페이지 템플릿은 [이전 게시글](/blog/hugo-blog-3/#게시글-목록-템플릿-추가)에서
구현한 게시글 목록 템플릿을 활용합니다.

앞으로의 진행을 위해 해당 과정이 선행되어야 합니다.
{{% /hint %}}

### 검색 기능 파일 구조 재설계

지금까지만해도 검색과 관련해서 1개의 템플릿과 2개의 애셋 파일을 만들었는데,
앞으로 검색 관련 파일이 계속 추가되면서 복잡해질 것 같아 한번 정리하려고 합니다.

|기존 파일|>>>|변경된 파일|
|---|---|---|
|`layouts/_partials/docs/search.html`|>>>|`layouts/_partials/search/input.html`|
|`assets/search-data.json`|>>>|`assets/search/data.json`|
|`assets/search.js` (인덱스 생성 함수)|>>>|`assets/search/fuse.js`|
|`assets/search.js` (검색 수행 함수)|>>>|`assets/search/input.js`|

검색 파일들이 앞으로 새로 추가될 것을 예상하여 `search` 폴더 내에 분류했습니다.

그리고, Fuse 인덱스를 생성하는 부분은 검색 페이지에서도 사용할 것이기 때문에,
하나의 `search.js` 스크립트를 `fuse.js`, `input.js` 라는 2개의 스크립트로 분리했습니다.
(변경된 파일명은 `<head>` 를 구성하는 `html-head.html` 에도 적용해야 합니다.)

이때, 서로 다른 자바스크립트 파일 간에 Fuse 인덱스를 공유하기 위해 `window` 전역 객체를 사용했습니다.
`fuse.js` 에서 전역 객체에 함수만 미리 정의해놓고 `input.js` 에서
검색 수행 시 해당 함수를 실행하는 방식으로 인덱스가 적절한 시점에 만들어지도록 했습니다.

이 과정을 아래의 `window` 그래프로 단순화할 수 있습니다.

<div id="window"></div>

{{< tabs "search-js" >}}

{{% tab "window" %}}
```
[HTML 페이지 로드]
       │
       ▼
┌──────────────────────────────────────┐
│  <script src="fuse.js">              │  ① 인덱스 생성 함수만 먼저 로드
│  window.bookSearch = {...}           │
│  window.bookSearch.initIndex = func  │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  <script src="list.js">              │  ② 검색 시 (performSearch)
│  window.bookSearch.initIndex()       │    fuse.js에서 정의한 함수 사용
│    .then(() => performSearch())      │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  window.bookSearchIndex              │  ③ 검색 시점에 인덱스가 생성됨
└──────────────────────────────────────┘
```
{{% /tab %}}

{{% tab "fuse.js" %}}
```js
'use strict';

{{ $searchDataFile := printf "search/%s.data.json" .Language.Lang }}
{{ $searchData := resources.Get "search/data.json" | resources.ExecuteAsTemplate $searchDataFile . | resources.Minify | resources.Fingerprint }}
{{ $searchConfig := i18n "bookSearchConfig" | default "{}" }}

window.bookSearch = window.bookSearch || {};
window.bookSearch.searchDataURL = '{{ partial "docs/links/resource-precache" $searchData }}';
window.bookSearch.getIndexConfig = function() {
  return Object.assign({{ $searchConfig }}, {
    includeScore: true,
    useExtendedSearch: true,
    fieldNormWeight: 1.5,
    threshold: 0.2,
    ignoreLocation: true,
    keys: [
      {
        name: 'title',
        weight: 0.7
      },
      {
        name: 'content',
        weight: 0.3
      }
    ]
  });
};

/**
 * Fuse 검색 인덱스 생성
 * @returns {Promise<Fuse>}
 */
window.bookSearch.initIndex = function() {
  if (window.bookSearchIndex) {
    return Promise.resolve(window.bookSearchIndex);
  }

  const indexConfig = window.bookSearch.getIndexConfig();

  return fetch(window.bookSearch.searchDataURL)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(pages => {
      window.bookSearchIndex = new Fuse(pages, indexConfig);
      return window.bookSearchIndex;
    });
};
```
{{% /tab %}}

{{% tab "input.js" %}}
```js
'use strict';

(function () {
  const input = document.querySelector('#book-search-input');
  const results = document.querySelector('#book-search-results');

  if (!input) {
    return
  }

  input.addEventListener('focus', init);           // 검색창이 포커스되면 검색 인덱스 생성
  input.addEventListener('keyup', search);         // 키 입력 시 검색 수행
  input.addEventListener('keydown', handleEscape); // ESC 키가 눌리면 검색 결과 초기화
  input.addEventListener('blur', clearResults);    // 검색창에서 포커스가 해제되면 검색 결과 초기화

  // 검색창으로 이동하는 단축키가 눌리는 이벤트 처리
  document.addEventListener('keypress', focusSearchFieldOnKeyPress);

  /**
   * 단축키('s' 또는 '/')가 눌리면 검색창으로 포커스 이동하는 함수
   * @param {Event} event
   */
  function focusSearchFieldOnKeyPress(event) {
    if (event.target.value !== undefined) {
      return;
    }

    if (input === document.activeElement) {
      return;
    }

    const characterPressed = String.fromCharCode(event.charCode);
    if (!isHotkey(characterPressed)) {
      return;
    }

    input.focus();
    event.preventDefault();
  }

  /**
   * 입력된 문자가 단축키와 일치하는지 확인하는 함수
   * @param {string} character
   * @returns {boolean}
   */
  function isHotkey(character) {
    const dataHotkeys = input.getAttribute('data-hotkeys') || '';
    return dataHotkeys.indexOf(character) >= 0;
  }

  /**
   * ESC 키가 눌리면 검색 결과를 초기화하고 검색창에서 포커스를 해제하는 함수
   * @param {KeyboardEvent} event
   */
  function handleEscape(event) {
    if (event.key === 'Escape') {
      clearResults();
      input.blur();
    }
  }

  function clearResults() {
    while (results.firstChild) {
      results.removeChild(results.firstChild);
    }
  }

  /**
   * 검색창이 최초로 포커스되면 검색 인덱스를 생성하는 함수
   */
  function init() {
    input.removeEventListener('focus', init);
    input.required = true;

    window.bookSearch.initIndex()
      .then(() => input.required = false)
      .then(search);
  }

  /**
   * 검색 수행 후 검색 결과 미리보기(최대 3개)를 표시하는 함수
   */
  function search() {
    clearResults();

    if (!input.value) {
      return;
    }

    const searchHits = window.bookSearchIndex.search(input.value);
    const searchPreview = searchHits.slice(0, 3);

    searchPreview.forEach(function (page) {
      const li = element('<li><a href></a></li>');
      const a = li.querySelector('a')

      a.href = page.item.href;
      a.textContent = page.item.title;

      results.appendChild(li);
    });

    // 검색 페이지로 이동하기 위한 더보기 링크를 표시
    if (searchHits.length > 3) {
      const moreLink = element('<li class="book-search-more"><a href></a></li>');
      const a = moreLink.querySelector('a');
      a.href = '{{ "/search/" | relURL }}?q=' + encodeURIComponent(input.value);
      a.textContent = '더보기 (총 ' + searchHits.length + '개)';
      results.appendChild(moreLink);
    }
  }

  /**
   * HTML 문자열로부터 DOM 요소를 생성
   * @param {string} content
   * @returns {Node}
   */
  function element(content) {
    const div = document.createElement('div');
    div.innerHTML = content;
    return div.firstChild;
  }
})();
```
{{% /tab %}}

{{% tab "html-head.html" %}}
```html
<!-- Search -->
{{- if default true .Site.Params.BookSearch -}}
  <!-- Search Data -->
  {{- $searchData := resources.Get "search/data.json" | resources.ExecuteAsTemplate "search/data.json" . | resources.Minify | resources.Fingerprint }}
  <link rel="preload" href="{{ $searchData.RelPermalink }}" as="fetch" crossorigin>
  <script>
    window.SEARCH_DATA_URL = "{{ $searchData.RelPermalink }}";
  </script>

  <!-- Search Fuse -->
  {{- $searchFuseJS := resources.Get "search/fuse.js" | resources.ExecuteAsTemplate "search/fuse.js" . | resources.Minify | resources.Fingerprint }}
  <script defer src="{{ "fuse.min.js" | relURL }}"></script>
  <script defer src="{{ partial "docs/links/resource-precache" $searchFuseJS }}" {{ template "integrity" $searchFuseJS }}></script>

  <!-- Search Input -->
  {{- $searchInputJS := resources.Get "search/input.js" | resources.ExecuteAsTemplate "search/input.js" . | resources.Minify | resources.Fingerprint }}
  <script defer src="{{ partial "docs/links/resource-precache" $searchInputJS }}" {{ template "integrity" $searchInputJS }}></script>
{{ end -}}
```
{{% /tab %}}

{{% tab "menu.html" %}}
```html
<nav>
{{ partial "docs/brand" . }}
{{ partial "docs/search/input" . }}
<!-- ... -->
</nav>
```
{{% /tab %}}

{{< /tabs >}}

### 빈 검색 페이지 생성

검색 페이지는 `/search` 경로로 연결되는데
Hugo에서 해당 경로를 인식시키기 위해 콘텐츠 파일을 만들어야 합니다.

`content/search/_index.md` 경로에 파일을 생성해줍니다.

```yaml
---
title: "Search"
type: "search"
---
```

파일 내용은 위와 같이 front matter만 입력해주고 본문은 비워놓으면 됩니다.
이 파일을 생성한 것으로 `/search` 경로를 인식할 수 있게 되었습니다.
실제로 `/search` 경로에 접속하면 아래 이미지와 같은 빈 페이지가 보입니다.

![비어있는 검색 페이지](https://dl.dropboxusercontent.com/scl/fi/rmii7uu5ff863s00aj2lp/hugo-47-search-page-empty.webp?rlkey=goo5yhox3ctedvjuqo85imtzq&raw=1)

### 검색 페이지 이동 기능 추가

검색창에 검색어가 입력된 상태에서 검색 페이지로 이동할 수 있는 3가지 방법을 정리해보았습니다.

{{% hint %}}
1. [검색 버튼](#검색-아이콘-추가)을 마우스 클릭
2. 검색창에서 엔터 키를 입력
3. 검색 결과 맨 아래 [더보기 링크](#검색-결과에-더보기-링크-추가)를 클릭
{{% /hint %}}

1, 2번 방법은 `search-input.html` 템플릿에서 구현하고 3번 방법은
`search-input.js` 스크립트에서 구현할 것입니다.

```js
function goToSearchPage() {
  const searchInput = document.getElementById('book-search-input');
  const query = searchInput.value.trim();
  if (query) {
    window.location.href = '/search/?q=' + encodeURIComponent(query);
  }
}
```

`goToSearchPage()` 함수는 `/search` 경로로 이동하면서,
검색창에 입력된 값을 `q` 파라미터로 전달하는 기능을 합니다.
만약 "Hugo" 라는 검색어를 입력했다면 `<baseUrl>/search/?q=Hugo` 주소로 매핑됩니다.

함수가 길지는 않으므로 템플릿 자체에 내장시키겠습니다.
`search-input` 템플릿에서 `<script>` 내부에 함수를 추가합니다.

```html
<!-- layouts/_partials/docs/search-input.html -->

<div class="book-search hidden">
  <div class="search-input-container">
    <input type="text" id="book-search-input"
      placeholder="{{ i18n "Search" }}" aria-label="{{ i18n "Search" }}"
      maxlength="64" data-hotkeys="s/" onkeydown="if(event.key==='Enter') goToSearchPage()" />
    <button type="button" id="book-search-button" class="book-search-btn" onclick="goToSearchPage()">
      <i class="fa-solid fa-magnifying-glass"></i>
    </button>
  </div>
  <div class="book-search-spinner hidden"></div>
  <ul id="book-search-results"></ul>
</div>
<script>
document.querySelector(".book-search").classList.remove("hidden");
// goToSearchPage() 함수 추가
</script>
```

그리고, 검색 버튼인 `<button>` 요소에 `onclick` 속성으로 `goToSearchPage()` 함수를 연결시키고,
검색창인 `<input>` 요소에도 `onkeydown` 속성으로 엔터 키를 감지하여 `goToSearchPage()` 함수를 실행하도록
적용했습니다.

이렇게 검색 페이지로 이동하는 1, 2번 방법이 구현되었습니다.

```js
// assets/search-input.js

(function () {
  // ...
  function search() {
    // ...
    if (searchHits.length > 3) {
      const moreLink = element('<li class="book-search-more"><a href></a></li>');
      const a = moreLink.querySelector('a');
      a.href = '{{ "/search/" | relURL }}?q=' + encodeURIComponent(input.value);
      a.textContent = '더보기 (총 ' + searchHits.length + '개)';
      results.appendChild(moreLink);
    }
  }
  // ...
})();
```

3번 방법인 더보기 링크는 `search-input.js` 에서 동적으로 만들어주므로,
더보기 링크에 해당하는 `<a>` 요소에 `href` 속성을 추가해줍니다.

3가지 방법 모두 실제로 테스트해보면 `/search` 경로로 연결됩니다.

### 검색 결과 표시 방식 구상

검색 페이지에서 검색 결과를 표시하는 방식으로 아래 2가지를 생각해볼 수 있습니다.

{{% hint %}}
1. 모든 게시글에 대한 요소를 생성해두고 검색 결과에 없는 요소는 숨기기
2. 자바스크립트에서 동적으로 검색 결과에 해당하는 요소를 생성하기
{{% /hint %}}

첫 번째 방식의 경우 모든 게시글에 대한 요소를 생성하기 때문에
초기에 로드되는 DOM 크기가 커진다는 단점이 있습니다.
하지만, 정적 사이트 생성기인 Hugo의 특성상 검색을 위한 게시글 정보도
정적 파일로 만들어놓고 불러와야하기 때문에 두 번째 방식과의 차이가 크지 않을거라 생각했습니다.

효율성을 생각하면 필요한 항목만 동적으로 생성하는 두 번째 방식이 더 나을 수 있지만,
두 번째 방식은 기존에 게시글 항목을 구성하기 위해 만들어뒀던
[`post-item`](/blog/hugo-blog-3/#게시글-항목-템플릿-추가) 템플릿을
활용할 수 없기 때문에 자바스크립트에서 템플릿의 기능을 다시 구현해야 합니다.

단순히 불편함만 따진다면 아직까지 여전히 효율이 좋은 두 번째 방식을 선택하고 싶지만,
향후 `post-item` 템플릿이 변경될 경우 자바스크립트도 동일하게 변경해줘야 하는
종속적인 관계가 되어버려 자칫하면 일관성을 잃어버릴 수 있을 문제가 있어
첫 번째 방식을 채택했습니다. 표로 정리하면 아래와 같습니다.

|항목|방식 1|방식 2|
|---|---|---|
|구현 방식|모든 게시글을 나열하고 검색되지 않은 게시글은 숨기기|검색된 게시글만 동적으로 생성|
|구현 복잡도|✅ 낮음 (템플릿 재사용 가능)|❌ 높음 (템플릿 재구현 필요)|
|초기 로드 크기|❌ 모든 페이지에 대한 `post-item` 요소|✅ 모든 페이지의 속성만 추출한 `data.json`|
|템플릿 일관성|✅ 높음 (템플릿의 변경사항만 고려하면 됨)|❌ 낮음 (템플릿 변경사항을 자바스크립트에도 반영)|

{{% details title="만약 방식 2를 사용할 경우 `data.json` 을 이렇게 구성해야 합니다." open=false %}}
`data.json` 에는 `post-item` 템플릿을 구성하는 모든 속성 값들이 포함됩니다.

```json
[
{{- $pages := where .Site.Pages "Kind" "in" (slice "page" "section") -}}
{{- $pages = where $pages "Params.bookSearchExclude" "!=" true -}}
{{- $pages = where $pages "Content" "!=" "" -}}

{{ range $index, $page := $pages }}
{{ if gt $index 0}},{{end }} {
    "id": {{ $index }},
    "href": "{{ $page.RelPermalink }}",
    "title": {{ (partial "docs/title" $page) | jsonify }},
    "section": {{ (partial "docs/title" $page.Parent) | jsonify }},
    "content": {{ $page.Plain | jsonify }},
    "date": "{{ $page.Date.Format "2006-01-02" }}",
    "parentCategory": {{ (partial "categories/value-first" $page.Params.categories) | jsonify }},
    "childCategory": {{ (partial "categories/value-second" $page.Params.categories) | jsonify }},
    "tags": {{ (first 5 ($page.Params.tags | default slice)) | jsonify }},
    "thumbnail": {{ $page.Params.thumbnail | jsonify }},
    "cover": {{ $page.Params.cover | jsonify }}
}
{{- end -}}
]
```
{{% /details %}}

### 검색 페이지 템플릿 추가

검색 결과를 표시하기 위해 방식 1을 선택했으므로
모든 게시글을 나열하기 위한 검색 페이지 템플릿을 구현해야 합니다.

검색 페이지로 연결되는 `/search` 경로와 대응되는 템플릿 위치는 `layouts/search/list.html` 인데,
여기에 다음과 같은 내용을 작성합니다.

{{< tabs "search-page" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/search/list.html -->

{{ define "main" }}
<article class="markdown book-article">
  <div class="search-header">
    <h1>검색 결과</h1>
    <div class="search-query-info">
      <p id="search-query-display"></p>
    </div>
  </div>

  <div id="search-no-results" class="search-no-results hidden">
    <p>검색 결과가 없습니다.</p>
  </div>

  <div class="search-base" style="display: none;">
    {{- $pages := where .Site.RegularPages "Params.bookSearchExclude" "!=" true -}}
    {{- range $pages.ByDate.Reverse -}}
      {{ partial "docs/post-item.html" . }}
    {{- end -}}
  </div>

  <div class="post-list search-results"></div>

  <div id="search-pagination"></div>
</article>
{{ end }}
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.search-header {
  margin-bottom: $padding-16;

  h1 {
    font-size: $font-size-40;
    margin-bottom: $padding-8;
  }

  .search-query-info {
    p {
      font-size: $font-size-18;
    }
  }
}

.search-no-results {
  text-align: center;
  padding: $padding-24;

  p {
    font-size: $font-size-20;
  }
}
```
{{% /tab %}}

{{< /tabs >}}

`post-item` 템플릿을 활용하여 모든 게시글들을 나열하는 것 외에
직접적인 검색 기능은 자바스크립트에서 구현됩니다.
ExampleSite는 현재 블로그와 구조가 달라서
게시글, Taxonomy 페이지 구분 없이 모든 페이지를 가져왔는데,
특정 섹션에 속하는 게시글만 보여주고 싶으면 이렇게 필터할 수 있습니다.

- `$pages := where .Site.RegularPages "Section" "posts"`

검색 결과는 `.search-results` 영역에 표시되고,
만약 검색 결과가 없다면 `#search-no-results` 영역이 나타날 것입니다.

## 검색 및 결과 표시 기능 추가

마지막으로, 검색 페이지의 핵심 기능을 자바스크립트로 구현하겠습니다.

파일명은 중요하지 않지만 `search/list.html` 템플릿 명칭과 맞춰서 `search/list.js` 로 하겠습니다.

### 파라미터 초기화 및 인덱스 생성

자바스크립트에서 처음에는 파라미터를 받습니다.

검색 키워드는 `q`, 페이지는 `page` 에 대응되며
각각 `query`, `currentPage` 상수에 할당됩니다.

```js
// assets/search/list.js

document.addEventListener('DOMContentLoaded', function() {
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get('q') || '';
  const currentPage = parseInt(urlParams.get('page')) || 1;
  const itemsPerPage = 10;

  window.bookSearch.initIndex()
    .then(() => {
      initSearch();
      performSearch();
    });

  function initSearch() {
    const displayElement = document.getElementById('search-query-display');
    if (query) {
      displayElement.innerHTML = `"${query}" 검색 결과 <em class="list-count" id="search-count">0</em>`;
    } else {
      displayElement.textContent = '검색어를 입력해주세요.';
    }
  }
  // ...
});
```

파라미터를 초기화한 후 `window.bookSearch.initIndex()` 함수를 호출하여
검색 인덱스를 생성합니다. 앞에서 [검색 기능 파일 구조를 재설계](#window)하는 과정에서
Fuse 인덱스를 생성하는 전역 함수 `initIndex()` 를 미리 정의했습니다.
해당 함수를 실행하면 마찬가지로 전역 위치에 인덱스가 생성되고
`window.bookSearchIndex` 를 호출하는 것으로 인덱스에 접근할 수 있습니다.

인덱스가 생성되면 이어서 `initSearch() >> performSearch()` 순서로 함수를 실행합니다.

`initSearch()` 함수는 간단하여 같이 설명합니다.
검색 쿼리가 있을 경우, 검색 결과가 몇 개 있는지 표시하는 `.list-count` 요소를 포함한
문장을 `.search-query-display` 영역 내에 삽입합니다.
만약 검색 쿼리가 없으면 검색어를 입력해달라는 안내 문구를 표시합니다.

### 검색 수행 및 결과 필터링

`performSearch()` 함수는 검색을 수행하고 검색 결과를 표시하는 기능을 합니다.
함수의 내용이 한 화면에 들어오지 않아 설명은 주석으로 대체합니다.

```js
document.addEventListener('DOMContentLoaded', function() {
  // ...

  function performSearch() {
    const sourceContainer = document.querySelector('.search-base');
    const resultsContainer = document.querySelector('.search-results');
    const allPostItems = Array.from(sourceContainer.querySelectorAll('.post-item'));

    if (!query) {
      document.getElementById('search-no-results').classList.remove('hidden');
      document.getElementById('search-pagination').style.display = 'none';
      return;
    }

    // Fuse 검색 인덱스를 활용한 검색 수행
    const searchHits = window.bookSearchIndex.search(query);

    if (searchHits.length === 0) {
      document.getElementById('search-no-results').classList.remove('hidden');
      document.getElementById('search-count').textContent = '0';
      document.getElementById('search-pagination').style.display = 'none';
      return;
    }

    // 검색 결과와 대응되는 DOM 요소를 찾기 (href 속성이 일치하는지 확인)
    const matchedItems = [];
    searchHits.forEach((result) => {
      const href = result.item.href;
      const matchedItem = allPostItems.find(item => {
        const link = item.querySelector('.post-title a');
        return link && link.getAttribute('href') === href;
      });
      if (matchedItem) {
        matchedItems.push(matchedItem.cloneNode(true));
      }
    });

    // 페이지네이션 생성을 위한 인덱스 계산
    const totalPages = Math.ceil(matchedItems.length / itemsPerPage);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, matchedItems.length);

    // 현재 페이지의 게시글을 가상 DOM 컨테이너에 추가하고 실제 DOM에 업데이트
    const fragment = document.createDocumentFragment();
    for (let i = startIndex; i < endIndex; i++) {
      fragment.appendChild(matchedItems[i]);
    }
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(fragment);

    // 검색 결과 수를 업데이트
    document.getElementById('search-count').textContent = matchedItems.length;

    buildPagination(currentPage, totalPages, query);
  }
  // ...
});
```

검색 페이지 템플릿에서 모든 게시글을 나열하는 `.search-base` 영역과
검색 결과를 표시하는 `.search-results` 영역이 따로 구분된 이유가 이 함수의 동작으로 설명됩니다.

검색 결과를 표시하는 방법으로, 처음에는 모든 게시글의 스타일에 `display = 'none';`
속성을 넣어서 전체 게시글을 숨기고 검색 결과에 해당하는 게시글에만
`display = 'block';` 속성을 덮어씌워 숨김을 해제했습니다.

하지만, 이 방식의 단점은 검색 결과를 유사도 순으로 표시하지 못하고
무조건 처음 페이지가 나열된 기준인 작성일 내림차순으로 정렬하여 표시합니다.
이렇게 정리하고보니 정렬 기준을 바꾸는 기능도 추가하면 좋겠다 생각하지만,
어쨋든 유사도 순으로 보여주는게 사용자 입장에서는 더 검색 결과에 대한 흥미를 끌 수 있을 것 같아
다른 방식을 생각했습니다.

자바스크립트로 사이트를 구현하는데 익숙하지 않다보니 코파일럿의 도움을 받았는데,
가장 매력적인 방식이 `DocumentFragment` 라는 가상의 DOM 컨테이너를 활용하는 것이었습니다.

매번 검색할 때마다 게시글 요소를 재배치하기 위해 반복문으로 DOM을 조작하는건
매우 큰 부하를 일으킬 수 있습니다.
단일 요소를 바꾸기 위해 매번 DOM 전체를 업데이트 해야하기 때문입니다.

이러한 문제를 해결할 수 있는 것이 `DocumentFragment` 입니다.
메모리에 존재하는 가상의 DOM 컨테이너에 검색 결과에 해당하는 `post-item` 요소들을 담아놓고
반복문이 끝난 시점에 실제 DOM에 있는 `.search-results` 영역에
요소들의 뭉치를 추가하면 단 한번의 DOM 업데이트만으로 모든 검색 결과를 나타낼 수 있습니다.
이는 아래 그래프로 단순화할 수 있습니다.

<div id="document-fragment"></div>

```
[메모리]                            [실제 DOM]
┌──────────────────┐              ┌──────────────────┐
│ DocumentFragment │              │  .search-results │
│  ├─ post-item 1  │              │  ├─ post-item 1  │
│  ├─ post-item 2  │  ─────────►  │  ├─ post-item 2  │
│  └─ post-item 3  │  appendChild │  └─ post-item 3  │
└──────────────────┘              └──────────────────┘
```

`performSearch()` 함수에서는 검색 결과를 토대로 총 페이지 수, 시작 페이지, 종료 페이지를
계산하는데, 이 값들은 곧바로 다음 `buildPagination()` 함수를 호출하면서
파라미터로 전달됩니다.

### 페이지네이션 동적 생성

페이지네이션 생성 함수 `buildPagination()` 의 내용은 길긴 하지만
[페이지네이션 템플릿](/blog/hugo-blog-3/#페이지네이션-템플릿-추가-1)인 `pagination` 의
내용을 그대로 자바스크립트로 구현한 것 뿐입니다.

페이지네이션 또한 `post-item` 처럼 `paginaiton` 템플릿을 그대로 사용하고 싶었지만,
단순 재배치만 하면 되는 `post-item` 과 다르게 페이지네이션은 링크나 페이지 번호 등
모든 요소의 텍스트까지 싹 바꿔야하다보니 템플릿을 사용하는 의미가 없어 완전히 동적으로 생성하게 되었습니다.

```js
document.addEventListener('DOMContentLoaded', function() {
  // ...

  /**
   * @param {number} currentPage - 현재 페이지 (1부터 시작)
   * @param {number} totalPages - 총 페이지 수
   * @param {string} query - 검색 쿼리
   */
  function buildPagination(currentPage, totalPages, query) {
    const paginationContainer = document.getElementById('search-pagination');

    if (totalPages <= 1) {
      paginationContainer.style.display = 'none';
      return;
    }

    paginationContainer.style.display = 'block';

    const createPageUrl = (page) => {
      return `/search/?q=${encodeURIComponent(query)}${page > 1 ? '&page=' + page : ''}#pagination-anchor`;
    };

    // 10개 게시글 단위로 페이지를 그룹화
    const groupNumber = Math.floor((currentPage - 1) / 10);
    const groupStart = groupNumber * 10 + 1;
    let groupEnd = groupStart + 9;
    if (groupEnd > totalPages) {
      groupEnd = totalPages;
    }

    // 이전 및 다음 페이지 그룹을 계산
    const prevGroupPage = groupStart - 10;
    const nextGroupPage = groupEnd + 1;

    // 이전 페이지 그룹으로 이동하는 링크
    const prevButtonHTML = groupStart > 1
      ? `<a href="${createPageUrl(prevGroupPage > 1 ? prevGroupPage : 1)}" class="pagination-nav pagination-link">
          <i class="fa-solid fa-backward"></i> 이전
        </a>`
      : `<span class="pagination-nav disabled">
          <i class="fa-solid fa-backward"></i> 이전
        </span>`;

    // 현재 페이지 그룹에 속한 각각의 페이지로 이동하는 링크
    let pagesHTML = '';
    for (let i = groupStart; i <= groupEnd; i++) {
      if (i === currentPage) {
        pagesHTML += `<span class="pagination-page current" id="current-page">${i}</span>`;
      } else {
        pagesHTML += `<a href="${createPageUrl(i)}" class="pagination-page pagination-link">${i}</a>`;
      }
    }

    // 다음 페이지 그룹으로 이동하는 링크
    const nextButtonHTML = nextGroupPage <= totalPages
      ? `<a href="${createPageUrl(nextGroupPage)}" class="pagination-nav pagination-link">
          다음 <i class="fa-solid fa-forward"></i>
        </a>`
      : `<span class="pagination-nav disabled">
          다음 <i class="fa-solid fa-forward"></i>
        </span>`;

    // 페이지네이션을 `#search-pagination` 영역에 업데이트
    paginationContainer.innerHTML = `
      <div id="pagination-anchor"></div>
      <nav class="pagination">
        ${prevButtonHTML}
        <div class="pagination-pages">
          ${pagesHTML}
        </div>
        ${nextButtonHTML}
      </nav>`;
  }
});
```

여기까지 적용하고 블로그에서 검색을 수행하면 아래 이미지와 같은 검색 페이지로 이동할 수 있습니다.

!["Hugo" 검색 결과](https://dl.dropboxusercontent.com/scl/fi/2kkw8zwdob4wy15xkg59t/hugo-48-search-page.webp?rlkey=vrjfr1vc54vpyhl2bsz2mut3g&raw=1)

검색 페이지와 관련된 모든 구현 과정이 종료되었습니다.

다음 게시글에서는 본문의 레이아웃을 개선하는 과정을 진행하겠습니다.
