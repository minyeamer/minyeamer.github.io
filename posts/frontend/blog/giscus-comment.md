---
title: "Hugo 블로그 댓글 시스템 교체 - Disqus에서 giscus로"
date: "2026-05-23T17:16:17+09:00"
layout: "post"
description: >
  Hugo 블로그 댓글 시스템을 Disqus에서 giscus로 교체한 과정을 다룹니다.
  Disqus 무료 플랜의 광고 문제와 utterances 및 giscus 비교, GitHub Discussions 기반 giscus 설치 및 설정 방법,
  서택스 테마에 라이트/다크 모드 및 다국어 번역을 연동한 giscus 구현 과정, Disqus와 병행 지원하는 멀티 프로바이더 구조까지 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/3ypdfi1yfpcex8vaej38p/giscus-00-cover.webp?rlkey=7jscfyt2iuz2797ppnmltgnx1&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/9i8sz89wvwrmywtedd0h2/giscus-00-logo.webp?rlkey=os60fso7gjmg8n9huf0zjdskj&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "giscus", "Disqus", "utterances", "댓글 시스템", "GitHub Discussions", "SeoTax", "서택스 테마", "개발 블로그"]
series: ["Hugo 테마 만들기"]
---

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo 블로그의 댓글 시스템을 Disqus에서 GitHub Discussions 기반 giscus로 교체한 과정을 다룹니다.
Disqus 무료 플랜에서 일정 트래픽 이후 노출되는 광고 문제를 계기로 이탈을 결심하고,
대안으로 utterances와 giscus를 비교해 giscus를 선택한 이유를 설명합니다.
또한 서택스 테마에 giscus를 통합하면서 라이트/다크 모드 전환 시 댓글창 테마가 함께 바뀌도록 구현한 방법,
언어 변경 시 댓글창 표시 언어가 함께 교체하도록 구현한 방법, 그리고
기존 Disqus도 설정 값 하나로 사용 가능한 멀티 프로바이더 구조를 설명합니다.

- **[Disqus 사용 경험](#disqus를-사용-경험)**: 무료 플랜에서 방문자 수 증가 후 노출되는 광고로 인해 이탈하게 된 경험
- **[댓글 시스템 비교](#utterances-vs-giscus)**: GitHub Issues 기반의 utterances와 GitHub Discussions 기반의 giscus 비교
- **[giscus 설정하기](#giscus-설정하기)**: Discussions 활성화 및 카테고리 생성, giscus 앱 설치, giscus 스크립트 속성 설정
- **[서택스 테마 적용](#서택스-테마에-giscus-추가하기)**: 댓글 템플릿 구현, 색상 테마 및 언어 속성 동적 변환 (postMessage API 사용)
- **[멀티 프로바이더 구조](#disqus와-병행-지원하기)**: provider 설정 한 줄로 giscus/Disqus 전환 지원
{{% /hint %}}

Hugo 블로그는 기본적으로 댓글 기능을 제공하지 않기 때문에 서드파티 댓글 서비스를 직접 연동해야 합니다.
저는 블로그를 운영하면서 utterances에서 Disqus로, 그리고 이번에 giscus로 세 번째 댓글 시스템을 바꾸게 되었습니다.

## Disqus 사용 경험

서택스(SeoTax) 테마는 [Hugo Book](https://themes.gohugo.io/themes/hugo-book/) 테마를
기반으로 제작되었고, 해당 테마에서 사용하던 Disqus 댓글 시스템을 그대로 사용했습니다.

이 테마를 사용하기 전에는 [utterances](/blog/hugo-blog-old-2/)라는
Github Issues 기반 댓글 시스템을 이미 사용하고 있었는데 Disqus로 바꾼 것은 접근성 때문이었습니다.
utterances 댓글을 작성하려면 Github 계정이 필요하지만,
Disqus는 일반적인 소셜 계정(구글, X, Facebook 등)만 있으면 댓글을 남길 수 있습니다.
더 다양한 독자층이 참여할 수 있을 것을 기대해서 Disqus를 선택했습니다.

특별히 댓글을 유도한 것은 아니지만, 4개월의 Disqus 사용 기간 동안 댓글은 거의 달리지 않았습니다.
원래부터 그정도의 관심이 없었을 수도 있었겠지만,
결과적으론 다양한 SNS 계정을 지원한다는 장점이 실질적인 참여율 향상으로 이어지지 않았던 것입니다.

Disqus를 사용하면서 한 가지 단점이, 상용 서비스의 무료 플랜을 사용하다보니
블로그 방문자 수가 일정 기준을 넘으면 댓글창 하단에 광고가 노출됩니다.
(기본적으로는 댓글창 위에 광고가 달리고, 댓글창 하단으로 광고를 이동시키거나 없애고 싶으면 유료 플랜을 구독해야 합니다.)

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/epooikfmgox4vbt8xnzcr/giscus-01-disqus.webp?rlkey=5voo7efblegi0ehnffyokixso&raw=1"
  alt="Disqus 댓글창과 광고"
  max-width="800px"
  align="center" >}}

저도 Disqus를 설치하고 한 달 이후부터 광고가 달리기 시작했는데,
무료 플랜으로 여전히 이용하고 싶었지만 댓글창 위에 광고가 달리면 아무도 댓글을 작성하지 않을 것 같아서,
그렇다고 광고 배너를 아예 없애버리면 Disqus 계정이 정지될 것 같아서
광고 배너를 댓글창 하단으로 이동시키는 스크립트를 적용했습니다.

{{% details summary="스크립트를 보고 싶으시면 여기를 클릭해서 펼쳐주세요." %}}
```javascript
window.relocateDisqus = () => {
  let attempts = 0;
  const maxAttempts = 20;
  const intervalId = setInterval(() => {
    attempts++;
    // `#disqus_thread` 요소를 다룬다는 것을 직접적으로 드러내지 않기 위해 Base64 인코딩
    const container = document.getElementById(atob(atob('WkdsemNYVnpYM1JvY21WaFpBPT0=')));
    var success = false;
    if (container) {
      const adframe = container.querySelector(atob(atob('VzNyWWM9JTJGYWRzJTJGYWRmcmFtZQ==')));
      if (adframe) {
        container.appendChild(adframe);
        success = true;
      }
    }
    if (success || (attempts > maxAttempts)) {
      clearInterval(intervalId);
    }
  }, 1000);
};
```
{{% /details %}}

이렇게라도 Disqus 댓글 시스템을 이용하려고 했지만,
몇 달 동안 통계를 보면서 광고 배너가 노출되는 결점을 감수하면서까지 사용할 필요성을 못느꼈습니다.
결국 다시 Github 기반 댓글 시스템으로 돌아가기로 결정했습니다.
오히려, 저는 기술적인 포스팅만 다루면서 독자의 대부분이 개발자인 것을 기대하기 때문에
소셜 계정보다 Github 계정의 접근성이 더 좋을 것이라 판단하여 giscus를 선택했습니다.

## utterances vs giscus

GitHub 기반 댓글 시스템으로 돌아오기로 결정하고 두 가지 선택지를 비교했습니다.

| | utterances | giscus |
|---|---|---|
| **데이터베이스** | GitHub Issues | GitHub Discussions |
| **라이트/다크 테마** | 지원 | 지원 |
| **반응(Reaction)** | 미지원 | 지원 |
| **대댓글** | 미지원 | 지원 |

[utterances](https://github.com/utterance/utterances)는
GitHub Issues를 댓글 저장소로 사용하는데, Issues는 본래 버그 리포트나 기능 제안을 위한 공간입니다.
제 블로그 저장소에 누군가가 이런 제안을 할 일은 없기 때문에 댓글 저장소로 사용하는데
문제되진 않지만, 그럼에도 여전히 인가되지 않은 사용자가 Issue를 생성하는 걸 막을 순 없습니다.

반면에, [giscus](https://github.com/giscus/giscus)는 GitHub Discussions을 사용하면서
카테고리를 공지(Announcement)로 설정하면 메인테이너를 제외한 사용자가 저장소에
Discussion을 생성하는 걸 차단할 수 있기 때문에 온전히 댓글 저장소로만 이용할 수 있다는 장점이 있습니다.
거기에 반응이나 대댓글도 활용할 수 있어서 상대적으로 장점이 많다고 판단했습니다.
(또한, utterances는 마지막 업데이트가 4년 전에 멈춰있지만, giscus는 아직도 업데이트되고 있어서
더욱 매력적이라 느꼈습니다.)

{{< bookmark "https://giscus.app" >}}

## giscus 설정하기

### GitHub Discussions 활성화

giscus를 사용하려면 우선 연결할 GitHub 저장소에 Discussions 기능이 활성화되어 있어야 합니다.
저장소는 공개(Public)되어있다면 별도의 빈 저장소를 만들어도 괜찮습니다.
저장소의 **Settings → General → Features** 섹션에서 **Discussions**를 체크합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/2qugt568d5tm7rlhy3u6y/giscus-02-enable-discussions.webp?rlkey=cmmdwk09s458a8eclwe1z5ucl&raw=1"
  alt="Discussions 활성화"
  max-width="700px"
  align="center" >}}

활성화하면 저장소 상단 탭에 **Discussions** 메뉴가 생깁니다.

![Discussions 메뉴](https://dl.dropboxusercontent.com/scl/fi/vqfp23krucja43n4k1q6b/giscus-03-navbar-discussions.webp?rlkey=i4wyrst8h9xtjpperjb2ti30f&raw=1)

### Discussions 카테고리 생성

Discussions에서 카테고리를 별도로 생성하는 것을 권장합니다.
기본으로 제공되는 General, Ideas 등의 카테고리와 블로그 댓글이 섞이지 않도록
**Discussions → Categories → New category**에서 전용 카테고리를 만듭니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/inoczxleon4ksq7jrz4eb/giscus-04-create-category.webp?rlkey=8as0jw856dlrybp5zjwt8fmdj&raw=1"
  alt="Discussions - Create Category"
  max-width="700px"
  align="center" >}}

Discussion Format을 선택할 때 **Announcements**를 권장합니다.
Open-ended discussion으로 설정하면 누구나 직접 Discussion을 생성할 수 있어
무관한 글이 댓글 카테고리에 섞일 수 있습니다.
Announcements 형식은 메인테이너와 giscus 봇만 Discussion을 생성할 수 있고,
나머지 사용자는 댓글과 반응만 남길 수 있어 관리가 깔끔합니다.

### giscus 앱 설치

giscus가 저장소의 Discussions에 접근하려면 GitHub App을 설치해야 합니다.
[giscus app](https://github.com/apps/giscus)에서 Install 버튼을 클릭합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/5w4teqvdjfovfk39bo7cd/giscus-05-install-giscus.webp?rlkey=337dvlxh32j5f3pbiemonzlm8&raw=1"
  alt="Giscus - Configure"
  max-width="800px"
  align="center" >}}

설치 시 레포지토리 접근 범위를 선택할 수 있습니다.
댓글 저장소로 사용할 하나의 저장소만 선택하면 됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/879con344461pkqneytc9/giscus-06-select-repositories.webp?rlkey=fj8e2xqvd00625vm0a6xg76rx&raw=1"
  alt="Giscus - Configure"
  max-width="600px"
  align="center" >}}

### giscus 스크립트 생성

설치가 완료됐다면 [giscus.app](https://giscus.app) 페이지에서
각 설정값을 입력하면 삽입할 스크립트가 자동으로 생성됩니다.

**Repository** — Discussions이 활성화된 저장소를 입력합니다.
giscus 권한을 부여한 저장소라면 녹색으로 성공 메시지가 표시됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/pzlz5dhhh4j80wa8tusvm/giscus-07-config-repository.webp?rlkey=i137dbfw34lgsukqjm4brxnsf&raw=1"
  alt="giscus.app - 저장소"
  max-width="700px"
  align="center" >}}

**Page ↔️ Discussions Mapping** — 블로그 포스트와 Discussions을 어떻게 매핑할지 결정합니다.
기본으로 `pathname`으로 선택되어 있고 가장 최소한의 고유한 값이기 때문에 이 선택지가 적절합니다.
URL 전체를 기준으로 하면 길이도 길면서 도메인이 변경되는 경우도 고려해야 하는 문제가 있고,
제목은 쉽게 변경될 수 있기 때문에 부적절합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/8b201r02kt5ff36pc0j9c/giscus-08-config-mapping.webp?rlkey=6tzulzla9mgrik9we7tf8ud16&raw=1"
  alt="giscus.app - 페이지 ↔️ Discussions 연결"
  max-width="700px"
  align="center" >}}

**Discussion Category** — 댓글이 기록된 Discussions 카테고리를 선택합니다.

**이 카테고리에서만 검색**한다는 옵션을 체크하면 다른 카테고리와 혼동되지 않게 댓글을 불러올 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/9ecj0vi6hewsz7p0i2lcy/giscus-09-config-category.webp?rlkey=zairj3hhszqannuanihvqmkpd&raw=1"
  alt="giscus.app - Discussion 카테고리"
  max-width="700px"
  align="center" >}}

**Features** — 반응 이모지 활성화와 지연 로딩을 활성화했습니다.
지연 로딩은 사용자가 댓글 영역 근처로 스크롤할 때 로드하므로 페이지 초기 로딩 성능에 영향을 주지 않습니다.
그 외에 메타데이터나 댓글 입력창 위치는 취향에 따라 선택할 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/uarkl8ag7ui3eth8ehuer/giscus-10-config-features.webp?rlkey=av8wpymq5d4uki9wos4onl4hl&raw=1"
  alt="giscus.app - 기능"
  max-width="700px"
  align="center" >}}

**Theme** — 다양한 색상 테마를 선택할 수 있습니다.
테마가 고정된 블로그라면 어울리는 색상을 선택하면 되고, 사용자의 시스템 설정에 따르려면
`Preferred color scheme`을 설정할 수 있습니다.

서택스 테마는 라이트 모드와 다크 모드를 전환하는 기능을 제공하기 때문에
동적으로 테마를 변경하는 스크립트를 구현했습니다. 이 부분은 아래에서 설명합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/anjftpv0lr8uvw21n5k7a/giscus-11-config-theme.webp?rlkey=up0thodlzv91tr0thkjb5g8rh&raw=1"
  alt="giscus.app - 테마"
  max-width="600px"
  align="center" >}}

**Language** — 한국어를 선택하면 giscus UI가 한국어로 표시됩니다.

서택스 테마는 일부 텍스트를 사용자가 원하는 언어로 변경하는 기능을 제공하기 떄문에
언어 속성 역시 동적으로 전환하는 스크립트를 구현했습니다. 이 부분은 아래에서 설명합니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/x628fly921uhn60mwvf2e/giscus-12-config-language.webp?rlkey=dxmbzdvlxxcdot921d1jaelc6&raw=1"
  alt="giscus.app - 언어"
  max-width="600px"
  align="center" >}}

모든 설정을 마치면 페이지 하단에 삽입할 스크립트 코드가 생성됩니다.

```html
<script src="https://giscus.app/client.js"
        data-repo="[ENTER REPO HERE]"
        data-repo-id="[ENTER REPO ID HERE]"
        data-category="[ENTER CATEGORY NAME HERE]"
        data-category-id="[ENTER CATEGORY ID HERE]"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="bottom"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
```

## giscus 댓글 작성하기

속성 값을 채워넣어 블로그 테마에 스크립트를 삽입하면 아래 이미지와 같은 댓글창이 추가됩니다.

![giscus 댓글창](https://dl.dropboxusercontent.com/scl/fi/xb0v7fwnwa81guvc8ue2h/giscus-13-comment-box.webp?rlkey=zsgn280cyff0ac56w9t5hddld&raw=1)

실제로 글을 발행하고 댓글을 작성하면 아래 이미지와 같이 Discussion이 생성됩니다.

![blog/giscus-comment/ #2](https://dl.dropboxusercontent.com/scl/fi/tgy30lam2u69824nqkl8e/giscus-14-giscus-bot.webp?rlkey=2ej7cbi5cc6oixzpqxi3i8mwb&raw=1)

## 서택스 테마에 giscus 추가하기

[giscus.app](https://giscus.app/)에서 생성된 스크립트를 그대로 HTML에 붙여넣을 수도 있지만,
서택스 테마에서는 3가지 고려해야 할 사항이 있습니다.

1. **사용자별 저장소 설정**: 서택스 테마는 공개적으로 배포되어 여러 사용자들이 이용할 것을 기대합니다.
   서로 다른 저장소를 갖고 있는 사용자에게 테마의 코드 베이스를 수정하라고 하는건 불편하기 때문에
   YAML 설정값을 읽어오도록 하는게 이상적입니다.
2. **라이트/다크 모드 전환**: 서택스 테마에서 좌측 사이드 메뉴에서 토글 버튼을 클릭하면 테마 색상을 전환할 수 있습니다.
   댓글창의 색상도 이를 따라서 동적으로 전환해야 합니다.
3. **표시 언어 변환**: 서택스 테마는 우측 하단 툴바에서 사용가 원하는 언어를 직접 선택할 수 있습니다.
   선택된 언어가 댓글창에도 동적으로 반영되어야 합니다.

이 문제를 해결하기 위해 스크립트를 동적으로 주입하는 방식을 선택했습니다.

### 동적 삽입 스크립트 구현

서택스 테마에서 기존에 Disqus 댓글창을 구현했던
`layouts/_partials/footer/comments.html` 템플릿을 giscus로 교체했습니다.

```html
<!-- layouts/_partials/footer/comments.html -->

<div class="giscus" id="giscus-container"></div>
<script>
  (function() {
    var s = document.createElement('script');
    s.src = 'https://giscus.app/client.js';
    s.setAttribute('data-repo', '{{ .Site.Params.comments.giscus.repo }}');
    s.setAttribute('data-repo-id', '{{ .Site.Params.comments.giscus.repoId }}');
    s.setAttribute('data-category', '{{ .Site.Params.comments.giscus.category }}');
    s.setAttribute('data-category-id', '{{ .Site.Params.comments.giscus.categoryId }}');
    s.setAttribute('data-mapping', '{{ .Site.Params.comments.giscus.mapping | default "pathname" }}');
    s.setAttribute('data-strict', '0');
    s.setAttribute('data-reactions-enabled', '1');
    s.setAttribute('data-emit-metadata', '0');
    s.setAttribute('data-input-position', '{{ .Site.Params.comments.giscus.inputPosition | default "bottom" }}');
    s.setAttribute('data-theme', 'preferred_color_scheme');
    s.setAttribute('data-lang', '{{ .Site.Language.Lang }}');
    s.setAttribute('data-loading', 'lazy');
    s.setAttribute('crossorigin', 'anonymous');
    s.async = true;
    document.getElementById('giscus-container').appendChild(s);
  })();
</script>
<noscript>{{ i18n "comments.noscript.text" | default "Please enable JavaScript to view the comments." }}</noscript>
```

Hugo 설정을 다음과 같이 구성했을 때,
Hugo 렌더링 시점에 `params`에서 대응되는 경로의 값을 읽어 스크립트에 주입할 수 있습니다.

```yaml
params:
  comments:
    giscus:
      repo: "[ENTER REPO HERE]"
      repoId: "[ENTER REPO ID HERE]"
      category: "[ENTER CATEGORY NAME HERE]"
      categoryId: "[ENTER CATEGORY ID HERE]"
      mapping: "pathname"
      inputPosition: "bottom"
```

### 라이트/다크 모드 전환

서택스 테마는 `localStorage`에 개인별 테마 설정을 저장합니다. 페이지 로드 시점에 이 값을 읽어서
giscus 스크립트의 `data-theme` 값에 주입하는 방식으로 색상 테마 변환을 적용했습니다.
(서택스 테마의 다크모드 토글에 대한 구체적인 설명은
[Hugo 블로그 다크모드 구현](/blog/hugo-seotax-4/#테마-전환-시스템-구현하기) 글을 참고할 수 있습니다.)

```html
<!-- layouts/_partials/footer/comments.html -->

<div class="giscus" id="giscus-container"></div>
<script>
  (function() {
    var savedTheme = localStorage.getItem('hugo-dark-mode');
    var isDark = (savedTheme === 'dark') ||
      (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches);

    var s = document.createElement('script');
    ...
    s.setAttribute('data-theme', isDark ? 'dark' : 'light');
    ...
    document.getElementById('giscus-container').appendChild(s);
  })();
</script>
```

서택스 테마의 색상을 고려하면 라이트 모드에서는 Github Light(`"light"`),
다크 모드에서는 Github Dark(`"dark"`) 테마가 적절합니다.
두 가지 경우에 따라 적절한 속성 값을 주입하도록 스크립트를 수정했습니다.
추가로, 사용자가 토글 버튼을 눌렀을 때 동적으로 테마가 전환되게 해야 합니다.

```html
<script>
  (function() {
    ...
    document.getElementById('giscus-container').appendChild(s);
    ...
    window.setGiscusTheme = function(theme) {
      var iframe = document.querySelector('iframe.giscus-frame');
      if (iframe) {
        iframe.contentWindow.postMessage(
          { giscus: { setConfig: { theme: theme } } },
          'https://giscus.app'
        );
      }
    };
  })();
</script>
```

giscus는 로드된 후에도 `postMessage` API를 통해 테마를 변경할 수 있습니다.
API를 호출하는 `setGiscusTheme` 전역 함수를 등록하고, 다크모드 토글 동작을 담당하는
`assets/js/core/set-theme.js` 파일에서 토글 액션이 발생했을 때 해당 함수를 호출하도록 수정했습니다.

기존에 Disqus를 새로고침하던 코드를:

```javascript
// 변경 전
if (window.DISQUS && typeof window.reloadDisqus === 'function') {
  window.reloadDisqus();
}
```

giscus의 `postMessage` API를 호출하는 코드로 교체했습니다:

```javascript
// 변경 후
if (typeof window.setgiscusTheme === 'function') {
  window.setgiscusTheme(isDark ? 'light' : 'dark');
}
```

`isDark`는 토글 직전의 상태이므로, 토글 후 테마는 반전된 값입니다.
Disqus처럼 iframe 전체를 다시 로드할 필요 없이 설정값만 전달하기 때문에
댓글 목록이 유지된 채 테마가 자연스럽게 전환됩니다.

### 표시 언어 변환

서택스 테마는 `localStorage`에 개인별 언어 설정을 저장합니다. 페이지 로드 시점에 이 값을 읽어서
giscus 스크립트의 `data-lang` 값에 주입하는 방식으로 언어 변환을 적용했습니다.
(서택스 테마의 동적 다국어 번역에 대한 구체적인 설명은
[Hugo 동적 다국어 번역](/blog/hugo-seotax-3/#javascript-동적-번역) 글을 참고할 수 있습니다.)

```html
<!-- layouts/_partials/footer/comments.html -->
 
<div class="giscus" id="giscus-container"></div>
<script>
  (function() {
    var s = document.createElement('script');
    ...
    var storedLang = localStorage.getItem('site-language') || '{{ .Site.Language.Lang }}';
    s.setAttribute('data-lang', storedLang);
    ...
    document.getElementById('giscus-container').appendChild(s);
  })();
</script>
```

색상 테마와 마찬가지로 해당 스크립트는 페이지의 초기 로그 시점만 고려합니다.
사용자가 언어를 교체했을 때 동적으로 언어가 변환되게 해야 합니다.
앞에서 `postMessage` API를 통해 색상 테마를 업데이트할 수 있었습니다.
변경된 언어 속성 적용도 동일한 방식을 사용합니다.

```html
<script>
  (function() {
    ...
    document.getElementById('giscus-container').appendChild(s);
    ...
    window.setGiscusLang = function(lang) {
      var iframe = document.querySelector('iframe.giscus-frame');
      if (iframe) {
        iframe.contentWindow.postMessage(
          { giscus: { setConfig: { lang: lang } } },
          'https://giscus.app'
        );
      }
    };
  })();
</script>
```

`assets/js/core/i18n.js` 파일에서 드롭다운 메뉴를 통해 언어 속성이 변경되었을 때,
giscus의 `postMessage` API를 호출하는 `setGiscusLang` 전역 함수를 실행하는 코드를 추가했습니다.

```javascript
window.addEventListener('DOMContentLoaded', function() {
  window.siteI18n.initData()
  .then(() => {
    ...
    if (selector) {
      ...
      // 언어 선택기의 속성 값이 변경되는 이벤트
      selector.addEventListener('change', (e) => {
        ...
        if (typeof window.setGiscusLang === 'function') {
          window.setGiscusLang(e.target.value);
        }
      });
    }

  })
  .catch(() => {
    if (selector) {
      selector.value = window.siteI18n.defaultLang;
    }
  });
});
```

서택스 테마에서 정의한 언어 코드와 giscus에서 정의한 `data-lang` 속성 값이 다르면
중간에 불편하게 매핑해야 했겠지만 다행히 값이 일치해서 그대로 전달했습니다.
이제 서택스 테마 언어를 변경하면 giscus의 표시 언어도 동적으로 변경됩니다.

## Disqus와 병행 지원하기

서택스 테마는 공개적으로 배포되어 여러 사용자들의 환경을 고려해야 합니다.
댓글 시스템 또한 저는 gisqus로 전환했지만, 누군가는 Disqus를 사용하고 싶을 수 있으므로
기존 Disqus도 제거하지 않고 설정에 따라 하나를 선택할 수 있는 멀티 프로바이더 구조로 개선했습니다.

이를 위해 하나의 `comments.html` 템플릿 파일을 3가지로 구분했습니다.

```bash
layouts/_partials/footer/
├── comments.html           # `proivder` 설정에 따라 라우팅
├── comments-disqus.html    # Disqus 구현
└── comments-giscus.html    # giscus 구현
```

기존 `comments.html`은 설정 파일의 `provider` 값을 읽어
해당 구현체로 라우팅하는 2줄짜리 라우터로 대체했습니다.

```html
<!-- layouts/_partials/footer/comments.html -->
{{ $provider := .Site.Params.comments.provider | default "giscus" }}
{{ partial (printf "footer/comments-%s.html" $provider) . }}
```

`provider`가 설정되지 않으면 기본값으로 `giscus`를 사용합니다.
Disqus로 전환하고 싶다면 Hugo 설정에서 한 줄만 바꾸면 됩니다.

```yaml
params:
  comments:
    provider: "giscus" # giscus 사용 (기본값)
    provider: "disqus" # 또는 Disqus 사용
```

giscus 동적 삽입 스크립트를 구현한 내용은 `comments-giscus.html` 파일로 이름 변경하고,
기존 Disqus 스크립트는 `comments-disqus.html` 파일로 이름 변경하여
두 가지 댓글 시스템을 구분했습니다.

## 마치며

Github Pages 무료 호스팅을 이용하는 입장에서 마찬가지로 돈을 안들이고 댓글 시스템을 운영하는데 고민이 있었습니다.
Disqus에 무료 플랜이 있어서 나 정도의 방문량이면 제한없이 이용할 수 있을 것이라 생각했지만,
광고가 붙기 시작하면서 더 이상 Disqus를 사용하기 어렵겠다고 판단했습니다.

대안으로 선택한 giscus를 서택스 테마에 추가해보면서 색상도 나름 잘 어울리고
광고가 달리던 Disqus보다 훨씬 가볍고 깔끔해서 마음에 들었습니다.
소셜 계정 대신 Github 계정으로 댓글을 남길 수 있도록 변경한 것이
개발자인 독자들의 참여를 일으킬 수 있을지는 다시 몇 개월 간 지켜봐야 할 것 같습니다.

기술 블로그를 운영 중이고 댓글 시스템에 고민이 있으시다면 giscus를 고려해보시기 바랍니다.
