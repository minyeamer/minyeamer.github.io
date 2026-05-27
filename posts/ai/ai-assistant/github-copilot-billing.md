---
title: "GitHub Copilot 사용량 기반 청구 전환 - AI credits로 내 요금 다시 계산하기"
date: "2026-05-24T23:54:15+09:00"
layout: "post"
description: >
  GitHub Copilot AI credits 요금제 전환을 실제 사용량 리포트로 계산한 분석 글입니다.
  Premium Requests와 AI credits 차이, Pro·Pro+·Max 포함량, 2026년 6월 1일 이후 예상 비용,
  그리고 Copilot을 떠나기로 한 이유까지 함께 정리했습니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/z0g7nrp7zd4hmvsjb9phc/github-00-usage-based-billing.webp?rlkey=decvi4ymp0axwytba8nhwr3sc&raw=1"
categories: ["AI", "AI Assistant"]
tags: ["GitHub Copilot", "GitHub Copilot AI credits", "Copilot 사용량 기반 청구", "Copilot Premium Requests", "Copilot 요금제 변경", "AI 코딩 에이전트", "VS Code AI", "개발 도구 비용"]
series: ["AI 코딩 에이전트 비교"]
---

{{< series "AI 코딩 에이전트 비교" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

GitHub Copilot 개인 계정의 사용량 리포트를 CSV 파일로 내려받아,
기존 Premium Requests 방식과 2026년 6월 1일부터 적용되는 AI credits 방식을 비교했습니다.
저처럼 긴 프롬프트와 큰 작업을 자주 맡기는 사용자라면, 기존보다 실제 체감 비용이 얼마나 달라지는지
사용량 리포트로 가늠해볼 수 있도록 정리한 글입니다.

- **[사용량 기반 청구 전환](#사용량-기반-청구-전환)**: 왜 GitHub가 요청 수가 아니라 사용량 중심으로 바꾸는지 정리합니다.
- **[Premium request와 AI credits](#premium-request에-대해)**: 예전 계산 방식과 새 과금 단위가 어떻게 다른지 비교합니다.
- **[새 Copilot 요금제](#github-ai-credits)**: Pro, Pro+, Max 플랜별 포함 credits와 초과 비용 구조를 봅니다.
- **[사용량 리포트 분석](#내-실제-사용량)**: 2026년 3월부터 5월까지 제 실제 사용량을 월별 예상 비용으로 다시 계산합니다.
- **[이탈 결정과 대안](#copilot-이탈-결정)**: Copilot을 계속 쓰지 않기로 한 이유와 다음 비교 대상도 이어서 정리합니다.
{{% /hint %}}

GitHub Copilot은 제가 VS Code에서 가장 오래, 가장 자연스럽게 사용한 AI 코딩 도구입니다.
누군가는 Claude Code가, 누군가는 Codex가 좋다고 하면서 매일매일 하네스를 깎는 얘기를 많이 들었지만,
저는 그정도의 성능이 필요하진 않기에 저에게 있어 가장 편하고 비용 대비 효율도 매우 저렴한
GitHub Copilot을 애용했습니다.

## 사용량 기반 청구 전환

그러다 최근에 GitHub Copilot 청구 방식이 바뀐다는 안내를 봤습니다.
공식 문서 기준으로 2026년 6월 1일부터 개인 Copilot 요금제는
기존 Premium request 중심의 방식에서 GitHub AI Credits 기반 사용량 청구로 전환됩니다.

{{< bookmark "https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals" >}}

평소 저의 사용 행태를 생각하면 GitHub Copilot이 막대한 토큰 사용료를 감당하고 있었음은 인지하고 있었고,
단순 구독료 인상 정도는 감당할 수 있었지만, 요금 산정 기준 자체가 바뀌는건 예상 밖의 일이었습니다.
일이 벌어지고 나서 대처하면 늦으니 일단 문서에서 안내하는대로 내 사용량 리포트를 내려받아
어느정도 수치의 차이가 발생하는지 짐작해 보았습니다.

### Premium request에 대해

GitHub Copilot 요금 산정 기준에 대해 제가 알고 있는 것을 우선 정리해 보고자 합니다.

{{< bookmark "https://docs.github.com/en/copilot/concepts/billing/copilot-requests" >}}

Premium request 방식은 Copilot에게 프롬프트를 한 번 보내면 대체로 요청 하나로 계산됐습니다.
모델별로 요청에 대한 multiplier가 있지만, 그 1회 요청에 아무리 많은 토큰을 처리해도 동등한 1회 요청으로 처리됩니다.
위 문서에서 Premium request 방식에 대한 자세한 설명을 읽어볼 수 있는데,
그 중에서 주요 모델의 multiplier는 다음과 같습니다.

{{% data-table align-center="1,2,3" %}}
Model,Multiplier for paid plans,Multiplier for Copilot Free
Claude Haiku 4.5,0.33,1
Claude Sonnet 4.5,1,Not applicable
Claude Opus 4.5,3,Not applicable
Claude Opus 4.7,15,Not applicable
Gemini 3 Flash,0.33,Not applicable
Gemini 3.1 Pro,1,Not applicable
Gemini 3.5 Flash,14,Not applicable
GPT-5 mini,0,1
GPT-5.4,1,Not applicable
GPT-5.4 mini,0.33,Not applicable
GPT-5.5,7.5,Not applicable
{{% /data-table %}}

저는 Premium request 과금 체계가 갖는 이점을 이용해
Copilot에게 요청할 때 한번에 대량의 프롬프트를 전달하여 끊기지 않는 작업을 처리하게 했습니다.
특히, GPT-5.4 모델의 추론 수준을 xhigh까지 높이고 1500자 정도의 프롬프트를 작성하면
빈 폴더에서 프로젝트 기획부터 풀스택 코드베이스 구현까지 수행할 수 있었습니다.

이것이 오히려 Claude Code나 Codex 같은 토큰 기반 요금제를 가진 AI 코딩 에이전트를
사용할 생각을 못했던 이유기도 합니다. 하지만, 제가 사용하는 AI 툴이 언제까지나 같은 조건으로
지원된다고 생각한 것은 너무 안일했습니다. 단 1회의 요청으로 여러 파일을 읽고, 긴 문맥을 모델에 넣고,
수정안을 만들고, 필요하면 다시 검토하는 작업까지 수행하는 것을 당연하다고 여기면 안됐습니다.

### 요청 기반 과금의 한계

GitHub 공식 블로그에서는 이 부분을 직접적으로 설명합니다.
Copilot이 단순한 에디터 보조 도구에서 여러 단계의 작업을 수행하는 "agentic platform"으로 커졌고,
긴 세션과 최신 모델 사용이 늘면서 추론 비용이 크게 증가했다는 내용입니다.

{{< bookmark "https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/" >}}

핵심은 간단합니다.

빠른 질문 하나와 여러 파일을 고치는 긴 에이전트 작업이 모두 1회 요청으로 처리되면,
공급자는 실제 토큰과 모델 비용을 요금에 반영하기 어렵습니다.
반대로 사용자는 요청 수를 아끼기 위해 더 긴 프롬프트와 더 큰 작업을 한 번에 넣는 방향으로 움직입니다.

이 구조는 저처럼 Copilot을 적극적으로 쓰는 사용자에게는 유리했습니다.
하지만 GitHub 입장에서는, 정확히 Microsoft 입장에서는 헤비 유저가 많아질수록 감당하기 어려운 구조였을 것입니다.

### AI 구독 시장에서 보이는 신호

GitHub Copilot만 이런 방향으로 가는 것은 아닙니다.

Claude Code는 한때 Pro 요금제에서 사라졌던 적도 있고,
OpenClaw 같은 서드파티 도구에서 재사용하는 것을 엄격하게 제한하고 있습니다.
최근에는 저성능의 하드웨어를 섞어서 사용하면서 모델의 성능도 저하되었다는 의견도 있습니다.

{{< bookmark "https://claude.com/pricing" >}}

OpenAI Codex 또한 2개월 전인 2026년 4월부터 메시지당 과금 방식에서
토큰 사용량 기반 요금제로 전환되었습니다.

{{< bookmark "https://developers.openai.com/codex/pricing" >}}

Google도 Gemini 쪽에서 일일 프롬프트 제한보다 컴퓨팅 사용량 기반(compute-used) 요금제로
변경한다고 설명합니다.

{{< bookmark "https://blog.google/products-and-platforms/products/google-one/google-ai-subscriptions/" >}}

결국 AI 코딩 도구는 "월 구독료만 내면 무제한으로 큰 작업을 맡기는 도구"에서
"월 구독료에 포함된 크레딧 안에서 작업량을 관리하는 도구"로 이동하고 있습니다.

## GitHub AI credits

GitHub 문서에 따르면 AI credits는 Copilot 사용량을 계산하는 billing unit입니다.
1 AI credit은 $0.01로 계산되고, 사용량은 모델과 토큰 수에 따라 달라집니다.
여기서 토큰은 입력, 출력, 캐시 토큰을 모두 포함합니다.

### 요금제별 AI credits

2026년 5월 23일 기준 문서에는 개인 요금제가 아래처럼 정리되어 있습니다.

{{% data-table delimiter="|" align-center="1,2,3,4,5" %}}
Plan|Price per month|Base credits|Flex allotment|Total monthly AI credits
Copilot Pro|$10|1,000|500|1,500
Copilot Pro+|$39|3,900|3,100|7,000
Copilot Max|$100|10,000|10,000|20,000
{{% /data-table %}}

여기서 중요한 부분은 `base credits`와 `flex allotment`가 나뉜다는 점입니다.
`base credits`는 구독료와 맞물린 기본 포함량이고,
`flex allotment`는 모델 가격과 효율 변화에 따라 조정될 수 있는 추가 포함량입니다.
그래서 단순히 "월 $10면 $10어치만 포함"이라고 보는 것보다,
현재 문서 기준으로는 Pro에 총 1,500 credits, 즉 $15 상당의 AI credits가 포함된다고 보는 편이 계산에 맞습니다.

다만 이 값은 문서 기준입니다. 실제 적용과 정책은 GitHub의 최종 안내와 계정 설정을 따라야 합니다.

### 자동완성은 계속 예외

> Copilot features that use AI models consume AI credits.
> This includes Copilot Chat, Copilot CLI, Copilot cloud agent,
> Copilot Spaces, Spark, and third-party coding agents.
>
> Code completions and next edit suggestions are not billed in AI credits.
> They remain unlimited for all paid plans.

모든 Copilot 기능이 AI credits를 쓰는 것은 아닙니다.
문서상 `code completions`와 `next edit suggestions`는
유료 요금제에서 AI credits로 청구되지 않고 계속 포함됩니다.
반대로 Copilot Chat, Copilot CLI, Copilot cloud agent, Spaces, Spark,
third-party coding agents 같은 기능은 AI credits를 사용할 수 있습니다.

저는 자동완성이 코드 작성 시 거슬려서 꺼두기 때문에 이점이라고 보긴 어렵습니다.
GitHub에서도 자동완성이 채팅만큼의 사용량이 적어서 비용을 청구하지 않는 것이라 추측합니다.

### 추가 사용량

> When your AI credits are exhausted, you can:
>
> - Set a budget for additional usage and pay extra to continue working
> - Wait until the next monthly cycle when your included usage resets
>
> Your additional usage budget is set in US dollars,
> and your usage is shown in GitHub AI Credits.
> GitHub AI Credits draw down your budget at a fixed rate:
> 1 AI credits = $0.01 USD, so a $10 budget covers 1,000 AI credits.

이 글에서 계산하는 금액은 예산을 열어두고 초과 사용을 계속 허용했을 때의 예상치입니다.
포함 credits를 다 썼다고 해서 무조건 그 금액이 청구된다고 단정하면 안 됩니다.

포함 AI credits를 모두 쓰면 추가 예산을 설정해 계속 사용할 수 있고,
예산을 설정하지 않으면 다음 월간 주기까지 사용이 제한될 수 있습니다.
따라서 중요한 것은 반드시 이만큼 청구된다는 것이 아니라
새 기준에서 내 사용량이 어느 정도 사용량으로 계산되어 빠르게 한계에 도달할 수 있는지 입니다.

## 사용량 리포트 받기

GitHub는 Copilot 사용량을 확인할 수 있는 리포트를 제공합니다.

사용량 리포트를 내려받기 위해서는 먼저 GitHub 개인 설정에서
`Billing and licensing` 하위의 `Premium request analytics` 화면으로 이동합니다.
[바로가기](https://github.com/settings/billing/premium_requests_usage)

![Premium request analytics](https://dl.dropboxusercontent.com/scl/fi/9bnl04tk6b6ur0da7o78i/github-01-premium-request-analytics.webp?rlkey=naeauv5f444c9ma9zuo8db397&raw=1)

`Get usage report` 버튼을 클릭하면 사용량 조회 기간을 지정할 수 있습니다.

리포트는 최대 31일 범위로 요청할 수 있어서, 저는 2026년 3월, 4월, 5월을 각각 선택했습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/yeptl8c86bmhqyfvcw0sb/github-02-get-usage-report.webp?rlkey=4ifmxyx33tl01oob487x80ojw&raw=1"
  alt="Get premium request usage report"
  max-width="600px"
  align="center" >}}

`Email me the report` 버튼을 클릭하면 몇 분 후 사용량 리포트가 이메일로 전달됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/x0s396mhaizcg9g6ytkoj/github-03-email-download-report.webp?rlkey=3ovgcy4sbjrse61tw7in2ksfb&raw=1"
  alt="Your usage report for minyeamer is ready"
  max-width="600px"
  align="center" >}}

`Download report` 버튼을 클릭하면 사용량 리포트가 CSV 형식으로 다운로드됩니다.

## 내 실제 사용량 분석

CSV 파일에는 기존 Premium request 기준 비용과 새로운 AI credits 기준 비용이 함께 들어 있었습니다.
제가 계산에 사용한 핵심 컬럼은 아래와 같습니다.

{{% data-table align-center="1,2" %}}
컬럼,의미
`quantity`,기존 Premium request 기준 사용량
`gross_amount`,기존 요청 단가 기준 금액
`discount_amount`,포함량으로 할인된 금액
`net_amount`,기존 기준 실제 청구 금액
`aic_quantity`,AI credits 사용량
`aic_gross_amount`,AI credits 기준 환산 금액
{{% /data-table %}}

기존 방식에서는 월 포함량 안에 들어가면 `net_amount`가 0으로 잡혔습니다.
실제로 3월부터 5월까지는 모두 추가 청구가 없었습니다.

하지만, `aic_gross_amount` 기준으로 보면 느낌이 완전히 달라집니다. 아래 표는 CSV를 월별로 합산한 결과입니다.

{{% data-table delimiter="|" align-center="1,2,3,4,5,6,7" %}}
월|Premium request 사용량|기존 기준 금액|기존 실제 청구|AI credits 사용량|AI credits 환산 금액|Pro 기준 총 예상
2026-03|232.07|$9.28|$0.00|18,852.01|$188.52|$183.52
2026-04|147.62|$5.86|$0.00|8,438.15|$84.38|$79.38
2026-05|215.93|$8.64|$0.00|12,430.05|$124.30|$119.30
{{% /data-table %}}

마지막 열은 Copilot Pro 월 구독료 $10과 포함 AI credits 1,500개, 즉 $15 상당을 기준으로 계산했습니다.

> `Pro 기준 총 예상 = 월 구독료 $10 + max(0, AI credits 환산 금액 - $15)`

그래서 3월은 `$10 + ($188.52 - $15) = $183.52`가 됩니다. 4월과 5월도 같은 방식으로 계산했습니다.

Copilot Pro 요금제에 포함된 Premium request 사용량이 300이므로, 저는 그것을 다 채우지도 않았는데도
실제 사용량이 이 정도가 된다면 6월부터는 보름은 커녕 3일도 온전히 사용하지 못할 것입니다.
심지어 저는 회사 계정으로도 Copilot Pro 요금제에 구독해 2개 계정을 돌려가며 사용하므로
제 실제 사용량은 Claude Code Max 20x에 버금가는 수준이었다는 것을 체감했습니다.

### 상위 플랜이면 해결될까

그렇다면 Pro+나 Max로 올리면 괜찮을까요.
같은 사용량을 각 플랜의 포함 credits로 다시 계산하면 아래처럼 보입니다.

{{% data-table delimiter="|" align-center="1,2,3,4,5" %}}
월|AI credits 환산 금액|Pro 예상 총액|Pro+ 예상 총액|Max 예상 총액
2026-03|$188.52|$183.52|$157.52|$100.00
2026-04|$84.38|$79.38|$53.38|$100.00
2026-05|$124.30|$119.30|$93.30|$100.00
{{% /data-table %}}

Pro+는 포함량이 $70 상당이라 Pro보다 확실히 낫습니다.
그래도 제 3월 사용량 기준으로는 월 $39 구독료에 초과분 $118.52가 더해져 $157.52가 됩니다.
Max는 포함량이 $200 상당이라 이 3개월 사용량에서는 초과분이 없지만, 구독료 자체가 $100입니다.

하지만, GitHub Copilot이 자체 AI 모델을 직접 제공하는 OpenAI Codex, Claude Code 등과
비교했을 떄 성능이 안좋다는 인식이 있고 실제로 컨텍스트 윈도우 등이 체감상 부족하다는 느낌을 받았습니다.

가장 큰 문제는, 사용량 기반 요금제는 매월마다 API 크레딧이 제공되는 개념인데,
이 크레딧이 1개월마다 초기화되기 때문에 다른 AI 코딩 에이전트와 비교했을 때
비용만 비싸고 성능은 안좋은 밑빠진 독이 되어버렸다는 점입니다.

### 어떤 모델이 비용을 만들었나

월별 합계만 보면 사용 패턴이 잘 보이지 않습니다.
그래서 CSV 파일에서 비용 비중이 컸던 모델을 같이 봤습니다.

{{% data-table delimiter="|" align-center="1,2,3" %}}
월|비용 비중이 컸던 모델|AI credits 환산 금액
2026-03|Claude Opus 4.6, Claude Sonnet 4.6|Opus $114.73, Sonnet $70.04
2026-04|Claude Sonnet 4.6, Claude Opus 4.6|Sonnet $35.00, Opus $33.22
2026-05|GPT-5.4, Gemini 3 Flash|GPT-5.4 $108.82, Gemini 3 Flash $9.49
{{% /data-table %}}

3월과 4월에는 Claude Sonnet/Opus 모델을 많이 썼고, 5월에는 GPT-5.4 비중이 압도적으로 컸습니다.
4월 중순부터 GitHub Copilot에서 Claude 모델의 컨텍스트 처리와 결과가 좋지 않았는데,
마침 컨텍스트 윈도우가 크게 좋아졌다는 GPT-5.4 모델이 Copilot에 추가된 시기와 겹쳐서
OpenAI 모델을 주로 사용하게 되었습니다.

기능 기획과 같은 넓은 범위의 작업에는 Claude Opus 또는 GPT-5.4와 같은 상위 모델을,
변수명 추천이나 커밋 메시지 추천과 같은 단순한 작업에는 Gemini 3 Flash 모델을 주로 사용했는데,
단순한 작업만으로도 월 $10 비용을 채우는 것을 보면 하위 모델로 바꾼다고 해결될 문제는 아닌 것 같습니다.

## Copilot 이탈 결정

GitHub Copilot의 갑작스런 변경은 고민할 여지도 없이 Copilot을 떠나야 한다는 결정을
내리게 만들었습니다.

여전히 Copilot의 VS Code 확장 프로그램으로서의 완성도는 가장 높다고 생각합니다.
파일 안에서 변경 전과 변경 후를 바로 보여주고,
`Keep`, `Undo` 버튼으로 결과를 빠르게 받아들이거나 되돌릴 수 있는 흐름은 정말 편리합니다.

![VS Code에서 Copilot 변경사항 검토](https://dl.dropboxusercontent.com/scl/fi/vjos5k4q1atpz0qbjwxp6/github-04-copilot-changes.webp?rlkey=1r0vencr0tqcu3kjl07fd6jpu&raw=1)

Copilot을 떠나야 한다는 것이 정말 안타깝지만, 15배나 증가한 비용을 감당하면서까지 이용할 여유는 안됩니다.
오히려 그동안 이정도의 비용을 부담해준 Microsoft에게 감사할 정도입니다.

Copilot의 요청 기반 요금제를 믿고 한 번에 프롬프트와 문맥을 전달하여 1시간, 2시간씩 돌아가는 작업을 시킨 것은
확실히 과도했습니다. 소비자 입장에서는 합리적인 사용법이었지만, AI 제공업체는 더 이상 이러한 사용 행태를 감당할 수 없습니다.

## 대안을 찾기

GitHub Copilot에 대한 미련을 완전히 내려두고 대안을 찾아보기 시작했습니다. 후보는 네 가지로 좁혔습니다.

{{% hint %}}
- OpenAI Codex
- Claude Code
- Gemini Code Assist
- NVIDIA NIM API
{{% /hint %}}

저는 VS Code 안에서 AI 코딩 에이전트를 사용하는 방식에 익숙합니다.
CLI가 아무리 강력해도, 제 기준에서는 에디터 안에서 파일을 보면서 대화하고 diff를 검토하는 흐름이 훨씬 중요합니다.

다만, 마지막 NVIDIA NIM API는 AI 코딩 에이전트가 아니라 API입니다.
무료로 제한 없는 수준의 한도를 제공하기 때문에 향후 코딩 에이전트를 직접 만들어서
무료로 이용해볼 수 있을 것을 기대하여 후보로 추가했습니다.

다음 글에서는 GitHub Copilot과 세 가지 AI 코딩 에이전트를 사용해보면서,
모델 성능보다는 **VS Code 확장 프로그램으로서 얼마나 편했는지**를 중심으로 비교합니다.
특히 구독 비용, 사용 가능한 모델, effort 설정, 변경사항 검토 방식까지 같이 보겠습니다.
