---
layout: post
title: Hugo 블로그 만들기 (2) - Utterances 댓글 적용
date: 2022-09-08 14:39:22 +0900
categories: [Blog, Tech]
tags: [Hugo, PaperMod, Github, Github Pages, Utterances]
---

Hugo 블로그는 기본적으로 댓글 기능을 제공하지는 않습니다.   
제가 사용하는 PaperMod 테마에서는 서드파티 서비스인 `Disqus`를 위한 레이아웃이 존재하지만,   
저는 기본적인 블로그 운영을 Github 플랫폼 내에서 구성하고 싶기 때문에 다른 기능을 사용해보려 합니다.

이번 포스트에서는 Utterances 댓글 기능을 추가하는 방법을 안내해드리겠습니다.

---

# Utterances 설치하기

Utterances는 Github issues 기반으로 댓글을 관리하는 기능입니다.   
무료 플랜에서 광고가 붙는 `Disqus`와 다르게 별도의 유료 플랜이 없어 간편하게 사용할 수 있습니다.   

Utterances 설치는 단순히 레이아웃 상에서 댓글이 위치할 곳에 자바스크립트 코드를 삽입하면 됩니다.   
하지만, 선행적으로 [해당 링크](https://github.com/marketplace/utterances)를 통해 Utterances와 연동시킬 저장소를 등록해야 합니다.

![utterances-1](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/utterances-1.png?raw=true)

무료 플랜 선택 후 Utterances를 적용할 저장소를 선택하게 되는데   
모든 저장소를 지정해도 되지만, 저는 댓글을 관리할 저장소만 지정하겠습니다.

<div align="center">
<img src="https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/utterances-2.png?raw=true" style="max-width:550px">
</div>

간단하게 Utterances 적용이 완료되면 아래 공식 문서 페이지로 이동합니다.

- https://utteranc.es/

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

---

# 스크립트 삽입하기

PaperMod 테마에는 `layouts/partials/` 위치에 `comments.html`이라는 레이아웃이 존재합니다.   
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

Hugo HTML 코드 내에 이중 중괄호({{ }})는 Go 템플릿을 코딩하는 부분으로,   
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

![utterances-3](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/utterances-3.png?raw=true)

댓글 기능이 정상적으로 적용되는지 확인하기 위해 실험적으로 댓글을 작성해봅니다.   
저도 과거 게시글에 댓글을 작성하여 아래와 같이 올라온 이슈를 확인했습니다.

![utterances-4](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/utterances-4.png?raw=true)

---

# 마치며

Hugo 블로그를 통한 소통을 기대하여 댓글 기능을 추가해보았습니다.   
생각보다 간단하기 때문에 깃허브 블로그를 꾸미면서 댓글 기능을 희망하시는 분들이라면   
Utterances를 적극 활용해보시기를 추천드립니다.

마지막 포스트로는 PaperMod 테마를 수정한 과정을 안내해드리겠습니다.   
Hugo 테마끼리 공통적인 부분이 있기 때문에 다른 테마를 사용하시더라도 도움이 될 것입니다.

## 참고 자료

- [Utterances Documents](https://utteranc.es/)
- [Introduction to Hugo Templating](https://gohugo.io/templates/introduction/)
