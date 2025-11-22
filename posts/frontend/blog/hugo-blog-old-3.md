---
title: "Hugo 블로그 만들기 [2022년] (3) - 테마 커스터마이징"
date: "2022-09-08T15:52:12+0900"
layout: "post"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "PaperMod", "Github", "Github Pages", "Go Template", "KaTex", "검색 엔진"]
---

## Hugo 블로그 만들기 (3) - 테마 커스터마이징

블로그를 구성할 때 기술적, 시간적 한계 때문에 이미 만들어진 테마를 사용하게 됩니다.   
제가 Hugo 블로그를 만들 때도 이러한 문제 때문에 [PaperMod](https://github.com/adityatelange/hugo-PaperMod) 테마를 사용했지만,   
블로그를 보다보면 만족스럽지 못한 부분이 발견됩니다.

이번 포스트에서는 제가 PaperMod 테마를 커스터마이징한 과정을 안내해드리겠습니다.

### Archive, Search 추가하기

PaperMod 테마를 가져오면서 가장 신경쓰였던 부분은   
메인 메뉴가 Categories, Tags 두 개 뿐이었단 점입니다.

Archive는 그렇다쳐도 Search 기능은 빼먹을 수 없는 부분이라 생각하기 때문에,   
Hugo 및 PaperMod 내 이슈를 참고하여 관련된 내용을 탐색했습니다.

다행히 PaperMod 테마에서 해당 기능을 연결하지 않았을 뿐,   
기능에 대한 레이아웃은 존재하기 때문에 `content/` 디렉토리 아래 다음과 같은 파일을 추가했습니다.

```yaml
# content/archive.md
---
title: "Archive"
layout: "archives"
url: "/archive"
summary: "archive"
---
```

```yaml
# content/search.md
---
title: "Search"
layout: "search"
url: "/search"
summary: "search"
---
```

추가로, 설정에서도 해당 파일을 인식해야되기 때문에 다음과 같은 설정을 추가했습니다.   
`post/` 외에 다른 디렉토리를 등록하고 싶은 경우에도 해당 키값을 활용할 수 있습니다.

```yaml
params:
  mainsections: ["page", "post", "archive", "search"]
```

마지막으로, 메인 메뉴에서 해당 링크로 이동하기 위한 바로가기를 추가했습니다.   
여기에는 카테고리, 태그 등이 있을건데 `weight` 값을 통해 적절하게 위치를 조정할 수 있습니다.

```yaml
menu:
  main:
    - identifier: archive
      name: Archive
      url: /archive/
      weight: 10
    - identifier: search
      name: Search
      url: /search/
      weight: 20
```

위와 같은 과정을 통해 Archive, Search 기능을 추가했습니다.

![archive](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/archive.png?raw=true)

![search](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/search.png?raw=true)

---

## 검색 엔진 등록하기

검색 엔진에 등록하기 위한 과정은 [해당 영상](https://youtu.be/OxRZrg0u6h4)을 참고해주시기 바랍니다.   
저는 위 과정에서 블로그 내에 추가해야 할 Site Verification Tag를 추가하는 법을 전달드리겠습니다.

PaperMod 테마에서는 아래처럼 해당 부분이 만들어져 있기 때문에 크게 걱정할 필요는 없습니다.   
아래는 `layouts/partials/` 내에 `head.html` 파일에서 가져왔습니다.

```html
{{- if site.Params.analytics.google.SiteVerificationTag }}
<meta name="google-site-verification" content="{{ site.Params.analytics.google.SiteVerificationTag }}">
{{- end }}
{{- if site.Params.analytics.yandex.SiteVerificationTag }}
<meta name="yandex-verification" content="{{ site.Params.analytics.yandex.SiteVerificationTag }}">
{{- end }}
{{- if site.Params.analytics.bing.SiteVerificationTag }}
<meta name="msvalidate.01" content="{{ site.Params.analytics.bing.SiteVerificationTag }}">
{{- end }}
{{- if site.Params.analytics.naver.SiteVerificationTag }}
<meta name="naver-site-verification" content="{{ site.Params.analytics.naver.SiteVerificationTag }}">
{{- end }}
```

구글, 네이버 외에 Bing, Yandex를 지원하며 저는 다음과 같이 구글과 네이버만 설정했습니다.

```yaml
params:
  analytics:
    google:
      SiteVerificationTag: <YOUR-VERIFICATION-TAG>
    naver:
      SiteVerificationTag: <YOUR-VERIFICATION-TAG>
```

번외로 Google Tag 등 head에 추가로 입력할 부분이 있다면,   
동일한 위치에 `extend_head.html`을 사용할 수 있습니다.   
아래는 제가 `extend_head.html` 내에 Google Tag를 위한 스크립트를 추가한 부분입니다.

```html
{{- if site.GoogleAnalytics }}
{{- /* Google tag (gtag.js) */}}
<script async src="https://www.googletagmanager.com/gtag/js?id={{ site.GoogleAnalytics }}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', '{{ site.GoogleAnalytics }}');
</script>
{{- end }}
```

---

## KaTex 추가하기

[KaTex](https://katex.org/)는 웹에서 수식을 표현하기 위한 방식입니다.   
제 과거 게시글엔 KaTex 표기법을 사용한 것이 존재하는데 이것이 제대로 표시되지 않는 문제를 발견했습니다.

저는 공식 문서 대신 Stack Overflow 등을 참고해 아래 코드를 `extend_head.html`에 추가했는데,   
아쉽게도 출처는 남겨두지 못했습니다.

```html
<script>
  MathJax = {
    tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$','$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true
    },
    options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
    }
  };

  window.addEventListener('load', (event) => {
    document.querySelectorAll("mjx-container").forEach(function(x){
      x.parentElement.classList += 'has-jax'})
  });
</script>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script type="text/javascript" id="MathJax-script" async
src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

---

## Cover 간편하게 지정하기

저는 Github 저장소 내에 업로드한 이미지 주소를 속성값에 연결해 블로그 이미지를 표시하는데,   
게시글을 작성할 때마다 지정하게 되는 Cover 이미지의 경우 매번 전체 링크를 지정하는게 불편했습니다.

대표적으로 해당 게시글의 Cover 이미지 주소는 다음과 같습니다.

```html
https://github.com/minyeamer/til/blob/main/.media/covers/hugo-logo.png?raw=true
```

저는 여기서 `hugo-logo.png`를 제외한 앞뒤의 요소가 불필요하다는 것을 인식했고   
설정 파일에 다음과 같이 `prefix`, `suffix`라는 키값으로 지정하게 처리했습니다.

```yaml
params:
  cover:
    prefix: "https://github.com/minyeamer/til/blob/main/.media/covers/"
    suffix: "?raw=true"
```

그리고 해당 설정을 적용시키기 위해 실질적으로 Cover 이미지를 표시하는
`layouts/partials/` 아래 `cover.html` 파일을 수정했습니다.   
주석으로 지정된 부분이 원본이며, `image` 키값의 앞뒤로 `prefix`와 `suffix`를 덧붙였습니다.

```html
<!-- {{- if $addLink }}<a href="{{ (.Params.cover.image) | absURL }}" target="_blank"
    rel="noopener noreferrer">{{ end -}}
    <img loading="lazy" src="{{ (.Params.cover.image) | absURL }}" alt="{{ $alt }}"> -->

{{- if $addLink }}<a href="{{ if site.Params.cover.prefix }}{{ site.Params.cover.prefix }}{{ end }}{{ .Params.cover.image }}{{ if site.Params.cover.suffix }}{{ site.Params.cover.suffix }}{{ end }}" target="_blank"
    rel="noopener noreferrer">{{ end -}}
    <img loading="lazy" src="{{ if site.Params.cover.prefix }}{{ site.Params.cover.prefix }}{{ end }}{{ .Params.cover.image }}{{ if site.Params.cover.suffix }}{{ site.Params.cover.suffix }}{{ end }}" alt="{{ $alt }}">
```

---

## 기타 설정

### 너비 설정

초기에 PaperMod 테마를 사용할 때 너비가 좁아 불편한 느낌이 있었습니다.   
해당 설정은 css 파일로 지정할 것이라 생각했고,   
`assets/css/core/` 경로에 있는 `theme-vars.css` 파일을 발견해 다음과 같이 수정했습니다.   
기존 720px에서 900px로 늘어나 쾌적하게 블로그를 볼 수 있게 되었습니다.

```css
:root {
    --main-width: 900px;
```

### 새 탭에서 링크 열기

다음으로 관심을 가진 건 깃허브에서 매번 불편하게 생각했던 링크 오픈 방식인데,   
개인적으로는 현재 탭이 아닌 새 탭에서 열리는 방식을 선호하기 때문에 해당 부분의 수정이 필요했습니다.   
다행히 Hugo 이슈 내용 중 [다음과 같은 답변](https://discourse.gohugo.io/t/simple-way-to-open-in-a-new-tab/28677/5)을 참고해 파일을 추가했습니다.   
아래는 `layouts/_default/_markup/` 경로에 추가한 `render-link.html` 파일입니다.

```html
<a href="{{ .Destination | safeURL }}"{{ with .Title}} title="{{ . }}"{{ end }}{{ if strings.HasPrefix .Destination "http" }} target="_blank" rel="noopener"{{ end }}>{{ .Text | safeHTML }}</a>
```

### 포스트 수정

마지막으로 포스트 수정 버튼에 문제를 인식했습니다.   
물론, 모든 포스트는 로컬에서 작성하고 수정하지만, 오류가 발생하는 버튼을 그냥 놔둘 수는 없습니다.   
Go에 대해 잘 알지 못해 최선의 기능이라고 생각하지는 않지만,   
검색을 통해 발견한 `replace` 함수를 사용해 기존 경로에서 오류를 일으키는 부분을 제거했습니다.

```html
{{- if or .Params.editPost.URL site.Params.editPost.URL -}}
{{- $fileUrlPath := path.Join .File.Path }}

{{- if or .Params.author site.Params.author (.Param "ShowReadingTime") (not .Date.IsZero) .IsTranslated }}&nbsp;|&nbsp;{{- end -}}
<a href='{{ .Params.editPost.URL | default site.Params.editPost.URL }}{{ if .Params.editPost.appendFilePath | default ( site.Params.editPost.appendFilePath | default false ) }}/{{ replace $fileUrlPath site.Params.editPost.ignoreFilePath "" 1 }}{{ end }}' rel="noopener noreferrer" target="_blank">
    {{- .Params.editPost.Text | default (site.Params.editPost.Text | default (i18n "edit_post" | default "Edit")) -}}
</a>
{{- end }}
```

---

## 개선사항

현재 PaperMod 테마의 카테고리는 아래 그림처럼 태그와 동일한 리스트 템플릿을 사용하는데,   
개인적으로는 트리 형태의 계층식 카테고리를 선호합니다.

![categories](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/categories.png?raw=true)

언제나처럼 PaperMod 이슈를 탐색하던 중 [해당 이슈](https://github.com/adityatelange/hugo-PaperMod/issues/24)를 발견했는데,   
아래 그림처럼 제가 머릿속에 그리던 방식을 그대로 표현하여 큰 관심을 가졌습니다.

![categories-tree](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/categories-tree.png?raw=true)

해당 기능을 구현한 분께 메일을 보내 참고 자료를 얻었지만,   
아직까진 시간적 여유가 부족해 해당 작업을 처리하지 못한 상태입니다.

향후 개선되기를 희망하는 부분입니다.

---

## 마치며

Hugo 블로그 만들기 시리즈의 마지막으로 커스터마이징 과정을 소개했습니다.   
커스터마이징은 그때그때 필요하다고 생각하는 부분을 수정하는 것이기 때문에   
본인의 입맛에 맛는 블로그를 만들기 위해서는 테마의 구조를 이해해야 합니다.

아직 Go에 대해서도 잘 몰라 검색을 통해 요령껏 찾아내는 수준이지만,   
Go에 익숙해지게 된다면 동적 TOC 등 기능의 개선을 기대해 볼 수 있을 것입니다.

해당 게시글을 통해 Hugo 블로그 만들기에 도움이 되었으면 좋겠습니다.

### 참고 자료

- [EP09. 구글, 네이버 검색엔진 등록하기](https://youtu.be/OxRZrg0u6h4)
- [KaTex](https://katex.org/)
- [Simple way to open in a new tab](https://discourse.gohugo.io/t/simple-way-to-open-in-a-new-tab/28677)
- [[Feature][Discussion] Tree-style category list page](https://github.com/adityatelange/hugo-PaperMod/issues/24)
