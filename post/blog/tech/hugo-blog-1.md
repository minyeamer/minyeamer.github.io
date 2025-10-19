---
layout: post
title: Hugo 블로그 만들기 (1) - Hugo 기본 구성
date: 2022-09-08 12:02:32 +0900
categories: [Blog, Tech]
tags: [Hugo, PaperMod, Github, Github Pages, Submodule]
---

얼마 전, 티스토리 블로그에서 [Jekyll 블로그](https://minyeamer.github.io/blog/jekyll-blog/)로 이동했는데,   
처음 기대했던 submodule을 활용한 효율적인 저장소 연동에서 어려움을 겪고 다른 대안을 탐색하게 되었습니다.

Jekyll 블로그를 사용함에 있어서, Ruby 언어로 구성된 블로그 구조에 대해 이해하기 어려운데다가   
로컬 환경에서 Jekyll 블로그를 실행하면서 발생하는 에러를 처리하는데도 난항을 겪었는데,   
웹상에서 자동 배포가 이루어지는 과정에서 submodule인 TIL 저장소를 포스트로 인식하지 못하는 문제가 있었습니다.

Jekyll 블로그의 대안으로 Hexo 및 Hugo 프레임워크에 주목했고,   
두 제품의 장단점을 비교하여 상대적으로 배포가 빠르고 현재까지도 업데이트가 이루어지는 Hugo를 선택했습니다.

이번 포스트에서는 제가 Hugo 블로그를 구성한 과정을 간략한 설명과 함께 안내해드리겠습니다.

---

# 테마 선택하기

블로그의 모든 페이지 레이아웃을 만들 계획이 아니라면 블로그 선택에 있어 테마 선정이 필요합니다.   
Hugo는 아래 페이지에서 다양한 테마를 제공하며, 태그를 통해 블로그 외에도 목적에 맞는 테마를 찾아볼 수 있습니다.   
미리보기만으로 알기 어렵다면 제작자가 제공하는 데모 사이트를 방문해볼 수 있고,   
아래 안내드릴 Hugo 설치를 통해 로컬에서 exampleSite를 확인해 볼 수도 있습니다.

- https://themes.gohugo.io/

Jekyll 블로그를 사용했을 당시 적용했던 Chirpy 테마는 사이드 메뉴, 계층식 카테고리, 동적 TOC 등   
제가 추구하는 모든 기능을 가지고 있었는데, Hugo에는 저의 취향을 완벽히 만족시키는 테마가 없었습니다.   
그나마 괜찮았던 [LoveIt 테마](https://themes.gohugo.io/themes/loveit/)의 경우 설정 곳곳에 중국어가 포함되어 있어 이해하기 어렵겠다는 생각이 들었습니다.   
결국, 저는 모든 테마를 둘러본 후 다루기 쉬워보이면서 외적으로도 괜찮았던 [PaperMod 테마](https://themes.gohugo.io/)를 선택했습니다.

![papermod](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/papermod.png?raw=true)

---

# Hugo 블로그 구성하기

이번 Hugo 블로그 구성은 Mac 환경에서 진행되었으며, 다른 환경의 구성 방식은 제공되지 않습니다.

## Hugo 설치

Mac 사용자라면 Homebrew를 통해 쉽게 Hugo를 설치하여 사용할 수 있습니다.   
터미널에 아래 명령어를 입력해 설치가 가능합니다.

```bash
brew install hugo
```

설치가 완료되면, 버전 정보를 출력해서 정상 설치 여부를 확인합니다.

```bash
% hugo version
hugo v0.102.2+extended darwin/arm64 BuildDate=unknown
```

## Github 저장소 생성

Hugo는 원본 데이터 및 설정 파일이 포함될 공간과, 렌더링된 페이지가 저장될 공간이 필요합니다.   
일반적으로는 분리된 저장소를 통해 구현하지만, 앞서 Jekyll 블로그를 구성해보면서   
브랜치를 통해 하나의 저장소에서 두 개의 공간을 관리할 수 있을 것이라 판단했습니다.

하나의 저장소를 `main`과 `gh-pages`, 두 개의 브랜치로 나누어 구성할 계획이며,   
우선적으로 `<USERNAME>.github.io` 명칭의 저장소를 생성합니다.

## Hugo 프로젝트 생성

일반적인 웹 프레임워크에서 프로젝트를 시작하는 것처럼, Hugo에서도 기본 템플릿을 제공합니다.
아래 명령어를 통해 프로젝트를 생성할 수 있고, 이름은 자유롭게 지정해도 됩니다.

```bash
% hugo new site <NAME>
```

만들어진 프로젝트 구조는 다음과 같습니다.   
만들어진 테마를 사용한다면 대부분의 구성요소들이 `themes/` 디렉토리 내에 위치하게 되며,   
포스트를 위한 `content/`, 이미지 등을 위한 `static/` 디렉토리 외엔 거의 사용하지 않습니다.

```bash
.
├── archetypes
│   └── default.md
├── config.toml
├── content
├── data
├── layouts
├── public
├── static
└── themes
```

## 저장소 연동

테마를 불러오기에 앞서 git 설정이 필요합니다.   
프로젝트 디렉토리로 이동한 후, 아래 명령어를 통해 원격 저장소와 연동합니다.

```bash
% git init
% git add .
% git commit -m "feat: new site"
% git branch -M main
% git remote add origin https://github.com/<USERNAME>/<USERNAME>.github.io.git
% git push -u origin main
```

추가적으로, 렌더링된 페이지가 저장되고 실질적인 배포가 이루어지는 브랜치를 생성합니다.

```bash
% git branch gh-pages main
% git checkout gh-pages
% git push origin gh-pages
% git checkout main
```

Hugo에서 페이지를 렌더링한 결과는 `public/` 디렉토리에 저장되며, 이를 `gh-pages` 브랜치와 연결해야 합니다.   
기존에 존재하는 빈 디렉토리를 제거하고 `gh-pages` 브랜치를 `main` 브랜치의 submodule로 연결합니다.   
submodule에 대한 개념은 [해당 영상](https://youtu.be/TAe4uZqYt6c)을 참고해주시기 바라며, 단순하게 설명하자면 동기화 기능입니다.

```bash
% rm -rf public
% git submodule add -b gh-pages https://github.com/<USERNAME>/<USERNAME>.github.io.git public 
% git add public
% git add .gitmodules
% git commit -m "feat: add submodule for github pages"
% git push
```

## 테마 불러오기

git 설정을 완료한 후, 미리 정해두었던 테마를 `themes/` 디렉토리 내에 위치시킵니다.   
마찬가지로 submodule을 활용하며, 테마의 디렉토리명은 반드시 테마 설정에 명시된 것과 동일한 이름이어야 합니다.   
커스터마이징을 고려하면 원본 저장소가 아닌 별도로 fork한 저장소를 연결시키는게 좋습니다.

```bash
% git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
% git add themes/PaperMod
% git add .gitmodules
% git commit -m "feat: import hugo theme"
```

만약 fork 저장소를 사용하면서 원본 저장소의 변경사항을 업데이트하고 싶다면,   
원본 저장소를 새로운 원격 저장소로 등록해 pull 작업을 수행합니다.

```python
git remote add upstream https://github.com/adityatelange/hugo-PaperMod
git fetch upstream
git merge upstream/master
git commit -m "update: pull upstream"
```

아래는 PaperMod 테마의 디렉토리 구조입니다.   
테마를 수정할 일이 있다면 아래 구조를 참고해 필요한 파일에 접근해 볼 수 있습니다.

```bash
themes/PaperMod
├── LICENSE
├── README.md
├── assets
│   ├── css
│   │   ├── common
│   │   ├── core
│   │   ├── extended
│   │   ├── hljs
│   │   └── includes
│   └── js
├── go.mod
├── i18n
├── images
├── layouts
│   ├── 404.html
│   ├── _default
│   │   └── _markup
│   ├── partials
│   ├── robots.txt
│   └── shortcodes
└── theme.toml
```

## Hugo 설정

Hugo 블로그 설정은 `config` 파일에서 지정할 수 있고, `toml`, `yaml`, `json` 형식을 지원합니다.   
테마를 사용할 경우 커스텀 키가 존재할 수 있어 별도의 문서를 참조하는게 좋습니다.   
Hugo 공식 설정에 관한 문서와 PaperMod 설정에 관한 문서는 아래를 참고해주시기 바랍니다.

- https://gohugo.io/getting-started/configuration/
- [https://github.com/adityatelange/hugo-PaperMod/wiki/Installation](https://github.com/adityatelange/hugo-PaperMod/wiki/Installation#sample-configyml)

제 [설정 파일](https://github.com/minyeamer/minyeamer.github.io/blob/main/config.yml)의 경우 커스터마이징을 통해 호환되지 않는 키가 존재할 수 있지만,   
동일한 테마를 사용한다면 일부분을 참고해 도움을 받을 수 있을거라 기대합니다.

## Hugo 배포

Hugo는 `hugo -t <THEMES>` 명령어를 통해 로컬에서 페이지 렌더링을 진행할 수 있고,   
그 결과인 `public/` 디렉토리 내 내용을 `gh-pages`에 push하여 배포를 수행합니다.

배포에 앞서, 깃허브에서 제공하는 Github Pages가 `gh-pages` 브랜치를 참고하도록   
아래 그림과 같이 저장소 설정에서 빌드 및 배포 대상 브랜치를 지정해주어야 합니다.

![github-pages](https://github.com/minyeamer/til/blob/main/.media/blog/tech/hugo-blog/github-pages.png?raw=true)

위와 같이 수동으로 배포할 경우 두 번의 push 과정을 거쳐야 합니다.   
매번 이 과정을 수행하는 것은 불편하기 때문에 쉘 스크립트를 작성하여 작업을 단순화합니다.   
해당 스크립트는 [다른 포스트](https://gurumee92.github.io/2020/08/블로그-구축기-1-hugo-github으로-개인-블로그-만들기/)를 참고해 작성했습니다.

```bash
#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
# hugo -t <your theme>
hugo -t PaperMod

# Go to public folder, submodule commit
cd public
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin gh-pages

# Come back up to the project root
cd ..

# Commit and push to main branch
git add .

msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

git push origin main
```

스크립트 파일에 실행 권한을 부여하고 실행해 볼 수 있습니다.

```bash
% chmod 777 deploy.sh
% ./deploy.sh
```

배포가 완료되면, https://<USERNAME>.github.io 주소로 접속해 블로그를 확인할 수 있습니다.

---

# 포스트 작성하기

Hugo 포스트는 아래 명령어를 통해 생성할 수 있고,   
별도의 markdown 파일을 `content/post/` 경로 내에 추가할 수도 있습니다.

```bash
% hugo new post/<FILENAME>.md
```

## Front Matter

제목, 작성일자 등을 지정하기 위해 포스트 상단에 Front Matter라고 하는 토큰을 작성해야 합니다.
Front Matter는 설정 파일과 동일하게 `toml`, `yaml`, `json` 형식을 지원하며,   
[Hugo 공식 문서](https://gohugo.io/content-management/front-matter/) 또는 PaperMod에서 안내하는 아래형식을 참고할 수 있습니다.

```yaml
---
title: "My 1st post"
date: 2020-09-15T11:30:03+00:00
# weight: 1
# aliases: ["/first"]
tags: ["first"]
author: "Me"
# author: ["Me", "You"] # multiple authors
showToc: true
TocOpen: false
draft: false
hidemeta: false
comments: false
description: "Desc Text."
canonicalURL: "https://canonical.url/to/page"
disableHLJS: true # to disable highlightjs
disableShare: false
disableHLJS: false
hideSummary: false
searchHidden: true
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true
UseHugoToc: true
cover:
    image: "<image path/url>" # image path/url
    alt: "<alt text>" # alt text
    caption: "<text>" # display caption under cover
    relative: false # when using page bundles set this to true
    hidden: true # only hide on current single page
editPost:
    URL: "https://github.com/<path_to_repo>/content"
    Text: "Suggest Changes" # edit text
    appendFilePath: true # to append file path to Edit link
---
```

## 게시글 저장소 연동

저는 기존 TIL 저장소를 게시글로 활용할 예정이었기에,   
`content/post/` 디렉토리를 TIL 저장소의 submodule로 대체했습니다.

```bash
% git submodule add https://github.com/minyeamer/til.git content/post/
% git add content/post/
% git add .gitmodules
% git commit -m "feat: add til repository as post"
```

이렇게 설정했을 때 장점은 TIL 저장소에 변경사항이 발생했을 경우,   
아래와 같은 단 한 줄의 명령어로 블로그 저장소에서 업데이트할 수 있습니다.   
해당 명령어는 물론, 테마와 같은 다른 submodule에도 적용할 수 있습니다.

```bash
% git submodule update --remote
```

---

# 마치며

Jekyll 블로그와 며칠간 씨름하다 Hugo로 이동해 기존의 목표를 달성할 수 있었습니다.   
Chirpy 테마를 활용하지 못하는 것이 아쉽지만, PaperMod의 코드는 알기 쉽게 작성되어 있어   
시간적 여유만 있다면 커스터마이징에서 어려움이 없을 것이라 판단합니다.

이번 포스트에서는 Hugo 블로그를 구성하고 포스트를 작성하는 과정을 전달했습니다.   
다음엔 Utterances 위젯을 활용해 댓글 기능을 추가하는 방법을 안내해드리겠습니다.

## 참고 자료

- [Hugo Documents](https://gohugo.io/getting-started/)
- [PaperMod Documents](https://github.com/adityatelange/hugo-PaperMod/wiki/)
- [블로그 구축기 (1) Hugo + Github으로 개인 블로그 만들기](https://gurumee92.github.io/2020/08/블로그-구축기-1-hugo-github으로-개인-블로그-만들기/)
- [저장소 안에 저장소 - git submodule](https://youtu.be/TAe4uZqYt6c)
