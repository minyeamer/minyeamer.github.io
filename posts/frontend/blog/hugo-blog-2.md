---
title: "Hugo Book 테마 커스터마이징 - 메뉴/목차/헤더 레이아웃 개선"
date: "2025-11-04T01:50:16+09:00"
layout: "post"
description: >
  Hugo Book 테마의 구조를 이해하고 메인 레이아웃을 개선하는 방법을 소개합니다.
  메뉴 영역에 프로필 사진과 소셜 링크를 추가하고,
  목차 영역에 하이라이트와 스크롤 이동 버튼을 구현하는 과정을 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Blog", "휴고 테마", "휴고 레이아웃", "HTML", "CSS", "JavaScript", "Hugo Book", "커스터마이징", "블로그 목차"]
series: ["Hugo 블로그 만들기"]
---

{{< series "Hugo 블로그 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo 블로그의 외형을 결정짓는 **메인 레이아웃(메뉴, 목차, 헤더)** 을 직접 뜯어고치며 프론트엔드 역량을 키워보세요.
템플릿 구조에 대한 기초 지식부터 CSS/JS를 활용한 세부 기능 구현까지 단계별로 설명합니다.

- **[테마 구조 분석](#book-테마-알아보기)**: Hugo의 템플릿 구조와 Book 테마의 구성 요소 파악
- **[메뉴 기능 개선](#메뉴-영역-개선하기)**: 사이드바 위치 고정부터 [프로필 사진](#2-프로필-사진을-표시하기), [소셜 링크 연동](#3-소셜-링크를-표시하기)으로 퍼스널 브랜딩 강화
- **[독자 편의성 향상](#목차-영역-개선하기)**: 현재 읽고 있는 위치를 알려주는 [목차 하이라이트](#2-목차-하이라이트-적용하기)와 [이동 버튼](#3-스크롤-이동-버튼-추가하기)으로 사용자 경험 극대화
- **[반응형 최적화](#헤더-영역-개선하기)**: 모바일 환경에서도 끊김 없는 사용성을 제공하는 헤더 디자인 개선
{{% /hint %}}

[앞선 게시글](/blog/hugo-blog-1/)에서 Hugo 테마에 대해 둘러보고 Hugo 프로젝트 구조를 설계하는 방법을 알아보았습니다.

## Hugo 서버 실행하기

Github Pages를 이용해 블로그를 `github.io` 주소로 배포해보았지만
테마를 개선하는 과정에서는 변경사항을 즉각적으로 확인해보기 위해 로컬에서 서버를 실행해 보는게 좋습니다.

Hugo 서버를 실행하려면 `hugo server` 명령어를 사용할 수 있습니다.

```bash
% hugo server
Watching for changes in .../{archetypes,content,static,themes}
...
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
```

기본적으로는 1313 포트에서 서버가 실행되며 `--port <포트번호>` 옵션을 추가하면
서버가 할당될 포트를 직접 지정할 수 있습니다.

서버를 실행하면 터미널에서 출력되는 주소 `http://localhost:1313/` 를 통해
블로그에 접속할 수 있습니다.

이렇게 서버를 실행했을 때 장점은 테마를 수정할 때마다 자동으로 빌드되어 변경사항이
즉각적으로 반영된다는 점입니다. 만약 변경사항이 적용되지 않는다면 서버를 실행할 때
`--disableFastRender` 옵션을 추가하거나 브라우저에서 캐시를 삭제해 볼 수 있습니다.

## Book 테마 알아보기

[앞선 게시글](/blog/hugo-blog-1/#book-테마-선정)에서 Book 테마에 대해 둘러보면서
앞으로 해당 테마를 바탕으로 레이아웃을 개선해보겠다고 전달드렸습니다.

### Book 테마 가져오기

Github에 올라온 [hugo-book 저장소](https://github.com/alex-shpak/hugo-book)를 Fork하여
개인 소유의 저장소로 가져오면 앞으로의 변경사항을 관리하는데 편리합니다.

저 또한 Book 테마를 개선하기 위해
[`hugo-book-custom`](https://github.com/minyeamer/hugo-book-custom)이라는
별도의 저장소를 Fork해서 만들었습니다.

![Book 테마 Fork하기](https://dl.dropboxusercontent.com/scl/fi/nlz6cmz7tu68u90muvomr/hugo-25-book-fork.webp?rlkey=o4a5k3phxon9jr4y4budm84sl&raw=1)

Fork한 저장소를 `git clone` 명령어로 로컬 경로로 가져와 코드를 확인해보겠습니다.

```bash
git clone https://github.com/minyeamer/hugo-book-custom
```

### Hugo 템플릿 구조

Hugo v0.146.0 공식문서에서 안내하는 폴더 구조를 알아보겠습니다.

{{< bookmark "https://gohugo.io/templates/new-templatesystem-overview/" >}}

`layouts/` 경로 아래에 다음과 같은 경로로 레이아웃을 구성하도록 권장합니다.

여기서 가장 기본이 되는 템플릿이 `layouts/baseof.html` 이고,
템플릿을 헤더, 목차 등 역할에 따라 작은 부분으로 나눠 `layouts/_partials/` 경로에 배치시킵니다.
`layouts/baseof.html` 에서는 이러한 부분 템플릿을 동적으로 가져옵니다.

```bash
layouts/
├── baseof.html
├── baseof.term.html
├── home.html
├── page.html
├── section.html
├── taxonomy.html
├── term.html
├── term.mylayout.en.rss.xml
├── _markup/
│   ├── render-codeblock-go.term.mylayout.no.rss.xml
│   └── render-link.html
├── _partials/
│   └── mypartial.html
├── _shortcodes/
│   ├── myshortcode.html
│   └── myshortcode.section.mylayout.en.rss.xml
├── docs/
│   ├── baseof.html
│   ├── _shortcodes/
│   │   └── myshortcode.html
│   └── api/
│       ├── mylayout.html
│       ├── page.html
│       └── _markup/
│           └── render-link.html
└── tags/
    ├── taxonomy.html
    ├── term.html
    └── blue
        └── list.html
```

### Book 테마 구조

`layouts/docs/` 경로를 활용하는 Hugo 공식문서와 다르게 Book 테마는 `layouts/_partials/` 경로에
`docs` 폴더를 배치시켰습니다.
따라서, 대부분의 테마 수정 작업은 `layouts/_partials/docs/` 경로에서 진행됩니다.

```bash
layouts/_partials/docs/
├── ...
├── brand.html
├── ...
├── footer.html
├── header.html
├── ...
├── html-head.html
├── ...
├── menu.html
├── ...
└── toc.html
```

Book 테마의 `layouts/_partials/docs/` 경로에는 다양한 템플릿이 있지만,
그 중에서 주로 보게될 것은 위 파일들 입니다.

- `brand.html` : 메뉴에서 블로그 제목을 표시합니다.
- `footer.html` : 본문 하단에 이전, 다음 게시글 및 글 수정 링크를 표시합니다.
- `header.html` : 본문 상단에 메뉴 또는 목차 영역을 펼치고 접는 버튼을 표시합니다.
- `html-head.html` : 메타(meta) 태그 등 `<head>` 태그 내에 들어갈 요소들을 나열합니다.
- `menu.html` : 본문 좌측 메뉴를 표시합니다. 여기서 `brand.html` 을 호출합니다.
- `toc.html` : 본문 우측에 목차(Table of Contents)를 표시합니다.

하지만, 기능적으로 무언가를 추가할게 아니라면, 단순히 시각적으로 테마를 변경하고자 한다면
템플릿 파일을 직접 건들지는 않고 CSS 파일을 주로 수정합니다.

Book 테마의 CSS 파일들은 `assets/` 경로 아래에 위치합니다.

```bash
assets/
├── _custom.scss
├── _defaults.scss
├── ...
├── _main.scss
├── _markdown.scss
├── ...
├── _shortcodes.scss
└── ...
```

`assets/` 경로의 파일들 중에서 위 파일들을 주로 수정합니다.

- `_custom.scss` : 사용자 커스터마이징을 위한 스타일을 작성합니다.
- `_defaults.scss` : 폰트 크기, 색상 등이 변수로 정의되어 있습니다.
- `_main.scss` : 메뉴, 목차 등 메인 레이아웃에 대한 스타일이 작성되어 있습니다.
- `_markdown.scss` : 마크다운을 HTML로 렌더링한 결과에 대한 스타일이 작성되어 있습니다.
- `_shortcodes.scss` : 마크다운 작성 시 미리 정해진 짧은 코드를 호출하는 경우가 있는데 이에 대한 스타일이 작성되어 있습니다.

이 외에 JS 파일 등도 `assets/` 경로에 위치합니다.

### Example Site

앞으로 Book 테마를 수정하게 되는데 아무런 글도 없으면 스타일이 어떻게 적용되었는지 확인하기 어렵습니다.

이미 작성한 게시글이 있다면 `content/` 경로에 가져다 놓아도 좋지만,
그러한 게시글이 없을 경우엔 테마에서 제공하는 `exampleSite/` 를 참고할 수 있습니다.

Book 테마의 Example Site는 영어, 히브리어, 중국어로 작성된 각각의 폴더로 나누어져 있는데,
이번 프로젝트에서 다국어 텍스트를 고려하지는 않으므로 영어 문서로 구성된 `content.en/` 폴더 내 파일들을
현재 프로젝트의 `content/` 경로로 가져옵니다.

```bash
exampleSite/content.en/
├── _index.md
├── docs
│   ├── example
│   │   ├── _index.md
│   │   └── ...
│   └── ...
├── posts
│   ├── _index.md
│   └── ....md
└── showcases.md
```

그리고, `exampleSite/` 경로 바로 아래에 있는 `hugo.yaml` 설정 파일도 현재 프로젝트로 가져옵니다.

해당 파일은 Hugo 블로그를 구성하는데 필요한 파라미터 등의 설정 정보가 기록되어 있는데,
TOML, YAML, JSON 등 다양한 형식을 지원합니다.
Hugo 프로젝트를 시작할 때 `hugo.toml` 이라는 파일이 기본적으로 생성되었을 것인데,
TOML 형식은 중첩된 구조를 표현하기에는 번거로워 YAML 형식을 사용합니다.

설정 파일에 대해서는 필요한 순간에 설명드릴 예정이지만,
설정 파일 상단에서 `baseUrl` 및 `theme` 값은 지금 변경해두는게 좋습니다.

```yaml
baseURL: http://localhost:1313/
title: Hugo Book
theme: Book
```

`baseUrl` 은 기본값으로 `http://localhost:1313/hugo-book/` 경로가 적용되어 있는데,
매번 테스트 페이지에 접근할 때마다 `hugo-book/` 경로를 추가하는게 불편하여 제거했습니다.

`theme` 은 기본값으로 `hugo-book` 이 적용되어 있는데, `themes/` 경로에 위치한
Book 테마의 폴더명을 입력해야 합니다.

## 메인 레이아웃 개선하기

Book 테마는 다음과 같은 형태를 가집니다.

![Example Site 보기](https://dl.dropboxusercontent.com/scl/fi/872htn2ieg1jk74k7cfm6/hugo-09-example-site.webp?rlkey=0ou1fendglqi8310cmzhk1fyh&raw=1)

브라우저에서 `<body>` 태그 바로 아래에 있는 `.container` 요소를 클랙해보면
아래와 같이 메뉴, 본문, 목차 3개의 부분으로 나눠져 있는 것을 확인할 수 있습니다.
HTML 소스코드에서 각각의 요소에 대한 클래스를 확인해보면 `book-menu`, `book-page`, `book-toc`
로 지정되어 있습니다.

![메인 컨테이너 영역 선택](https://dl.dropboxusercontent.com/scl/fi/q3m1gtqi2kwz1109pz8nq/hugo-10-main-container.webp?rlkey=5g1s015httn7c8nilwhv0w9pb&raw=1)

브라우저의 너비를 줄이다 보면 메뉴와 목차 영역이 사라지고 헤더 영역이 나타나게 됩니다.
헤더 영역은 `book-header` 클래스로 특정할 수 있습니다.
헤더 양옆의 버튼을 클릭하면 메뉴(왼쪽 버튼)와 목차(오른쪽 버튼)가 다시 나타납니다.

![모바일 헤더 영역 선택](https://dl.dropboxusercontent.com/scl/fi/x68lh4nu28awnctyyoc9p/hugo-11-mobile-header.webp?rlkey=1ktuycfbolqs19t7wok1q72l0&raw=1)

이번 게시글에서는 메뉴, 목차, 헤더 영역을 순차적으로 개선해보겠습니다.

## 메뉴 영역 개선하기

Book 테마에서 메뉴 영역은 아래 이미지에서 선택된 부분입니다.

![book-menu 영역 선택](https://dl.dropboxusercontent.com/scl/fi/vql6oba5mxrrv1yskoqjv/hugo-12-book-menu.webp?rlkey=99je2sfrmzs92jpbhuezlun58&raw=1)

좌측 사이드바에 해당하는 메뉴 영역은 `book-menu` 클래스가 적용된 요소로 감싸져 있으며,
`baseof.html` 파일에서 다음과 같이 `menu.html` 템플릿 파일을 호출합니다.

```html
<!-- baseof.html -->

{{ define "menu-container" }}
<aside class="book-menu">
  <div class="book-menu-content">
    {{ template "menu" . }}
  </div>
</aside>
{{ end }}
```

`menu.html` 템플릿 파일은 `layouts/_partials/docs/` 경로에 있으며,
이름에서 알 수 있듯이 검색창을 나타내는 `docs/search` 템플릿이 두 번째로 호출되고,
그 가장 먼저 호출되는 `docs/brand` 템플릿이 이번 문단에서 개선하고자 하는 부분입니다.

```html
<!-- layouts/_partials/docs/menu.html -->

<nav>
{{ partial "docs/brand" . }}
{{ partial "docs/search" . }}
<!-- ... -->
</nav>
```

다시 [위 이미지](#메뉴-영역-개선하기)와 아래 개선하고 싶은 사항을 같이 보면서
어떤 점을 해결해야 하는지 생각해보겠습니다.

{{% hint %}}
1. 좌측에는 메뉴 영역을 표시합니다.
2. 프로필 사진을 표시합니다. 클릭하면 블로그 홈페이지와 연결됩니다.
3. 소셜 링크 또는 기능성 버튼을 표시합니다.
{{% /hint %}}

### 1. 메뉴 영역 위치 고정하기

일단, 결론적으로 제가 희망하는 디자인은 아래 이미지와 같습니다.
티스토리의 hELLO 테마입니다.

![티스토리 인터페이스](https://dl.dropboxusercontent.com/scl/fi/4xn1fjflju78w0jv76i7h/hugo-02-example-tistory.webp?rlkey=ixtuq0oo3xa26cgqfkwri1i4t&raw=1)

위 스타일을 구현하는데 있어 문제점은 메뉴 영역이 어중간하게 화면 좌측 중간에 위치한다는 점입니다.

Book 테마에서는 메뉴 영역에 배경색이 없어서 자연스러워 보이지만,
저는 메뉴 영역과 본문 영역의 경계를 명확히 하기 위해 배경색을 넣어보면서 해당 문제점을 발견했습니다.

![book-menu 영역에 회색 배경 스타일 적용 결과](https://dl.dropboxusercontent.com/scl/fi/r91v7nhof30antpb5wauo/hugo-13-book-menu-bg.webp?rlkey=vscar5p994g1xglcekt96r04l&raw=1)

이러한 스타일을 만들어낸 `assets/_main.scss` 파일의 `.book-menu` 부분을 확인해보니까
`flex` 속성이 적용되어 있었습니다. 메뉴, 본문, 목차 영역이 나란히 붙어있고
모니터의 너비가 길어질수록 좌우에 공백이 생기게 됩니다.

```scss
// assets/_main.scss

.book-menu {
  flex: 0 0 $menu-width;
  font-size: var(--font-size-smaller);
  // ...
}
```

메뉴 영역을 고정시키려면 `position: fixed;` 속성을 부여하고,
좌측 끝에 고정시키기 위해 `top: 0; left: 0;` 속성을 추가로 부여합니다.
나머지 `width: $menu-width; flex-shrink: 0;` 속성은 메뉴 영역의 너비를 고정시키는 스타일입니다.

참고로, 배경색은 `.book-menu` 하위의 `.book-menu-content` 요소에 적용했습니다.

```scss
.book-menu {
  position: fixed;
  top: 0;
  left: 0;
  width: $menu-width;
  flex-shrink: 0;

  .book-menu-content {
    background: var(--gray-200);
    // ...
  }
  // ...
}
```

아직 목차 영역의 차례는 아니지만, 목차 영역도 메뉴 영역과 동일하게 우측 끝에 고정시킬 필요가 있어
미리 적용하겠습니다.

목차 영역에 해당하는 `book-toc` 클래스가 적용된 요소를 대상으로
`top: 0; right: 0;` 부분만 다르게 하여 `.book-menu` 와 동일한 속성을 적용했습니다.

```scss
.book-toc {
  position: fixed;
  top: 0;
  right: 0;
  width: $menu-width;
  flex-shrink: 0;
  // ...
}
```

이렇게 적용했을 때, 본문 영역이 가운데 위치하지 않고 메뉴 영역에 치우친 쪽으로 정렬됩니다.

가운데 정렬하기 위해 본문 영역에 해당하는 `book-page` 클래스가 적용된 요소를 대상으로
`margin: 0 auto;` 속성을 적용하면 본문 영역 양 옆에 자동으로 동일한 크기의 여백을 만들어 줍니다.

초기 Book 테마에는 `min-width` 속성만 적용되어 있는데,
본문이 전체 영역을 차지해버려 여백이 만들어지지 않기 때문에 `max-width` 속성을 추가합니다.

`$body-max-width` 변수는 기본적으로 없을건데, 저는 `assets/_defaults.scss` 파일에서 `$body-max-width: 48rem;` 라인을 추가해 본문의 최대 너비가 48rem이 되도록 적용했습니다.
(앞으로의 진행 과정에서 기존에 존재하지 않는 변수를 정의하여 사용하는 경우가 있을텐데,
`$padding-24` 등 직관적으로 이해할 수 있는 변수에 대한 설명은 생략하겠습니다.)

```scss
.book-page {
  max-width: $body-max-width;
  min-width: $body-min-width;
  margin: 0 auto;
  flex: 1 1 0;
  padding: $padding-16;
}
```

위 스타일을 적용하면 아래 이미지와 같이 좌측 끝의 고정된 위치에 메뉴가 보여집니다.

![book-menu 영역 위치 고정 결과](https://dl.dropboxusercontent.com/scl/fi/2mr2dsohsmvog0vb36w9k/hugo-14-book-menu-pos.webp?rlkey=48smm08lv0n1ua8ojxv0w77wz&raw=1)

잘 보이기 위해 브라우저의 너비를 1500px 정도로 줄이고 캡쳐한 것인데,
여기서 브라우저의 너비를 1200px까지 줄여보니까 아래 이미지처럼
본문이 메뉴 및 목차 영역 뒤에 겹쳐서 숨어버리는 현상이 발생했습니다.

![book-menu 영역 간 겹치는 문제](https://dl.dropboxusercontent.com/scl/fi/4i0yr7l89580syf3z2b9f/hugo-15-book-menu-overlap.webp?rlkey=adw6l26t24bvbo17jqj7d4wmr&raw=1)

메뉴, 본문, 목차 영역이 flexible하게 정렬된 기존의 스타일과 다르게
메뉴와 목차 영역을 `position` 속성으로 양끝에 고정시키면서 본문 영역과 독립적인 요소가 되었습니다.
이로 인해 본문 영역이 메뉴와 목차 영역을 인식하지 못하고 침범하게 된 것입니다.

본문 메뉴가 메뉴와 목차 영역에 겹치지 않기 위해 다양한 해결 방법들이 있겠지만,
저는 Book 테마에서 이미 만들어놓은 반응형 디자인을 사용했습니다.

```scss
@media screen and (max-width: $mobile-breakpoint) {
  .book-menu {
    visibility: hidden;
    margin-inline-start: -$menu-width;
    z-index: 1;
  }

  .book-toc {
    display: none;
  }

  .book-header {
    display: block;
  }

 // ...

}
```

`@media screen and (max-width: $mobile-breakpoint)` 는
화면의 너비가 `$mobile-breakpoint` 보다 작아지는 경우를 기점으로 발생하는 조건문 입니다.

`assets/_defaults.scss` 파일에서 `$mobile-breakpoint` 는
`$menu-width + $body-min-width * 1.2 + $toc-width` 정도의 크기를 가집니다.
계산하면 56rem 정도 되는데, 화면의 너비가 이보다 작아지면 메뉴와 목차 영역을 숨기고 헤더를 표시하게 됩니다.
(헤더에 대한 설명은 헤더를 개선할 때 할 예정이지만, 헤더에서 메뉴와 목차를 펼치고 접을 수 있습니다.)

변경된 스타일에서 본문이 메뉴 및 목차와 겹치게 되는 지점은
메뉴와 목차 영역의 너비에 `$body-max-width` 길이를 더한 크기입니다.
즉, `$mobile-breakpoint` 에서 `$body-min-width` 를
`$body-max-width` 로 바꿔주기만 하면 됩니다.
이렇게 변경하고 다시 계산하면 93.6rem이 되어 본문이 메뉴 및 목차와 겹치지 않게 됩니다.

```scss
$mobile-breakpoint: $menu-width + $body-max-width * 1.2 + $toc-width !default;
```

이렇게 해결된 줄 알았지만, 32인치 모니터 및 모바일 기기를 사용하는 입장에서 문제가 없었던 것이고
13인치 노트북에서 블로그에 접속해보니까 모바일처럼 메뉴와 본문이 숨겨져 보였습니다.
그래서 이후에 단일 `$mobile-breakpoint` 를 `$wide-breakpoint`, `$toc-breakpoint`, `$menu-breakpoint` 3단계로 나누고 `$wide-breakpoint` 지점에서 본문의 너비를 한 번 줄여주어
11인치 너비까지는 메뉴와 목차가 전부 표시되도록 수정했습니다.
이 부분은 각자의 화면 크기에 맞춰 직접 진행해보시기 바랍니다.

### 2. 프로필 사진을 표시하기

현재까지의 변경사항을 적용하면 블로그가 아래와 같이 보여집니다.

![book-menu 영역 위치 고정 결과](https://dl.dropboxusercontent.com/scl/fi/2mr2dsohsmvog0vb36w9k/hugo-14-book-menu-pos.webp?rlkey=48smm08lv0n1ua8ojxv0w77wz&raw=1)

메뉴 영역에서 블로그 제목만 있고 눈길을 끌만한 이미지가 없습니다.
이번에는 제목 위에 프로필 사진을 추가해보겠습니다.

[메뉴 영역 개선하기](#메뉴-영역-개선하기) 문단의 첫 부분에서 설명했듯이
블로그 제목이 위치한 템플릿은 `layouts/_partials/docs/brand.html` 파일입니다.
파일의 내용은 다음과 같습니다.

```html
<!-- layouts/_partials/docs/brand.html -->

<h2 class="book-brand">
  <a class="flex align-center" href="{{ cond (not .Site.Home.File) .Sites.Default.Home.RelPermalink .Site.Home.RelPermalink }}">
    {{- with .Site.Params.BookLogo -}}
    <img src="{{ . | relURL }}" alt="{{ partial "docs/text/i18n" "Logo" }}" />
    {{- end -}}
    <span>{{ .Site.Title }}</span>
  </a>
</h2>
```

설정 파일에서 BookLogo 파라미터를 추가하면 제목 옆에 로고를 표시하는듯 하지만,
프로필 사진은 이보다 더 크게 제목 위에 나타낼 것이기 때문에 새로운 요소를 추가하겠습니다.
(프로필 사진을 원형으로 표현하는 CSS 스타일도 `assets/_custom.scss` 에 적용합니다.)

{{< tabs "profile-image" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/brand.html -->

<div class="sidebar-profile">
  <div class="profile-img-wrap">
    <a href="{{ .Site.BaseURL }}">
      <img src="{{ .Site.Params.BookMenu.profileImage }}" alt="Profile" class="profile-img" />
    </a>
  </div>
</div>

<h2 class="book-brand">
<!-- ... -->
</h2>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.profile-img-wrap {
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1rem;
}

.profile-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 50%;
  display: block;
}
```
{{% /tab %}}

{{< /tabs >}}

템플릿에서 `{{ .Site.Params.BookMenu.profileImage }}` 부분은
설정 파일에서 파라미터를 호출하는 부분입니다.
기본 설정 파일은 Hugo 프로젝트 루트 경로에 있는 `hugo.toml` 파일입니다.
해당 파일에서 `profileImage` 파라미터를 추가해야 하는데 YAML 형식에서는
이렇게 추가할 수 있습니다.

```yaml
# hugo.yaml

params:
  BookMenu:
    profileImage: "<프로필-사진-주소>"
```

프로필 사진의 주소까지 설정한 결과는 아래 이미지와 같습니다.

![book-menu 영역에 프로필 사진 추가](https://dl.dropboxusercontent.com/scl/fi/ctvdfak8bnphkkjcu08xf/hugo-16-book-menu-profile.webp?rlkey=vv1amtzqw7er0vezhsac2tmn2&raw=1)

### 3. 소셜 링크를 표시하기

다음으로, 프로필 사진 아래에, 그리고 블로그 제목 위에 소셜 링크를 표시할 것입니다.

`brand.html` 템플릿에 소셜 링크를 추가하면 되는 것은 이미 알고 있으므로
부가적인 설명없이 바로 추가해보겠습니다.

{{< tabs "social-links" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/brand.html -->

<div class="sidebar-profile">
  <div class="profile-img-wrap">
    <!-- ... -->
  </div>
  <div class="sidebar-social">
    <a href="{{ .Site.Params.BookMenu.githubLink }}" target="_blank" title="GitHub" {{ if not .Site.Params.BookMenu.githubLink }}class="disabled"{{ end }}>
      <i class="fa-brands fa-github"></i>
    </a>
    <a href="{{ .Site.Params.BookMenu.linkedinLink }}" target="_blank" title="LinkedIn" {{ if not .Site.Params.BookMenu.linkedinLink }}class="disabled"{{ end }}>
      <i class="fa-brands fa-linkedin"></i>
    </a>
    <a href="{{ .Site.Params.BookMenu.notionLink }}" target="_blank" title="Notion" {{ if not .Site.Params.BookMenu.notionLink }}class="disabled"{{ end }}>
      <i class="fa-brands fa-notion"></i>
    </a>
    <a href="{{ .Site.Params.BookMenu.twitterLink }}" target="_blank" title="Twitter" {{ if not .Site.Params.BookMenu.twitterLink }}class="disabled"{{ end }}>
      <i class="fa-brands fa-twitter"></i>
    </a>
  </div>
</div>

<h2 class="book-brand">
<!-- ... -->
</h2>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_custom.scss

.sidebar-social {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  width: 100%;
  margin-bottom: 1rem;
}

.sidebar-social a, i {
  color: --color-social-link;
  font-size: 2rem;
  flex: 1 1 0;
  text-align: center;
  transition: color 0.2s;
}

.sidebar-social a.disabled {
  pointer-events: none;
  opacity: 0.5;
  cursor: default;
}
```
{{% /tab %}}

{{< /tabs >}}

총 4개의 소셜 링크 [ 깃허브, 링크드인, 노션, 트위터 ] 를 추가했습니다.

`<a>` 태그에서 if 문을 사용하는 것을 볼 수 있는데, 이는 소셜 링크를 가리키는
`BookMenu.githubLink` 등의 파라미터가 설정 파일에 없을 경우 추가되는 구문입니다.
소셜 링크가 없으면 아래 CSS 설정에서 활용될 `disabled` 클래스가 적용되어 링크가 비활성화됩니다.

그리고, `<a>` 태그의 내용을 보면 알 수 있듯이 소셜 플랫폼에 대한 로고 이미지가 아니라
`<i>` 태그 아이콘을 사용하고 있습니다. 이것은 [Font Awesome](https://fontawesome.com/)에서
제공하는 스타일인데, 이를 사용하기 위해 외부 소스의 CSS 파일을 가져와야 합니다.

{{< bookmark "https://fontawesome.com/" >}}

[Book 테마 구조](#Book-테마-구조) 문단에서 했던 것처럼
`<head>` 태그 내에 들어갈 요소는 `layouts/_partials/docs/html-head.html`
템플릿에 추가합니다.

```html
<!-- layouts/_partials/docs/html-head.html -->

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css" crossorigin="anonymous" />
```

로고 이미지를 사용했다면 소셜 로고 크기를 조절하기 위해 `width` 속성을 적용해야 하지만,
텍스트 유형인 `<i>` 태그를 사용하기 때문에 `font-size` 속성으로 크기를 조절해주어야 합니다.
(`--color-social-link` 변수는 라이트 모드와 다크 모드에 따라 달라지는데,
아직 다크 모드를 추가하기 전이므로 `#fff` 색상을 적용해주세요.
변수가 정의되지 않아도 오류는 발생하지 않습니다.)

또한, 소설 링크를 설정 파일에서 추가하지 않았을 경우에 추가되는 `disabled` 클래스에
링크를 비활성화하는 스타일을 적용했습니다.

소셜 링크까지 추가한 결과는 아래 이미지와 같습니다.

![book-menu 영역에 소셜 링크 추가](https://dl.dropboxusercontent.com/scl/fi/wnx9vi7vszdijhyg6fyre/hugo-17-book-menu-social.webp?rlkey=2x53x3i816t9rshv25va0bjgi&raw=1)

추후에 카테고리, 태그 등을 추가하기 위해 메뉴 영역을 수정할 일이 있지만,
이번 게시글에서는 메뉴 영역에 대해 여기까지 진행하겠습니다.

## 목차 영역 개선하기

Book 테마에서 목차 영역은 아래 이미지에서 선택된 부분입니다.

![book-toc 영역 선택](https://dl.dropboxusercontent.com/scl/fi/s6ntlk5pgwkqi3kdtopnb/hugo-18-book-toc.webp?rlkey=b35n6qbjlk3sbateixn0jn4br&raw=1)

위 이미지는 메뉴 영역을 개선하기 전인 Example Site 기준이고,
[메뉴 영역을 위치 고정하기](#1-메뉴-영역-위치-고정하기) 문단에서
목차 영역도 우측 끝에 고정시켰습니다.
(너무 끝에 붙어있으면 보기 안좋아 `1.5rem` 수준의 여백을 추가했습니다.)

![book-toc 영역 위치 고정 결과](https://dl.dropboxusercontent.com/scl/fi/lh2apnezxbezik8n5hpan/hugo-19-book-toc-pos.webp?rlkey=tuwvadpunh2try3jvw3lptvpz&raw=1)

목차 영역은 `book-toc` 클래스가 적용된 요소로 감싸져 있으며, `baseof.html` 파일에서
다음과 같이 `toc` 템플릿을 호출합니다.

```html
<!-- baseof.html -->

{{ define "toc-container" }}
{{ if partial "docs/toc-show" . }}
<aside class="book-toc">
  <div class="book-toc-content">
    {{ template "toc" . }}
  </div>
</aside>
{{ end }}
{{ end }}
```

`toc.html` 템플릿 파일은 `layouts/_partials/docs/` 경로에 있는데,
내용은 별 거 없습니다. Hugo 공식문서
[TableOfContents](https://gohugo.io/methods/page/tableofcontents/)를
보면 `{{ .TableOfContents }}` 템플릿을 통해 목차를 만들 수 있다고 안내되어 있습니다.
Book 테마에서도 Hugo에 내장된 목차 템플릿을 호출하여 목차를 생성합니다.

```html
<!-- layouts/_partials/docs/toc.html -->

{{ partial "docs/inject/toc-before" . }}
{{ .TableOfContents }}
{{ partial "docs/inject/toc-after" . }}
```

참고로, 같은 경로에 있는 `toc-show.html` 파일은 `baseof.html` 에서
`book-toc` 를 생성할지 결정하는 역할을 수행하는데
내용을 보면 `nav#TableOfContents` 영역이 있는지 검사합니다.

```html
<!-- layouts/_partials/docs/toc-show.html -->

{{ return default
  (not (eq .TableOfContents "<nav id=\"TableOfContents\"></nav>"))
  (default .Site.Params.BookToC .Params.BookToC)
}}
```

다시 Hugo 공식문서
[TableOfContents](https://gohugo.io/methods/page/tableofcontents/)를
보면 목차 영역이 아래 HTML 형태로 만들어지는 것을 알 수 있습니다.
`#TableOfContents` 요소를 대상으로 CSS 스타일을 적용할 일이 있어서 알고 있으면 좋습니다.

```
<nav id="TableOfContents">
  <ul>
    <li><a href="#section-1">Section 1</a>
      <ul>
        <li><a href="#section-11">Section 1.1</a></li>
        <li><a href="#section-12">Section 1.2</a></li>
      </ul>
    </li>
    <li><a href="#section-2">Section 2</a></li>
  </ul>
</nav>
```

목차 영역에서는 어떤 점을 해결하면 좋을지 생각해보겠습니다.

{{% hint %}}
1. 목차와 본문의 사이에 목차의 길이만큼 구분선을 추가합니다.
2. 스크롤이 위치한 목차를 하이라이트로 강조합니다.
3. 우측 하단의 고정된 위치에 이동 버튼을 추가합니다.
   - 맨 위로 이동, 맨 아래로 이동, 뒤로 가기 버튼을 세로로 나열합니다.
{{% /hint %}}

### 1. 목차 옆에 구분선 추가하기

단순히 목차 영역에 `border` 속성을 추가하면 되지만, 목차 영역을 어디까지 볼 것인지 고려해야 합니다.

`book-toc` 클래스가 적용된 요소는 목차를 포함한 우측 사이드바 전체 영역입니다.
`book-toc` 클래스를 대상으로 `border` 속성을 추가하면 본문과 목차 사이에
끝없이 긴 라인이 만들어질 것입니다.

제가 원하는 것은 목차 텍스트가 있는 영역에만 `border` 속성을 추가하는 것입니다.

Book 테마의 `toc.html` 템플릿만 보았다면 어디에 `border` 속성을 추가해야 하는지
알 수 없지만, Hugo 공식문서
[TableOfContents](https://gohugo.io/methods/page/tableofcontents/)를
통해 `#TableOfContents` 요소가 목차 텍스트가 있는 영역이란 것을 확인했습니다.

이제 `assets/_main.scss` 파일에 스타일을 추가하겠습니다.

```scss
// assets/_main.scss

#TableOfContents {
  margin-top: 2rem;
  padding-left: 1rem;
  border-left: 1px solid var(--toc-font-color);

  a {
    color: var(--toc-font-color);
  }
}
```

단순히 `border` 속성만 추가하면 구분선과 목차 텍스트가 딱 붙어버리기 때문에
적당한 여백을 추가했습니다.

저는 구분선의 색상을 나타내는 `--toc-font-color` 변수에 검은색(`black`)을 지정했습니다.
추가로, 목차를 구성하는 `<a>` 태그가 링크와 동일한 파란색 글씨색을 가져서 보기 안좋아
구분선과 동일한 색상을 적용했는데, 이 부분은 취향에 맞게 수정해보시기 바랍니다.

![book-toc 영역에 구분선 추가](https://dl.dropboxusercontent.com/scl/fi/ji6qysyrb41vogsh95g2z/hugo-20-book-toc-border.webp?rlkey=wcu0nu9xg5oes1im89ds7tclt&raw=1)

목차 영역을 돋보이기 위해 잠시 본문의 헤딩을 늘렸습니다.

### 2. 목차 하이라이트 적용하기

독자에게 게시글에서 자신이 어떤 위치에 있는지 알려주는 것은 가독성을 크게 향상시킬 수 있다고 생각합니다.

하지만, 이러한 기능을 구현하는 방법을 몰라 코파일럿의 Sonnet 4.5 모델에게
목차 하이라이트를 구현하는 방법을 물어보았습니다.
프롬프트는 특별히 길게 쓴건 아니라서 따로 저장해두진 않았는데,
에이전트 모드로 Book 테마 경로를 첨부하여 문맥을 제공하였고 아래와 같은 코드가 생성되었습니다.

{{< tabs "toc-highlight" >}}

{{% tab "JavaScript" %}}
```js
// assets/toc-highlight.js

document.addEventListener('DOMContentLoaded', function() {
    const headings = document.querySelectorAll('h2[id], h3[id]');

    function getVisibleToc() {
        const bookToc = document.querySelector('.book-toc');

        if (bookToc) {
            const style = window.getComputedStyle(bookToc);
            if (style.visibility === 'visible') {
                return bookToc.querySelector('#TableOfContents');
            }
        }

        return document.querySelector('#TableOfContents');
    }

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            const id = entry.target.getAttribute('id');
            const toc = getVisibleToc()
            const tocLinks = toc.querySelectorAll('a');
            const correspondingTocLink = toc.querySelector(`a[href="#${id}"]`);

            if (correspondingTocLink) {
                if (entry.isIntersecting) {
                    tocLinks.forEach(link => link.classList.remove('active'));
                    correspondingTocLink.classList.add('active');
                }
            }
        });
    }, {
        rootMargin: '0px 0px -70% 0px'
    });

    headings.forEach(heading => {
        observer.observe(heading);
    });
});
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

#TableOfContents {
  // ...

  a.active {
    color: var(--toc-active-color);
    font-weight: bold;
  }
}
```
{{% /tab %}}

{{< /tabs >}}

자바스크립트로 기능을 정의하는데 익숙하지는 않지만,
함수명 등으로 유추해봤을 때 `getVisibleToc()` 함수에서 `#TableOfContents` 요소를 가져와
`toc` 상수에 할당하는데 사용되는 것으로 보입니다.
그리고, `toc` 상수로부터 `<a>` 태그들을 꺼내서 순회하면서 `<a>` 태그가 가리키는
헤딩 요소가 화면에 들어오면 `active` 클래스를 추가한다고 해석할 수 있습니다.

CSS 스타일을 통해 `active` 클래스인 요소에 대해서만 하이라이트를 적용했습니다.
`--toc-active-color` 변수는 제가 입맛에 맞게 바꾼 색상인데
라이트 모드에서는 다른 목차 글씨 색상과 동일한 검은색(`black`)이며,
`font-weight: bold;` 속성으로 글씨를 굵게하는 것으로 하이라이트를 표현했습니다.

이렇게하면 목차 하이라이트가 적용되지만, `assets/` 경로에 새로 추가한 자바스크립트 파일은
`layouts/_partials/docs/html-head.html` 템플릿에서 호출해주어야 합니다.

```html
<!-- layouts/_partials/docs/html-head.html -->

{{- $tocHighlightJS := resources.Get "toc-highlight.js" | resources.ExecuteAsTemplate "toc-highlightjs" . | resources.Minify | resources.Fingerprint }}
<script defer src="{{ partial "docs/links/resource-precache" $tocHighlightJS }}" {{ template "integrity" $tocHighlightJS }}></script>
```

이렇게 적용하면 아래 이미지와 같이 현재 보고 있는 헤딩이 목차에서 하이라이트됩니다.
스크롤을 할만큼 본문이 길지 않지만, 이미지를 기준으로 "제목 2-3" 헤딩을 현재 보고 있는 것으로 인식하여
목차에서 "제목 2-3" 항목이 굵은 글씨로 강조되고 있습니다.

![book-toc 영역에 하이라이트 기능 추가](https://dl.dropboxusercontent.com/scl/fi/0ncrj5rqapnj3ikwqzx70/hugo-21-book-toc-highlight.webp?rlkey=cune4iwe36oamxeszzmbtawyc&raw=1)

### 3. 스크롤 이동 버튼 추가하기

제가 경험해 본 웹사이트 중에서 우측 하단에 스크롤 이동 버튼을 놓는 경우가 종종 있었습니다.
PC에서는 굳이 이러한 버튼을 안써도 키보드 단축키로 이동하기 쉽지만,
모바일에서는 그 긴 스크롤을 일일이 내리기 불편해 있으면 매우 편한 기능이라고 생각합니다.

그렇다면 이 버튼을 어느 템플릿에 넣으면 좋을지 생각해봐야 합니다.

새로운 템플릿을 만들어서 `toc.html` 템플릿에서 호출할 수도 있지만,
저는 `layouts/_partials/docs/inject/` 경로에 있는
`toc-after.html` 템플릿에 추가하는게 적절하다고 생각했습니다.

이유는 `toc.html` 템플릿에서 이미 해당 템플릿을 호출하고 있고,
`toc-after.html` 템플릿 자체는 비어있는 파일이라
새로운 템플릿 파일을 만드는 것과 별 차이가 없다고 판단했기 때문입니다.

```html
<!-- layouts/_partials/docs/toc.html -->

{{ partial "docs/inject/toc-before" . }}
{{ .TableOfContents }}
{{ partial "docs/inject/toc-after" . }}
```

`toc-after.html` 에 다음 3개의 버튼을 추가했습니다. `onclick` 이벤트에 대해서
위에서부터 스크롤을 맨 위로, 스크롤을 맨 아래로, 그리고 이전 페이지로 이동하는 3가지 기능을
하는 버튼입니다.

{{< tabs "book-nav" >}}

{{% tab "HTML" %}}
```html
<!-- layouts/_partials/docs/inject/toc-after.html -->

<div class="book-nav">

  <button class="book-nav-btn3" onclick="window.scrollTo({top: 0, behavior: 'smooth'})" title="Go to top">
    <i class="fa fa-chevron-up"></i>
  </button>

  <button class="book-nav-btn3" onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})" title="Go to bottom">
    <i class="fa fa-chevron-down"></i>

  <button class="book-nav-btn3" onclick="history.back()" title="Go back">
    <i class="fa-solid fa-arrow-left"></i>
  </button>

</div>
```
{{% /tab %}}

{{% tab "CSS" %}}
```scss
// assets/_main.scss

.book-nav, .book-mobile-nav {
  position: fixed;
  bottom: 0;
  right: 0;

  margin-bottom: $padding-16;
  margin-right: $padding-16;

  display: flex;
  align-items: flex-end;
  flex-direction: column;

  .book-nav-btn3 {
    width: $font-size-40;
    height: $font-size-40;
    margin: $padding-4;

    border: 0px;
    border-radius: 50%;
    background: var(--gray-200);
    color: var(--body-font-color);

    cursor: pointer;

    i {
      font-size: $font-size-20;
    }
  }

  // ...
}
```
{{% /tab %}}

{{% /tabs %}}

CSS 스타일에서 스크롤 이동 버튼을 표현하는데 핵심적인 속성은 `border-radius: 50%;` 및
`background: var(--gray-200);` 입니다.
Font Awesome에서 가져온 단순한 화살표 아이콘을 동그란 버튼처럼 가공해 보기 좋아졌습니다.
그런데, 이렇게 적용했을 때 스크롤 이동 버튼이 우측 끝에 너무 딱 붙어있어서
`book-toc` 영역 전체에 `margin-right: $padding-48;` 속성을 추가했습니다.

스크롤 이동 버튼까지 추가한 결과는 아래와 같습니다.
(하단에 있는 버튼이 잘 보이기 위해 브라우저 높이를 450px 정도로 줄였습니다.)

![book-toc 영역 하단에 스크롤 이동 버튼 추가](https://dl.dropboxusercontent.com/scl/fi/dsdk1qgd6ymnaziu2g83o/hugo-22-book-toc-button.webp?rlkey=ycvts8xntyix655ym1m6nsvhs&raw=1)

목차 영역은 여기서 완성입니다.
나중에 다크 모드를 적용할 때 전용 색상 스타일을 추가할 일이 있지만,
더 이상 목차 영역에 새로운 기능을 추가하는 경우는 없습니다.

## 헤더 영역 개선하기

헤더 영역은 브라우저 너비가 일정 크기 이상 줄어들 때만 나타나는 모바일 전용 헤더입니다.

![모바일 화면에서 book-header가 보이는 모습](https://dl.dropboxusercontent.com/scl/fi/tnmxpbfinoqf0o3z0wi72/hugo-23-book-header.webp?rlkey=tc7h4bspbn2ea5scnjqbqrdl8&raw=1)

헤더 영역은 `book-header` 클래스가 적용된 요소로 감싸져 있으며, `baseof.html` 파일에서
다음과 같이 `header` 템플릿을 호출합니다. `book-header` 의 바로 위를 보면
본문을 나타내는 `book-page` 요소의 하위에 헤더 영역이 있음을 알 수 있습니다.

```html
<!-- baseof.html -->

    <!-- ... -->
    <div class="book-page">
      <header class="book-header">
        {{ template "header" . }} <!-- Mobile layout header -->
      </header>
    <!-- ... -->
```

`header.html` 템플릿 파일은 `layouts/_partials/docs/` 경로에 있는데
내용은 직관적으로 읽힙니다. 메뉴 버튼을 의미하는 `menu-control` 요소,
제목을 가리키는 `<h3>` 태그, 그리고 목차 버튼을 의미하는 `toc-control` 요소가 있습니다.

```html
<!-- layouts/_partials/docs/header.html -->

<div class="flex align-center justify-between">
  <label for="menu-control">
    <img src="{{ partial "docs/icon" "menu" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Menu" }}" />
  </label>

  <h3>{{ partial "docs/title" . }}</h3>

  <label for="toc-control">
    {{ if partial "docs/toc-show" . }}
    <img src="{{ partial "docs/icon" "toc" }}" class="book-icon" alt="{{ partial "docs/text/i18n" "Table of Contents" }}" />
    {{ end }}
  </label>
</div>
```

헤더 영역에서는 어떤 점을 해결하면 좋을지 생각해보겠습니다.

{{% hint %}}
1. 헤더 영역의 가운데에는 블로그 제목을 표시하고 홈페이지로 이동하는 링크를 설정합니다.
2. 헤더 영역은 반투명한 배경색을 가지고 스크롤 위치에 관계없이 고정됩니다.
{{% /hint %}}

헤더 영역은 특별히 수정할건 없습니다.

먼저, 제목에 홈페이지로 이동하는 링크를 거는건 아래처럼 간단합니다.

```html
<h3>
  <a href="{{ .Site.BaseURL }}" class="site-title">{{ .Site.Title }}</a>
</h3>
```

다음으로, 헤더에 반투명한 배경색을 넣고 상단에 고정하는건 아래 스타일을 적용하면 됩니다.

```scss
// assets/_main.scss

.book-header {
  display: block;
  position: sticky;
  opacity: 0.9;
  top: 0;
  background-color: var(--body-background);
  padding: 1rem;
}
```

기존 Book 테마에서는 모바일 화면에서 스크롤하면 헤더가 사라져버려
메뉴 및 목차 버튼을 클릭하기 위해 매번 맨 위로 이동해야 하는 불편함이 있었습니다.

그래서 헤더 영역을 상단에 고정시켜 봤는데, 문제가 이 버튼을 클릭하면 자동으로 맨 위로 올라가 버립니다.
결국 의도했던 동작을 수행하지 못해 아직까지 해결책을 찾고 있는데,
해결되었다면 해당 게시글에 업데이트 하겠습니다.

![book-header 영역에 반투명한 배경 추가](https://dl.dropboxusercontent.com/scl/fi/t71bdlejum4fopmg4ic1s/hugo-24-book-header-bg.webp?rlkey=zvh85hvkiwik4b3x0zy7do81a&raw=1)

스크롤을 내려보면 헤더가 반투명하게 보이면서 헤더 밑에 있는 본문을 읽을 수 있습니다.

다음 게시글에서는 카테고리와 태그 기능을 추가하고, 관련 게시글을 목록을 보여주는 템플릿을
작성하는 과정을 진행하겠습니다. 카테고리와 태그 기능은 특히 내용이 길어서
다음 게시글로 분리하게 되었는데, 다음 게시글에서 이를 포함한 메뉴 영역을 완성할 수 있게 됩니다.
