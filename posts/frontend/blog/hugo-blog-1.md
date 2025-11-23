---
title: "Hugo 블로그 만들기 (1) - 프로젝트 기획 및 구조 설계"
date: "2025-11-01T20:42:21+09:00"
layout: "post"
description: >
  Hugo 블로그 프로젝트 기획부터 구조 설계까지 단계별로 안내합니다.
  타 블로그 플랫폼과 비교하고 Hugo 테마를 선정하는 방법을 소개하며,
  GitHub Pages와 Submodule을 활용한 효율적인 배포 방법을 설명합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/tmx5klj6hyiupke0u01ef/hugo-00-cover.png?rlkey=1cxv77edyfl0w2ljjqvjxg1mr&dl=0"
categories: ["Frontend", "Blog"]
tags: ["Hugo", "Blog", "티스토리", "Velog", "Git", "Github Pages", "Submodule", "Hugo Book", "휴고", "벨로그"]
---

{{% hint info %}}
<i class="fa-solid fa-circle-info"></i> 대상 독자
- 마크다운으로 작성할 수 있는 나만의 블로그를 만들고 싶은 분들
- 블로그를 기능적으로 또는 시각적으로 커스터마이징 하고 싶은 분들
- Github Pages 서비스를 활용한 웹 호스팅을 하고 싶은 분들
- Git Submodules 기능을 활용한 프로젝트 구성 방식을 알고 싶은 분들
{{% /hint %}}

{{% hint success %}}
<i class="fa-solid fa-lightbulb"></i> 주요 내용
- 과거 다른 블로그 플랫폼을 이용하면서 겪은 경험 및 장단점 ([나만의 블로그를 만들게 된 계기](#나만의-블로그를-만들게-된-계기))
- 나만의 블로그에 추가하고 싶은 기능 목록을 영역 별로 나열 ([나만의 블로그 기획하기](#나만의-블로그-기획하기))
- 관심있는 Hugo 테마에 대한 소개 ([기본 테마 선정하기](#기본-테마-선정하기))
- Hugo 설치부터 Submodule 활용까지 프로젝트 구조를 설계하고 배포 스크립트 작성 ([블로그 프로젝트 구성하기](#블로그-프로젝트-구성하기))
{{% /hint %}}

## 나만의 블로그를 만들게 된 계기

블로그 플랫폼을 선택하는데 있어 편의 기능, 외관, 작성 방식 등을 고려할 수 있습니다.

Velog, 티스토리 등의 블로그 플랫폼을 이용해 봤지만 원하는 요소들을 전부 추가하는데는 제약이 많았습니다.

### <img src="https://dl.dropboxusercontent.com/scl/fi/rclmscmcgcz0re8hq60pd/logo-velog.jpg?rlkey=3d1nh4v5s46oz094lx9tos3vl&dl=0" alt="Velog" class="h3-image"> Velog 사용 경험

Velog는 개인적으로 느끼기에 블로그 플랫폼들 중에서 따로 테마를 설정하지 않아도 기본 스타일이 보기 좋다는 장점이 있지만,
다크모드 ON/OFF 버튼 추가 또는 코드 블럭 스타일 변경 등의 커스터마이징이 불가능하고,
무엇보다 카테고리 없이 태그로만 게시글을 구별해야 한다는걸 가장 큰 제약으로 인식했습니다.

<a href="https://velog.io/@minyeamer/posts" target="_blank">
<img src="https://dl.dropboxusercontent.com/scl/fi/2aspdgqtn9er0wpvvgh5v/hugo-01-example-velog.webp?rlkey=6nxofpq3gndqrnogm3m1o3dxl&dl=0" alt="Velog 인터페이스">
</a>

### <img src="https://dl.dropboxusercontent.com/scl/fi/u28ide6ixcwmte9deafju/logo-tistory.png?rlkey=thffzqj0ouhn0axj6fapizz7x&dl=0" alt="Tistory" class="h3-image"> 티스토리 사용 경험

티스토리는 테마 수정은 자유로운 편이지만, 테마 편집이든 블로그 게시글 작성이든 티스토리 UI에서 편집 과정을 거쳐야 반영되는 점에서
즉각적인 피드백이 어렵다고 느꼈습니다. 그리고, 무엇보다 글 편집이나 블로그 관리 등의 설정 메뉴에는 다크모드가 적용이 안돼서 개인적으로 쓰기 싫었습니다.

<a href="https://minyeamer.tistory.com/" target="_blank">
<img src="https://dl.dropboxusercontent.com/scl/fi/4xn1fjflju78w0jv76i7h/hugo-02-example-tistory.webp?rlkey=ixtuq0oo3xa26cgqfkwri1i4t&dl=0" alt="티스토리 인터페이스">
</a>

### <img src="https://dl.dropboxusercontent.com/scl/fi/xgh0tzbm00qneoy4x1par/logo-hugo.png?rlkey=xnyulio177owaxe8pjir0vf9j&dl=0" alt="Hugo" class="h3-image"> Hugo 사용 경험

3년 전에 Hugo를 활용한 [Github 블로그](http://localhost:1313/blog/hugo-blog-old-1/)를 만든 적이 있었는데,
당시에는 테마를 원하는대로 수정할 수 있을 만큼의 전문 지식이 없어서 다른 블로그 플랫폼들과 마찬가지로 잠깐 이용하다 말았지만,
AI 에이전트의 도움을 받으면 자연어 프롬프트로 원하는 기능들을 추가해볼 수 있지 않을까라는 막연한 생각에 다시 Hugo 블로그를 도전해보게 되었습니다.

![Hugo 블로그 - PaperMod 테마 인터페이스](https://dl.dropboxusercontent.com/scl/fi/o5ppc9sdj1jee5wvzp0ck/hugo-03-example-hugo.webp?rlkey=w6w8nobkuond1rva40wbqei7k&dl=0)

Hugo 블로그의 단점이라고 한다면 웹 호스팅을 직접 해야한다는 점입니다.
과거에 블로그를 운영할 때는 Github Pages 기능을 활용해 무료로 웹 호스팅을 제공받았습니다.
물론, 이번 블로그도 동일하게 Github Pages 기능을 사용할 것입니다.

또 하나의 단점으로는 이미지 등록하기 어렵다는 점이 있습니다.
과거에는 Github에 이미지를 올려서 참조했지만, 이미지 포함한 변경사항을 커밋/푸쉬한 후
Github 웹사이트에서 raw 이미지 링크를 찾아와야 해서 비효율적이었습니다.

이번에 새로운 블로그를 준비하면서 [Dropbox](https://www.dropbox.com/)를 통해
이미지를 드래그해서 올리고 간편하게 링크를 복사할 수 있는 방법을 알게 되어서 이미지 호스팅은 해결되었습니다.
이미지 호스팅과 관련해서는 별도의 글을 작성할 예정입니다.

## 나만의 블로그 기획하기

나만의 블로그인만큼 원하는 외형과 기능들을 전부 집어넣을 생각입니다.

물론, 기획한 내용들은 이미 현재 블로그에 구현되어 있어서 시각적으로 참고해볼 수 있습니다.

### 레이아웃

블로그의 전체적인 구성은 과거 티스토리 블로그를 이용할 때 사용했던 [hELLO 테마](#티스토리-사용-경험)를 참고합니다.

{{% hint %}}
1. 좌측에는 메뉴 영역을 표시합니다.
2. 우측에는 목차 영역을 표시합니다.
3. 중앙에는 본문 영역을 표시합니다.
4. 본문의 상단에는 글 제목을 표시합니다.
5. 본문의 하단에는 댓글 영역을 표시합니다.
6. 모바일 화면에 맞춘 반응형 디자인을 고려합니다.
{{% /hint %}}

기능은 각 영역 별로 구분합니다.

### 메뉴 영역

좌측 메뉴 영역의 기능들을 위에서부터 순서대로 나열합니다.

{{% hint %}}
1. 프로필 사진을 표시합니다. 클릭하면 블로그 홈페이지와 연결됩니다.
2. 소셜 링크 또는 기능성 버튼을 표시합니다.
3. 제목을 표시하고, 다음으로 검색창을 표시합니다.
   - 검색어를 입력하고 엔터 또는 검색 아이콘을 클릭하면 검색 페이지로 이동합니다.
4. 카테고리 목록을 표시합니다. 카테고리는 최대 2단계로 펼치고 접을 수 있습니다.
5. 최신글 목록을 보여줍니다. 작성일 순으로 최대 5개까지 표시합니다.
{{% /hint %}}

### 목차 영역

우측 목차 영역은 상단과 하단으로 구분됩니다.

{{% hint %}}
1. 우측 상단의 고정된 위치에 목차를 표시합니다.
   - 목차와 본문의 사이에 목차의 길이만큼 구분선을 추가합니다.
   - 스크롤이 위치한 목차를 하이라이트로 강조합니다.
   - 목차를 클릭하면 해당 위치로 이동하는 앵커 링크를 설정합니다.
2. 우측 하단의 고정된 위치에 이동 버튼을 추가합니다.
   - 맨 위로 이동, 맨 아래로 이동, 뒤로 가기 버튼을 세로로 나열합니다.
{{% /hint %}}

### 본문 영역

중앙의 본문 영역은 마크다운 문서가 렌더링되는 부분이며, 상단과 하단에 기능이 추가됩니다.

{{% hint %}}
1. 본문 상단에는 카테고리, 글 제목, 작성일시를 순서대로 표시합니다.
2. 글 하단에는 태그 목록을 표시합니다.
3. 카테고리 또는 태그를 클릭하면 관련 게시글 목록으로 이동합니다.
{{% /hint %}}

### 헤더 영역

헤더 영역은 반응형 디자인의 일부로, 기본적으로는 나타나지 않고 모바일 사이즈에서만 표시됩니다.

{{% hint %}}
1. 헤더 영역에는 메뉴 또는 목차를 펼치고 접을 수 있는 버튼이 좌우 양끝에 표시됩니다.
2. 브라우저 너비에 따라 목차, 메뉴 순서로 숨기고 해당 영역이 숨겨질 때 버튼이 활성화됩니다.
3. 헤더 영역의 가운데에는 블로그 제목을 표시하고 홈페이지로 이동하는 링크를 설정합니다.
4. 헤더 영역은 반투명한 배경색을 가지고 스크롤 위치에 관계없이 고정됩니다.
{{% /hint %}}

### 푸터 영역

푸터 영역은 게시글(post) 유형의 레이아웃을 사용하는 경우만 설정합니다.

{{% hint %}}
1. 본문에 설정된 카테고리 내 게시글 중에서 작성일 순으로 이전, 다음 게시글로 이동하는 버튼을 추가합니다.
2. 댓글 영역을 추가합니다. 댓글 기능을 직접 만들진 않고 외부 서비스를 이용합니다.
{{% /hint %}}

### 기타 기능

{{% hint %}}
1. Open Graph 설정 및 외부 링크 미리보기 기능을 추가합니다.
2. 스크롤 위치에 맞춰 상단에 진행도를 표시합니다.
3. 다크모드 ON/OFF 버튼을 추가합니다.
   - 기본 시스템 설정을 인식하여 라이트/다크모드를 설정합니다.
4. 코드 블럭을 맥 터미널처럼 보이게 꾸밉니다.
   - 코드 블럭 우측 상단에 복사 버튼을 추가합니다.
   - 코드 블럭 우측 상단에 언어를 표시합니다.
5. 홈 페이지를 추가합니다. 등록일 순으로 게시글을 정렬하여 목록으로 표시합니다.
6. 태그 전용 페이지를 추가합니다. 태그는 Hugo에서 기본적으로 지원합니다.
7. 카테고리 전용 레이아웃을 추가합니다.
   - 자식 카테고리를 부모 카테고리로 그룹화한 디렉터리 구조를 가집니다.
   - 부모/자식 카테고리 페이지에서 각각 하위/상위 카테고리로 이동을 지원합니다.
   - 전체 카테고리 목록을 나열하는 페이지를 추가합니다.
8. GA4를 연결하고 구글, 네이버 검색엔진에 등록합니다.
{{% /hint %}}

처음부터 위 목록을 전부 생각했던 것은 아니고, 블로그 테마를 발전시켜 나가면서
점진적으로 추가한 기능들을 같이 정리한 것입니다.

## 기본 테마 선정하기

빈 프로젝트부터 시작하지는 않고 잘 만들어진 테마의 레이아웃을 참고할 예정입니다.

Hugo 테마는 아래 경로에서 찾아볼 수 있습니다.

{{< bookmark "https://themes.gohugo.io/" >}}

### PaperMod 테마 사용 경험

처음 Hugo 블로그를 만들 땐 [PaperMod](https://themes.gohugo.io/themes/hugo-papermod/)라는 테마를 사용했습니다.

{{< bookmark "https://themes.gohugo.io/themes/hugo-papermod/" >}}

다크모드 ON/OFF 버튼 및 소셜 링크 기능을 지원하고 디자인이 마음에 들어 초기 테마로 사용을 했지만 Velog에서 느꼈던 단점인,
카테고리를 지원하지 않는 문제로 인해 블로그를 쓰고 싶다는 생각이 갈수록 줄어들었습니다.

그래도 당시에 카테고리 기능을 만들어 보려고 여기저기 알아보면서,
[Tree-style category list page #24](https://github.com/adityatelange/hugo-PaperMod/issues/24)
이슈를 작성한 분께 메일을 보내 HTML 소스 파일을 공유받기도 했습니다.
이때 공유받은 소스 코드는 당시에는 사용하지 못했지만, 보관해뒀다가 현재 블로그에 녹여서 사용하고 있습니다.

### Book 테마 선정

최근에 다시 테마를 찾아보면서 가장 마음에 들은 것은 Book 테마입니다.

{{< bookmark "https://themes.gohugo.io/themes/hugo-book/" >}}

Book 테마는 좌측의 `book-menu`, 우측의 `book-toc`, 그리고 중앙의 본문인 `book-page` 영역으로 나눠집니다.

![Hugo 블로그 - Book 테마 인터페이스](https://dl.dropboxusercontent.com/scl/fi/zuksrebozfve99snbqb6z/hugo-04-book-theme.webp?rlkey=ezk4ocya4qf6p33st2kxmz8he&dl=0)

`book-menu` 영역에는 상단에 검색창이 있고 그 아래에 카테고리 목록을 표시합니다.
검색창에 키워드를 입력하면 카테고리 목록을 밀어내고 검색창 바로 아래에 검색 결과를 표시합니다.
따로 검색 결과를 나타내는 페이지가 존재하지는 않습니다.

`book-toc` 영역은 일반적인 목차(Table of Contents) 영역이며, 스크롤 위치에 관계없이 고정된 위치에 있습니다.
게시글 내 특정 위치로 이동할 수 있는 앵커 링크를 지원합니다.
앵커 링크를 클릭하면 부드럽게 이동하는 애니메이션이 적용되어 있습니다.

`book-page` 영역은 마크다운으로 작성한 본문이 렌더링되는 영역입니다.
해당 영역의 아래에 있는 `book-footer` 영역에는 이전, 다음 게시글로 이동할 수 있는 링크가 표시됩니다.

추가로 관심을 가져볼만한 기능은, 브라우저가 정해진 모바일 크기만큼 줄어들게 되면 `book-menu` 및 `book-toc` 영역을 숨기고
`book-header` 영역을 표시하는 반응형 디자인입니다. `book-header` 영역은 본문에 표시되지 않는 게시글 제목을
중앙에 보여주고 좌우에 `book-,enu` 및 `book-toc` 영역을 펼치고 접을 수 있는 버튼을 제공합니다.

과거 티스토리 블로그를 이용할 때 사용했던 [hELLO 테마](#티스토리-사용-경험)와 구성이 비슷해 해당 테마를 보자마자 기본 레이아웃으로
사용하면 좋겠다고 생각했습니다. 마침 hELLO 테마에서 가져오려는 기능들도 많아서 해당 테마가 적절했습니다.

## 블로그 프로젝트 구성하기

마음에 드는 테마를 선정했다면 본격적으로 Hugo 프로젝트를 구성하여 테마를 적용해볼 차례입니다.

### 1. Hugo 설치

Mac 사용자라면 [Homebrew](https://brew.sh/)를 통해 간단하게 Hugo를 설치하여 사용할 수 있습니다.

```bash
brew install hugo
```

설치가 완료되면, 버전 정보를 출력해서 정상 설치 여부를 확인해 봅니다.

```bash
% hugo version
hugo v0.150.0+extended+withdeploy darwin/arm64 BuildDate=2025-09-08T13:01:12Z VendorInfo=brew
```

### 2. Hugo 프로젝트 생성

Hugo 프로젝트를 생성하기 위해서는 터미널에서 아래 명령어를 입력합니다.

```bash
hugo new site <프로젝트명>
```

Hugo 프로젝트는 다음과 같은 구조를 가집니다.

```bash
.
├── archetypes/
│   └── default.md
├── content/
├── data/
├── layouts/
├── public/
├── static/
├── themes/
└── hugo.toml
```

각 폴더는 다음과 같은 역할 또는 목적이 있습니다.
- `archtypes/` : 게시글 템플릿이 위치한 폴더이며, `hugo new <파일명>` 명령어로 템플릿 내용을 가지는 게시글 파일을 생성할 수 있습니다.
- `content/` : 게시글 목록이 위치한 폴더입니다.
- `data/` : CSV, JSON, YAML 등의 데이터들을 관리하는 폴더입니다.
- `layouts/` : 블로그에 적용되는 HTML 형식을 관리하는 폴더입니다. `themes/` 폴더보다 우선순위를 가집니다.
- `public/` : 빌드한 결과, 즉 정적 HTML 파일들이 생성되는 폴더입니다.
- `static/` : 빌드할 때 포함시킬 이미지, JS, CSS 등의 파일들이 위치하는 폴더입니다.
- `themes/` : 만들어진 테마를 블로그에 적용하기 위해 위치시키는 폴더입니다.
- `hugo.toml` : 블로그에 대한 설정을 위한 파일입니다. YAML 등 다른 형식도 지원합니다.

### 3. Github 저장소 생성

블로그를 개발하면서 진행 과정을 기록해두면 과거에 어떤 작업을 했는지,
그리고 실수로 돌이킬 수 없는 오류가 발생해 이전 시점으로 돌아가고 싶은 경우에
버전 관리를 해두면 좋습니다.

로컬에서 Git을 통해 버전 관리를 하면서 커밋한 이력을 Github에 올릴 것입니다.
이를 위한 Github 저장소를 생성합니다.

단순히 버전 관리 목적으로 Github을 이용한다면 저장소 명칭은 아무렇게나 해도 괜찮지만,
아래에서 설명할 Github Pages 서비스를 이용하려면 `<사용자명>.github.io` 명칭을 사용해야 합니다.

![Github 저장소 생성 예시](https://dl.dropboxusercontent.com/scl/fi/qs3zxgai75efvghshsccg/hugo-05-github-repo.webp?rlkey=cgizkyzr06ku7abreqtaqpslf&dl=0)

Github 저장소를 생성했다면 앞에서 생성한 Hugo 프로젝트와 연동합니다.

```bash
git init
git add .
git commit -m "feat: new site"
git branch -M main
git remote add origin https://github.com/<사용자명>/<사용자명>.github.io.git
git push -u origin main
```

Hugo 프로젝트를 생성하면서 발생한 변경사항을 커밋하고
Github 저장소의 `main` 를 원격 저장소로 등록한 후 푸쉬합니다.

### 4. Github Pages 설정

블로그를 인터넷 상의 모두에게 공개하기 위해서는 일반적으로 홈서버 구축, 도메인 구매, DNS 설정 등
신경써야 할게 많아서 편리한 웹 호스팅 서비스를 이용합니다.
컴퓨팅 자원을 제공하는 웹 호스팅 서비스들은 대부분 유료로 제공되기 때문에
무료로 간단하게 이용할 수 있는
[Github Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
서비스를 사용하고자 합니다.

Github 저장소의 설정(Settings) 탭에 접근한 후, 사이드바의 Pages 메뉴에서 Github Pages를 설정할 수 있습니다.

![Github Pages 설정 화면](https://dl.dropboxusercontent.com/scl/fi/k730csxion7uu41rymefr/hugo-06-github-pages.webp?rlkey=iibu1g2awc4toyoedksjv5lgz&dl=0)

Github Actions를 사용해 빌드 과정을 커스터마이징할 수 있지만,
해당 프로젝트에서는 단순하게 별도의 브랜치에 HTML 소스코드를 두고
해당 브랜치에서 변경사항이 발생할 때마다 빌드되도록 설정하겠습니다.

Source에 `Deploy from a branch` 를 선택하고 Branch에 대상 브랜치를 지정하면
Github Pages 설정이 완료되지만, 브랜치 지정 시 고려할 사항이 있어 우선 다음 단계로 넘어갑니다.

### 5. Submodule 구성

Submodule은 Git에서 외부 프로젝트를 현재 프로젝트에서 포함시킬 수 있게 하는 기능입니다.
Submodule이 무엇인지 설명하려면 너무 길어지기 때문에 자세하게 알고 싶다면
[저장소 안에 저장소 - git submodule](https://youtu.be/TAe4uZqYt6c)
영상 등을 참고해주시기 바랍니다.

Submodule은 외부 프로젝트를 연결시키는 역할을 하지만, 반대로 이용하면
현재 프로젝트의 일부를 독립적인 외부 프로젝트로 분리할 수 있습니다. 해당 프로젝트에서는 다음 2가지 사유로 Submodule을 이용합니다.

1. Submodule로 분리하려는 폴더는 `public/` 입니다.
해당 폴더는 Hugo 빌드한 결과가 생성되는 경로인데, 이때마다 많은 파일들이 변경사항에 포함됩니다.
자동으로 생성되는 파일들을 `main` 브랜치의 변경사항에 포함하고 싶지 않아 분리하려고 합니다.

2. 앞에서 Github Pages를 설정할 때 `public/` 경로를 지정하려고 했는데,
이 때 고려할 사항이 브랜치에서 변경사항이 발생할 때마다 빌드가 진행된다는 점입니다.
커밋을 푸쉬하면서 빌드하고 싶지 않은 경우가 있는데
`main` 브랜치를 Github Pages 대상으로 지정하게 되면 빌드 시점을 제어할 수 없어
독립적인 브랜치를 사용해야 합니다.

따라서, `public/` 폴더를 독립적인 브랜치의 루트 경로로 지정하고,
해당 브랜치를 Submodule로 분리하려고 합니다.

우선, 브랜치를 생성합니다. 브랜치명은 자유롭게 지정할 수 있으며 해당 프로젝트는 `source` 라고 지정했습니다.

```bash
git branch source main
git checkout source
```

`source` 브랜치는 `public/` 폴더를 루트 경로로 가집니다.
즉, 현재 `public/` 폴더는 비어있으므로 모든 파일을 삭제하고 원격 저장소에 올립니다.
이때, 모든 파일을 삭제한다고 `.git` 폴더까지 삭제하면 안됩니다.

```bash
find . -maxdepth 1 -not -name '.*' -exec rm -rf {} \;
git add .
git commit -m "update: init source"
git push origin source
```

원격 저장소에 브랜치를 추가했으면 다시 `main` 브랜치로 되돌아가서
원격의 `source` 브랜치를 Submodule로 연결합니다.

```bash
git checkout main
rm -rf public
git submodule add -b source https://github.com/<사용자명>/<사용자명>.github.io public
git commit -m "feat: add submodule for source"
```

그리고, 다시 [Github Pages 설정](#5-github-pages-설정)으로 되돌아가서
`source` 브랜치를 지정하고 설정을 저장하면 됩니다.

추가적으로, 게시글 목록이 위치하는 `content/` 폴더도 독립적으로 관리하고 싶어서 Submodule로 분리했습니다.   
`source` 브랜치와 동일한 과정으로 `content` 브랜치를 생성했습니다.

```bash
git branch content main
git checkout content

find . -maxdepth 1 -not -name '.*' -exec rm -rf {} \;
git add .
git commit -m "update: init content"
git push origin content

git checkout main
rm -rf content
git submodule add -b content https://github.com/<사용자명>/<사용자명>.github.io content
git commit -m "feat: add submodule for content"
```

### 6. 테마 적용하기

해당 단계에서도 Submodule을 활용하여 별도의 저장소에 있는 테마를
`themes/` 폴더 아래에 연결시킬 것입니다.

만들어진 테마를 그대로 사용할 것이라면 해당 테마의 Github 저장소를 Submodule로 연결합니다.   
Hugo Book 원본 테마를 사용하고 싶다면 아래 명령어를 입력합니다.   
`Book` 은 Hugo 설정에서 지정한 `hugo-book` 에 대한 테마명이고, 다른 테마라면 명칭을 변경합니다.

```bash
git submodule add https://github.com/alex-shpak/hugo-book themes/Book
```

테마를 커스터마이징할 것이라면 원본 테마를 Fork한 저장소를 Submodule로 연결합니다.   
테마 커스터마이징을 위해 만든 `hugo-book-custom` 저장소를 연결하겟습니다.

```bash
git submodule add https://github.com/minyeamer/hugo-book-custom themes/Book
```

### 7. 배포 스크립트 작성하기

Hugo 빌드는 `hugo -t <테마명>` 명령어를 통해 수행합니다.
그리고, `public/` 경로에 생성된 HTML 소스코드를 `source` 브랜치에 푸쉬하여
Github Pages 배포를 진행합니다.

이 과정을 쉘 스크립트로 표현하면 아래와 같습니다.

```bash
#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub***\033[0m"

# 모든 서브모듈의 변경사항을 업데이트
git submodule update --remote

# 프로젝트 빌드
# `hugo -t <테마명>`
hugo -t Book

# `source` 브랜치로 이동
cd public
git add .

# 인자가 없을 경우 현재 시간을 커밋 메시지로 등록
msg="rebuild: $(date +"%Y-%m-%dT%H:%M:%S%z")"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# 빌드 결과를 `source` 브랜치에 반영
git push origin source

# `main` 브랜치로 이동
cd ..

# 현재까지의 변경사항을 `main` 브랜치에 반영
git add .

if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push origin main
```

해당 내용의 `deploy.sh` 스크립트 파일을 생성하고 `chmod 755 deploy.sh`
명령어로 실행 권한을 부여하여 복잡한 배포 과정을 쉘 스크립트 하나를 실행하는 것으로 대체합니다.

스크립트를 실행하면 Hugo 프로젝트를 HTML 소스코드로 빌드한 후 원격 저장소에 푸쉬하여
Github Pages 배포하게 됩니다. Github Actions를 확인하면 다음과 같은 과정으로
배포가 진행되는 것을 확인할 수 있습니다.

![Github Pages 배포 과정](https://dl.dropboxusercontent.com/scl/fi/tx2mlp4r4busainz1fgx1/hugo-07-github-workflow.webp?rlkey=rdjb1kvitpnkiol8h7kdlp238&dl=0)

모든 과정이 성공하면 `https://<사용자명>.github.io/` 주소로 배포된 블로그를 조회할 수 있습니다.

기본 Hugo Book 테마를 사용할 경우 배포했을 때 좌측 메뉴에 블로그 제목과 검색창만 덩그러니 놓여있을 것입니다. 임시로 게시글을 생성하고 게시글 경로로 직접 이동해보면 아래와 같은 결과를 확인할 수 있습니다.

![초기 Hugo Book 테마](https://dl.dropboxusercontent.com/scl/fi/6fmjemvbe3mx0kcbsjlf6/hugo-08-new-site.webp?rlkey=2z7oobn7o3pryg1eneu04tb9g&dl=0)

다음 게시글에서는 본격적으로 테마를 커스터마이징하는 과정을 진행하겠습니다.
