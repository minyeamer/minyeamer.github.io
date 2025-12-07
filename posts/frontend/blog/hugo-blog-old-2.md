---
title: "Hugo 블로그 만들기 [2022년] (2) - Utterances 댓글 시스템 설치 및 설정"
date: "2022-09-08T14:39:22+0900"
layout: "post"
description: >
  Hugo PaperMod 테마에 Utterances 댓글 기능을 추가하는 방법입니다.
  Github Issues 기반의 무료 댓글 시스템 Utterances 설치, 레이아웃 커스터마이징, 동적 설정 방법을 설명합니다.
  Disqus 대신 Utterances를 선택하는 이유와 실제 적용 과정을 다룹니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/w0zho4wlgq6m8db5mvn9k/hugo-00-cover.webp?rlkey=et2tlzgb0h6blgf8klzbqjxem&dl=0"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/hp31764bfpm55wanzj5le/hugo-00-logo.webp?rlkey=rkezagmfupugt717a5fx2xqs2&dl=0"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Utterances", "댓글 시스템", "Github Issues", "PaperMod", "Github", "블로그 만들기", "Blog", "개발 블로그"]
---

Hugo 블로그는 기본적으로 댓글 기능을 제공하지는 않습니다.

제가 사용하는 PaperMod 테마에서는 서드파티 서비스인 `Disqus`를 위한 레이아웃이 존재하지만,
저는 기본적인 블로그 운영을 Github 플랫폼 내에서 구성하고 싶기 때문에 다른 기능을 사용해보려 합니다.

이번 포스트에서는 Utterances 댓글 기능을 추가하는 방법을 안내해드리겠습니다.

## Utterances 설치하기

Utterances는 Github issues 기반으로 댓글을 관리하는 기능입니다.
무료 플랜에서 광고가 붙는 `Disqus`와 다르게 별도의 유료 플랜이 없어 간편하게 사용할 수 있습니다.

Utterances 설치는 단순히 레이아웃 상에서 댓글이 위치할 곳에 자바스크립트 코드를 삽입하면 됩니다.
하지만, 선행적으로 [해당 링크](https://github.com/marketplace/utterances)를 통해
Utterances와 연동시킬 저장소를 등록해야 합니다.

![Application > utterances](https://dl.dropboxusercontent.com/scl/fi/w5cuo428u0kss2tkie8kw/hugo-2022-02-utterances-application.webp?rlkey=dzktkckia9fbmjvl0cyng9fie&dl=0)

무료 플랜 선택 후 Utterances를 적용할 저장소를 선택하게 되는데
모든 저장소를 지정해도 되지만, 저는 댓글을 관리할 저장소만 지정하겠습니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/6wg0cqovib47bd1i0a3t8/hugo-2022-03-utterances-install.webp?rlkey=1qpnaqk2hsr90609cap0s3p3w&dl=0"
  alt="Install utterances"
  max-width="550px"
  align="center" >}}

간단하게 Utterances 적용이 완료되면 아래 공식 문서 페이지로 이동합니다.

{{< bookmark "https://utteranc.es/" >}}

공식 문서에서 저장소 이름, 이슈 맵핑 방식 등을 지정하면 해당하는 스크립트가 생성됩니다.
저는 포스트 제목이 변경될 수 있기 때문에 `pathname`을 기준으로 이슈를 생성하고,
사용자 시스템 설정에 호환되는 Preferred Color Scheme 테마를 사용합니다.

```html
<script src="https://utteranc.es/client.js"
        repo="[ENTER REPO HERE]"
        issue-term="pathname"
        theme="github-light"
        crossorigin="anonymous"
        async>
</script>
```

## 스크립트 삽입하기

PaperMod 테마에는 `layouts/partials/` 위치에 `comments.html` 이라는 레이아웃이 존재합니다.
테마 별로 레이아웃이 다르기 때문에 다른 테마의 경우 이슈 등을 참고하여 구조를 파악할 필요가 있습니다.

```html
{{- /* Comments area start */ -}}
{{- /* to add comments read => https://gohugo.io/content-management/comments/ */ -}}
{{- if $.Site.Params.utteranc.enable -}}
    <script src="https://utteranc.es/client.js"
            repo="{{ .Site.Params.utteranc.repo }}"
            issue-term="{{ .Site.Params.utteranc.issueTerm }}"
            {{- if $.Site.Params.utteranc.label -}}label="{{ .Site.Params.utteranc.label }}"{{- end }}
            theme="{{ .Site.Params.utteranc.theme }}"
            crossorigin="{{ .Site.Params.utteranc.crossorigin }}"
            async>
    </script>
{{- end }}
{{- /* Comments area end */ -}}
```

단순하게 레이아웃에 스크립트를 붙여넣어도 되지만,
향후 속성값을 변경하기 위해 불필요하게 테마를 수정하는 경우를 방지하기 위해
설정 파일을 통해 동적으로 속성값을 집어넣도록 설정했습니다.

Hugo HTML 코드 내에 이중 중괄호(`{{ }}`)는 Go 템플릿을 코딩하는 부분으로,
아래와 같은 설정 파일을 읽어서 각각의 키에 해당하는 값을 할당합니다.

이에 대한 자세한 사용법은 [Hugo 공식 문서](https://gohugo.io/templates/introduction/)를 참조할 수 있습니다.

```yaml
params:
  utteranc:
    enable: true
    repo: "minyeamer/minyeamer.github.io"
    issueTerm: "pathname"
    label: "comments"
    theme: "preferred-color-scheme"
    crossorigin: "anonymous"
```

정상적으로 스크립트가 삽입되었다면 아래와 같이 댓글을 입력하는 부분이 표시됩니다.

![powered by utteranc.es](https://dl.dropboxusercontent.com/scl/fi/odmsjy5hw3en7k8rhtigt/hugo-2022-04-utterances-ui.webp?rlkey=1je72ah0ufukuppee7u5j13ui&dl=0)

댓글 기능이 정상적으로 적용되는지 확인하기 위해 실험적으로 댓글을 작성해봅니다.
저도 과거 게시글에 댓글을 작성하여 아래와 같이 올라온 이슈를 확인했습니다.

![blog/jekyll-blog/ #1](https://dl.dropboxusercontent.com/scl/fi/80ovwfrk5lecwjpd68m8o/hugo-2022-05-utterances-issue.webp?rlkey=pf4howfeibzzhpvptil9z5gkt&dl=0)

## 마치며

Hugo 블로그를 통한 소통을 기대하여 댓글 기능을 추가해보았습니다.
생각보다 간단하기 때문에 깃허브 블로그를 꾸미면서 댓글 기능을 희망하시는 분들이라면
Utterances를 적극 활용해보시기를 추천드립니다.

마지막 포스트로는 PaperMod 테마를 수정한 과정을 안내해드리겠습니다.
Hugo 테마끼리 공통적인 부분이 있기 때문에 다른 테마를 사용하시더라도 도움이 될 것입니다.

### 참고 자료

- [Utterances Documents](https://utteranc.es/)
- [Introduction to Hugo Templating](https://gohugo.io/templates/introduction/)
