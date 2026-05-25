---
title: "[VS Code] AI 코딩 에이전트 비교 - Copilot, Codex, Claude Code, Gemini"
date: "2026-05-25T00:00:00+09:00"
layout: "post"
description: >
  VS Code에서 GitHub Copilot, OpenAI Codex, Claude Code, Gemini Code Assist를 직접 비교한 후기입니다.
  요금제, 사용 가능 모델, effort 설정, 인증 방식, 변경사항 검토 UI, 실제 블로그 글 수정 경험을 기준으로
  어떤 AI 코딩 에이전트를 선택할지 정리했습니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/897mc3dmsloub9iri35v8/vscode-00-all-assistants.webp?rlkey=gpvblwksuls4vefh8zfnj5d48&raw=1"
categories: ["AI", "AI Assistant"]
tags: ["VS Code AI 코딩 에이전트", "AI 코딩 도구 비교", "GitHub Copilot", "OpenAI Codex", "Claude Code", "Gemini Code Assist", "VS Code 확장 프로그램", "코딩 에이전트 추천", "reasoning effort", "개발 생산성"]
series: ["AI 코딩 에이전트 비교"]
---

<style>.data-table td {max-width: 800px !important;}</style>

{{< series "AI 코딩 에이전트 비교" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

GitHub Copilot, OpenAI Codex, Claude Code, Gemini Code Assist 4가지 AI 코딩 에이전트를
동일한 블로그 글 수정 작업에 투입해보고 VS Code 확장 프로그램으로 쓸 때의 차이를 중심으로 비교했습니다.
벤치마크 점수보다 실제 사용 흐름, 비용 구조, 수정 검토 경험이 궁금한 분에게 맞는 글입니다.

- **[요금제와 모델 비교](#요금제와-모델-비교하기)**: 구독 플랜, 제공 모델, effort 설정부터 먼저 정리합니다.
- **[GitHub Copilot](#github-copilot)**: 익숙한 VS Code 통합 경험은 좋지만 AI credits 체계가 부담이었습니다.
- **[OpenAI Codex](#openai-codex)**: 모델 선택과 작업 수행 능력은 좋지만 VS Code 안의 검토 흐름엔 아쉬움이 있었습니다.
- **[Claude Code](#claude-code)**: 대화 품질과 변경사항 검토 방식이 가장 자연스럽게 느껴졌습니다.
- **[Gemini Code Assist](#gemini-code-assist)**: 무료에 가까운 접근성과 Google 생태계 장점이 있지만 제 작업 방식과는 조금 달랐습니다.
- **[최종 선택](#최종-선택)**: 결국 어떤 도구를 계속 쓰기로 했는지 제 기준으로 결론을 정리합니다.
{{% /hint %}}

저는 그동안 GitHub Copilot을 사용해왔지만,
Copilot이 [사용량 기반 요금제](/blog/github-copilot-billing)로 변경되면서
예상 사용량을 계산해봤고 더 이상 Copilot 구독을 지속할 수 없다는 판단을 내렸습니다.
Copilot을 떠나면서 대안으로 다른 AI 코딩 에이전트에 대해 알아본 과정을 정리합니다.

이 글은 제공 업체별 AI 모델의 벤치마크 성능 차이를 비교하기 위한 글이 아닙니다.
제가 주로 사용하는 VS Code 환경에서 확장 프로그램 형태로 제공되는 AI 코딩 에이전트가
얼마나 사용이 편리한지, 그리고 얼마나 비용 효율적인지를 핵심 포인트로 다룹니다.

## 요금제와 모델 비교하기

AI 코딩 에이전트를 고를 때 예전에는 어느 모델이 더 똑똑한지 벤치마크 지표를 따지고
해당 모델을 제공하는 서비스를 구독하면 되었습니다. 하지만, 이제는 모델들이 상향 평준화되었고
같은 모델이라도 Reasoning Effort 설정에 따라 토큰을 더 많이 잡아먹으면서 더 높은 성능을 발생시킵니다.
넓은 범위의 작업을 한다면 사람의 기억력과 같은 역할을 하는 컨텍스트 윈도우 크기도 무시할 수 없습니다.

아래 내용은 2026년 5월 25일 기준으로 공식 문서와 가격 페이지를 확인해 정리한 것입니다.
AI 제품 요금제와 모델 목록은 자주 바뀌므로, 실제 결제 전에는 반드시 공식 문서를 다시 확인해야 합니다.

### 구독 플랜 비교

저가 요금제를 세분화한 업체도 있고 프리미엄 요금제를 세분화한 업체도 있습니다.
4개 업체가 일관된 정책을 가지지 않기 때문에 정확히 같은 분류로 나눌 수는 없지만,
개인 플랜을 기본/상위/프리미엄으로 구분해 임의로 분류했습니다.

{{% data-table delimiter="|" align-center="1" %}}
AI 코딩 에이전트|개인 기본 플랜|개인 상위 플랜|개인 프리미엄 플랜|제한 방식
GitHub Copilot|Pro $10/월|Pro+ $39/월|Max $100/월|월간 AI credits 제공, 세션 제한, 주간 한도
OpenAI Codex|ChatGPT Plus $20/월|ChatGPT Pro $100/월|ChatGPT Pro 20x $200/월|5시간 단위 + 주간 한도
Claude Code|Claude Pro $20/월|Claude Max $100/월|Claude Max 20x $200/월|5시간 단위 + 주간 한도
Gemini Code Assist|Google AI Plus $7.99/월|Google AI Pro $19.99/월|Google AI Ultra $99.99/월|일/시간/분 단위 한도
{{% /data-table %}}

요금만 보면 GitHub과 Google AI에서만 저가 요금제를 제공하고,
ChatGPT와 Claude는 반대로 사용량을 증대시킨 프리미엄 요금제를 제공합니다.
AI 코딩 에이전트를 이용할 수 있는 유료 플랜 순서대로 나열해서 GitHub Copilot과
Gemini Code Assist가 저렴해 보이지만, 토큰 사용량 기준으로 따지면
Codex와 Claude Code도 합리적인 가격입니다.

GitHub Copilot의 경우 [앞선 글](/blog/github-copilot-billing)에서
2026년 6월 1일부터 사용량 기반 요금제로 전환된다고 설명드렸습니다.
해당 요금제에서 토큰 사용량과 대응이되는 AI credits를 제공하는데,
GitHub에서 제공하는 실제 사용량으로 계산했을 때 API 크레딧을 결제해서 사용하는 것과
큰 차이가 없다는 결론을 내렸습니다.
이 글에서 GitHub Copilot은 비교 기준이며 고려 대상은 아닙니다.

{{< bookmark "https://github.com/features/copilot/plans" >}}

{{< bookmark "https://developers.openai.com/codex/pricing" >}}

{{< bookmark "https://claude.com/pricing" >}}

{{< bookmark "https://gemini.google/us/subscriptions" >}}

### 모델과 effort 설정 비교

AI 코딩 에이전트는 제공 업체별로 사용할 수 있는 모델이 한정적입니다.
그리고, 같은 모델이어도 추론(effort) 설정을 다르게 주어 결과물의 깊이를 키우거나
토큰 사용량을 절약할 수 있습니다.

{{% data-table delimiter="|" align-center="1" %}}
AI 코딩 에이전트|모델 관련 정보|추론(effort) 설정
GitHub Copilot|GPT, Claude, Gemini 모델을 자유롭게 선택|각각의 모델에서 제공하는 effort 선택
OpenAI Codex|GPT-5.5, GPT-5.4, GPT-5.3-Codex, GPT-5.4-mini 등|Low, Medium, High, Extra High
Claude Code|Opus 4.7, Sonnet 4.6, Haiku 4.5 등|Low, Medium, High, Max
Gemini Code Assist|Gemini 3 Pro, Gemini 3.5 Flash, Gemini 3 Flash 등|effort 선택 기능 제공 안함
{{% /data-table %}}

GitHub Copilot은 자체 모델을 제공하지 않는 대신에 다른 업체의 모델을 전부 제공합니다.
구독 플랜에 따라 Claude Opus 4.7 등 일부 모델엔 사용 제한이 있습니다.
그리고, GitHub Copilot은 내부 시스템 프롬프트의 한계 때문인지 같은 모델을 사용하더라도
Claude Code 등에서 사용하는 것 대비 성능이 떨어진다는 의견이 있습니다.

Codex와 Claude Code는 둘 다 추론(effort) 설정을 4단계로 줄 수 있습니다.
기본적인 작업은 Medium, 복잡한 작업은 High 이상을 설정하면 토큰 사용량과 성능의 trade-off를
최적화할 수 있습니다.
아쉽게도 Gemini는 API에서 Thinking level이란걸 제공하는 걸로 알고 있지만,
Gemini Code Assist에서는 추론(effort) 설정을 선택하는 기능은 제공하지 않습니다.

{{< bookmark "https://developers.openai.com/api/docs/models" >}}

{{< bookmark
  url="https://platform.claude.com/docs/en/about-claude/models/overview"
  title="Models overview"
  description="Claude is a family of state-of-the-art large language models developed by Anthropic. This guide introduces the available models and compares their performance."
  image="https://dl.dropboxusercontent.com/scl/fi/o7zc81u0m3ueaix03je9s/claude-models-og-image.webp?rlkey=mjo5g7710em1twgo3k3f00hzf&raw=1"
  siteName="Claude API Docs"
  fetch="false" >}}

{{< bookmark "https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/google-models" >}}

## GitHub Copilot

GitHub Copilot은 이번 비교의 기준점입니다.
제가 가장 오래 썼고, VS Code와의 통합도 가장 익숙합니다.

{{< bookmark "https://github.com/features/copilot" >}}

### 제공 기능

Copilot은 VS Code 안에서 Copilot Chat, Inline Chat, Code completions 등의
기능을 제공합니다. VS Code는 이 기능을 지속적으로 업데이트하고,
사용자는 내장 기능인 것처럼 자연스럽게 사용할 수 있습니다.

Copilot Chat은 코드를 수정할 때, 변경 전후를 수정 중인 파일 위에서 inline diff 형태로 보여줍니다.
개인적으로 마음에 드는 기능이며, Codex나 Claude Code가 제공하지 않는 강점이라고 생각합니다.

{{< bookmark "https://code.visualstudio.com/docs/copilot/chat/review-code-edits" >}}

요금제 측면에서는 2026년 6월 1일부터 AI credits 기준이 중요해집니다.
Code completions, next edit suggestions 기능은 유료 플랜에서 제한없이 제공되지만,
Copilot Chat은 AI credits를 소모하는 방식으로 변경됩니다.

그래서 GitHub Copilot은 VS Code에서 사용성은 가장 좋지만,
앞으로 API를 직접 사용하는 것과 같은 비싼 도구로 바뀌었습니다.

### 채팅 및 코드 수정 경험

제가 Copilot에서 가장 좋아한 점은 파일 안에서 코드 변경사항을 직접적으로 보여준다는 것입니다.
예시로 Markdown 글을 고칠 때 변경 전에 대한
<span style="background: #4B1818; color: white;">빨간색 라인</span>과
변경 후에 대한 <span style="background: #374121; color: white;">초록색 라인</span>이
에디터 위에 표시되고, `Keep`, `Undo` 버튼으로 빠르게 받아들이거나 되돌릴 수 있습니다.
되돌리기는 라인 단위로 적용할 수 있고, 단일 파일 또는 전체 되돌리기도 가능합니다.

![VS Code에서 Copilot 변경사항 검토](https://dl.dropboxusercontent.com/scl/fi/vjos5k4q1atpz0qbjwxp6/github-04-copilot-changes.webp?rlkey=1r0vencr0tqcu3kjl07fd6jpu&raw=1)

Autopilot 모드도 편했습니다. 권한을 계속 묻지 않고 끝까지 처리할 수 있어서,
여러 파일을 한 번에 정리할 때 흐름이 끊기지 않았습니다.

요청 기반의 Premium request 청구 방식에서는 Autopilot을 적극적으로 활용하여
넓은 범위의 작업을 처리하는 긴 프롬프트를 전달하면 1회 요청으로 높은 토큰량을 소모할 수 있었습니다.
구체적으로는, GPT-5.4 기준 1회 요청이 $0.28 가치를 가지는데, 장시간 돌아가는 작업을 요청하면
실제 사용량은 $10을 초과할 수도 있습니다.

하지만, 사용량 기반 청구 방식으로 변경되면서 이런 사용 방식은 더 이상 유효하지 않게 되었습니다.

### 글 작성 및 수정 요청 (영상)

VS Code에서 GitHub Copilot을 사용하여 자신의 사용법을 설명하는 블로그 글을 작성하고
글 속성을 SEO를 고려하여 수정하라고 요청했습니다. 작성된 글은 [바로가기](/blog/github-copilot-guide/)로
이동하여 확인할 수 있고, 아래에 동작 영상을 첨부합니다.

우선, 아무런 맥락을 제공하지 않고 GPT-5.4 모델에
"GitHub Copilot 사용법을 설명하는 블로그 글을 작성하라"고 요청했습니다.

<video controls preload="metadata" style="width: 100%;">
  <source src="https://dl.dropboxusercontent.com/scl/fi/ws053z4aypls0lwk7pent/vscode-chat-01-github-copilot.mp4?rlkey=rnipfnkqiiq0pnx45x4s1lmyz&st=rag1frky&raw=1" type="video/mp4">
  브라우저가 video 태그를 지원하지 않습니다.
</video>

작성된 글을 토대로 "SEO를 고려하여 front matter를 다시 작성하라"고 요청했습니다.

(이전 영상에서는 테마를 포함한 루트 경로에서 요청했는데,
여기서부터는 마크다운 파일만 있는 `content/` 경로 아래에서 요청합니다.)

<video controls preload="metadata" style="width: 100%;">
  <source src="https://dl.dropboxusercontent.com/scl/fi/7k4c4youxnle8m3hj3xmc/vscode-diff-01-github-copilot.mp4?rlkey=2xl2y0ap5ytcd2esx64yt27po&st=y1sva24v&raw=1" type="video/mp4">
  브라우저가 video 태그를 지원하지 않습니다.
</video>

작성된 글 [GitHub Copilot 사용법 가이드 - VS Code AI 코딩으로 개발 생산성 높이기](/blog/github-copilot-guide/)에서
커버 이미지는 제가 직접 다운로드 받은 이미지 파일을 넣었고, 추가로 AI 작성 주의 문구와 시리즈를 넣은 것을 제외하면 나머지는
GitHub Copilot의 GPT-5.4 (Medium) 모델이 작성한 것을 여과없이 올렸습니다.

제 블로그 글은 상단에 "AI 요약 & 가이드" 영역이 배치되고 H2, H3 목차로 글을 구성하는데,
별도로 맥락을 제공하지 않아도 제가 작성한 다른 글을 보고 저의 스타일을 모방했습니다.
북마크(bookmark)와 같이 서택스(SeoTax) 테마에서 제공하는 Shortcode 기능을
이해하고 사용한 것도 놀라운 점입니다.
수정하고 싶은 부분이라면, 목차를 너무 세분화해서 우측 하단의 툴바 버튼과 겹치는 부분 정도입니다.

![GitHub Copilot 사용법 가이드 - VS Code AI 코딩으로 개발 생산성 높이기](https://dl.dropboxusercontent.com/scl/fi/fvkrpju98h3dj3iegaj55/vscode-01-copilot-blog-post.webp?rlkey=6ocpdy3mzht8koh5vd4nw6uyz&raw=1)

## OpenAI Codex

Codex는 사용 전부터 기대가 컸습니다.
GitHub Copilot에서 Claude 모델의 성능이 저하되었고, Claude Code 안에서도 Anthropic이
모델의 성능을 낮췄다는 얘기도 있어서 OpenAI 모델이 상대적으로 나을 것이라는 내적 판단이 있었습니다.
2026년 5월달부터는 이런 판단 하에 GitHub Copilot에서 Sonnet 모델 대신에 GPT-5.4 모델을 주로 사용했습니다.

Codex는 이제 막 사용했기 때문에 구체적인 기능을 알진 못하지만,
`/plan`과 같은 CLI 명령어를 제공하는 점은 GitHub Copilot과 마찬가지로 직관적입니다.
최근에는 Claude Code의 `/ralph-loop` 플러그인을 모방한 `/goal` 명령어를 제공하는 것도 인상적입니다.

{{< bookmark "https://developers.openai.com/codex/cli/slash-commands" >}}

### Codex 인증 (device code)

VS Code에서 Codex 확장 프로그램을 설치할 수 있습니다.
확장 프로그램을 설치하면 우측 채팅창에 CODEX 탭이 새로 추가됩니다.

![Codex 설치](https://dl.dropboxusercontent.com/scl/fi/ghaokq1he0tlfffkexra1/vscode-02-codex-install.webp?rlkey=vx8t9o98gbj80k2tua5ninbu7&raw=1)

GitHub Copilot의 Chat과 같은 위치에서 Codex를 이용할 수 있는 점은 매우 큰 장점입니다.
Codex를 사용하려면 ChatGPT Plus 이상의 플랜이 구독된 계정에 로그인해야 합니다.
단순하게 브라우저에서 로그인할 수도 있지만, 저는 원격 PC를 통해 로그인을 대신하는 방식을 사용하려 합니다.

로그인 버튼 중에서 마지막 `More options` 버튼을 클릭하면 device code와 접속 링크가 생성됩니다.
원격 PC의 브라우저에서 해당 링크에 접속하면 9자리 코드를 입력할 수 있는 페이지가 나타납니다.
ChatGPT 계정에 로그인된 상태에서 코드를 입력하면 인증이 완료되어 해당 계정의 권한으로 Codex를 이용할 수 있습니다.

![장치 코드를 사용해 Codex CLI에 액세스를 부여하세요](https://dl.dropboxusercontent.com/scl/fi/s5abc9qo6uzcvc23d1ago/vscode-03-codex-device-code.webp?rlkey=octzqjh2y168fuidmjmbx61y3&raw=1)

주의할 점은, ChatGPT 계정 설정에서 "보안" 메뉴의 "Codex용 장치 코드 인증 활성화" 옵션을 활성화해야
위 페이지에서 "계속" 버튼을 클릭할 수 있습니다.

![Codex용 장치 코드 인증 활성화](https://dl.dropboxusercontent.com/scl/fi/2mqbmtd7qmlqnqplu8yf1/vscode-04-codex-enable-device-code.webp?rlkey=b05m0504rs7ylezw4xcitn4mf&raw=1)

### 글 작성 및 수정 요청 (영상)

VS Code에서 Codex를 사용하여 자신의 사용법을 설명하는 블로그 글을 작성하고
글 속성을 SEO를 고려하여 수정하라고 요청했습니다. 작성된 글은 [바로가기](/blog/openai-codex-guide)로
이동하여 확인할 수 있고, 아래에 동작 영상을 첨부합니다.

우선, 아무런 맥락을 제공하지 않고 GPT-5.4 모델에
"Codex 사용법을 설명하는 블로그 글을 작성하라"고 요청했습니다.

![Codex 사용법을 설명하는 블로그 글을 작성하라](https://dl.dropboxusercontent.com/scl/fi/el43wpc9zu9tn2tfxiaat/vscode-05-codex-edit-new-post.webp?rlkey=t26vvjkk2f07p5vuw7q5cxfya&raw=1)

글 작성 과정이 길고 추론 과정은 비슷해서 Codex부터는 글 작성 영상을 남기지 않았습니다.
Codex와 GitHub Copilot의 코드 수정 시 차이점은 수정 결과가 파일 위에 표시되지 않는 점입니다.
채팅창에서 `Review`를 클릭하면 새로운 탭에 Codex Diff를 보여주지만,
GitHub Copilot의 inline diff 표시 방식와 비교하면 확실히 불편했습니다.

![Codex Code Review](https://dl.dropboxusercontent.com/scl/fi/c18fyruf5ps33gyyd1caj/vscode-06-codex-code-review.webp?rlkey=kxtr1jswrzrp5bd714s7q5c77&raw=1)

작성된 글을 토대로 "SEO를 고려하여 front matter를 다시 작성하라"고 요청한 영상은 다음과 같습니다.
영상 마지막에 `Review`를 클릭해서 어떤 라인이 변경되었는지 알려주는 Codex Diff 결과를 볼 수 있습니다.

<video controls preload="metadata" style="width: 100%;">
  <source src="https://dl.dropboxusercontent.com/scl/fi/qeujuyoab47052g5xnpda/vscode-diff-02-openai-codex.mp4?rlkey=flxwq8ms8fktfm22bknb49x22&st=845onps8&raw=1" type="video/mp4">
  브라우저가 video 태그를 지원하지 않습니다.
</video>

작성된 글 [OpenAI Codex 사용법 - CLI, VS Code, 웹에서 AI 코딩 에이전트 활용하기](/blog/openai-codex-guide)에서
커버 이미지는 제가 직접 다운로드 받은 이미지 파일을 넣었고, 추가로 AI 작성 주의 문구와 시리즈를 넣은 것을 제외하면 나머지는
Codex의 GPT-5.4 (Medium) 모델이 작성한 것을 여과없이 올렸습니다.

아무래도 같은 모델을 사용했기 때문에 GitHub Copilot과 결과가 비슷하게 나타났는데,
VS Code에 대해서 언급하진 않았기 때문에 범용적인 Codex CLI에 대한 설명이 작성되었습니다.
마찬가지로 "AI 요약 & 가이드" 영역과 북마크 Shortcode 사용을 원활히 수행했습니다.

![OpenAI Codex 사용법 - CLI, VS Code, 웹에서 AI 코딩 에이전트 활용하기](https://dl.dropboxusercontent.com/scl/fi/5qql98aho21tjzzqphqsg/vscode-07-codex-blog-post.webp?rlkey=b2wgwl18nv1l95ljb7xbo8tsv&raw=1)

## Claude Code

Claude Code는 초기 기대치가 높지 않았습니다.
Codex 부분에서 설명했듯이 최근에 Claude 모델의 성능이 저하되었다는 느낌을 받았고,
실제로 하드웨어 병목 문제로 Anthropic이 저성능 GPU를 섞어서 모델을 돌린다는 의혹도 있었기 때문에
예전처럼 Claude가 절대적이라는 인식은 없었습니다.

하지만, VS Code 확장 프로그램으로써 Claude Code는 Codex보다 좋았습니다.

CLI 명령어 또한 `/plan`을 활용할 수 있고, `/plugin`이라는 부가 기능도 제공하는 점이 좋았습니다.
확장 프로그램을 처음 사용할 때 사용량을 채팅창에서 제공하지 않아 어떻게 보는지 몰랐는데,
`/usage` 명령어를 입력하면 모달창으로 띄워서 보여주었습니다.

{{< bookmark
  url="https://code.claude.com/docs/en/commands"
  title="Commands - Claude Code Docs"
  description="Complete reference for commands available in Claude Code, including built-in commands and bundled skills."
  image="https://dl.dropboxusercontent.com/scl/fi/n2454ehrxgd6uqxuc0pa1/claude-commands-og-image.webp?rlkey=xgkehhwr03b7le7vl5v4dznf4&raw=1"
  fetch="false" >}}

### Claude Code 인증

VS Code에서 Claude Code 확장 프로그램을 설치할 수 있습니다.
확장 프로그램을 설치하면 우측 채팅창에 CLAUDE CODE 탭이 새로 추가됩니다.

![Claude Code 설치](https://dl.dropboxusercontent.com/scl/fi/6rhyxdhmeojq8vcnuxh5u/vscode-08-claude-code-install.webp?rlkey=zvd5togj07mz6hk0guert9lny&raw=1)

GitHub Copilot이나 Codex와 동일한 채팅창을 공유하여 이들을 같이 이용하더라도
전환하는데 전혀 불편함이 없는 점이 좋았습니다.

Claude Code를 사용하려면 Claude Pro 이상의 플랜이 구독된 계정에 로그인해야 합니다.
마찬가지로 저는 원격 PC를 통해 로그인을 대신하는 방식을 사용하겠습니다.
Claude Code의 인증은 원격 PC로 로그인하더라도 직관적인 편입니다.
`Claude.ai Subscription` 버튼을 클릭하면 인증 URL이 생성됩니다.

![Continue in browser](https://dl.dropboxusercontent.com/scl/fi/4yotm3fdp8dtsa2e7efxp/vscode-09-claude-code-auth-url.webp?rlkey=316tnwk450lsd4xspbvjrnjgl&raw=1)

어떤 PC든 상관없이 브라우저에서 인증 URL로 접속하면 Claude 계정 로그인 후 간단하게 승인할 수 있습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/g664pc1beq9n7221a4c7q/vscode-10-claude-code-authorization.webp?rlkey=oyowklc2hpne50vlw7e2d287b&raw=1"
  alt="Claude Code님이 귀하의 Claude chat account에 연결을 요청했습니다"
  max-width="550px"
  align="center" >}}

### 글 작성 및 수정 요청 (영상)

VS Code에서 Claude Code를 사용하여 자신의 사용법을 설명하는 블로그 글을 작성하고
글 속성을 SEO를 고려하여 수정하라고 요청했습니다. 작성된 글은 [바로가기](/blog/claude-code-guide)로
이동하여 확인할 수 있고, 아래에 동작 영상을 첨부합니다.

우선, 아무런 맥락을 제공하지 않고 Sonnet 4.6 모델에
"Claude Code 사용법을 설명하는 블로그 글을 작성하라"고 요청했습니다.

![Claude Code Review](https://dl.dropboxusercontent.com/scl/fi/yaxlrjcjugrkazqpp4sln/vscode-11-claude-code-review.webp?rlkey=ghh8p4kac40l7u87ppx9kdryo&raw=1)

마찬가지로 추론 과정에 대한 영상은 생략합니다.
Claude Code가 Codex와 다르게 인상적이었던 점은, 코드 작성을 완료하고 사용자에게 변경사항을 보여주면서
작성할지 여부를 묻는다는 것이었습니다. GitHub Copilot처럼 inline diff 형태로 보여주지 못한다는게
아쉽지만, 대안으로는 Codex보다 낫다고 생각합니다.
채팅 UI의 생김새는 GitHub Copilot이나 Codex보다 훨씬 마음에 들었습니다.

![Claude Code 사용법을 설명하는 블로그 글을 작성하라](https://dl.dropboxusercontent.com/scl/fi/15j0ga1sx1apqmtolr1hi/vscode-12-claude-code-edit-new-post.webp?rlkey=rffay72jqvlgfh6kb8prmqj0h&raw=1)

작성된 글을 토대로 "SEO를 고려하여 front matter를 다시 작성하라"고 요청한 영상은 다음과 같습니다.
중간에 변경사항을 보여주면서 수정 확인을 요청하고, `Yes`를 클릭하면 변경된 파일로 넘어가는 모습을 볼 수 있습니다.

<video controls preload="metadata" style="width: 100%;">
  <source src="https://dl.dropboxusercontent.com/scl/fi/csmos0qgi32kvrve4v1n3/vscode-diff-03-claude-code.mp4?rlkey=772q1q3khbcoovunwmwqv9w05&st=x7x5gys1&raw=1" type="video/mp4">
  브라우저가 video 태그를 지원하지 않습니다.
</video>

작성된 글 [Claude Code 사용법 완벽 가이드 - 설치부터 MCP 서버, CLAUDE.md 설정까지](/blog/claude-code-guide)에서
커버 이미지는 제가 직접 다운로드 받은 이미지 파일을 넣었고, 추가로 AI 작성 주의 문구와 시리즈를 넣은 것을 제외하면 나머지는
Claude Code의 Sonnet 4.6 (Medium) 모델이 작성한 것을 여과없이 올렸습니다.

Codex와 마찬가지로 별도의 맥락을 제공하지 않아도 제 블로그 글의 구성을 이해하고 일관성있게 작성했습니다.
글에 제한을 두지 않았기 때문에 목차가 길어지는 것은 아쉽지만 목차 문제는 공통적인 부분이라 넘어갈만 합니다.

![Claude Code 사용법 완벽 가이드 - 설치부터 MCP 서버, CLAUDE.md 설정까지](https://dl.dropboxusercontent.com/scl/fi/iubked8fpxs9lsgzsoaox/vscode-13-claude-code-blog-post.webp?rlkey=k03h38iixixj2q2dyirfrsxf8&raw=1)

## Gemini Code Assist

Gemini Code Assist는 사실 처음에는 비교 대상에 넣지 않으려고 했습니다.
요금제나 모델이 직관적으로 다가오지 않았고, VS Code 확장 프로그램도 불편했기 때문입니다.
그래도 회사에서 지원하는 계정이 있어서 한 번은 써봐야 한다고 생각해서 설치하고 테스트했습니다.

### Gemini 인증

VS Code에서 Gemini Code Assist 확장 프로그램을 설치할 수 있습니다.
하지만, 확장 프로그램을 설치했을 때 우측 채팅창에 새로운 탭이 생기지 않아 어떻게 실행해야 할지 당황했습니다.
제가 찾은 채팅창 진입 방법은 하단 상태 표시줄에서 Gemini 아이콘을 클릭하는 것이었고,
VS Code를 재부팅하니 파일 탭 우측에도 Gemini 아이콘이 나타났습니다.

문제는, Gemini 채팅창이 오른쪽이 아니라 왼쪽에 나타난다는 점이었습니다.
왼쪽 사이드바는 탐색기나 검색에 빈번히 사용되는데 이렇게 영역이 겹치면 다루기가 불편합니다.

![Gemini Code Assist 설치](https://dl.dropboxusercontent.com/scl/fi/7fnk4tw0etkbajb59orb0/vscode-14-gemini-install.webp?rlkey=4ox8unukrbt8sjfpbe2yfzq1r&raw=1)

구글 계정 인증은 Claude Code와 마찬가지로 인증 URL을 원격 PC에서 접속해 로그인을 대신할 수 있었습니다.

### 글 작성 및 수정 요청 (영상)

VS Code에서 Gemini Code Assist를 사용하여 자신의 사용법을 설명하는 블로그 글을 작성하고
글 속성을 SEO를 고려하여 수정하라고 요청했습니다. 작성된 글은 [바로가기](/blog/gemini-code-assist-guide)로
이동하여 확인할 수 있고, 아래에 동작 영상을 첨부합니다.

우선, 아무런 맥락을 제공하지 않고 Gemini 3.1 Pro 모델에
"Gemini Code Assist 사용법을 설명하는 블로그 글을 작성하라"고 요청했습니다.
Gemini 모델의 추론 시간이 다른 모델들보다 길다고 느껴졌는데 결과는 다소 부실했습니다.
(아마, "Gemini"가 아니라 "Gemini Code Assist"에 특정해서 설명을 요청해서 그럴지 모르겠습니다.)

GitHub Copilot처럼 inline diff 형태로 변경사항을 보여주는 것은 장점이라고 생각하지만,
Pro와 Flash라는 단순한 모델 분류와 아직 이해하기 어려운 사용 한도 때문에 Gemini를 사용할
필요성은 못느끼고 있습니다.

![Gemini Code Assist 사용법을 설명하는 블로그 글을 작성하라](https://dl.dropboxusercontent.com/scl/fi/tt6r0dka2tml66lfkyxla/vscode-16-gemini-code-review.webp?rlkey=djw2wjx1nfowfi0khh1uccytv&raw=1)

작성된 글을 토대로 "SEO를 고려하여 front matter를 다시 작성하라"고 요청한 영상은 다음과 같습니다.
inline diff 형태로 파일 위에 변경사항을 보여주고 `Accept`를 클릭하면 저장되는 모습을 볼 수 있습니다.

<video controls preload="metadata" style="width: 100%;">
  <source src="https://dl.dropboxusercontent.com/scl/fi/z0ofh2q5mz9hilas7dizb/vscode-diff-04-gemini-code-assist.mp4?rlkey=tum34oilkgwefqchrdktxewd3&st=055t75hc&raw=1" type="video/mp4">
  브라우저가 video 태그를 지원하지 않습니다.
</video>

작성된 글 [Gemini Code Assist 사용법 완벽 가이드 - VS Code AI 코딩으로 생산성 극대화](/blog/gemini-code-assist-guide)에서
커버 이미지는 제가 직접 다운로드 받은 이미지 파일을 넣었고, 추가로 AI 작성 주의 문구와 시리즈를 넣은 것을 제외하면 나머지는
Gemini Code Assist의 Gemini 3.1 Pro 모델이 작성한 것을 여과없이 올렸습니다.

글의 구성을 이해하고, 특히 Hint Shortcode에 `warning` 파라미터를 주어 응용한 것은
차별화된 부분입니다. 하지만, 쓸 내용이 없었는지 다소 짧고 부실한 구성은 아쉬운 점입니다.

![Gemini Code Assist 사용법 완벽 가이드 - VS Code AI 코딩으로 생산성 극대화](https://dl.dropboxusercontent.com/scl/fi/0ocw3h7n13p1o4j1lyomf/vscode-17-gemini-blog-post.webp?rlkey=584flcdd2rmbsncb8pksn825y&raw=1)

## 최종 선택

이번 비교의 결론은 하나의 도구로 통일하는 것이 아니었습니다. 작업 성격에 따라 나눠 쓰는 쪽이 더 현실적이었습니다.

{{% data-table delimiter="|" align-center="1" %}}
AI 코딩 에이전트|가장 좋았던 점|가장 아쉬웠던 점|내 사용 계획
GitHub Copilot|파일 안에서 보여주는 inline diff와 Autopilot|AI credits 기준 비용 부담|무료 모델로 질의 응답
OpenAI Codex|큰 문맥 파악, 다양한 모델/effort 선택|Review를 자동으로 보여주지 않음|새 프로젝트 기획 등 큰 작업
Claude Code|대화 흐름과 변경사항 검토 경험|Codex 대비 부족한 사용량|기존 코드 수정, 리뷰가 중요한 작업
Gemini Code Assist|GitHub Copilot과 유사한 inline diff|왼쪽 패널과 결과 품질이 아쉬움|사용 계획 없음
{{% /data-table %}}

### 내 기준의 결론

제 선택은 아래처럼 정리됩니다.

{{% hint info %}}
처음부터 프로젝트를 시작할 때는 **Codex**를 먼저 사용합니다.   
기존 코드를 수정해야 하고 변경사항을 직관적으로 확인해야 할 때는 **Claude Code**를 사용합니다.   
그 외 사소한 요청이나 문서 정리는 상대적으로 토큰 효율을 기대할 수 있는 **Codex**에서 처리합니다.  
**GitHub Copilot**은 단순 질의 응답에 한해 무료 모델을 사용할 수도 있습니다.   
**Gemini Code Assist**는 다른 유료 플랜의 사용량 한도에 도달하지 않는 한 사용할 계획이 없습니다.
{{% /hint %}}

GitHub Copilot은 여전히 좋은 도구입니다.
특히 VS Code 안에서 변경사항을 보여주는 방식은 다른 AI 코딩 에이전트를 사용하면서 더욱 편리하다고 느꼈습니다.
다만, 제 사용 패턴에서는 사용량 기반 요금제로 전환한 후 마음 놓고 큰 작업을 맡기기 어려워졌습니다.

AI 제공 업체들은 이미 많은 비용을 부담하고 있고 그것이 버티지 못하는 순간이 얼마 남지 않았다고 생각합니다.
이미 GitHub Copilot은 감당하지 못하는 수준에 진입한 것 같고,
나머지 OpenAI나 Anthropic 같은 업체들도 상장하게 된다면 비용 압박에 시달리면서 AI 구독료를 올릴 것입니다.
이러한 생각에 저는 [NVIDIA NIM API](https://build.nvidia.com/explore/discover)라는
무료 API에 자체 AI 코딩 에이전트 툴을 만들어서 사용할까도 고민하고 있습니다.

![NVIDIA NIM API](https://dl.dropboxusercontent.com/scl/fi/pbdauquu5x5ujuvve2lan/vscode-18-nvidia-nim-api.webp?rlkey=ovdapgtn6zykjytj43yy3c2gk&raw=1)

구독형 AI 모델은 더 이상 안식처가 아니고, 언제든지 갈아탈 수 있도록 2차, 3차 대안을 마련할 필요가 있다고 깨달았습니다.
