---
layout: post
title: 깃허브 블로그 시작하기
date: 2022-08-30 16:28:43 +0900
categories: [Blog, Tech]
tags: [Jekyll, Chirpy, Github, Github Pages]
---

블로그를 처음 시작함에 있어서 모든 것이 준비된 호스팅 서비스의 편의성은 무시할 수 없습니다.   
저도 처음엔 코드를 직접 건드리는 자유도 높은 방식의 블로그에 진입 장벽을 느끼고   
가볍게 시작할 수 있는 티스토리를 통해 블로그에 입문했습니다.   
하지만, 개발적 지식을 학습하면서 깃허브에 마크다운 문서를 올리는 빈도가 늘어났고,   
깃허브에 올린 문서를 굳이 티스토리로 다시 옮겨 담는 것에 불편함을 느끼게 되었습니다.

마크다운 문서를 자주 작성하고 깃허브 저장소를 학습 노트로 활용한다면,   
깃허브 블로그를 구성해보는 것이 문서를 통합적으로 관리할 수 있다는 점에서 매력적이라 생각합니다.   
현재는 막 깃허브 블로그를 꾸려서 적응해가는 단계에 불과하지만,   
웹에서 정적 파일을 수집하는 기술을 적용할 수 있다면 중복된 자료를 생성할 필요 없이   
TIL 저장소 자체를 블로그 포스트 저장소로도 활용할 수 있을 것이라 기대합니다.

블로그를 개설하고 처음 작성하는 이번 포스트에서는 깃허브 블로그를 만든 과정을 소개해드리겠습니다.

---

# 테마 선택 및 가져오기

깃허브 블로그를 생성하는데 있어 주로 사용되는 기술이 Jekyll이라는 사이트 생성 엔진 입니다.   
Jekyll을 구성하는 Ruby와 쉘 스크립트 작성에 대한 이해가 있다면 더욱 자유도 높은 작업을 할 수 있지만,   
다행히 이를 모를지라도 다른 사용자들이 만든 테마를 가져와 블로그를 구성해 볼 수 있습니다.
Jekyll 테마는 아래와 같은 사이트를 참조하여 마음에 드는 UI를 확인할 수 있습니다.

- https://jekyllthemes.io
- http://jekyllthemes.org

무료로 가져다 사용할 수 있는 여러 테마 중 개인적으로 마음에 드는 Chirpy 테마를 활용해 보겠습니다.   
테마 별로 적용 및 활용하는 방식에 다소 차이가 있지만,   
Chirpy 같은 경우 아래 튜토리얼 사이트가 만들어져 있어 비교적 쉽게 블로그를 구성할 수 있습니다.

- https://chirpy.cotes.page

---

# 블로그 배포하기

Chirpy 테마를 설치하고 배포하는 방법엔 두 가지 방식이 있습니다.

1. [Chirpy Starter](https://github.com/cotes2020/chirpy-starter/generate)를 통해 간단하게 설치하기   
   튜토리얼에서는 Jekyll을 전혀 모르는 사용자도 쉽게 테마를 활용할 수 있는 프로젝트 파일이 마련되어 있습니다.   
   깃허브 저장소를 생성하는 것과 같은 단순한 버튼 클릭만으로 완성된 사이트를 배포할 수 있습니다.

2. [Github](https://github.com/cotes2020/jekyll-theme-chirpy)에서 소스코드를 fork 받아 직접 설치하기   
   스크립트를 실행하는 등 다소의 작업이 추가되지만, 블로그 커스터마이징에 유리한 방식입니다.   
   Jekyll을 다뤄볼 줄 안다면 직접 설치를 진행하는 것이 취향에 맞는 방식일 수 있습니다.

저 같은 경우 Jekyll에 친숙한 편이 아니기 때문에 1번째 방법을 통해 설치를 진행했습니다.

![chirpy-starter](https://github.com/minyeamer/til/blob/main/.media/blog/tech/jekyll-blog/chirpy-starter.png?raw=true)

이때, 저장소 이름은 `<GH_USERNAME>.github.io` 형식으로 지정해야 하며,   
`<GH_USERNAME>`에는 깃허브 아이디를 입력하면 됩니다.

위 방식으로 저장소를 생성하면 자동으로 배포가 수행되는데, `Actions` 탭을 통해 아래처럼 진행사항을 확인할 수 있습니다.

![github-actions](https://github.com/minyeamer/til/blob/main/.media/blog/tech/jekyll-blog/github-actions.png?raw=true)

빌드 및 배포가 완료되면 `https://<저장소 이름>` 주소를 통해 블로그 페이지에 접근할 수 있는데,   
2022년 8월 기준에서 해당 테마를 가져온 직후엔   
`--- layout: home # Index page ---` 텍스트만 존재하는 화면을 마주하게 됩니다.   
이것은 현재 Github Pages가 스타일이 적용되지 않는 `main` 브랜치를 대상으로 하고 있는 것이 원인으로,   
`Settings` 탭 아래 `Pages` 메뉴를 클릭했을 때 보이는 `Branch` 부분을 `gh-pages`로 수정하면 됩니다.

![github-pages](https://github.com/minyeamer/til/blob/main/.media/blog/tech/jekyll-blog/github-pages.png?raw=true)

---

# 블로그 설정하기

향후 블로그 호스팅 및 사이트 제목을 수정하는 등의 설정을 위해 `_config.yml` 파일을 수정할 필요가 있습니다.   
제가 블로그 세팅에 도움을 받은 [게시글](https://www.irgroup.org/posts/jekyll-chirpy/)로부터 일부 항목에 대한 설명을 가져왔습니다.

| 항목 | 값 | 설명 |
|---|---|---|
| timezone | Asia/Seoul | 시간대를 설정하는 부분으로 서울 표준시로 설정합니다. |
| title | 블로그 제목 | 프로필 사진 아래 큰 글씨로 제목이 표시됩니다. |
| tagline | 프로필 설명 | 블로그 제목 아래에 작은 글씨로 부연설명을 넣을 수 있습니다. |
| description | [SEO](https://searchengineland.com/guide/what-is-seo) | 구글 검색에 어떤 키워드로 내 블로그를 검색하게 할 것인가를 정의하는 부분입니다. |
| url | https://*.github.io | 블로그와 연결된 url을 입력합니다. |
| github | Github ID | 본인의 github 아이디를 입력합니다. |
| twitter.username | Twitter ID | 트위터를 사용한다면 아이디를 입력합니다. |
| social.name | 이름 | 포스트 등에 작성자로 표시할 나의 이름을 입력합니다. |
| social.email | 이메일 | 나의 이메일 계정을 입력합니다. |
| social.links | 소셜 링크들 | 트위터, 페이스북 등 내가 사용하고 있는 소셜 서비스의 나의 홈 url을 입력합니다. |
| avatar | 프로필 사진 | 블로그 왼쪽 상단에 표시될 프로필 사진의 경로를 설정합니다. |
| toc | true | 포스트 오른쪽에 목차를 표시합니다. |
| paginate | 10 | 한 목록에 몇 개의 글을 표시할 것인지 지정합니다. |

이 부분은 저의 설정 파일 [`_config.yml`](https://github.com/minyeamer/minyeamer.github.io/blob/main/data/config.old.yml) 또는 github 내 검색을 통해 접근할 수 있는   
다른 사용자 분들의 설정 파일을 참고하면 원하는 부분을 수정하는데 도움이 될 것입니다.   
`_config.yml` 파일이 수정 등 저장소에 변화가 발생하면 자동으로 빌드 및 배포 과정이 수행되며,   
변경사항이 적용되는데 약간 시간이 걸릴 수 있습니다.

---

# 포스트 작성하기

Jekyll은 마크다운 문법으로 글을 작성할 수 있습니다.   
마크다운 문법에 익숙하지 않다면 [해당 게시글](https://heropy.blog/2017/09/30/markdown/)을 참고해 주시기 바랍니다.   
VS Code 또는 기타 웹 편집기를 활용하면 마크다운 작성 내용을 실시간으로 렌더링해 확인할 수 있습니다.

게시글에 대한 마크다운 파일은 `_posts` 디렉토리 내에 위치시키고,   
`yyyy-mm-dd-제목.md`의 형식으로 파일 이름을 지정해야 합니다.   
제목에 해당하는 부분은 실제 포스트 제목이 아닌, url로 활용되는 부분이기 때문에   
게시글의 내용을 짐작하게 하는 간단한 단어나 문장을 활용하는게 좋습니다.

마크다운 파일의 상단엔 Front Matter라고 하는 Jekyll 게시글에서 허용하는 규칙을 통해   
게시글 제목, 작성일자, 카테고리, 태그 등을 지정할 수 있습니다.   
자세한 내용은 [튜토리얼](https://chirpy.cotes.page/posts/write-a-new-post/)을 참조할 수도 있고,   
해당 게시글에 대한 [raw 파일](https://raw.githubusercontent.com/minyeamer/til/main/blog/tech/jekyll-blog.md)을 확인해보셔도 좋습니다.

---

# 마치며

과거 깃허브 블로그를 만들려고 했을 때는 Jekyll을 직접 다뤄야 해서 쉽게 접근하지 못했는데,   
이제는 그럴 필요 없이 완성된 패키지를 가져다 쓸 수 있게 되어서 많이 편해졌다고 생각합니다.

## 참고 자료

- [Chirpy Documents](https://chirpy.cotes.page/)
- [깃헙(GitHub) 블로그 10분안에 완성하기](https://youtu.be/ACzFIAOsfpM)
- [Jekyll Chirpy 테마 사용하여 블로그 만들기](https://www.irgroup.org/posts/jekyll-chirpy/)
- [Github 블로그 테마적용하기(Chirpy)](https://seong6496.tistory.com/267)
