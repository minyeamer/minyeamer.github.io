---
title: "Hugo Themes에 테마 등록하기 - hugoThemesSiteBuilder"
date: "2026-07-26T22:53:43+09:00"
layout: "post"
description: >
  Hugo Themes에 서택스 테마를 등록하는 방법을 정리합니다. hugoThemesSiteBuilder 저장소의 README 문서를 기준으로
  hugo.toml, theme.toml, 스크린샷 이미지를 준비하고, GitHub Fork, themes.txt, PR, Netlify Deploy Preview까지
  Hugo 테마 등록 절차를 실제 사례와 함께 소개합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/p34fzd0mjmhtedh2wgcdj/hugo-themes-00-desktop.webp?rlkey=ry00bwyo44inuazy535puit13&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/l5xubh8muic13bm9sj40u/hugo-themes-00-mobile.webp?rlkey=6xdb4lp73laurceoy2ndzt4ud&raw=1"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Hugo Themes", "Hugo 테마", "hugoThemesSiteBuilder", "서택스 테마", "theme.toml", "hugo.toml"]
series: ["Hugo 테마 만들기"]
---

{{< series "Hugo 테마 만들기" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Hugo 테마를 만들었다면 [Hugo Themes](https://themes.gohugo.io/)에 등록해 다른 사용자에게 알릴 수 있습니다.
이 글에서는 공식 `hugoThemesSiteBuilder` 저장소를 찾은 뒤 README 문서의 안내에 따라 서택스 테마를 등록 준비하고,
Fork와 Pull Request, Netlify Deploy Preview까지 진행한 과정을 소개합니다.

등록 과정에서는 `hugo.toml`로 지원 Hugo 버전을 선언하고, `theme.toml`에 테마 메타데이터를 작성해야 합니다.
또한 영문 README, 절대 경로 이미지, 3:2 비율의 스크린샷과 썸네일, 오픈소스 라이선스를 준비해야 합니다.
현재 새 테마 등록은 중단되어 있지만, PR을 올려 배포 검증 결과를 미리 확인할 수 있습니다.

- **[Hugo Themes](#hugo-themes)**: Hugo Themes와 `hugoThemesSiteBuilder` 저장소를 찾은 과정
- **[테마 등록 조건](#테마를-등록하는-과정)**: README가 요구하는 파일과 등록 단계 확인
- **[테마 등록 전 파일 준비](#테마를-등록하기-전-파일-추가하기)**: `hugo.toml`, `theme.toml`, 스크린샷, 썸네일 추가
- **[GitHub Fork와 themes.txt 수정](#서택스-테마를-등록하기)**: 테마 URL을 추가하고 커밋한 과정
- **[PR과 Netlify 배포 테스트](#pr-제출하기)**: 등록 중단 이슈를 확인하고 [PR #752](https://github.com/gohugoio/hugoThemesSiteBuilder/pull/752)와 Deploy Preview를 검증한 결과
{{% /hint %}}

Hugo로 블로그 테마인 서택스(SeoTax) 테마를 만든 후,
저뿐만 아니라 다른 사람들도 제가 만든 테마를 사용하고
피드백을 주었으면 좋겠다는 생각을 하게 되었습니다.
이를 위해 Hugo 테마를 알릴 수 있는 방법을 찾아보았습니다.

## Hugo Themes

일반적인 서비스처럼 개발 커뮤니티에 알리는 것도 방법일 수 있지만,
Hugo에 관심있는 사람들이 찾는 플랫폼인 [Hugo Themes](https://themes.gohugo.io/)에
공개하는 것이 가장 확실한 방법입니다.

Hugo Themes는 [Hugo 공식 사이트](https://gohugo.io/)에서 제공하는
디자인 템플릿으로, Hugo를 사용해 정적 사이트를 만들어보려는 사람들이 테마를 쉽게 찾을 수 있도록
지원해주는 공간입니다.
Hugo Themes에 등록된 테마들은 오픈소스에 무료로 누구나 사용할 수 있는 것을 원칙으로 하기 때문에
라이선스 걱정 없이 가져다 활용할 수 있다는 장점이 있습니다.

저도 여기서 [Book](https://themes.gohugo.io/themes/hugo-book/) 테마와
[PaperMod](https://themes.gohugo.io/themes/hugo-papermod/) 테마를 접하여
초창기 GitHub 블로그 테마로 사용했습니다.

![Hugo Themes](https://dl.dropboxusercontent.com/scl/fi/p34fzd0mjmhtedh2wgcdj/hugo-themes-00-desktop.webp?rlkey=ry00bwyo44inuazy535puit13&raw=1)

### hugoThemesSiteBuilder

그렇다면 Hugo Themes에 자신이 만든 테마를 등록하기 위해서는 어떻게 해야할까요?

Hugo의 GitHub 공식 계정인 [GoHugo.io](https://github.com/gohugoio)에서 관리하는
저장소 목록을 둘러봤을 때, Hugo Themes 사이트의 소스라는 설명이 적힌
[hugoThemesSiteBuilder](https://github.com/gohugoio/hugoThemesSiteBuilder) 저장소가
그 대상으로 유력했습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/4976eyn6fhyhf81dshdjb/hugo-themes-01-repositories.webp?rlkey=2rj295w5w3f8tghhnsc9pa8su&raw=1"
  alt="Hugo Themes - Repositories"
  max-width="720px"
  align="center" >}}

`hugoThemesSiteBuilder` 저장소에 방문하면 README 문서를 통해
Hugo Themes에 자신의 테마를 등록하는 과정을 안내하고 있습니다.

{{< bookmark "https://github.com/gohugoio/hugoThemesSiteBuilder" >}}

### 테마를 등록하는 과정

README 문서에서 테마를 등록하기 위해 요구하는 파일들은 다음과 같습니다.

{{% hint %}}
1. 테마가 지원하는 Hugo 버전이 명시된 `hugo.toml` 파일 생성하기
2. 테마에 대한 메타데이터가 포함된 `theme.toml` 파일 추가하기
3. 테마를 설명하는 `README.md` 문서 작성하기
4. 스크린샷 이미지 `/images/screenshot.{png,jpg}` 추가하기
5. 썸네일 이미지 `/images/tn.{png,jpg}` 추가하기
{{% /hint %}}

그리고, 필요한 파일들을 추가했다면 다음 단계를 거쳐 테마를 등록할 수 있습니다.

{{% hint %}}
1. `gohugoio/hugoThemesSiteBuilder` 저장소 Fork하기
2. [themes.txt](https://github.com/gohugoio/hugoThemesSiteBuilder/edit/main/themes.txt) 파일에 테마 URL을 추가하기
   - 테마 URL은 `github.com/user/my-blog-theme` 형식으로 작성한다.
3. "Add theme my-blog-theme"과 같이 의미있는 커밋 메시지를 작성하기
4. PR을 올리고 Netlify 배포를 성공시키기
{{% /hint %}}

## 테마를 등록하기 전 파일 추가하기

`hugoThemesSiteBuilder` 저장소의 README 문서에서 안내하는대로
서택스 테마에 필요한 파일들을 추가하겠습니다.

### hugo.toml - Hugo 버전

테마의 루트 경로에 `hugo.toml` 파일을 추가해야 합니다.

해당 파일에는 다음과 같이 지원하는 Hugo 버전을 명시하도록 안내하고 있습니다.

```toml
[module]
  [module.hugoVersion]
    extended = true
    min = "0.55.0"
    max = "0.84.2"
```

제가 서택스 테마를 생성할 당시 Hugo는 0.146.0 버전이었기 때문에
서택스 테마에 해당 버전을 명시했습니다.

```toml
[module]
  [module.hugoVersion]
    extended = true
    min = "0.146.0"
```

### theme.toml - 테마 메타데이터

테마의 루트 경로에 `theme.toml` 파일을 추가하고 다음과 같은 항목들을 작성해야 한다고
문서에서 안내하고 있습니다.

```toml
name = "Theme Name"
license = "MIT"
licenselink = "Link to theme's license"
description = "Theme description"

# The home page of the theme, where the source can be found.
homepage = "https://github.com/gohugoio/gohugoioTheme"

# If you have a running demo of the theme.
demosite = "https://gohugo.io"

tags = ["blog", "company"]
features = ["some", "awesome", "features"]

# If the theme has multiple authors
authors = [
  {name = "Name of author", homepage = "Website of author"},
  {name = "Name of author", homepage = "Website of author"}
]

# If the theme has a single author
[author]
    name = "Your name"
    homepage = "Your website"

# If porting an existing theme
[original]
    author = "Name of original author"
    homepage = "Link to website of original author"
    repo = "Link to source code of original theme"
```

여기에 작성한 메타데이터는 Hugo Themes에서 테마별 상세 페이지를 구성할 때 사용됩니다.

예시로, Book 테마의 상세 페이지를 확인하면 `theme.toml`에서 각 항목이
어떻게 사용되는지 확인할 수 있습니다.

`name`과 `description`은 상세 페이지의 상단에서 테마의 제목과 설명을 표현되는데 사용됩니다.
그리고, GitHub 페이지를 가리키는 `homepage`와 데모 사이트를 가리키는 `demosite`는
각각 `Download`와 `Demo` 버튼으로 연결되는 링크로 사용됩니다.

`tags`와 `features`는 테마의 특성을 표현할 수 있는 키워드를 목록으로 명시하는데,
특히 `tags`는 Hugo Themes에서 블로그(`blog`), 다크모드(`dark`) 등
원하는 기능을 가진 테마를 필터해서 볼 때 사용되기 때문에 해당 기능을 지원한다면
작성하는 것이 좋습니다.

![Hugo Themes - Book](https://dl.dropboxusercontent.com/scl/fi/6iqn7vu1xw01woemaezy7/hugo-themes-02-book.webp?rlkey=ukdssh5bo4su93p6g4ttcd2d9&raw=1)

서택스 테마는 다음과 같이 메타데이터를 작성했습니다.

현재는 구조가 많이 달라졌지만 초기엔 Hugo Book 테마에서 파생되어 시작했기 때문에 `original`도 명시했습니다.

```toml
name = "SeoTax"
license = "MIT"
licenselink = "https://github.com/minyeamer/hugo-seotax/blob/main/LICENSE"
description = "Hugo theme for bloggers with advanced taxonomy search for better content discovery."
homepage = "https://github.com/minyeamer/hugo-seotax"
demosite = "https://minyeamer.github.io/hugo-seotax/"
tags = ["blog", "light", "dark", "dark mode", "search", "categories", "responsive", "multilingual"]
features = ["search", "categories", "tags", "dark mode", "i18n"]
min_version = "0.146.0"

[author]
  name = "minyeamer"
  homepage = "https://github.com/minyeamer/"

[original]
  author = "Alex Shpak"
  homepage = "https://book.alxs.dev/"
  repo = "https://github.com/alex-shpak/hugo-book"
```

### images - 이미지 추가하기

앞선 테마 상세 페이지에서 테마의 형태를 직관적으로 확인할 수 있는 이미지를 보여주기 위해
`/images` 경로 아래에 다음 2가지 이미지 파일을 추가해야 합니다.

- `/images/screenshot.{png,jpg}`
- `/images/tn.{png,jpg}`

주의할 점은 `screenshot` 이미지 파일은 최소 1500×1000 px,
`tn` 이미지 파일은 최소 900×600 px 크기로 만들어야 합니다.

저는 다음과 같이 라이트 모드와 다크 모드의 모습을 반반 잘라 붙여서
1500×1000 px 크기의 `screenshot` 이미지를 만들었습니다.

썸네일을 가리키는 `tn` 이미지는 `screenshot` 이미지를 단순하게 900x600 px 크기로 줄여서
크기만 다르고 동일한 이미지를 사용합니다.

![/images/screenshot.png](https://dl.dropboxusercontent.com/scl/fi/e6m87o7rqv3vedt30u7nk/hugo-themes-03-screenshot.webp?rlkey=n2or2oo7b39geleull5lxocjq&raw=1)

## 서택스 테마를 등록하기

`README.md` 문서는 [바로가기](https://github.com/minyeamer/hugo-seotax/blob/main/README.md)와 같이
미리 작성해두었기 때문에 모든 요구사항을 만족했습니다.

### 저장소 Fork하기

다음으로 `gohugoio/hugoThemesSiteBuilder` 저장소를 Fork하여 자신의 저장소로 가져옵니다.

{{< bookmark "https://github.com/minyeamer/hugoThemesSiteBuilder" >}}

### themes.txt - 테마 URL

`hugoThemesSiteBuilder` 저장소의 루트 경로에 있는 `themes.txt` 파일 내용을 보면
다음과 같이 테마 URL들이 한줄씩 나열되어 있습니다.
여기에 사전순 정렬 순서를 지켜서 서택스 테마 URL을 추가해야 합니다.

```txt
codeberg.org/farooqkz/hugo-vitae
codeberg.org/gbilder/eurozephyr
codeberg.org/VaDeCodiNet/hugo-landing-accordion
codeberg.org/VaDeCodiNet/hugo-landing-sections
codeberg.org/VaDeCodiNet/hugo-simple-sections
...
```

서택스 테마의 URL은 `github.com/minyeamer/hugo-seotax` 입니다.
이것을 `themes.txt` 파일 중간에 추가했습니다.

```txt
...
github.com/miguelsimoni/hugo-initio
github.com/mikeblum/hugo-now
github.com/minyeamer/hugo-seotax << 추가
github.com/mirus-ua/hugo-theme-re-terminal/v2
github.com/mismith0227/hugo_theme_pickles
...
```

그리고, 해당 변경사항에 대해 "Add theme SeoTax" 커밋 메시지를 작성하여
[8ff0eda](https://github.com/minyeamer/hugoThemesSiteBuilder/commit/8ff0edaba3cb461a9cfef608dd85714c11251e2f)
커밋을 추가했습니다.

### Hugo 테마 등록 일시 중단

마지막으로 PR을 올려 등록 절차를 진행하려던 시점에,
[Issue #718](https://github.com/gohugoio/hugoThemesSiteBuilder/issues/718)을 발견했습니다.

이 이슈에 따르면 2026년 5월 7일부터 Hugo Themes의 새 테마 등록은 중단된 상태였습니다.

처음에는 등록 작업을 멈춰야 하나 고민했습니다. 하지만 등록이 재개될 때까지 아무것도 하지 않는 것보다,
PR을 먼저 올려 두고 테마가 등록 기준을 통과하는지 확인하는 편이 낫다고 판단했습니다.
테마 등록이 바로 반영되지는 않더라도, Netlify 배포를 성공시키는지 여부를 확인하는 것을
목적으로 이어서 진행합니다.

### PR 제출하기

변경사항을 커밋한 후 원본 저장소를 대상으로 Pull Request를 만들고자 합니다.
PR을 제출할 때 다음과 같이 등록 조건을 확인하는 체크리스트가 제공됩니다.

이미 README 문서에서 안내한 내용들이고, 앞선 [테마를 등록하기 전 파일 추가하기](#테마를-등록하기-전-파일-추가하기)
문단에서 처리한 내용들입니다.
따로 설명 안드린 부분이라면, 오픈소스에 무료로 사용 가능한 라이선스를 적용해야 하는 부분입니다.
저는 MIT 라이선스를 사용하기 때문에 충분히 만족했습니다.

{{% hint %}}
After you have read the [instructions for adding a theme](https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/README.md#adding-a-theme), please make sure:

- [ ] your theme.toml [is complete](https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/README.md#theme-configuration)
   - [ ] name
   - [ ] license
   - [ ] licenselink
   - [ ] description
   - [ ] homepage
   - [ ] demosite (if one exists)
   - [ ] tags
   - [ ] features
   - [ ] authors/author (depending on whether the theme has multiple or a single author)
   - [ ] original (if the theme is a fork)
- [ ] you're using [absolute paths for images](https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/README.md#use-absolute-paths-for-images) in your README
- [ ] you've got [appropriate thumbnail and screenshot images](https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/README.md#media)
- [ ] your theme comes with an [appropriate license](https://github.com/gohugoio/hugoThemesSiteBuilder/blob/main/README.md#2-license)
{{% /hint %}}

체크를 마친 뒤 서택스 테마를
[PR #752](https://github.com/gohugoio/hugoThemesSiteBuilder/pull/752)로
제출했습니다. 등록이 재개될 때까지 기다려야 하지만,
Hugo Themes에 테마를 올리기 위해 필요한 준비와 신청 절차는 마쳤습니다.

![PR #752](https://dl.dropboxusercontent.com/scl/fi/illacujbev2lsvg68emp8/hugo-themes-04-pr-752.webp?rlkey=vpw93bily3cd86v8w3xw2mgyu&raw=1)

### Netlify 배포 테스트

PR을 올린 다음에는 Netlify Bot의 배포 테스트 결과를 확인했습니다.

테마 등록 PR은 `themes.txt` 파일에 추가된 한 줄의 텍스트뿐만 아니라
테마 저장소의 설정과 이미지, 그리고 exampleSite까지 함께 빌드하므로,
이 검증을 통과해야 Hugo Themes에서 실제로 보일 결과를 신뢰할 수 있습니다.

![Netlify - Deploy Preview for hugothemes ready!](https://dl.dropboxusercontent.com/scl/fi/lqe2xvtxqfak9pyhli6xe/hugo-themes-05-netlify.webp?rlkey=2e2duldrckyd17wrotavetpox&raw=1)

다행히 서택스 테마의 배포 테스트는 성공했습니다.
[Deploy Preview](https://deploy-preview-752--hugothemes.netlify.app) 링크에서
Hugo Themes에 서택스 테마가 추가된 것을 미리 확인할 수 있었습니다.
PR이 병합되기 전에 실제 배포 환경과 같은 흐름을 검증할 수 있어서 안심했습니다.

![Hugo Themes - SeoTax](https://dl.dropboxusercontent.com/scl/fi/mhj6dcb0zo9vkovbcz8sb/hugo-themes-06-deploy-preview.webp?rlkey=phmocbqd9d9a58jtu7csd68mn&raw=1)

## Hugo Themes 등록 완료

서택스 테마를 만들기로 계획했을 때부터, 단순히 제 블로그에만 적용하는 테마로 끝내고 싶지는 않았습니다.
테마를 완성하고 Hugo Themes에 등록해
다른 Hugo 사용자들도 발견하고 사용할 수 있게 만드는 일을 최종 목표로 삼았습니다.

현재 새 테마 등록은 중단되어 목록에 반영되기 까지는 다소의 기다림이 필요합니다.
그래도 테마의 메타데이터와 문서, 라이선스, 예제 사이트, 미리보기 이미지를 모두 갖추고
PR과 Deploy Preview까지 통과했습니다.

처음 세운 목표였던 "서택스 테마를 Hugo Themes에 등록할 수 있는 테마로 완성하기"는 드디어 달성했습니다.

이제는 등록 재개 소식을 기다리며, Hugo 업데이트와 사용자 피드백에 맞춰 서택스 테마를 계속 다듬어 가려고 합니다.
