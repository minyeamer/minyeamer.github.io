---
title: "Hugo 서택스(SeoTax) 테마 제작기 - 동적 렌더링으로 확장된 검색"
date: "2026-01-25T23:48:16+09:00"
layout: "post"
description: >
  Hugo 서택스(SeoTax) 테마는 동적 렌더링을 활용해 정적 페이지의 한계를 극복하고,
  고급 검색 및 분류(Taxonomy) 기능을 제공합니다. 테마의 설계 목적 및 주요 기능을 소개하니,
  Hugo 블로그 테마 개발에 관심이 있다면 꼭 참고하세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/4ypgz37ygay76807x2gpd/seotax-00-cover.webp?rlkey=vuon12lsgu8xk2ya2153wxvel&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "서택스 테마", "Hugo 검색", "Hugo 분류", "다국어 번역", "휴고 테마", "Vanilla JS", "UI/UX", "반응형 디자인", "태그", "카테고리", "i18n", "Blog"]
series: ["Hugo 테마 만들기"]
---
<style>
.content-cover, .screenshot-image { border: 3px solid var(--gray-200); }
.sc-columns .sc-codeblock { margin: 0; }
.sc-columns:has(.screenshot-image) { gap: 0.25rem; }
.columns-4 { display: flex; }
@media screen and (max-width: 1254px) { .columns-4 { flex-wrap: wrap; } }
</style>

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="fa-solid fa-wand-magic-sparkles"></i> **AI 요약 & 가이드**

Hugo의 서택스(SeoTax) 테마 설계 목적과 레이아웃 구조를 한눈에 정리하고,
이어지는 글에서는 구현 세부사항을 코드 예제와 함께 자세히 다룰 예정입니다.
정적 페이지 생성기의 한계를 보완하기 위해 동적 렌더링을 활용한 점이 특징입니다.

- **[주요 고려사항](#주요-고려사항)**: 서택스 테마를 만들면서 고민했던 내용 (검색, 다국어 번역 등)
- **[주요 기능](#주요-기능)**: 고려사항을 바탕으로 실제로 구현한 서택스 테마의 주요 기능 (툴바, 시리즈 등)
- **[검색 페이지](#검색-페이지)**: 검색 모달 및 결과 페이지 스크린샷과 함께 간략한 조작 방식 설명
- **[테마 디렉터리 구조](#테마-디렉터리-구조)**: `assets/`, `layouts/` 등 폴더별 역할 설명
{{% /hint %}}

Hugo Book 테마 커스터마이징 과정을 기록한 후 한 달의 시간이 지났습니다.

[지난 과정](/blog/hugo-blog-1/)에서 Book 테마를 입맛대로 바꿔보면서 Hugo의 동작 원리를 이해하고
테마 내 템플릿이 어떤 구조로 배치되는지 알아볼 수 있었습니다.
하지만, [카테고리와 태그 페이지](/blog/hugo-blog-3/)를 정적으로 생성해보면서,
동시에 [검색 페이지](/blog/hugo-blog-4/)를 동적으로 만들어내는 Book 테마의 동작을 보면서
불필요한 정적 페이지들이 많이 만들어진다는 것을 느꼈습니다.

서택스(SeoTax) 테마는 이러한 문제점을 개선하고자 개발되었습니다.

검색 결과에서 고급 필터로 카테고리와 태그를 선택할 수 있게 지원하고,
이를 통해 분류(Taxonomies) 하나하나마다 만들어지는 수백 개의 정적 페이지를
하나의 검색 페이지에 녹였습니다.

이것이 서택스 테마의 핵심 기능이며, 따라서 두 기능(Search/Taxonomies)의 앞글자를 따서 테마명으로 사용했습니다.

## 서택스(SeoTax) 테마란?

서택스 테마는 Hugo 블로그를 위한 테마 레이아웃입니다.

블로그에 처음 유입된 사용자가 **블로그를 탐색하는 경험에 집중**하였으며,
블로그 내 게시글을 탐색하기 위해 단순 키워드 검색 뿐 아니라,
카테고리 및 태그 필터로 검색 결과를 세분화하는 향상된 검색 기능을 제공합니다.

앞에서 언급했듯이, 정적 페이지 생성기인 Hugo의 한계를 극복하는 것이 주요 도전과제였고,
Vanila JS를 활용한 동적 페이지 렌더링을 적극적으로 활용해
기존 Book 테마의 UI/UX에서 불편하다고 느꼈던 문제점들을 정의하고 해결했습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/gqsgo2otrmou4qj77k8iz/seotax-01-search-demo.gif?rlkey=ti6ysbvm9906qe7ypdzejxag9&raw=1"
  alt="서택스 테마 - 검색 동작"
  caption="서택스 테마 - 검색 모달 > 검색 페이지 > Taxonomies 필터 조작"
  class="screenshot-image" >}}

### 주요 고려사항

서택스 테마를 만들면서 고민했던 내용을 아래와 같이 정리해 볼 수 있습니다.

{{% hint %}}
1. Hugo는 특정 태그를 포함하는 게시글 목록을 표현하기 위해 태그 하나하나마다 정적 페이지를 만들어야 합니다.   
  장기적으로 수백, 수천 개의 태그가 추가될 수 있는데 이 모두에 공통 레이아웃을 포함한 정적 페이지를 만드는 것은 대단한 낭비입니다.
{{% /hint %}}

{{% hint warning %}}
2. 기존의 검색 UI/UX는 사이드 메뉴의 검색창에서 키워드를 입력하면 작은 영역에 검색 미리보기를 표시하고 검색 페이지로 이동을 지원했습니다.
   독자들이 검색 결과에 흥미를 느끼고 검색 페이지에 진입하게 하려면 검색 미리보기를 더 큰 모달 창에 띄울 필요가 있습니다.
{{% /hint %}}

{{% hint %}}
3. 기존의 모바일 UI에서 사이드 메뉴 또는 목차를 접고 펼치는 동작은 CSS로 구현되었습니다.   
   하지만, 글을 읽던 중 목차를 보려고 아이콘을 클릭하여 포커스되면 최상단으로 이동해 독자들의 경험을 심각하게 방해합니다.
{{% /hint %}}

{{% hint warning %}}
4. 한국어를 모르더라도 테마를 활용할 수 있게 주요 문구(label)에 대한 27개 언어 번역(i18n)을 지원합니다.   
   하지만, 이것은 Hugo 렌더링 시에 1회 적용되고 이후에 임의로 변경할 수 없어 독자들을 배려하지 못합니다.
{{% /hint %}}

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/hxkxy1azs1zvtbdn143ak/seotax-02-i18n-demo.gif?rlkey=vdl5r9kllp0i3mptiyzcksek2&raw=1"
  alt="서택스 테마 - 다국어 지원"
  caption="서택스 테마 - 다국어 지원"
  class="screenshot-image" >}}

### 주요 기능

고민했던 내용을 바탕으로 실제로 구현한 기능,
그리고 다른 웹사이트에서 마음에 들어 채택한 기능들이 있습니다.

{{% hint %}}
1. 블로그의 어느 페이지에서든 `/` 단축키를 누르거나 사이드 메뉴의 **검색창**을 클릭하면 **모달** 창이 열립니다.   
   모바일에서는 상단 헤더에 추가로 검색창을 배치해 접근성을 높였습니다.
{{% /hint %}}

{{% hint warning %}}
2. 검색 페이지에서 특정 카테고리 및 태그를 포함하는 게시글만 필터해서 볼 수 있습니다.   
   검색어 없이 **카테고리 또는 태그를 필터**하면 일반적인 검색 페이지와 다른 전용 UI를 보여줍니다.
{{% /hint %}}

{{% hint %}}
3. 사이드 메뉴 상단의 햄버거 아이콘을 클릭하면 **메뉴를 펼치고 접을 수 있습니다.**
   (토글 상태가 로컬 스토리지에 저장됩니다.)   
   모바일에서는 상단 헤더 양쪽의 아이콘을 클릭해 사이드 메뉴 및 목차를 펼치고 접을 수 있습니다.
{{% /hint %}}

{{% hint warning %}}
4. 우측 하단의 **툴바**에서 다국어 번역, 맨 위로 이동, 맨 아래로 이동, 뒤로 가기 기능의 버튼이 제공됩니다.   
   다국어 번역은 레이아웃의 주요 제목(`h1`, `h2`), 라벨(`p`, `span`), 일부 속성(`aria-label`, `title`) 등이 대상입니다.   
   `+`, `x` 버튼을 클릭해 툴바를 펼치고 접을 수 있으며, 모바일에서는 기본적으로 접힌 상태입니다.
{{% /hint %}}

{{% hint %}}
5. 상세페이지 상단의 글 제목 영역에서 **글을 읽는데 걸리는 시간**을 표시합니다.   
   미디엄 블로그에서 아이디어를 얻었으며, 텍스트 뿐 아니라 이미지, 코드블럭, 표에 대해서도 계산식을 만들었습니다.
{{% /hint %}}

{{% hint warning %}}
6. Velog의 **시리즈** 기능을 그대로 구현했습니다. 시리즈는 Shortcode로써, 본문의 어느 위치에서든 호출해 표시할 수 있습니다.   
   페이지 이동 시마다 커버 이미지의 높이 차이로 인해 위치가 바뀌는 불편함을 개선하고자 앵커가 적용되어 있습니다.
{{% /hint %}}

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/vtek4qj407tedlmubqdi5/seotax-03-series-demo.gif?rlkey=5sxz068y5db6rbho3zp09e04z&raw=1"
  alt="서택스 테마 - 시리즈 확장기능"
  caption="서택스 테마 - 시리즈 확장기능"
  class="screenshot-image" >}}

## 테마 사용 방법

서택스 테마는 Github 저장소 `hugo-seotax` 에서 관리됩니다.

{{< bookmark "https://github.com/minyeamer/hugo-seotax" >}}

이 글을 작성하는 시점엔 아직 README 나 ExampleSite 를 만들지 않아서
서택스 테마를 직관적으로 이해하기 어려울 수 있습니다.
서택스 테마의 시리즈 글을 모두 작성하게 되면 이 부분도 개선할 예정입니다.

Hugo 블로그를 만들어본 경험이 없으시다면
[Hugo 블로그 만들기 - Git Submodule로 구성하고 배포하기](/blog/hugo-blog-1/#블로그-프로젝트-구성하기)
글을 참고해주시기 바랍니다.

Github 저장소로부터 ZIP 파일로 다운로드 받거나, 터미널에서 `git clone` 명령어를 통해
소스코드를 복제할 수 있습니다. Hugo의 `themes/` 경로 아래에 임의의 폴더를 하나 만들고 그 안에
테마 소스코드를 배치하면 준비가 끝났습니다.

```bash
# Hugo 프로젝트 루트 경로에서 실행합니다.
# 임의의 폴더를 `seotax` 라고 만들었는데, 다른 폴더명을 사용해도 됩니다.

git clone https://github.com/minyeamer/hugo-seotax themes/seotax
```

Hugo 설정 파일(`hugo.toml`, `hugo.yaml` 등)의 `theme` 값으로
앞에서 생성한 임의의 폴더 명칭을 작성해두면, Hugo 빌드 명령어를 호출할 때
`--t`, `--theme` 옵션을 생략해도 서택스 테마가 기본 테마로 적용됩니다.

{{% columns %}}
```yaml
theme: "seotax"
```
<--->
```toml
theme = "seotax"
```
{{% /columns %}}

## 테마 레이아웃 안내

서택스 테마의 레이아웃을 스크린샷과 함께 안내합니다.

이미지는 다크모드 기준으로 보여주지만, 모든 레이아웃에서 라이트모드도 지원됩니다.

### 메인 페이지

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/furcvh2rmo2s1eledk5zd/seotax-04-layout-main.webp?rlkey=8h10cxj6z7o1abupmnbvekvhi&raw=1"
  alt="서택스 테마 레이아웃 - 메인 페이지"
  caption="메인 페이지 - 게시글 목록"
  class="screenshot-image" >}}

`/` 경로로 접근 가능한 메인 페이지는 모든 게시글 목록을 표시합니다.

하나의 게시글 항목은 제목, 내용, 작성일, 카테고리, 태그, 그리고 커버 이미지 정보를 보여줍니다.
- 제목을 클릭하면 해당 게시글의 상세 페이지로 이동할 수 있습니다.
- 작성일은 다국어 번역을 지원합니다. 언어별로 적절한 날짜 형식으로 표시됩니다.
- 카테고리 및 태그 칩을 클릭하면 관련 게시글 목록을 조회할 수 있는 검색 페이지로 이동합니다.
- 커버 이미지는 데스크탑 너비에서 정사각형 비율에 적절한 썸네일 이미지로 대체할 수 있습니다.

좌측의 사이드 메뉴와 우측의 툴바는 모든 레이아웃에서 공통적으로 표시되는 부분 템플릿 입니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/a160e910lfn3l1wef9i6w/seotax-05-layout-pagination.webp?rlkey=xndbe1he2hfnxhczicfgzm0qm&raw=1"
  alt="서택스 테마 레이아웃 - 페이지네이션"
  caption="메인 페이지 - 페이지네이션"
  class="screenshot-image" >}}

페이지네이션 방식으로 게시글을 10개 단위로 나눠서 보여주며,
게시글 목록 하단에 페이지를 이동할 수 있는 링크가 있습니다.

페이지 링크 또한 10개 단위로 그룹화하여 현재 페이지가 속한 그룹만 표시합니다.   
이전 또는 다음 페이지 그룹이 있을 경우 이전/다음 버튼이 활성화됩니다.

페이지 이동 시 스크롤이 맨 위로 이동하는 불편함을 방지하기 위해   
페이지네이션 영역에 앵커를 적용하여 페이지 이동 후에도 스크롤 위치가 유지됩니다.

메인 페이지의 게시글 항목과 페이지네이션 템플릿은
이후 검색 페이지에서도 동일하게 사용됩니다.

### 상세 페이지

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/f9win2bs897fo0kkca586/seotax-06-layout-content.webp?rlkey=k3dmdi6ij37eaqjjvmhsgx7nw&raw=1"
  alt="서택스 테마 레이아웃 - 상세 페이지 상단"
  caption="상세 페이지 - 헤더"
  class="screenshot-image" >}}

상세 페이지는 마크다운으로 작성된 컨텐츠를 보여주는 페이지입니다.

상세 페이지의 상단에는 제목이 포함된 헤더 영역과 그 아래에 커버 이미지가 표시됩니다.

상세 페이지의 헤더 영역은 카테고리, 제목, 작성일시 순서로 나열됩니다.
- 카테고리는 관련 게시글 목록을 조회할 수 있는 검색 페이지와 연결됩니다.
- 작성일시는 마크다운 컨텐츠의 프론트매터(front matter)에 작성된 `date` 값을 분 단위까지 표시합니다.
- 작성일시 우측에는 글을 읽는데 걸리는 시간을 계산하여 같이 표시합니다. 이 부분은 다국어 번역이 지원됩니다.

프론트매터에 `cover` 값을 추가했다면 헤더 바로 아래에 커버 이미지로 표시합니다.   
`cover` 값이 `<img>` 태그에 `src` 속성으로 전달되므로 이미지 주소 형식만 허용됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/s2v83k6igaxhohh0x9ql1/seotax-07-layout-footer.webp?rlkey=oyiyrwpjk2ivvajyal3eyv0q8&raw=1"
  alt="서택스 테마 레이아웃 - 상세 페이지 푸터"
  caption="상세 페이지 - 푸터"
  class="screenshot-image" >}}

상세 페이지의 하단에는 푸터 영역이 있습니다.   
푸터 영역은 태그 목록, 이전/다음 게시글 링크, Disqus 댓글창, 카피라이트 문구 순으로 구성됩니다.
- 태그 목록에서 태그 칩 하나를 클릭하면 관련 게시글 목록을 조회할 수 있는 검색 페이지와 연결됩니다.
- 이전/다음 게시글 링크는 작성일 기준으로 이전과 다음 순서의 게시글을 알려줍니다.   
  전환율을 높이기 위해 `자식 카테고리` > `부모 카테고리` > `전체 게시글` 순으로 더 연관성 높은 게시글을 보여줍니다.
- Disqus 댓글 영역은 서비스에서 제공되는 스크립트가 적용되는 곳으로, SNS 로그인을 통해 댓글을 남길 수 있습니다.   
  Hugo 설정 내 파라미터 중 `comments.disqusShortname` 에 Disqus의 사이트명을 작성할 수 있습니다.

### 검색 페이지

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/z4k9q8irzuvitrw2mx3ze/seotax-08-layout-search-modal.webp?rlkey=16ij0g11elonaslnf30odzz8d&raw=1"
  alt="서택스 테마 레이아웃 - 검색 모달"
  caption="검색 페이지 - 모달"
  class="screenshot-image" >}}

검색 페이지에 접근하는 방식은 4가지가 있습니다. (URL을 통해 직접 접근하는건 생략합니다.)

{{% hint %}}
1. 검색 모달창에서 키워드를 입력하고 엔터 키 입력, 검색 아이콘 클릭, "결과 보기" 라벨을 클릭하기
2. 게시글 항목의 카테고리 칩 또는 본문 헤더의 카테고리 라벨을 클릭하기
3. 사이드 메뉴에서 카테고리를 클릭하기
4. 게시글 항목의 태그 칩 또는 본문 푸터의 태그 칩을 클릭하기
{{% /hint %}}

이 중에서 1번을 제외하고는 Taxonomy 전용 UI를 가진 검색 페이지로 이동하기 때문에,
키워드 기반 검색은 모달창을 통해서만 접근할 수 있다고 볼 수 있습니다.
그리고, 모달창은 다음 2가지 방식으로 접근할 수 있습니다.

{{% hint %}}
1. 사이드 메뉴의 검색창을 클릭하기
2. 특정 요소에 포커스되지 않은 상태로 단축키 `/` 또는 `s` 를 입력하기
3. 모바일 전용 헤더의 검색창을 클릭하기
{{% /hint %}}

검색 페이지는 헤더에 키워드 입력창과 고급 필터가 있다는 것을 제외하면
메인 페이지와 동일합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/1zqe0fz7r1u3upcbn3yiy/seotax-09-layout-search-page.webp?rlkey=4f70xges6xm3mrfpofgmh4zit&raw=1"
  alt="서택스 테마 레이아웃 - 검색 페이지"
  caption="검색 페이지 - 검색 결과"
  class="screenshot-image" >}}

게시글 항목 템플릿을 공유하여 사용하기 때문에 해당 부분 템플릿을 변경하면
메인 페이지와 검색 페이지에 같이 반영됩니다.
하지만, 검색 페이지에서 페이지네이션은 JS를 활용해 동적으로 생성하기 때문에
페이지네이션 템플릿을 변경해도 검색 페이지에서는 반영되지 않습니다.

{{< columns >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/8lp7kwykjgzm7m6t8xszk/seotax-10-layout-search-category1.webp?rlkey=ssl44wsb3wxdkodb5knl8gkme&raw=1"
  alt="서택스 테마 레이아웃 - 부모 카테고리 검색 페이지"
  caption="검색 페이지 - 부모 카테고리"
  class="screenshot-image" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/zcdv81er5vhxs4xrk3qve/seotax-11-layout-search-category2.webp?rlkey=xd5i52b1xsnupi867duqrykmy&raw=1"
  alt="서택스 테마 레이아웃 - 자식 카테고리 검색 페이지"
  caption="검색 페이지 - 자식 카테고리"
  class="screenshot-image" >}}
{{< /columns >}}

검색 시 키워드 없이 카테고리 필터만 적용하면 카테고리 전용 UI를 가진 검색 페이지로 이동합니다.

카테고리 검색 페이지에서는 "검색 결과" 라는 제목 대신 카테고리 명칭을 제목으로 표시합니다.

부모 카테고리와 자식 카테고리에서 보여지는 모습도 다른데,
부모 카테고리에서는 하위에 있는 자식 카테고리들을 칩 형태로 표시하고,
자식 카테고리에서는 상위에 있는 부모 카테고리를 칩 형태로 표시합니다.
카테고리 칩을 클릭하면 해당 카테고리 검색 결과로 이동할 수 있습니다.

{{< columns >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/1bc1my7pkrlmzgu0ko5ap/seotax-12-layout-search-tag.webp?rlkey=3g7qzikewtihk2mzvt8q3n2uo&raw=1"
  alt="서택스 테마 레이아웃 - 단일 태그 검색 페이지"
  caption="검색 페이지 - 단일 태그"
  class="screenshot-image" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/dz5qw2nxplbly4dutvif5/seotax-13-layout-search-tags.webp?rlkey=kf1hgdnfebakkqinlqtorgakk&raw=1"
  alt="서택스 테마 레이아웃 - 여러 개 태그 검색 페이지"
  caption="검색 페이지 - 여러 개 태그"
  class="screenshot-image" >}}
{{< /columns >}}

태그 페이지 또한 단일 태그만 선택한 경우와 여러 개의 태그를 선택한 경우가 다릅니다.

단일 태그 검색 시에는 태그 명칭을 제목으로 사용하지만,
태그가 여러 개라면 일반적인 검색 페이지처럼 "검색 결과" 라는 제목을 표시합니다.   
대신, 태그가 여러 개일 경우 "검색 태그" 라는 영역을 별도로 표시하여
단일 태그 검색으로 즉시 이동할 수 있도록 지원합니다.

### 카테고리 페이지

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/s30dtz21t0108viy7b3as/seotax-14-layout-categories.webp?rlkey=8e5o67hrfl4fblu10hjfpwtkn&raw=1"
  alt="서택스 테마 레이아웃 - 카테고리 페이지"
  class="screenshot-image" >}}

카테고리 페이지는 사이드 메뉴에서 폴더 아이콘 또는 "전체" 카테고리를 클릭하면 이동할 수 있습니다.

2단계 카테고리가 트리 구조로 나열되며, 카테고리에 속한 게시글들을 최대 3개까지 보여줍니다.
만약 관련 게시글이 더 있다면 카테고리 전용 검색 페이지로 이동하는 더보기 링크가 나타납니다.

### 태그 페이지

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/akchj2px0quzh1tfkunpd/seotax-15-layout-tags.webp?rlkey=7zfkorz2b2p49nej7msl6vgq8&raw=1"
  alt="서택스 테마 레이아웃 - 태그 페이지"
  class="screenshot-image" >}}

태그 페이지는 사이드 메뉴에서 태그 아이콘을 클릭하면 이동할 수 있습니다.

게시글에 등록된 모든 태그들이 칩 형태로 나열되어 있습니다.
태그 칩을 클릭하면 태그 전용 검색 페이지로 이동합니다.

### 반응형 디자인

{{< columns class="columns-4" >}}
{{< columns >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/80anepeo1tm9xiqd2z6av/seotax-16-layout-mobile-main.webp?rlkey=vq94p5tgaaql3xb8k4lrqakb3&raw=1"
  alt="서택스 테마 레이아웃 - 반응형 모바일 메인 페이지"
  caption="모바일 - 메인 페이지"
  class="screenshot-image" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/ps9eoehqob5xqcqgs5ydg/seotax-17-layout-mobile-search.webp?rlkey=jd28nckfeolgm8226lb8m5exd&raw=1"
  alt="서택스 테마 레이아웃 - 반응형 모바일 검색 페이지"
  caption="모바일 - 검색 페이지"
  class="screenshot-image" >}}
{{< /columns >}}
<--->
{{< columns >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/lz5kdvsrmmkgin85hd2u5/seotax-18-layout-mobile-menu.webp?rlkey=69a4sw0k5ifbbdzbaiw8vk6l0&raw=1"
  alt="서택스 테마 레이아웃 - 반응형 모바일 사이드 메뉴"
  caption="모바일 - 사이드 메뉴"
  class="screenshot-image" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/kb4jirkcdhpmzhqhow34n/seotax-19-layout-mobile-toc.webp?rlkey=f0li3d8gfwiwatvh0otpwtrxx&raw=1"
  alt="서택스 테마 레이아웃 - 반응형 모바일 목차 오버레이"
  caption="모바일 - 목차 오버레이"
  class="screenshot-image" >}}
{{< /columns >}}
{{< /columns >}}

화면 너비에 따른 디자인도 CSS 미디어 쿼리로 자연스럽게 제어했습니다.
- 본문 영역이 사이드 메뉴 또는 목차와 겹치지 않도록 특정 너비 이하에서 숨김 처리합니다.
- 데스크탑 너비에서는 게시글 항목의 정사각형 썸네일 이미지를 우선적으로 표시하지만,
  모바일 너비에서는 가로형 비율인 커버 이미지를 우선적으로 표시합니다.
- 페이지네이션, 검색 필터 등 가로로 길어 모바일 너비에서 오버플로우가 발생하는 영역을 보기 좋게 정렬했습니다.
- 모바일 너비에서는 상단에 전용 헤더가 표시됩니다.   
  모바일 헤더에서 햄버거 또는 리스트 아이콘을 클릭하면 사이드 메뉴 또는 목차 오버레이를 노출시킵니다.

## 테마 디렉터리 구조

서택스 테마의 디렉터리 구조는 단순히 계층적인 구조를 풀어서 설명하기보다,
해당 테마 제작에 많은 영향을 받은 Book 테마의 구조와 비교하는게 설계 의도를 파악하는데
더 유용할 것이라 생각합니다.

따라서, 두 테마의 디렉터리 구조를 아래와 같이 트리 구조로 비교해서 보여드립니다.
(왼쪽이 서택스 테마, 오른쪽이 Book 테마입니다.)

{{% columns %}}
```bash
seotax/
├── archetypes/
├── assets/
│   ├── css/
│   ├── data/
│   ├── js/
│   ├── main.scss
│   ├── sw-register.js
│   └── sw.js
├── exampleSite/
├── i18n/
│   ├── en.yaml
│   └── ...
├── layouts/
│   ├── _markup/
│   ├── _partials/
│   ├── _shortcodes/
│   ├── categories/
│   ├── search/
│   ├── tags/
│   ├── 404.html
│   ├── baseof.html
│   ├── index.html
│   ├── list.html
│   └── single.html
├── static/
└── theme.toml
```
<--->
```bash
book/
├── archetypes/
├── assets/
│   ├── ...
│   ├── _main.scss
│   ├── ...
│   ├── book.scss
│   ├── ...
│   ├── sw-register.js
│   └── sw.js
├── exampleSite/
├── i18n/
│   ├── en.yaml
│   └── ...
├── layouts/
│   ├── _markup/
│   ├── _partials/
│   ├── _shortcodes/
│   ├── posts/
│   ├── 404.html
│   ├── baseof.html
│   ├── landing.html
│   ├── list.html
│   ├── single.html
│   └── term.html
├── static/
└── theme.toml
```
{{% /columns %}}

`assets/`, `layouts/` 등 1단계 경로들은 Hugo에서 요구하는 명칭이므로 동일하고,
2단계 경로부터 차이가 있습니다.

(Hugo에서 정의한 디렉터리 구조를 알고 싶다면 아래 공식문서를 참고할 수 있습니다.)

{{< bookmark "https://gohugo.io/getting-started/directory-structure/" >}}

### 리소스 경로

{{% columns %}}
```bash
seotax/assets/
├── css/
│   ├── main/
│   ├── themes/
│   ├── variables/
│   └── ...
├── data/
├── js/
│   ├── core/
│   ├── partials/
│   ├── search/
│   └── shortcodes/
├── main.scss
├── sw-register.js
└── sw.js
```
<--->
```bash
book/assets/
├── ...
├── _defaults.scss
├── ...
├── _main.scss
├── ...
├── _shortcodes.scss
├── ...
├── book.scss
├── clipboard.js
├── ...
├── search-data.json
├── search.js
├── sw-register.js
└── sw.js
```
{{% /columns %}}

`assets/` 경로는 CSS, JavaScript 등의 리소스를 모아두는 경로인데,
Book 테마에서는 이러한 `.scss`, `.json`, `.js` 파일들이 같은 수준에 배치되어 있습니다.
세어보면 20개 정도 있는데, 서택스 테마는 동적 페이지 렌더링을 위해 JavaScript를 적극 활용하다보니
파일들이 계속 추가되면서 세로로 너무 길어진다는 불편함을 느꼈습니다.

그래서, `css/`, `data/`, `js/` 세 종류의 폴더로 확장자별 파일들을 구분하고,
그 안에서도 각각의 파일이 웹사이트에서 수행하는 역할에 따라 세분화시켰습니다.
예를 들어, `css/variables/` 경로는 색상 변수들을 정의한 `.scss` 파일 등이 있고,
`js/partials/` 경로는 `layouts/` 경로의 특정 템플릿 파일을 대상으로 수행되는 `.js` 파일들이 존재합니다.

`data/` 경로는 따로 하위 경로를 구분하지 않았는데,
검색 인덱스로 활용할 데이터를 구성하는 `content.json` 파일 등이 배치됩니다.

### 레이아웃 경로

{{% columns %}}
```bash
seotax/layouts/
├── _markup/
├── _partials/
│   ├── ...
│   ├── head.html
│   └── ...
├── _shortcodes/
├── categories/
├── search/
├── tags/
├── 404.html
├── baseof.html
├── index.html
├── list.html
└── single.html
```
<--->
```bash
book/layouts/
├── _markup/
├── _partials/
│   └── docs/
│       ├── ...
│       ├── head.html
│       └── ...
├── _shortcodes/
├── posts/
├── 404.html
├── baseof.html
├── landing.html
├── list.html
├── single.html
└── term.html
```
{{% /columns %}}

`_markup/`, `_partials/`, `_shortcodes/` 는 Hugo에서 정의된 경로로
폴더명을 동일하게 유지했습니다.

각각의 역할은 이어지는 게시글에서 자세하게 설명하겠지만, 간략하게 말씀드리면
`_markup/` 은 마크다운 렌더링과 관련,
`_partials/` 는 사이드 메뉴, 목차 등 부분적인 템플릿과 관련,
`_shortcodes/` 는 마크다운 파일에서 호출할 목적의 HTML 코드 뭉치로 이해할 수 있습니다.

Book 테마는 컨텐츠들이 `/docs/` 경로에 위치하여 부분 템플릿도 `_partials/docs/` 로 맞춰놨는데,
서택스 테마는 `posts/` 경로 아래에 컨텐츠들을 놓는데다가, 폴더 하나 달랑 놓자고 깊이를 하나 더 추가하는건
낭비라고 생각해서 `_partials/` 경로 바로 아래에 부분 템플릿 파일들을 배치했습니다.
서택스 테마의 `_partials/` 에서는 `assets/css/` 경로에서와 마찬가지로 역할 별로 하위 경로를 구분했습니다.

`term.html` 템플릿 파일은 앞선 고려사항에서 태그 하나하나에 대해 정적 페이지가 만들어지는 것을 중지시켰기 때문에
더 이상 필요하지 않아 삭제했습니다. 하지만, 카테고리 및 태그 목록을 표시하는 페이지(`/categories/`, `/tags/`)는
여전히 필요해서 `categoires/terms.html`, `tags/terms.html` 레이아웃을 추가했습니다.

## 다음 글 안내

지금까지 Hugo의 서택스 테마를 만들게 된 계기부터 각각의 레이아웃 및 디렉터리 구조를 정리했습니다.

다음 글에서는 서택스 테마의 핵심 기능들에 대한 구현 원리와 동작 흐름을 살펴보겠습니다.

각 기능별로 관련 HTML 템플릿, SCSS 스타일, Vanilla JS 모듈을 예제 코드와 함께 분석하여,
테마 이용자가 필요에 따라 일부 코드를 수정해서 사용할 수 있도록 도움이 되기를 바랍니다.
특히, 이러한 기능을 만들게 된 계기와 기능을 구현하면서 겪은 시행착오를 같이 안내하여
개발자의 의도가 전달되기를 기대합니다.
