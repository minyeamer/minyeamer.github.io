---
title: "Airflow에 기여하기 - doc_md 마크다운 렌더링 개선 PR (#66809)"
date: "2026-05-18T01:52:47+09:00"
layout: "post"
description: >
  Apache Airflow UI의 doc_md 마크다운 렌더링을 개선한 PR #66809 기여 기록.
  ReactMarkdown 구조 분석부터 코드 블록, KaTeX 수식, Mermaid 다이어그램 렌더링 구현,
  static checks와 provider tests 실패 및 코드 리뷰에 대응하고, 최종 구조 정리까지 기술적으로 설명합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/8oxi6rw0kesl9l3egs78s/airflow-00-cover.webp?rlkey=6abx67jiweasmlwehj4o4gdle&raw=1"
categories: ["Data Engineering", "Apache Airflow"]
tags: ["Apache Airflow", "doc_md", "ReactMarkdown", "Markdown", "KaTeX", "Mermaid", "Pull Request", "오픈소스 기여", "UI 개선", "에어플로우", "리액트", "OSSCA"]
series: ["오픈소스 컨트리뷰션 아카데미"]
---

<style>
.content-cover, .screenshot-image { border: 3px solid var(--gray-200); }
.github-suggestion {
  margin: 1.25rem 0;
  border: 1px solid var(--gray-300);
  border-radius: 12px;
  overflow: hidden;
  background: var(--gray-50);
}
.github-suggestion__title {
  padding: 0.8rem 1rem;
  font-weight: 700;
  background: var(--gray-100);
  border-bottom: 1px solid var(--gray-300);
}
.github-suggestion__line {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  padding: 0.25rem 1rem;
  font-family: var(--font-family-mono);
  overflow-x: auto;
}
.github-suggestion__line code {
  white-space: pre;
  background: transparent;
}
.github-suggestion__line--remove {
  background: rgba(248, 81, 73, 0.12);
}
.github-suggestion__line--add {
  background: rgba(63, 185, 80, 0.14);
}
.github-suggestion__prefix {
  font-weight: 700;
  min-width: 1rem;
}
.github-suggestion__line--remove .github-suggestion__prefix {
  color: #b42318;
}
.github-suggestion__line--add .github-suggestion__prefix {
  color: #067647;
}
</style>

{{< series "오픈소스 컨트리뷰션 아카데미" >}}

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Apache Airflow UI의 `doc_md` 마크다운 렌더링을 개선한
PR [#66809](https://github.com/apache/airflow/pull/66809) 작업 기록입니다.
단순한 UI 개선으로 시작했지만, 실제로는 공용 `ReactMarkdown` 렌더러의 구조를 변경하면서
동시에 테스트 실패와 코드 리뷰에 대응하는 과정을 함께 이해할 수 있었습니다.

- **[배경과 목적](#배경과-목적)**: `doc_md` 문서 렌더링이 왜 어색하게 보였는지, 그리고 왜 이 문제를 직접 고치기로 했는지 정리합니다.
- **[초기 구현 - 마크다운 렌더링](#초기-구현---마크다운-렌더링)**: 수정 전 `ReactMarkdown.tsx` 동작을 분석하고, 수식과 Mermaid를 어떻게 구현했는지 정리합니다.
- **[테스트 실패](#테스트-실패)**: Static checks와 Provider tests 실패에 직면했을 때 어떻게 대응했는지 안내합니다.
- **[코드 리뷰 반영](#코드-리뷰-반영)**: 다른 사람들의 코드 리뷰를 반영하면서 수식 정책과 Mermaid 구조 등이 어떻게 바뀌었는지 정리합니다.
- **[최종 변경 사항](#최종-변경-사항)**: 최종적으로 어떤 파일이 추가/수정되었고 각 파일이 어떤 책임을 갖는지 표로 정리합니다.
{{% /hint %}}

이번 글은 OSSCA 체험형 과정의 2~3주차 동안 진행한 Apache Airflow PR [#66809](https://github.com/apache/airflow/pull/66809)
기여를 하면서 겪은 경험에 대한 기록입니다.

[1주차](/blog/ossca-airflow-i18n.md)에선 Airflow UI 내에서 한 문장을 한국어로 번역하고 제가 올린 PR이
Airflow 프로젝트에 Merge되는 경험을 했다면, 이번에는 제 필요성에 의해 실제 Airflow UI의 기능을 개선하는
PR을 올리게 되었습니다. Airflow UI의 내부적 구조가 어떻게 되어있는지 이해하지 못했던 제가 가벼운 마음으로 PR을 올리고,
리뷰를 받으면서 이해하고 깨달은 것을 중심으로 정리하려고 합니다.

{{< bookmark "https://github.com/apache/airflow/pull/66809" >}}

## 배경과 목적

저는 여러 웹사이트의 자료를 스크래핑하는 기능을 일정 간격마다 주기적으로 실행하기 위해 Airflow를 사용합니다.
Airflow는 crontab같은 단순 스케줄러의 기능을 넘어서 하나의 목적
_(예를 들어, 웹 스크래핑한 데이터를 파싱하고 DB에 적재하는 과정)_ 을 이루기 위해 세분화된 작업(Task) 간의
의존성을 관리하고 UI를 통해 모니터링하는 기능을 제공합니다.

이러한 Task 간의 연결 관계를 아래 이미지처럼 표현한 것이 DAG(Directed Acyclic Graph)입니다.

![DAGs - Airflow Documentation](https://dl.dropboxusercontent.com/scl/fi/ngxutq3ok3w4zin85ftt9/airflow-01-dag-example.webp?rlkey=5u21auwiiqf32ziksstmeu16r&raw=1)

일반적으로 함수를 정의할 때 내용이 길어지면서 과거에 작성한 함수가 무슨 기능을 하는건지 까먹지 않기 위해,
그리고 협업하는 다른 사람들에게 제가 함수를 만든 의도를 이해시키기 위해 주석을 작성합니다.
Airflow에서는 이와 마찬가지로 Dag 또는 Task 대한 설명을 적을 수 있는 `doc_md` 속성을 제공합니다.

```python
"""
### My great Dag
"""

import pendulum

dag = DAG(
    "my_dag",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
)
dag.doc_md = __doc__

t = BashOperator("foo", dag=dag)
t.doc_md = """\
#Title"
Here's a [url](www.airbnb.com)
"""
```

`doc_md` 속성은 단순한 코드 내에 적는 주석일 뿐 아니라, Airflow UI에서 마크다운 렌더링되어 사용자에게 표시됩니다.
하지만, 여기서 제가 겪은 문제점은 Airflow UI의 마크다운 렌더링 기능이 `인라인 코드` 표현을 지원하지 않는다는 것이었습니다.

예를 들어, "The \`\<code\>\` element is used for inline code." 문장을 `doc_md` 내용에 작성했다고 가정합시다.
이 마크다운 문장은 Airflow UI에서 아래 이미지처럼 렌더링됩니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/ue25mj2f1eeu822x2lykl/pr-66809-01-inline-code.webp?rlkey=dqbx0qv61glcbp97kb90dcj7x&raw=1"
  alt="The code element is used for inline code."
  max-width="691px"
  align="center" >}}

"The `<code>` element is used for inline code." 와 같이 한 문장으로 이어지는 것을 기대했지만,
실제로는 백틱(\`)으로 감싸진 `<code>` 부분이 하나의 문장을 3가지 요소로 구분해버리는 코드 블럭이 되었습니다.

저는 주석에 인라인 코드 표현을 꽤 자주 사용하는 편인데,
`doc_md`에는 이러한 문제로 백틱(\`) 대신에 홑따옴표(')로 인라인 코드를 표현해야 했습니다.
Airflow를 도커 이미지로 내려받아 사용하던 입장에서는 이를 개선할 방법을 알지 못했고
기능에 영향을 주는 요소가 아니라서 어쩔 수 없이 넘어갔습니다.
하지만, 이번에 Airflow에 기여하는 방법을 배우면서 이 기능을 가장 먼저 구현해야겠다고 다짐했습니다.

## 초기 구현 - 마크다운 렌더링

Airflow UI를 수정하고 PR을 올리기 위해 우선 Airflow 프로젝트의 main 브랜치를 Fork하여
개인 저장소로 복제하고 로컬에 내려받았습니다.
이후, PR을 올리기 위한 `ui/markdown-rendering` 브랜치를 만들어 코드 변경을 시작했습니다.

{{< bookmark "https://github.com/apache/airflow" >}}

### 구현 계획

초기 구현에서 넣고 싶었던 기능은 다음 4가지였습니다.
계획을 세우다보니 인라인 코드 외에도 Airflow UI의 마크다운 렌더링을
Hugo와 같은 블로그 수준으로 개선하고 싶은 욕심이 생겼습니다.

{{% hint %}}
1. 인라인 코드가 하나의 문장으로 연결되도록 개선하기
2. 코드 블록 스타일을 개선하고 언어 라벨과 복사 버튼을 추가하기
3. KaTeX 기반 수식 렌더링을 추가하기
4. Mermaid 다이어그램 렌더링을 추가하기
{{% /hint %}}

안타깝게도 전 웹 개발자도 아니고 리액트와 같은 프론트엔드 프레임워크에 대한 개념도 없어서
생성형 AI(GPT-5.4)에게 요청해 내가 원하는 기능의 구현을 요청했습니다.
그렇게 탄생한 첫 번째 커밋
[247d1f7](https://github.com/apache/airflow/pull/66809/changes/247d1f71e7f246c914d240ca902d9b9446752f5a)은
다음 파일들의 변경을 포함했습니다.

```bash
airflow-core/src/airflow/ui/
├── src/
│   ├── components/
│   │   ├─+ ReactMarkdown.test.tsx
│   │   ├── ReactMarkdown.tsx
│   │   └─+ ReactMarkdownBlocks.tsx
│   ├── utils/
│   │   ├─+ renderMermaid.ts
│   │   └── syntaxHighlighter.ts
│   └── main.tsx
├── package.json
└── pnpm-lock.yaml
```

기존에 마크다운 렌더링 기능이 구현된 파일은 `ReactMarkdown.tsx` 하나였고,
여기서 코드 블록의 하이라이트 스타일을 불러오는 `syntaxHighlighter.ts`을 참조하고 있었습니다.
생성형 AI는 코드 블록을 렌더링하는 부분을 `ReactMarkdownBlocks.tsx`라는 별도의 파일로 분리하고,
Mermaid 다이어그램을 렌더링하는 부분을 또 별도의 `renderMermaid.ts`로 만들었습니다.

변경 사항을 적용하면 실제 Airflow UI에서 다음 이미지와 같이 변경됩니다.

{{< columns >}}
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/sszkjvlqfdo4y068djh3a/pr-66809-02-doc-md-before.webp?rlkey=8lsxc1mdwsy4ta71g3hxnmup6&raw=1"
  alt="Dag Documentation - Before"
  caption="Dag Documentation - 수정 전 (라이트 모드)" >}}
<--->
{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/6xu6q9fa5vbdw65sgw8v6/pr-66809-03-doc-md-after.webp?rlkey=tbpxzd9mmb4id1qkm989xk3uh&raw=1"
  alt="Dag Documentation - After"
  caption="Dag Documentation - 수정 후 (라이트 모드)" >}}
{{< /columns >}}

### 변경 전 코드 분석

변경 전의 `ReactMarkdown.tsx`는 전형적인 `react-markdown` 래퍼였습니다.
여기서 인라인 코드(`code`)는 `createCodeComponent` 함수를 통해,
코드 블록(`pre`)은 단순한 블록 요소로 처리되었습니다.
`pre` 요소 안에는 `code` 요소가 있기 때문에 결국 인라인 코드와 코드 블록 모두 같은 함수로 처리합니다.
핵심 코드만 정리하면 아래와 같습니다.

```typescript
// src/components/ReactMarkdown.tsx

import { oneDark, oneLight, SyntaxHighlighter } from "src/utils/syntaxHighlighter";

const PreComponent = ({ children }: PropsWithChildren) => <Box my={3}>{children}</Box>;

const createCodeComponent =
	(style: typeof oneDark | typeof oneLight) =>
	({ children, className, inline }) => {
		if (inline) {
			return <Code display="inline" p={2}>{children}</Code>; // 인라인 코드 처리
		}

		const match = /language-(?<lang>\w+)/u.exec(className ?? "");
		const language = match?.groups?.lang; // 클래스명에서 언어 문자열을 추출
		let childString = children; // `children`이 배열이면 문자열로 합치는 if-else 구문 생략

		return (
			<SyntaxHighlighter language={language ?? "text"} PreTag="div" style={style} wrapLongLines>
				{childString.replace(/\n$/u, "")} // 코드 블록 처리
			</SyntaxHighlighter>
		);
	};

const ReactMarkdown = (props: Options) => {
  const { colorMode } = useColorMode();
  const style = colorMode === "dark" ? oneDark : oneLight; // 테마에 따라 `CSSProperties` 속성 선택

  const components = {
    code: createCodeComponent(style),
    pre: PreComponent,
  }
  // return <ReactMD .../>
}
```

`createCodeComponent` 함수는 구체적으로는, `CSSProperties` 타입에 해당하는
`oneDark` 또는 `oneLight` 요소를 전달받습니다. 여기서 자식 요소와 클래스명을 추출하고,
클래스명에선 추가로 언어 문자열을 추출해 `SyntaxHighlighter`에게 넘겨줍니다.

이어서 `SyntaxHighlighter`가 있는 `syntaxHighlighter.ts`의 내용을 살펴보았습니다.

```typescript
// src/utils/syntaxHighlighter.ts

import { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
import bash from "react-syntax-highlighter/dist/esm/languages/prism/bash";
import json from "react-syntax-highlighter/dist/esm/languages/prism/json";
import python from "react-syntax-highlighter/dist/esm/languages/prism/python";
import sql from "react-syntax-highlighter/dist/esm/languages/prism/sql";
import yaml from "react-syntax-highlighter/dist/esm/languages/prism/yaml";

// 하이라이트를 지원하는 모든 언어를 여기에 입력
SyntaxHighlighter.registerLanguage("python", python);
SyntaxHighlighter.registerLanguage("json", json);
SyntaxHighlighter.registerLanguage("yaml", yaml);
SyntaxHighlighter.registerLanguage("sql", sql);
SyntaxHighlighter.registerLanguage("bash", bash);

export { oneDark, oneLight } from "react-syntax-highlighter/dist/esm/styles/prism";

export { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";
```

`PrismLight`라는 하이라이팅 방식을 사용하면서 `python`, `json`, `yaml`, `sql`, `bash`
5가지의 언어에 대한 하이라이트만 가져와서 가볍고 효율적인 렌더링을 지원하고 있었습니다.
하지만, 저는 초기 구현 당시에 이러한 의도를 파악하지 못하고 Github Copilot의 리뷰를 그대로 받아들여
코드를 무겁게 하는 실수를 저질렀습니다. 이것은 추후 리뷰 반영 항목에서 설명하겠습니다.

### 서드파티 라이브러리 도입

초기 구현에서 수식과 Mermaid 렌더링을 구현하기 위해 4가지 서드파티 라이브러리를 도입했습니다.

{{% hint %}}
- `katex`: 수식 스타일과 렌더링 자산 제공
- `mermaid`: 코드 블록 안의 다이어그램 정의를 SVG로 렌더링
- `remark-math`: 마크다운 문자열에서 수식 문법을 파싱
- `rehype-katex`: 파싱된 수식 문법을 KaTeX HTML로 변환
{{% /hint %}}

이것은 생성형 AI의 판단이기도 했지만, 이러한 파서나 렌더러를 직접 구현하는 것은 제가 생각해도 복잡할 것이라
판단해 서드파티 도입을 수용했습니다. 요즘엔 공급망 공격으로 피해를 입었다는 사례도 있어서
서드파티 사용에는 다소 조심스럽지만, 그래도 Github 스타 수에 기반해 어느 정도 검증된 라이브러리인 것은 확인했고
프론트엔드에 문외한인 제가 건드리는 것보다는 서드파티에 의존하는 것이 더 안전하다 생각해 결정했습니다.

Airflow에서는 서드파티 도입 시 라이선스를 확인해야 했었는데 초기 구현에서는 이점을 간과하고
PR의 코멘트를 통해 인지했습니다.
다행히 위 라이브러리들은 모드 MIT 라이선스로 등록되어 있어서 특별히 문제될 건 없었습니다.

### 코드 블록 처리 개선

초기 구현에서 가장 중요한 설계 변화는 마크다운 파싱 시
`code` 와 `pre` 요소를 같은 경로에서 다루지 않는 것이었습니다.
`code` 요소는 `createCodeComponent` 함수 대신에 텍스트를
단순히 `<code>` 요소로 감싸는 `InlineCodeComponent`로 처리하고,
`pre` 요소는 Mermaid 처리를 포함한 `createPreComponent` 함수를 적용해 두 요소의 렌더링 방식을 바꿨습니다.

```typescript
// src/components/ReactMarkdown.tsx

import { MarkdownCodeBlock, MarkdownMermaid } from "./ReactMarkdownBlocks";

const InlineCodeComponent = ({ children }: PropsWithChildren) => <Code display="inline">{children}</Code>;

const createPreComponent =
  (style: SyntaxTheme, mermaidTheme: MermaidDiagramProps["theme"]) =>
  ({ children }: { readonly children?: ReactNode }) => {
    const [codeElement] = Children.toArray(children); // 항상 멀티-라인 코드 블록만 처리
    // language, childString 추출 등
    if (language === "mermaid") { // Mermaid 분기 처리
      return <MarkdownMermaid chart={childString} fallbackStyle={style} theme={mermaidTheme} />;
    } // 나머지는 코드 블록 처리
    return <MarkdownCodeBlock language={language} style={style} value={childString} />;
  };

const createMarkdownComponents = ({ mermaidTheme, style }: MarkdownRendererProps): Components => ({
  code: CodeComponent,
  pre: createPreComponent(style, mermaidTheme),
});

const ReactMarkdown = (props: Options) => {
  const { colorMode } = useColorMode();
  const style = colorMode === "dark" ? oneDark : oneLight;
  const mermaidTheme = colorMode === "dark" ? "dark" : "default";
  const components = createMarkdownComponents({ mermaidTheme, style });
  // return <Box><ReactMD .../></Box>
};
```

덕분에 인라인 코드와 멀티-라인 코드 블록 처리가 명확히 분류되었고,
코드 블록을 처리할 때 Mermaid 다이어그램을 분기 처리할 수 있게 되었습니다.
이제 코드 블록 처리가 아무리 복잡해져도 `ReactMarkdown.tsx`에서는 어떤 방식으로
코드 블록을 처리할지만 정해주면 되고, 실질적인 구현은 `ReactMarkdownBlocks.tsx`에서 이루어지게 됩니다.

`ReactMarkdownBlocks.tsx`는 HTML 요소의 구조를 정의하면서 각 요소의 속성을 적용해는 과정이 반복되어
코드로 담기엔 블로그 글이 길어져 생략합니다.
대신에, 코드 블록을 구현할 때 제가 의도한 기능 또는 스타일을 어떻게 구현했는지 간략히 설명드리겠습니다.

{{% hint %}}
- `SyntaxHighlighter`에 `customStyle` 속성 내에 `width: "100%"`를 적용해 전체 너비 적용
- `SyntaxHighlighter`를 감싸는 `MarkdownBlockFrame`를 정의하고 복사 버튼과 언어 라벨을 구현
   - 복사 버튼을 추가하기 위해 Airflow UI에서 이미 구현된 `LazyClipboard`요소를 가져와 `action` 속성으로 전달
   - 언어 라벨을 표시하기 위해 언어 문자열을 `label` 속성으로 전달
- `SyntaxHighlighter`에 `lineNumberStyle` 속성을 추가해 행 번호 표시
{{% /hint %}}

### Mermaid 렌더링 구현

Mermaid는 `renderMermaid.ts`에서 구현하지만 실질적인 다이어그램 생성은
서드파티 라이브러리 `mermaid`에 위임하기 때문에 코드는 단순합니다.
`mermaid.initialize` 함수로 Mermaid를 한 번 초기화하고 나면
`mermaid.render` 함수를 사용해 다이어그램 표현식(`chart`)을 SVG 형식으로 변환할 수 있습니다.

```typescript
// src/utils/renderMermaid.ts

import mermaid from "mermaid";

export const renderMermaidDiagram = async ({ chart, diagramId, theme }): Promise<string> => {
  initializeMermaid(theme); // mermaid.initialize({ securityLevel: "strict", startOnLoad: false, theme });
  const { svg } = await mermaid.render(diagramId, chart);

  return svg;
};
```

### 수식 렌더링 구현

마크다운 렌더링을 담당하는 `react-markdown` 라이브러리의 `ReactMD` 컴포넌트에
플러그인으로 `rehypeKatex`와 `remarkMath`를 전달하는 것으로 구현됩니다.
Mermaid와 마찬가지로 서드파티 라이브러리를 이용하기 때문에 코드는 단순합니다.

수식은 `ReactMarkdown.tsx`에서 

수식 지원도 마찬가지로 markdown 파이프라인 자체를 넓힌 작업이었습니다.
초기 구현에서는 가장 직선적인 방식으로 `remark-math` 와 `rehype-katex` 를 함께 붙이고,
`main.tsx` 에서 KaTeX CSS를 전역 import 했습니다.

```typescript
// src/components/ReactMarkdown.tsx

// import "katex/dist/katex.min.css";
import ReactMD from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";

const ReactMarkdown = (props: Options) => {
  // ...
  return (
    <Box css={markdownContentStyles}>
      <ReactMD
        components={components}
        {...props}
        rehypePlugins={[rehypeKatex]}
        remarkPlugins={[remarkGfm, remarkMath]}
        skipHtml
      />
    </Box>
  );
};
```

KaTex CSS 스타일 `katex.min.css`는 `main.tsx`에서 전역 import로 추가되었는데,
코드 리뷰를 통해 특정 상황에서만 사용하는 스타일을 전역 import로 호출하는건 불필요하다는 의견을 받아
lazy-load로 변경했습니다. 이것은 리뷰 반영 항목에서 다시 설명하겠습니다.

## 테스트 실패

처음 PR을 올린 뒤 바로 부딪힌 것은 코드 리뷰를 통한 개선점을 파악하는 것이 아니라, 다음 2개의 테스트 실패였습니다.

{{% hint danger %}}
1. CI image checks / Static checks
2. provider distributions tests / Compat 3.0.6:P3.10:
{{% /hint %}}

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/x4rcm7eldd8k6w1oxy5wj/pr-66809-04-failling-checks.webp?rlkey=io2ulospvszohpk66411ixv9s&raw=1"
  alt="Some checks were not successful"
  max-width="800px"
  align="center" >}}

### Static checks

Airflow는 코드 품질 기준을 만족하기 위해 정적 체크(Static checks)를 해야 합니다.
[Static code checks 문서](https://github.com/apache/airflow/blob/main/contributing-docs/08_static_code_checks.rst)를
참고하면 자세한 설명을 볼 수 있는데, `uv`를 통해 `prek` hook을 설치하면 간단하게 정적 체크를 할 수 있습니다.

```bash
uv tool install prek
```

`prek`은 Rust로 작성된 도구로, 기존 `pre-commit`을 대체하는 품질 검사기 입니다.
Rust로 작성되어 매우 빠르다고 안내되는데, 처음에 모르고 전체 파일 검사를 돌려서 10분 정도가 나와 의아했지만
나중에 변경된 파일만 특정해 `prek`을 실행하니 확실히 몇 초도 안되는 속도로 검사가 완료되었습니다.

`prek`은 설치 후 실행하기 전에 활성화해야 합니다. 그 전에 `xmllint`와 `golang`이 먼저 설치되어야 합니다.

```bash
# macOS 기준
brew install libxml2 golang
prek install
```

다음에 `prek`을 실행하려면 다음 명령어를 사용할 수 있습니다.

```bash
# 모든 파일 검사
prek --all-files

# 특정 파일 검사 (여러 개 인자 전달 가능)
prek run --files airflow-core/src/airflow/ui/src/components/ReactMarkdown.tsx
```

제가 `prek`을 실행했을 때, 일부 파일에서 마지막 줄 비워두기 또는 함수 매개변수 줄바꿈 등
코드 가독성 및 품질과 관련된 문제가 정리되었습니다.
이 변경 사항을 새로운 커밋으로 올리니까 정적 검사에 통과했습니다.
Airflow와 같은 대형 프로젝트에서는 이런 코드 품질 검사가 자동화되어 있다는 점이 꽤 인상적이었습니다.

### Provider tests

두 번째 실패는 더 당황스러웠습니다. 로컬에서 배포하는데 문제가 없었고 UI에서 작은 부분인
마크다운 렌더링만 건드렸다고 생각했지만 이러한 실패가 발생해 무엇이 문제인지 감이 안잡혔습니다.

코드 리뷰를 남겨주신 [@choo121600](https://github.com/choo121600)님께서
[Provider distributions 문서](https://github.com/apache/airflow/blob/main/contributing-docs/08_static_code_checks.rst)를
참고하라고 코멘트를 주셨고, 생성형 AI에게도 오류 로그를 전달하면서
이 문제를 터미널에서 해결하라고 지시했지만 해결할 수 없었습니다.

당시에 늦은 시간이라 마지막으로 할만한 수단으로,
`Update branch` 버튼을 눌러서 `ui/markdoown-rendering` 브랜치를 최신 `main` 브랜치와
Merge하는 커밋을 남기고 잠들었는데 아침에 확인하니 모든 테스트가 통과되어 있었습니다.
이 경험 덕분에 다음에 이런 테스트 실패가 발생하면 바로 `main` 브랜치의 최신 커밋과 Merge하여
즉시 실패를 해결할 수 있었습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/fsaulk1q3hw3uajf4b5sr/pr-66809-05-all-passed.webp?rlkey=6p0p0b80gfb7c2jt1ot49invq&raw=1"
  alt="All checks have passed"
  max-width="800px"
  align="center" >}}

## 코드 리뷰 반영

PR의 완성도를 끌어올린 건 다른 사람들이 남긴 코드 리뷰를 반영하면서부터 시작되었습니다.

초기 구현할 당시엔 기능만 구현되면 될 줄 알았지만 여러 사람들의 다양한 관점에서 비롯된 지적을 받으면서
제가 좁은 시점으로 코드를 보고 있었다는 것을 깨달았습니다.
이제부터는 코드 리뷰를 받고 수정하는 과정을 전달드리겠습니다.

### Github Copilot 리뷰

처음 PR을 올린 뒤 GitHub Copilot으로부터 7개의 자동 코멘트를 받았습니다.
초기 구현 때는 제가 코드를 잘 알고 있지 않았기에 그중 대부분은 실제로 수용할 만한 내용이라고 생각했습니다.
하지만, 이후 사람들의 리뷰를 받으면서 잘못 반영한 것이 있었다는 것을 깨닫고 몇 개를 되돌렸습니다.
Github Copilot의 제안은 아래와 같이 정리할 수 있습니다.

{{% hint %}}
1. 언어 문자열 추출 시 하이픈(-)으로 연결된 경우(예: language-objective-c)를 고려해
   정규식을 기존 `/language-(?<lang>\w+)/` 대신에 `/language-(?<lang>[-\w]+)/`로 변경
2. `renderMermaid.ts`에서 `mermaid` 라이브러리를 즉시 import하지 않고 동적 import로 변경
3. Mermaid는 `dangerouslySetInnerHTML`를 사용해 SVG를 생성하는데 여전히 XSS 공격에 취약하므로
   명시적인 검증 단계를 추가하거나 SVG에 스크립트가 포함되지 않는 테스트 추가
4. 코드 블록에서 복사 버튼에 대한 텍스트 속성(`title`, `aria-label`)에 i18n 번역 처리
5. Mermaid 블록에서도 복사 버튼에 대한 텍스트 속성(`title`, `aria-label`)에 i18n 번역 처리
6. `syntaxHighlighter.ts`에서 `PrismLight`에 명시적으로 언어를 등록하는 대신
   `react-syntax-highlighter`를 사용해 지원가능한 모든 언어에 하이라이트 적용
7. 테스트 파일에서 중복된 import를 제거
{{% /hint %}}

### @choo121600 리뷰

[@choo121600](https://github.com/choo121600)님께서 가장 먼저 짚어주신 건 다음 두 가지였습니다.

{{% hint %}}
1. `syntaxHighlighter.ts`에서 굳이 모든 언어를 지원할 필요가 있는가
2. 테스트 파일이 너무 장황한데 꼭 필요한 smoke test만 남길 수 없는가
{{% /hint %}}

이 중에서 첫 번째 리뷰의 원문은 다음과 같습니다.

<div class="github-suggestion">
  <div class="github-suggestion__title">Suggested change</div>
  <div class="github-suggestion__line github-suggestion__line--remove">
    <span class="github-suggestion__prefix">-</span>
    <code>export { default as SyntaxHighlighter } from "react-syntax-highlighter";</code>
  </div>
  <div class="github-suggestion__line github-suggestion__line--add">
    <span class="github-suggestion__prefix">+</span>
    <code>export { PrismLight as SyntaxHighlighter } from "react-syntax-highlighter";</code>
  </div>
</div>

> Could you share the reasoning behind switching from PrismLight
> with selective language registration to the default react-syntax-highlighter export here?
>
> This change may impact the initial bundle size,
> so I’d like to understand the rationale behind this decision :)

바로 앞에서 Github Copilot의 제안으로 `PrismLight`를 기본 `react-syntax-highlighter`로
대체했지만, 파이썬 프로젝트인 Airflow에서 그 모든 언어를 문서로 사용할 일은 없을 것이기에
초기 로드 시간을 줄이는데에 집중한 것이라 추측했습니다.
Github Copilot도 이런 문제점을 안내했지만, 개인 Hugo 블로그에서 모든 하이라이트 스타일을 불러오는게
대수롭지 않다고 생각하여 Airflow에도 이를 대입하는 실수를 저질렀습니다.
결국 이를 되돌리고, 앞으로 프로덕트 수준에서는 최대한 보수적으로 접근해야겠다고 느꼈습니다.

`syntaxHighlighter.ts`를 수정하면서 코드 블록에 한 가지 오점을 발견했습니다.
라이트 모드에서는 티가 안났는데 다크 모드에서 모서리가 둥근 사각형 프레임 안쪽 하단에 코드 블록의 회색 배경색이
채워지지 않은 부분이 눈에 띄었습니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/b4uhcgkrjkfw8jfy8jqx4/pr-66809-06-code-block.webp?rlkey=usot44y3x6xlynjj8dv08rqr6&raw=1"
  alt="Code block"
  max-width="691px"
  align="center" >}}

처음에는 바깥 프레임에 배경색을 넣으려고 했지만, 내부 `pre` 영역에 적용되는 `padding` 여백도 문제란 것을 발견하여
아래 2가지 변경 사항을 적용했습니다. 내부 프레임에 해당하는 `SyntaxHighlighter` 컴포넌트에는 여백을 없애고,
외부 프레임에 해당하는 `Box` 컴포넌트에는 `pre` 요소의 배경색을 포함한 스타일을 넣는 변경입니다.

<div class="github-suggestion">
  <div class="github-suggestion__title">&lt;Box ...&gt;</div>
  <div class="github-suggestion__line github-suggestion__line--add">
    <span class="github-suggestion__prefix">+</span>
    <code>css={{ ...style['pre[class*="language-"]'], borderRadius: 0, margin: 0 }}</code>
  </div>
</div>

<div class="github-suggestion">
  <div class="github-suggestion__title">&lt;SyntaxHighlighter ...&gt;</div>
  <div class="github-suggestion__line github-suggestion__line--remove">
    <span class="github-suggestion__prefix">-</span>
    <code>customStyle={{ borderRadius: 0, margin: 0, width: "max-content" }}</code>
  </div>
  <div class="github-suggestion__line github-suggestion__line--add">
    <span class="github-suggestion__prefix">+</span>
    <code>customStyle={{ background: "transparent", borderRadius: 0, margin: 0, padding: 0, width: "max-content" }}</code>
  </div>
</div>

다음으로 두 번째 리뷰의 원문은 다음과 같습니다.

> Personally, I think this part may not strictly need to be tested,
> but if we want to keep the tests, would it be okay to reduce them to a minimal set of smoke tests,
> such as the mermaid error fallback and basic math integration, and drop the rest?

테스트 코드 또한 제 의도를 거치지 않고 생성형 AI에 의해 만들어져서 검증하지 못했는데,
리뷰어에게 제가 해야할 검증 과정을 떠넘긴 것 같아 후회되는 순간이었습니다.
그럼에도, 이번 변경 제안 또한 제가 직접 코드를 수정하지 못하고 생성형 AI에게 의도를 전달하여
테스트 파일을 수정했습니다.
하루빨리 타입스크립트와 리액트에 대해 배워야 할 필요성을 느꼈습니다.

결론적으로, 코드 리뷰를 반영하여 테스트 파일에서는 다음 두 가지만 확인하도록 변경했습니다.

{{% hint %}}
1. 수식이 의도대로 렌더링되는가.
2. Mermaid 렌더링이 실패해도 fallback으로 다어어그램 표현식 원문을 표시하는가.
{{% /hint %}}

[@choo121600](https://github.com/choo121600)님께서 주신 2개의 리뷰는 검증 없이 생성형 AI로 작성한 코드를
올린 자신에 대해 뒤돌아보는 계기를 마련해주셨습니다. 오픈 소스의 다양한 기능에 기여하기 위해
제 전문 분야인 파이썬 개발에만 안주하지 말고 타입스크립트, 그리고 프론트엔드 영역에도 전문성을 터득할 필요성을 느꼈습니다.

### @parkhojeong 리뷰

[@parkhojeong](https://github.com/parkhojeong)님께서는 수식과 관련한 다음 4가지 리뷰를 남겨주셨습니다.

{{% hint %}}
1. `$` 기호를 인라인 수식 표현으로 사용할 경우 원래 목적인 달러 단위를 표현하는 문서에서
   의도치 않은 수식 렌더링이 적용될 수 있다는 문제 상황을 제기
2. 위 문제점으로 인해 이번 PR을 Dag Documentation에만 한정해서 적용할 수 있을지 제안
3. 서드파티 의존성은 `airflow-core/LICENSE`에 기록하는데, 이번에 추가한 4가지 라이브러리도
   이 파일에 포함하고 `airflow-core/3rd-party-licenses/` 경로에 각각의 라이선스를 넣어야 한다고 지적
4. KaTex CSS 스타일 `katex.min.css`를 전역 import하면 안된다고 지적
{{% /hint %}}

이 중에서 첫 번째 리뷰의 원문은 다음과 같습니다.

> This enables remarkMath with its default `singleDollarTextMath: true`,
> which changes how ordinary dollar text is parsed across all ReactMarkdown usages.
> For example, `Costs $5 and $10 today.` is parsed as inline math (`5 and `),
> so the dollar amounts render incorrectly.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/xncbikq916p6e7d5ksizf/pr-66809-07-math-check.webp?rlkey=zbxmo3un9yfvv25sq90juzw3z&raw=1"
  alt="Math rendering check"
  max-width="691px"
  align="center" >}}

마크다운을 작성할 때 인라인 수식은 `$` 기호로 표현하는 것이 당연하다 생각하여 인지하지 못했는데,
Airflow는 원래 수식을 지원하지 않아서 `$` 기호가 달러 화폐를 의미한다는 것을 간과했습니다.
이미지까지 제공해주셔서 보자마자 심각한 문제임을 인지했습니다.

제가 생각한 해결 방법은 다음 3가지였습니다.

{{% hint %}}
1. `$` 기호를 사용하면서 사용자에게 달러 기호를 escape하라고 안내한다.
2. 인라인 수식을 표현하는 기호를 `$` 대신에 `{{ math }}`와 같은 임의의 문법으로 대체
3. 인라인 수식 파싱을 비활성화한다.
{{% /hint %}}

제 선택은 3번이었습니다. 2번 선택지인 표준과 동떨어진 문법을 만드는건 마크다운 문서를 관리하는 입장에서
Airflow에서만 다른 문법을 사용해야 하는 불편함을 감수할 수 있을지 저조차도 동의하지 못했습니다.
1번 선택지는 가장 이상적인 대안이지만, 향후 필요성이 제기되면 커뮤니티 투표를 통해 반영하는게
좋을거라고 의견을 남겼습니다.

인라인 수식 파싱을 비활성화하는 방법은 생각보다 간단했습니다.
`remark-math` 플러그인에서 제공하는 [문서](https://unifiedjs.com/explore/package/remark-math/#fields)에서
`singleDollarTextMath: false` 옵션을 넣으면 비활성화됩니다.
또한, 수식(Equation) 표현에 해당하는 `$$` 기호가 문서 내에 있는지 확인하여
선택적으로 수식 파싱을 활성화하는 기능도 추가했습니다.

```typescript
// src/components/ReactMarkdown.tsx

const hasDisplayMath = (children: Options["children"]): boolean =>
  typeof children === "string" && children.includes("$$");

const shouldEnableMath = hasDisplayMath(children);

<ReactMD
  rehypePlugins={shouldEnableMath ? [rehypeKatex] : []}
  remarkPlugins={
    shouldEnableMath ? [remarkGfm, [remarkMath, { singleDollarTextMath: false }]] : [remarkGfm]
  }
>
</ReactMD>
```

다음으로 두 번째 리뷰의 원문은 다음과 같습니다.

> Could we scope these changes to Dag Documentation to limit the impact?
>
> This component is shared by Dag/Task docs, dashboard alerts, action note previews,
> Trigger Dag / FlexibleForm descriptions, and editable markdown previews.

이 의견을 받고 제가 수정하고 있는 마크다운 렌더링 기능이 Dag Documentation에 한정되지 않고
모든 마크다운 렌더링에 사용되고 있다는 것을 인지했습니다.
생각보다 제가 하는 작업의 범위가 넓었다는 것을 인식한 순간이었습니다.

그럼에도, 위에서 첫 번째 리뷰에 대한 해결책으로 적용한 "인라인 수식 파싱 비활성화"가
이번 두 번째 리뷰에서도 해결책이 될 수 있을거라 생각했습니다.
이미 `$` 기호 한 개에 대한 인라인 수식을 비활성화했고, `$$` 기호를 달러 화폐로 표현하는 경우는
일반적으로 없을 것이기에 이 변경 사항이 마크다운 렌더링 전반에서 의도치 않은 렌더링을 만들지 않을 것이라고
설명했습니다.

세 번째 리뷰의 원문은 다음과 같습니다.

> Should we update the third-party license notices
> for the new bundled UI dependencies added in this PR?
>
> For reference, `airflow-core/LICENSE` already lists bundled UI dependencies
> such as Chakra UI and hue, with their corresponding license texts
> under `airflow-core/3rd-party-licenses/`.

개인용 사이드 프로젝트하던 감각을 Airflow에 대입하여 서드파티 기능을 가벼운 마음으로 가져다 사용했는데
대규모 오픈소스 프로젝트에서는 의존성을 추가하는 순간 라이선스 고지가 필요하다는 것을 알게된 사례였습니다.
다행히 추가한 라이브러리들은 모두 MIT 라이선스로 등록되어 있어서 코드를 수정할 일은 없었습니다.

`airflow-core/LICENSE` 파일에 아래와 같이 4개 의존성에 대한 저장소 경로를 고지하고,
`airflow-core/3rd-party-licenses/` 경로 아래에 각 저장소에 있는 라이선스 파일을 복사해 옮겨넣엇습니다.

```
========================================================================
MIT licenses
========================================================================

    (MIT License) KaTeX v0.16.45 (https://katex.org)
    (MIT License) mermaid v11.14.0 (https://github.com/mermaid-js/mermaid)
    (MIT License) rehype-katex v7.0.1 (https://github.com/remarkjs/remark-math/tree/main/packages/rehype-katex)
    (MIT License) remark-math v6.0.0 (https://github.com/remarkjs/remark-math/tree/main/packages/remark-math)
```

마지막 네 번째 리뷰의 원문은 다음과 같습니다.

> Could we avoid loading KaTeX CSS globally?
> This makes KaTeX assets part of the app-wide cost, even on screens that never render math.

`main` 모듈에서 KaTex CSS 스타일인 `katex.min.css`를 전역 import하고 있었던 것이 문제였습니다.
수식을 항상 사용하는 것이 아니기 때문에 수식 파싱을 하는 순간에 동적으로 import하는 것이 효율적입니다.

결국 앞서 `shouldEnableMath` 값이 `true`인 경우에만 `katex/dist/katex.min.css`를 lazy-load 하도록
수정했습니다. 처음에는 `ReactMarkdown.tsx` 파일 안에서 KaTex를 불러오는 `katexStyleLoader`를 추가했는데,
테스트 과정에서 실패해서 이 기능만 `KatexStyleLoader.ts`라는 별도의 파일로 분리했습니다.

```typescript
// src/components/ReactMarkdown.tsx

useEffect(() => {
  if (shouldEnableMath) {
    void katexStyleLoader.load();
  }
}, [shouldEnableMath]);
```

[@parkhojeong](https://github.com/parkhojeong)님께서 주신 4개의 코드 리뷰는
PR을 개선하는데 특히나 도움을 주었습니다.
Airflow UI에서 마크다운 렌더링이 미치는 영향을 고려하게 되었고,
서드파티 라이브러리의 라이선스를 고려하여 올바르게 가져다 사용하는 방법도 배웠습니다.
가장 중요했던 건, 인라인 수식 파싱을 활성화한 채로 PR을 반영했을 때
잠재적으로 발생할 문제점을 미연에 방지할 수 있었다는데서 큰 도움을 받았습니다.

### @bbovenzi 리뷰

며칠 후 [@bbovenzi](https://github.com/bbovenzi)님께서
Airflow 3.3.0 milestone에 이 PR을 올리면서
Mermaid 관련한 requested changes를 남겨주셨습니다.
이와 관련된 6가지 리뷰가 있었지만, 사소한 수정 요청을 제외한 핵심 리뷰 하나만 전달드리겠습니다.

> We should really change the renderMermaid into a context provider.
>
> Elsewhere please have your AI do another pass at simplifying the code.
> There's a lot of verbosity thats hard to follow.

> We should make this into a react context provider and move it to `src/context`.
> Then we only need to initialize mermaid theme once for anywhere we use it,
> theme updates exist in the react lifecycle and we can manage
> the `initializedTheme` as a real state instead of a mutable variable.

[@bbovenzi](https://github.com/bbovenzi)님의 요구는
`utils/renderMermaid.ts`의 Mermaid 다이어그램을 그리는 기능을
`src/context` 경로 아래에 context provider로 옮기라는 것이었습니다.
리뷰어 관점에서 느낀 문제점을 다음 한 문장으로 이해했습니다.

> Mermaid 코드 블록을 렌더링하는 `MarkdownMermaid`가 `renderMermaid` 함수를 직접 호출하는 구조라,
> React lifecycle과 동떨어진 mutable variable로 보였다.

context provider가 무엇인지 완벽히 이해하지는 못했지만,
리액트의 관점에서 Props를 일일이 넘겨주지 않아도 트리 안의 모든 하위 컴포넌트가
특정 데이터에 쉽게 접근할 수 있게 하는 전역 요소의 역할을 하는 것이라는 설명을 들으니
어렴풋이 이해가 되었습니다. Mermaid는 한 번만 초기화하면 되니까 이 제안이 타당해보였습니다.

그래서 최종적으로 `utils/renderMermaid.ts` 모듈을 `src/context/mermaid/` 경로 아래에
다음 4가지 파일로 나눠서 구성했습니다.

```bash
airflow-core/src/airflow/ui/
└── src/context/mermaid/
    ├── Context.ts
    ├── index.ts
    ├── MermaidProvider.tsx
    └── useMermaid.ts
```

또한, `main.tsx`의 트리 구조 사이에 `<MermaidProvider>`를 끼워넣었습니다.

```typescript
createRoot(document.querySelector("#root") as HTMLDivElement).render(
  <StrictMode>
    <I18nextProvider i18n={i18n}>
      <QueryClientProvider client={client}>
        <ChakraCustomProvider>
          <ColorModeProvider>
            <MermaidProvider> // << 여기
              <TimezoneProvider>
                <RouterProvider router={router} />
              </TimezoneProvider>
            </MermaidProvider> // << 여기
          </ColorModeProvider>
        </ChakraCustomProvider>
      </QueryClientProvider>
    </I18nextProvider>
  </StrictMode>,
);
```

여전히 완벽하게 이해하진 못했지만, [@bbovenzi](https://github.com/bbovenzi)님은
마크다운 렌더링 코드가 리액트스럽게 작성되어야 한다는 것을 알려주신 것 같습니다.

## 최종 변경 사항

최종적으로 이 PR은 아래 파일을 수정하거나 추가했습니다.

```bash
airflow-core/
├── 3rd-party-licenses/
│   ├─+ LICENSE-katex.txt
│   ├─+ LICENSE-mermaid.txt
│   ├─+ LICENSE-rehype-katex.txt
│   └─+ LICENSE-remark-math.txt
├── src/airflow/ui/
│   ├── src/
│   │   ├── components/
│   │   │   ├─+ KatexStyleLoader.ts
│   │   │   ├─+ ReactMarkdown.test.tsx
│   │   │   ├── ReactMarkdown.tsx
│   │   │   └─+ ReactMarkdownBlocks.tsx
│   │   ├─+ context/mermaid/
│   │   │   ├─+ Context.ts
│   │   │   ├─+ index.ts
│   │   │   ├─+ MermaidProvider.tsx
│   │   │   └─+ useMermaid.ts
│   │   └── utils/
│   │       └── syntaxHighlighter.ts
│   ├── main.tsx
│   ├── package.json
│   └── pnpm-lock.yaml
└── LICENSE
```

주요 파일들의 역할과 책임을 아래 표로 정리해볼 수 있습니다.

| 파일 | 역할과 책임 |
| --- | --- |
| `ReactMarkdown.tsx` | 인라인 코드와 코드 블록 분리, 수식 사용 여부 판단, KaTeX lazy-load, Mermaid 분기 |
| `ReactMarkdownBlocks.tsx` | 복사 버튼, 행 번호 등을 포함한 코드 블록 렌더링 |
| `KatexStyleLoader.ts` | 수식이 필요한 경우에만 KaTeX CSS를 동적으로 로드 |
| `src/context/mermaid/*` | Mermaid 동적 import, theme 초기화, `useMermaid()` 제공 |
| `syntaxHighlighter.ts` | `PrismLight` 기반 5개 언어만 명시적으로 등록 |
| `ReactMarkdown.test.tsx` |수식 통합 테스트와 Mermaid fallback 중심의 smoke test |

처음에는 단순히 `doc_md` 속성과 연결된 Dag Documentation을 보강하는
작은 개선으로 시작했지만, 최종적으로는 공유된 마크다운 렌더러를 수정하면서 전역 파일에까지
영향을 주는 방향으로 확대되었습니다.

이 글을 쓰는 시점 기준으로 PR은 아직 열려 있고, Airflow 3.3.0 milestone에 올라간 상태에서
maintainer review queue에 들어가 있습니다.
진행 상황이 업데이트됨에 따라 글의 내용이 변경될 수 있습니다.

## 배운 점

이번 PR은 기능 구현 자체도 재미있었지만, 그보다 더 오래 남을 교훈을 몇 가지 줬습니다.

첫째, UI에 대한 PR이라고 해서 UI만 보면 된다고 생각하면 안 됩니다.
Airflow처럼 대형 프로젝트에서는 코드 품질을 고려하면서 각종 테스트에 통과하고,
서드파티 라이브러리 사용 시 라이선스를 고지하는 등 직접 수정한 파일 바깥에서의 역할도 고려해야 합니다.

둘째, 공유 컴포넌트를 손대는 순간 문제의 성격이 달라집니다. 처음엔 `doc_md` 전용 개선처럼 보였던 작업이
실제로는 Airflow UI 전반의 마크다운 렌더링 정책을 바꾸는 일이었습니다.
그래서 수식 문법 하나를 켤지 끌지, CSS를 전역으로 가져올지 lazy-load 할지 같은 판단이 더 중요해졌습니다.

셋째, 생성형 AI를 사용해도 첫 번째 리뷰어는 결국 작성자 본인입니다.
이번 PR에서 가장 크게 배운 점도 이 부분입니다. AI는 빠르게 초안을 만들고 가능성을 넓혀주지만,
리뷰어의 스트레스를 줄이기 위해서는 제가 먼저 코드를 충분히 검수하고, 왜 이렇게 바꿨는지 설명할 수 있어야 합니다.

이번 Airflow PR은 작은 UI 개선에서 출발했지만,
결국 마크다운 렌더링 기능, 테스트, 리뷰 문화, 의존성 관리, 그리고 생성형 AI 사용 태도까지 함께 배우게 만든 작업이었습니다.
그래서 이 PR은 결과물보다 과정이 더 많이 남는 작업으로 기억될 것 같습니다.
