---
title: "Hugo 코드블럭 UI 개선 - Mac 스타일 UI와 복사 버튼 구현"
date: "2026-02-17T23:54:34+09:00"
layout: "post"
description: >
  Hugo 서택스(SeoTax) 테마의 코드블럭에 줄 번호, Mac 스타일 UI, 복사 버튼을 구현한 과정을 다룹니다.
  highlight.js의 xcode/vs2015 테마를 CSS Variables로 내재화하고,
  개발자 블로그에 최적화된 시각적이고 기능적인 코드블럭 시스템을 완성했습니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/x5nr8dn33t1k8n79skn28/seotax-40-codeblock-wide.webp?rlkey=f6gz3ysn8iq88f7665dy0vjwd&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/ij840qdz6ci2djdj33odl/seotax-41-codeblock-mobile.webp?rlkey=d2z6is2czkhbofu1ah5ful4re&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "서택스 테마", "코드블럭", "highlight.js", "Mac 스타일", "복사 버튼", "Vanilla JS", "highlightjs-line-numbers", "Clipboard API", "코드블록"]
series: ["Hugo 테마 만들기"]
---
<style>
.content-cover, .screenshot-image { border: 3px solid var(--gray-200); }
</style>

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo 서택스(SeoTax) 테마의 코드블럭을 개발자 친화적으로 개선한 과정을 다룹니다.
기존 Hugo Book 테마의 코드블럭 스타일 및 기능적 한계를 극복하고, highlight.js 색상 팔레트를 내재화했습니다.
플러그인을 활용한 줄 번호 표시, Mac 스타일 윈도우 컨트롤, 직관적인 복사 버튼, 언어 표시 기능을 구현했습니다.

- **[Hugo Book 테마의 한계](#hugo-book-테마의-코드블럭)**: 코드블럭 클릭 시 전체 선택되는 방식의 불편함과 개선이 필요한 이유
- **[highlight.js 테마 적용](#highlightjs-테마-선택과-적용)**: xcode/vs2015 CDN 추출, CSS Variables 변환, data-theme 속성 기반 전환
- **[줄 번호 표시](#코드-줄-번호-표시하기)**: highlightjs-line-numbers.js 플러그인 활용, 테이블 스타일 개선, 줄 번호 드래그 비활성화
- **[Mac 스타일 UI 구현](#mac-스타일-ui-구현하기)**: CSS 가상 요소로 빨강/노랑/초록 윈도우 컨트롤 버튼 추가
- **[코드 복사 기능 구현](#코드-복사-버튼-구현하기)**: 복사 버튼 및 클립보드 API로 복사 기능 제공, 복사 성공 피드백 애니메이션
{{% /hint %}}

개발 블로그에서 코드블럭은 글의 핵심 컨텐츠입니다.
독자가 코드를 읽고, 이해하고, 복사하여 활용하는 과정이 얼마나 편리한지가
블로그의 가독성과 사용자 경험(UX)을 좌우합니다.

Hugo 서택스(SeoTax) 테마를 만들면서 코드블럭을 단순한 텍스트 표시를 넘어
**시각적으로 아름답고 기능적으로 편리한** 인터페이스로 만들고자 했습니다.

```js
console.log('Hello world!');
```

## 왜 코드블럭 개선이 필요했을까?

여러 개발 블로그에서 다양한 코드블럭 스타일을 보면서 다음과 같은 경우에 불편함을 느꼈습니다.

{{% hint %}}
1. **코드 줄 번호 없음**: 세로로 긴 코드블럭에 줄 번호가 없으면 코드와 글을 오갈 때 어디까지 봤는지 기억하기 어렵습니다.
2. **복사 버튼 부재**: 코드 전체를 드래그하여 선택하는 것은 번거롭고, 일부는 줄 번호까지 선택되는 문제도 있습니다.
3. **언어 정보 없음**: 코드가 어떤 언어인지 명시되지 않으면 문맥을 통해 유추해야 합니다.
{{% /hint %}}

제가 사용했던 Hugo 테마에서도 이런 문제를 경험했고,
이를 해결하기 위해 코드블럭을 시각적으로, 그리고 기능적으로 개선하기로 했습니다.

## Hugo Book 테마의 코드블럭

서택스 테마를 만들기 전에 사용했던 [Hugo Book 테마](https://github.com/alex-shpak/hugo-book)는
[highlight.js](https://highlightjs.org/)를 활용한 코드 하이라이팅을 지원했지만,
아쉬운 점이 있습니다.

### 단일 코드블럭 스타일의 한계

Hugo Book 테마는 라이트/다크 모드를 지원하지만, 독자가 주도적으로 테마를 전환할 수 없는 문제를
[이전 글](/blog/hugo-seotax-4/)에서 해결했습니다.
이 과정에서 사이드 메뉴에 달 모양의 다크모드 ON/OFF 버튼이 추가되었습니다.
하지만, Hugo Book 테마의 코드블럭을 그대로 사용하려니 문제가 있었습니다.

![Hugo Book 테마 - 코드블럭](https://dl.dropboxusercontent.com/scl/fi/mqtsklc4aj3kbgo9joxak/seotax-42-codeblock-book.webp?rlkey=qp4iubjf1t87ysz37mlmw8ndx&raw=1)

Hugo Book 테마는 기본적으로 `base16-snazzy` 코드블럭 스타일을 사용하는데,
라이트모드와 다크모드 모두에서 공통된 코드블럭 스타일이 적용됩니다.
제가 라이트모드를 중요시하지는 않지만, 라이트모드에서 어두운 코드블럭을 사용하는건
완성도가 떨어진다고 생각합니다.

하지만, Hugo Book 테마는 라이트/다크 모드에 따라 코드블럭 스타일을 바꾸는 기능을 제공하지 않습니다.

### 코드 내용 복사의 한계

Hugo Book 테마는 `clipboard.js` 를 제공하여 코드블럭을 클릭하면 내용이 전체 선택되는 기능을 지원합니다.

```js
document.querySelectorAll("pre code").forEach(code => {
  code.addEventListener("click", function (event) {
    if (window.getSelection().toString()) {
      return;
    }
    select(code.parentElement);

    if (navigator.clipboard) {
      navigator.clipboard.writeText(code.parentElement.textContent);
    }
  });
});
```

이 복사 방식에는 3가지 문제점을 인식했습니다.
- **직관성 부족**: 클릭하면 복사되는지, 선택되는지 명확하지 않습니다.
- **복사 후 피드백 없음**: 복사가 성공했는지 시각적인 피드백이 없습니다.
- **부분 선택 어려움**: 코드블럭의 일부를 선택하고 싶어도 강제로 전체 내용이 선택되어 버립니다.

결론적으로, 이 기능은 불필요하고 대신에 복사 버튼을 만드는 것이 낫다고 판단했습니다.

## highlight.js 테마 선택 및 적용

### 라이트/다크 테마 선택

[highlight.js 데모 페이지](https://highlightjs.org/demo)에서 다양한 테마를 비교한 결과,
라이트/다크 모드에 어울리는 다음의 두 테마를 선택했습니다.

{{< columns >}}
<h4>라이트 모드 (xcode)</h4>
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/grbkii9twa03ha1pe6kkr/seotax-43-codeblock-xcode.webp?rlkey=uz1m6goxe621zbg66aqrsrj7t&raw=1"
  alt="highlight.js - xcode"
  caption="Xcode IDE의 기본 색상 팔레트" >}}
<--->
<h4>다크 모드 (vs2015)</h4>
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/pk07syzh7iqwv9eg6t0kt/seotax-43-codeblock-vs2015.webp?rlkey=ph6f1aoe41xs04p4hhxwk27yv&raw=1"
  alt="highlight.js - vs2015"
  caption="Visual Studio 2015의 어두운 테마" >}}
{{< /columns >}}

### highlight.js CDN 추출

처음에는 CDN을 통해 두 가지 highlight.js 테마의 색상 팔레트를 불러왔습니다.
이후, 서택스 테마를 개선하면서 네트워크 요청 속도를 저해하는 외부 CDN 의존성을 제거하고자 했고,
highlight.js 또한 그 대상이었습니다.

두 가지 테마에 대한 CSS 설정은 아래 CDN 링크를 통해서 확인할 수 있는데, 공백을 제거하고 몇 줄 안될 정도로 단순합니다.

{{< columns >}}
<h4>라이트 모드 (xcode)</h4>
{{< bookmark "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/xcode.min.css" >}}
<--->
<h4>다크 모드 (vs2015)</h4>
{{< bookmark "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.11.1/styles/vs2015.min.css" >}}
{{< /columns >}}

서택스 테마는 highlight.js CDN의 CSS를 분석하여 `_highlight.scss` 파일로 내재화했습니다.

```scss
// assets/css/variables/_highlight.scss

/* Light Theme (xcode) */
[data-theme="light"] {
  --hljs-background: #fff;
  --hljs-color: #000;
  --hljs-comment: #007400;
  --hljs-keyword: #aa0d91;
  --hljs-string: #c41a16;
  --hljs-number: #1c00cf;
  // ... 기타 색상 변수
}

/* Dark Theme (vs2015) */
[data-theme="dark"] {
  --hljs-background: #1e1e1e;
  --hljs-color: #dcdcdc;
  --hljs-comment: #57a64a;
  --hljs-keyword: #569cd6;
  --hljs-string: #d69d85;
  --hljs-number: #b8d7a3;
  // ... 기타 색상 변수
}
```

CDN에서 추출한 CSS 변수를 [다크모드를 구현한 글](/blog/hugo-seotax-4/#속성-값에-따른-테마-전환)에서
설명한 `data-theme` 속성 기반 테마 전환 시스템과 통합했습니다.

`<html>` 요소에 `data-theme` 속성 값이 `light` 인 경우에는
`xcode` 테마 색상 변수를, 속성 값이 `dark` 인 경우에는 `vs2015` 테마 색상 변수가 적용됩니다.
전체 코드는 아래 링크를 참고해주시기 바랍니다.

{{< bookmark "https://github.com/minyeamer/hugo-seotax/blob/main/assets/css/variables/_highlight.scss" >}}

### 주요 색상 매핑

각 코드 요소에 대한 색상 매핑을 시각적으로 안내드립니다.

{{% columns %}}
#### 라이트 모드 (xcode)
- **키워드**: <span style="background: #fff; color: #aa0d91;">#aa0d91</span> (보라색)
- **문자열**: <span style="background: #fff; color: #c41a16;">#c41a16</span> (빨강색)
- **주석**: <span style="background: #fff; color: #007400;">#007400</span> (초록색)
- **숫자**: <span style="background: #fff; color: #1c00cf;">#1c00cf</span> (파랑색)
<--->
#### 다크 모드 (vs2015)
- **키워드**: <span style="background: #000; color: #569cd6;">#569cd6</span> (하늘색)
- **문자열**: <span style="background: #000; color: #d69d85;">#d69d85</span> (주황색)
- **주석**: <span style="background: #000; color: #57a64a;">#57a64a</span> (초록색)
- **숫자**: <span style="background: #000; color: #b8d7a3;">#b8d7a3</span> (연두색)
{{% /columns %}}

## 코드 줄 번호 표시하기

코드블럭에 줄 번호가 보이지 않던 것도 Hugo Book 테마의 단점입니다.

### 플러그인 활용

highlight.js 자체는 줄 번호를 표시하는 기능을 제공하지 않지만,
[highlightjs-line-numbers.js](https://github.com/yauhenipakala/highlightjs-line-numbers.js) 플러그인을 통해
이 기능을 쉽게 추가할 수 있었습니다. 해당 플러그인도 마찬가지로
[CDN](https://cdnjs.cloudflare.com/ajax/libs/highlightjs-line-numbers.js/2.9.0/highlightjs-line-numbers.min.js)을
활용하지 않고 직접 내려받아 `static/` 경로에 추가했습니다.

{{< bookmark "https://github.com/yauhenipakala/highlightjs-line-numbers.js" >}}

플러그인을 `static/` 경로에 추가했다면, `<head>` 태그 내에서 이렇게 불러올 수 있습니다.

```go-html
<script defer src="{{ `highlightjs-line-numbers.min.js` | relURL }}"></script>
```

플러인을 불러오고 highlight.js를 초기화 했다면 다음과 같이 줄 번호를 표시할 수 있습니다.

```js
hljs.highlightAll(); // highlight.js 초기화

hljs.initLineNumbersOnLoad(); // 줄 번호 표시
```

또는 코드블럭 요소를 직접 지정해서 줄 번호를 표시할 수도 있습니다.

서택스 테마는 highlight.js 초기화 대상이 되지 않은
코드블럭에도 줄 번호를 표시하기 위해 다음과 같은 줄 번호 표시 방식을 응용했습니다.

```js
$(document).ready(function() {
    $('code.hljs').each(function(i, block) {
        hljs.lineNumbersBlock(block);
    });
});
```

### 줄 번호 스타일 개선

아쉽게도 `highlightjs-line-numbers.js` 플러그인은 코드블럭을 아래 이미지처럼
못생긴 테이블 형태로 바꿔버립니다.

![highlightjs-line-numbers > 테이블 스타일](https://dl.dropboxusercontent.com/scl/fi/5qxgcdtc5z0xhcypei1ek/seotax-44-codeblock-ln.webp?rlkey=rfnkeonfc4v8md8vv2q3y9f30&raw=1)

그래서, 테이블 구분선을 없애고 라인 간 간격을 적절히 조정하는 스타일을 추가해
자연스러운 하나의 블록처럼 보이게 개선했습니다.

```scss
.hljs-ln {
  border-spacing: 0;
  border-collapse: collapse;
  width: 100%;
  display: table;

  tbody {
    display: table-row-group;
  }

  tr {
    display: table-row;
  }

  td {
    display: table-cell;
    border: none !important;
    vertical-align: top;
    margin: 0;
    padding: 0 0.625rem 0;
    white-space: pre;
  }
}
```

추가로, 줄 번호는 코드와 구분되지만 독자가 복사할 때는 선택되지 않아야 합니다.

코드의 일부를 복사하려는 블로그 독자들이 불편함을 겪지 않도록 `user-select: none;`
과 같이 줄 번호만 마우스 드래그 대상이 되지 않도록 하는 스타일을 추가했습니다.

```scss
.hljs-ln-numbers {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;

  display: table-cell;
  text-align: right;
  white-space: nowrap;

  width: 2rem;
  min-width: 2rem;
  color: var(--lineno-font-color);
}
```

이렇게 개선한 줄 번호는 코드의 가독성을 해치지 않으면서도
독자가 특정 줄을 참조하기 쉽게 만들어 줍니다.

## Mac 스타일 UI 구현하기

몇몇 개발 블로그를 보면서 Mac의 윈도우 컨트롤 버튼(빨강, 노랑, 초록)이
코드블럭의 좌측 상단에 배치된 경우를 보았습니다.
저는 이 스타일이 겉보기에 아름다우면서, 동시에 독자들의 시선을 끄는 효과가 있다고 생각하여
서택스 테마에도 적용하기로 했습니다.

Mac 스타일을 구현하는 방법을 찾아보니 [carbon](https://carbon.now.sh/)이라는
미리 만들어진 기능이 있었는데, 블로그에 적용하는 방법을 확인하기 어려워 CSS로 직접 구현했습니다.

### CSS 가상 요소로 버튼 생성

`::before` 가상 요소와 `box-shadow`를 활용하여
세 개의 버튼을 하나의 요소로 표현했습니다.

```scss
pre {
  &::before {
    content: '';
    position: absolute;
    top: 0.9375rem;
    left: 1.25rem;
    width: 0.75rem;
    height: 0.75rem;
    background: #ff5f57; // 빨간 버튼
    border-radius: radius(button);
    box-shadow: 1.375rem 0 0 #ffbd2e, 2.75rem 0 0 #28ca42; // 노란 버튼, 초록 버튼
  }
}
```

구현 결과는 이미 코드블럭으로 보고 계십니다.
코드블럭의 좌측 상단에 빨강, 노랑, 초록 색상의 버튼이 순서대로 표시됩니다.

### 코드블럭 여백 조정

Mac 컨트롤 버튼은 highlight.js 코드블럭과 별개의 요소이므로,
코드블럭 내용과 겹치지 않게 상단에 여백을 추가해야 합니다.

```scss
pre {
  // 한 줄 코드
  &:not(:has(.hljs-ln)) {
    padding-top: 2rem;
  }

  // 여러 줄 코드 (줄 번호 있음)
  &:has(.hljs-ln) {
    padding-top: 1.5rem;
  }
}
```

개인적으로는 줄 번호가 표시되는 여러 줄 코드와 그렇지 않은 한 줄 코드에
다른 크기의 여백을 넣는 것이 보기에 좋았습니다.
`:has()` 선택자를 사용하여 줄 번호(`.hljs-ln`) 유무에 따라
다른 여백을 적용했습니다.

## 코드 복사 버튼 구현하기

Hugo Book 테마의 내용 전체 선택 방식 대신,
**직관적인 복사 버튼**을 우측 상단에 배치했습니다.

### HTML 템플릿 수정

Hugo는 다음 한 줄의 코드로 마크다운 코드블럭을 highlight.js 코드블럭으로 변환해줍니다.

```go-html
{{- (transform.HighlightCodeBlock . .Options).Wrapped -}}
```

`layouts/_markup/render-codeblock.html` 경로의 HTML 템플릿을 통해 코드블럭을 렌더링 하는데,
해당 라인의 상단에 복사 버튼을 배치할 `.code-actions` 영역을 추가했습니다.

```go-html
<!-- layouts/_markup/render-codeblock.html -->

<div class="code-actions">
  <button class="code-copy-button code-action" onclick="copyCode(this)">
    <i class="icon-file-copy"></i>Copy
  </button>
  <span class="code-language code-action">{{ .Type | default "text" }}</span>
</div>
{{- (transform.highlightCodeBlock . .Options).Wrapped | safeHTML -}}
</div>
```

`.code-actions` 영역에는 2개의 요소가 있습니다.
- 복사 버튼에 해당하는 `.code-copy-button` 요소
- 언어 표시를 위한 칩 형태의 `.code-language` 요소

### JavaScript 복사 로직

복사 버튼을 클릭하면 `copyCode()` 함수가 호출됩니다.
이 코드 복사 함수는 `copy-code.js` 에서 구현했습니다.

```js
// themes/seotax/assets/js/shortcodes/copy-code.js

function copyCode(button) {
  const codeBlock = button.closest('.sc-codeblock');
  const code = codeBlock?.querySelector('pre code');

  if (!code) return;

  // 줄 번호 제외하고 코드만 추출
  const codeLines = code.querySelectorAll('.hljs-ln-code');
  const text = Array.from(codeLines)
    .map(line => {
      const content = line.textContent || line.innerText || '';
      return content.trim() === '' ? '' : content;
    }).join('\n');

  if (navigator.clipboard) {
    navigator.clipboard.writeText(text)
      .then(() => copySuccess(button))
      .catch(() => fallbackCopy(text, button));
  } else {
    fallbackCopy(text, button);
  }
}
```

`copyCode()` 함수는 코드블럭의 모든 라인을 순회하면서 텍스트만 추출하고
클립보드에 복사하는 동작을 합니다.

클립보드가 없거나 실패하는 경우는 `fallbackCopy()` 함수를 호출하는데,
이 함수는 코드 텍스트를 임시 `textarea` 요소로 추가하고 `copy` 명령어를 수행하도록
동작하는 구형 브라우저 대비책 입니다.

### 복사 성공 피드백

독자들에게 시각적 피드백을 제공하기 위해 복사 성공 시 버튼 텍스트를
<span style="background: rgba(0, 0, 0, 0.9); color: #fff;"><i class="icon-file-copy"></i> COPY</span>
에서
<span style="background: rgba(76, 175, 80, 0.8); color: #fff;"><i class="icon-check"></i> COPIED</span>
로 2초간 변경합니다.

```js
function copySuccess(button) {
  const icon = button.querySelector('i');
  const textNode = Array.from(button.childNodes)
    .find(node => node.nodeType === Node.TEXT_NODE && node.textContent.trim());

  if (!icon || !textNode) return;

  const originalClass = icon.className;
  const originalText = textNode.textContent;

  icon.className = 'icon-check';
  textNode.textContent = 'COPIED';
  button.classList.add('copied');

  setTimeout(() => {
    icon.className = originalClass;
    textNode.textContent = originalText;
    button.classList.remove('copied');
  }, 2000);
}
```

동시에, 복사 성공 시 초록색 배경을 적용하여 복사 성공을 명확하게 표시합니다.

```scss
.code-copy-button {
  &.copied {
    background: rgba(76, 175, 80, 0.8);
  }
}
```

## 코드 언어 정보 표시

복사 버튼을 추가할 때 `.code-actions` 영역에 `.code-language` 요소를 하나 더 추가했습니다.

```go-html
<!-- layouts/_markup/render-codeblock.html -->

<div class="code-actions">
  <button class="code-copy-button code-action" onclick="copyCode(this)">
    <i class="icon-file-copy"></i>Copy
  </button>
  <span class="code-language code-action">{{ .Type | default "text" }}</span>
</div>
{{- (transform.highlightCodeBlock . .Options).Wrapped | safeHTML -}}
</div>
```

이 요소는 칩 형태로 보이게 스타일 적용한 텍스트 요소인데,
Hugo는 코드블럭을 대상으로 `.Type` 을 컨텍스트를 호출하면
마크다운 코드블럭의 첫 번째 줄에 작성한 언어 정보를 반환합니다.

````markdown
```js
console.log('Hello world!');
```
````

위 마크다운 코드블럭은 렌더링 후 우측 상단에 "JS" 라고 언어 정보가 표시됩니다.

`.Type` 외에 Hugo에서 코드블럭을 다루는 방법을 알고 싶다면 아래 공식 문서를 참고해주시기 바랍니다.

{{< bookmark "https://gohugo.io/render-hooks/code-blocks/" >}}

## 추가 개선 아이디어

현재 코드블럭도 충분히 만족스럽지만, 앞으로 구현해보고 싶은 기능들이 아직 있습니다.

{{% hint %}}
1. **코드 접기/펼치기**: 긴 코드를 접어서 페이지 스크롤 줄이기 (노란색 Mac 컨트롤 버튼 활용)
2. **코드 전체 화면 보기**: 긴 코드를 전체 화면에 확대해서 보기 (초록색 Mac 컨트롤 버튼 활용)
3. **diff 표시**: 코드 변경사항을 `+` / `-` 로 강조
4. **특정 줄 강조**: 중요한 줄을 배경색으로 하이라이트
5. **다운로드 버튼**: 코드를 파일로 다운로드
{{% /hint %}}

지금까지의 모든 개선 사항을 적용한 결과, 독자들은 이제 미리 제공되는 언어 정보를 바탕으로 코드를 읽고,
한 번의 버튼 클릭으로 내용을 복사할 수 있으며, Mac 스타일의 세련된 디자인까지 경험할 수 있게 되었습니다.
