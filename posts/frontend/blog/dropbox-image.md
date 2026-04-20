---
title: "이미지를 Dropbox에 업로드하는 VS Code 확장 프로그램 만들기"
date: "2026-03-02T17:07:19+09:00"
layout: "post"
description: >
  Github 블로그에서 이미지를 삽입할 때마다 브라우저를 오가야 하는 불편함을 해소하기 위해
  Dropbox API를 활용한 VS Code 확장 프로그램을 바이브 코딩으로 개발했습니다.
  명령어 하나로 여러 이미지를 Dropbox에 업로드하고 마크다운 링크를 자동 삽입하며,
  ffmpeg으로 이미지 포맷 변환 및 크기 조정까지 처리하는 전체 개발 과정을 공유합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/pk4xy0ihcgwwxbk4vnt0e/dropbox-00-cover.webp?rlkey=d7u8bdntnh4c9au6148yw48e9&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/gjry70so67eg9ao9fssq5/dropbox-00-logo.webp?rlkey=5vac2tmon2zgkpw4zjhd2vl6r&raw=1"
categories: ["Frontend", "Blog"]
tags: ["VS Code", "VS Code 확장 프로그램", "드롭박스", "Dropbox API", "블로그 이미지 업로드", "마크다운 이미지", "TypeScript", "바이브 코딩", "ffmpeg", "Github 블로그"]
series: ["Hugo 테마 만들기"]
---

{{% hint info %}}
<i class="icon-magic"></i> **AI 요약 & 가이드**

Github 블로그에서 이미지를 삽입할 때마다 브라우저를 오가며 수동으로 업로드해야 하는 불편함을 해소하기 위해
Dropbox API를 활용한 VS Code 확장 프로그램을 바이브 코딩으로 개발했습니다.
마크다운 파일에서 명령어를 실행하면 이미지를 선택하고, Dropbox에 업로드하고, 마크다운 링크를 커서 위치에 자동 삽입하는 과정이
한 번에 처리됩니다. ffmpeg을 이용한 이미지 포맷 변환 및 리사이징 기능도 추가했으며, VS Code Marketplace에 배포까지 마쳤습니다.

- **[Dropbox API 설정하기](#dropbox-api-설정하기)**: 앱 생성, 권한 추가, 액세스 토큰 발급 방법
- **[VS Code 확장 프로그램 설계](#vs-code-확장-프로그램-설계)**: `package.json`, `extension.ts`, 명령어 콜백 함수 구조
- **[이미지 업로드 함수 정의하기](#이미지-업로드-함수-정의하기)**: Dropbox SDK 초기화, 파일 업로드, 공유 링크 생성 및 변환
- **[이미지 변환 함수 정의하기](#이미지-변환-함수-정의하기)**: ffmpeg으로 포맷 변환 및 최대 크기 제한
- **[확장 프로그램 배포하기](#확장-프로그램-배포하기)**: VSIX 파일 생성, Marketplace Publisher 등록 및 업로드
{{% /hint %}}

## 블로그 이미지 업로드의 불편함

Github 블로그 글을 작성하면서 가장 번거로웠던 작업 중 하나가 이미지 삽입이었습니다.
티스토리나 미디엄 같은 블로그 플랫폼의 경우 편집창에서 바로 이미지를 업로드할 수 있게 지원하지만,
그러한 편집창이 없는 Github 블로그에서는 다음과 같은 과정을 반복해야 했습니다.

{{% hint %}}
1. 이미지 호스팅 서비스(Dropbox, Imgur 등) 웹사이트에 접속
2. 수동으로 이미지 파일 업로드
3. 생성된 이미지 공유 URL 복사
4. 미리보기로 연결되는 공유 URL을 다운로드 URL로 변환
5. 에디터로 돌아와서 `![설명](URL)` 마크다운 형식으로 이미지 첨부
{{% /hint %}}

이미지 하나 넣기도 불편한데, 여러 개의 이미지를 삽입할 때는 이 과정을 계속 반복해야 했습니다.
작업 흐름이 끊기고, 브라우저와 VS Code 에디터를 오가면서 집중력이 흐트러졌습니다.
실제로 이러한 문제 때문에 과거 Github 블로그에서 다른 블로그 플랫폼으로 옮긴 경험도 있습니다.

## VS Code 확장 프로그램

이 불편함에 대한 해결책으로 생각한 것이 VS Code 확장 프로그램입니다.

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/k479on0o4k06rm9824hu1/dropbox-00-preview.gif?rlkey=e68aj559ulf8xudc6b0ko6t5g&raw=1"
  alt="Use dropbox-image-uploader for VS Code extension"
  caption="Dropbox Image Uploader - VS Code 확장 프로그램 동작 미리보기" >}}

VS Code를 사용하는 이유라고도 볼 수 있는 확장 프로그램은
VS Code 사용자 누구나가 개발환경을 개선하기 위해 에디터를 뜯어고칠 수 있는
커스터마이징 기능과 같은 것입니다. 개인적으로도
[괄호 쌍을 색상으로 구분](https://marketplace.visualstudio.com/items?itemName=BracketPairColorDLW.bracket-pair-color-dlw)한다든가
[괄호 안의 텍스트를 단축키로 선택](https://marketplace.visualstudio.com/items?itemName=chunsen.bracket-select)하는 등
다른 사용자가 만든 편리한 기능들을 설치해서 사용했습니다.

저는 이미지 호스팅 서비스로 드롭박스(Dropbox)를 사용하는데,
드롭박스에서 제공하는 API를 활용해서 이미지를 업로드하는 VS Code 확장 프로그램을
만들어보고자 합니다.

아쉽게도, 저는 VS Code 확장 프로그램을 만들어본 경험이 없기 때문에
AI의 도움을 받는 바이브 코딩으로 개발을 진행했습니다.
제가 이해하는 선에서 설명을 드리려 하지만, 코드 동작에 대한 설명이 부족할 수 있습니다.

## Dropbox API 설정하기

제가 Github 블로그로 다시 돌아오려고 했을 때,
이미지 업로드를 보통의 블로그 플랫폼 수준으로 편하게 만드는 것이 최우선 과제였습니다.

VS Code 확장 프로그램을 만들어보자는 것까지는 생각했지만,
구체적으로 어떤 이미지 호스팅 서비스를 사용할지는 정하지 않았습니다.
이러한 상황에서 제가 바라는 요소는 다음 3가지였습니다.

{{% hint %}}
1. 이미지 업로드 시 웹사이트를 거치지 않도록 API를 제공할 것
2. API를 사용하기 위해 HTTP 요청으로 API 키를 전달하는 수준의 단순한 인증을 요구할 것
3. **무료**로 이용할 수 있을 것
{{% /hint %}}

제가 알고 있는 서비스 중에 위 조건에 부합하는 건 **구글 드라이브**와 **드롭박스**였습니다.
구글 드라이브는 무료로 15GB 용량을 제공해주기 때문에 처음엔 구글 드라이브를 사용해 봤지만,
이미지 호스팅으로 사용하기엔 다소 불안정하여 차선책으로 드롭박스를 선택하게 되었습니다.

드롭박스는 무료 사용량이 2GB라서 이미지를 원본으로 업로드한다면
금방 용량이 소진될 수 있습니다. VS Code 확장 프로그램을 만들 때 이런 점도 고려해서
이미지 크기 변환 기능도 추가했습니다.

### Dropbox 앱 만들기

드롭박스 API를 사용하기 위해서는 **액세스 토큰**이 필요합니다.

액세스 토큰을 만들기 위해서는 [Dropbox App Console](https://www.dropbox.com/developers/apps)에
접속하여 새 앱을 만들어야 합니다.   
"Create app" 버튼을 누르고 다음과 같이 진행합니다.

![Dropbox - Create a new app on the DBX Platform](https://dl.dropboxusercontent.com/scl/fi/jjtm7b7pod122jcvnwm86/dropbox-01-create-app.webp?rlkey=atak2ckorsccc1iwc6zjz0l5h&raw=1)

앱 이름은 자유롭게 작성하는데, 다른 사용자가 사용한 명칭을 중복해서 쓸 수 없습니다.

### 권한 설정 및 액세스 토큰 발급

앱을 생성하면 바로 앱 설정 화면으로 이동됩니다.   
Permissions 탭으로 이동해서 이미지 업로드 시 필요한 권한을 추가해줍니다.

{{% hint %}}
1. `files.content.write`: 파일 업로드를 위해 필요
2. `sharing.write`: 공유 링크 생성을 위해 필요
{{% /hint %}}

![Dropbox - Permissions](https://dl.dropboxusercontent.com/scl/fi/94s9dkv85ykg0xfq0uhhp/dropbox-02-app-permissions.webp?rlkey=3jpn2ee2zuzs5zf7hsc0gxsp7&raw=1)

다시 Settings 탭으로 돌아가서 중간에 `OAuth 2` 섹션을 보면
`Generated access token` 이라는 항목이 있습니다.   
`Generate` 버튼을 클릭하면 액세스 토큰을 생성할 수 있습니다.
(이 토큰은 4시간 동안만 사용할 수 있습니다.)

![Dropbox - Generated access token](https://dl.dropboxusercontent.com/scl/fi/le8hvvjwdbeg02bsm3cn4/dropbox-03-access-token.webp?rlkey=dw3zhxcpgrdg9yf6gsitsv2hk&raw=1)

## VS Code 확장 프로그램 설계

드롭박스 API에 대해 이해하셨다면 본격적으로 VS Code 확장 프로그램을 만들어봅시다.

제가 정의한 확장 프로그램의 기능은 아래 2가지 입니다.

{{% hint %}}
1. **이미지 업로드**: 단일 또는 여러 개의 이미지를 업로드하고 마크다운 링크 삽입
2. **이미지 변환**: 이미지 업로드 전에 이미지 크기 또는 포맷을 변환
{{% /hint %}}

확장 프로그램의 기능을 구현하기 위한 기본적인 파일 구조는 다음과 같습니다.

```bash
dropbox-image-uploader/
├── src/
│   ├── extension.ts        # 확장 프로그램 진입점
│   ├── dropboxService.ts   # 드롭박스 API 통신
│   └── imageProcessor.ts   # 이미지 크기 및 포맷 변환
├── package.json            # 확장 프로그램 메타데이터
└── tsconfig.json           # TypeScript 컴파일 설정
```

`src/` 경로에 확장 프로그램의 기능을 TypeScript로 작성합니다.
2개의 기능은 각각의 `.ts` 파일로 정의했습니다.
확장 프로그램의 파일 구조에 대해 구체적으로 알아보고 싶으시다면
VS Code에서 제공하는 공식 문서
[Extension Anatomy](https://code.visualstudio.com/api/get-started/extension-anatomy)
를 참고해주시기 바랍니다.

### `package.json` - 설계도

`package.json` 은 VS Code가 확장 프로그램을 인식하고 로드하는데
필요한 모든 정보를 담고 있습니다.

```json
{
  "name": "dropbox-image-uploader",
  "displayName": "Dropbox Image Uploader",
  "version": "0.0.1",
  "engines": {
    "vscode": "^1.85.0"
  },
  "activationEvents": [
    "onLanguage:markdown"
  ],
  "contributes": {
    "commands": [
      {
        "command": "dropboxImageUploader.uploadImage",
        "title": "Upload Image to Dropbox",
        "category": "Dropbox"
      }
    ],
    "configuration": {
      "properties": {
      "dropboxImageUploader.accessToken": {
          "type": "string",
          "default": "",
          "description": "Dropbox App Console > OAuth 2 > Generated access token"
        }
      }
    }
  }
}
```

`package.json` 에는 다음과 같은 주요 항목들이 있습니다.

- `activationEvents`: 마크다운 `.md` 파일에서만 확장 프로그램 활성화
- `contributes.commands`: Command Palette 에 등록할 명령어
- `contributes.configuration`: 사용자 설정 항목 (Access Token 등)

그 외 `package.json` 항목들은 VS Code에서 안내하는 API 문서
[Extension Manifest](https://code.visualstudio.com/api/references/extension-manifest)
를 참고해주시기 바랍니다.

### `extension.ts` - 진입점

VS Code가 확장 프로그램을 활성화할 때 `activate()` 함수를 호출합니다.
여기서 명령어 ID와 실행할 함수를 전달합니다.

```typescript
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const command = 'dropboxImageUploader.uploadImage';   // 명령어 ID

  context.subscriptions.push(
    vscode.commands.registerCommand(command, uploadImagesViaDialog)
  );
}

async function uploadImagesViaDialog() {
  ...   // 실행할 함수
}
```

`extension.ts` 에서는 VS Code에서 제공하는 두 가지 메서드를 사용합니다.

- `vscode.commands.registerCommand()`: 명령어 ID와 실행할 함수 쌍을 전달해 명령어를 등록합니다.
- `context.subscriptions.push()`: 등록할 명령어 목록을 추가합니다.

### 명령어 콜백 함수 정의하기

`extension.ts` 에서 `uploadImagesViaDialog()` 함수는
사용자가 명령어를 실행하는 이벤트가 감지되었을 때 호출됩니다.
해당 함수는 사용자 설정을 읽고 이미지 파일을 입력받는 역할을 하며,
구체적인 이미지 업로드 동작은 `uploadAndInsertImages()` 함수에 위임합니다.

```typescript
async function uploadImagesViaDialog() {
  // 현재 파일이 마크다운 파일인지 확인
  const editor = vscode.window.activeTextEditor;
  if (!editor || editor.document.languageId !== 'markdown') {
    vscode.window.showWarningMessage('This command is only available in Markdown files.');
    return;
  }

  // 업로드 경로 설정 확인
  const config = vscode.workspace.getConfiguration('dropboxImageUploader');
  const useCustomPath = config.get<boolean>('useCustomPath', false);

  // 업로드 경로가 설정에 없으면 입력 상자를 열어 입력받기
  let targetFolder: string | undefined;
  if (!useCustomPath) {
    targetFolder = await vscode.window.showInputBox({...});
    if (!targetFolder) return;
  }

  // 이미지 파일 선택
  const fileUris = await vscode.window.showOpenDialog(...);
  if (fileUris?.length) {
    await uploadAndInsertImages(fileUris.map(uri => uri.fsPath), editor, targetFolder);
  }
}
```

`uploadAndInsertImages()` 함수는 앞에서 이미지 파일 선택 후,
크기 변환 → 업로드 → 공유 링크 생성 → 마크다운 링크 삽입에 이르는 전체 동작을 제어합니다.
이 중에서 링크 삽입을 제외한 나머지 동작은 `uploadImageToDropbox()` 함수에서 진행합니다.

```typescript
import { uploadImageToDropbox } from './dropboxService';

async function uploadAndInsertImages(filePaths: string[], editor: vscode.TextEditor, targetFolder?: string) {
  // 이미지 업로드 진행 상황 표시
  await vscode.window.withProgress({...},
    async (progress) => {
      const markdownLinks: string[] = [];

      // 이미지 파일 업로드 후 공유 링크 생성 → 마크다운 링크로 변환
      filePaths.forEach(filePath => {
        const sharedLink = await uploadImageToDropbox(filePath, targetFolder);
        const fileNameWithoutExt = path.basename(filePath, path.extname(filePath));
        markdownLinks.push(`![${fileNameWithoutExt}](${sharedLink})`);
      });

      if (markdownLinks.length > 0) {
        // 마크다운 링크가 있으면 현재 파일에 추가
        await editor.edit(editBuilder => {
          editBuilder.insert(editor.selection.active, markdownLinks.join('\n') + '\n');
        });
        // 작업 완료 메시지 알림
        vscode.window.showInformationMessage(...);
      }
    }
  );
}
```

입력 상자, 알림 등을 표시하기 위해 전달하는 옵션은 생략했습니다. Github에 업로드된
[`extension.ts` 파일](https://github.com/minyeamer/dropbox-image-uploader/blob/main/src/extension.ts)을
참고해주시기 바랍니다.

## 이미지 업로드 함수 정의하기

`dropboxService` 모듈에는 드롭박스 API를 사용하여 이미지를 업로드하는
구체적인 동작이 구현되어 있습니다.
진입점인 `extension.ts` 에서 호출하는 함수는 `uploadImageToDropbox()` 하나 뿐이지만,
이 함수는 여러 부분으로 나뉘어 있습니다.

```typescript
export async function uploadImageToDropbox(
  filePath: string,
  targetFolder?: string
): Promise<string> {
  ...
  return sharedLink
}
```

### Dropbox SDK 초기화

드롭박스 API 엔드포인트에 직접 POST 요청을 보내 인증하고 이미지를 업로드할 수 있지만,
이러한 기능을 직접 구현하는 것보다 더욱 간단한 방법이 있습니다.
드롭박스에서 제공하는 JavaScript SDK를 사용하는 것입니다.

{{< bookmark
  src="https://www.npmjs.com/package/dropbox"
  title="dropbox - npm"
  description="The Dropbox JavaScript SDK is a lightweight, promise based interface to the Dropbox v2 API that works in both nodejs and browser environments.. Latest version: 10.34.0, last published: 3 years ago. Start using dropbox in your project by running `npm i dropbox`. There are 242 other projects in the npm registry using dropbox."
  image="https://static-production.npmjs.com/338e4905a2684ca96e08c7780fc68412.png"
  fetch="false" >}}

드롭박스의 JavaScript SDK는 NPM을 통해 설치하고 다음과 같이 초기화할 수 있습니다.

```typescript
import { Dropbox } from 'dropbox';
import * as vscode from 'vscode';

function getDropboxClient(): Dropbox {
  const config = vscode.workspace.getConfiguration('dropboxImageUploader');
  accessToken = config.get<string>('accessToken');

  return new Dropbox({ accessToken: token, fetch: fetch });
}
```

액세스 토큰은 [권한 설정 및 액세스 토큰 발급](#권한-설정-및-액세스-토큰-발급)
문단을 따라 생성할 수 있습니다.
사용자가 이 토큰을 VS Code 설정에 입력하면, 확장 프로그램에서 사용자의 설정을
읽어 `Dropbox` 객체를 초기화할 때 전달합니다.
(`fetch()` 는 HTTP 요청을 위한 JavaScript의 내장 함수입니다.)

### 이미지 파일 업로드

드롭박스 SDK를 사용한 이미지 업로드 방식은 여러 가지가 있지만
가장 기본적인 `filesUpload` 메서드를 사용합니다.

```typescript
const dbx = getDropboxClient();

dbx.filesUpload({
  path: dropboxPath,        // 드롭박스 저장 경로 (파일명)
  contents: fileBuffer,     // 업로드할 파일 내용
  mode: { '.tag': 'add' },  // 추가(add), 덮어쓰기(overwrite) 등
  autorename: true,         // 동일한 파일이 있을 경우 업로드할 파일명 변경
  mute: false,              // 알림/미리보기 생성 비활성화 (true)
});
```

`filesUpload` 메서드의 주요 매개변수들은 주석으로 설명을 첨부했는데
다른 사용 가능한 매개변수 또는 더 자세한 설명을 알고싶으시다면
[Dropbox Node SDK](https://dropbox.github.io/dropbox-sdk-js/global.html#FilesUploadArg) 문서를 참고해주시기 바랍니다.

### 공유 링크 생성

`filesUpload` 메서드는 이미지를 업로드할 뿐이지, 블로그에서 사용가능한
공유 링크를 만들어주지는 않습니다.
업로드된 파일의 공유 링크를 조회하기 위해선 `sharingListSharedLinks()` 메서드를 사용합니다.

```typescript
async function createSharedLink(dropboxPath: string): Promise<string> {
  const dbx = getDropboxClient();

  const existingLinks = await dbx.sharingListSharedLinks({ 
    path: dropboxPath,
    direct_only: true
  });

  if (existingLinks.result.links.length > 0) {
    return existingLinks.result.links[0].url  // 공유 링크가 있으면 반환
  }
  ...
}
```

하지만, 파일을 업로드한다고 공유 링크가 자동으로 만들어지지 않습니다.
파일을 업로드한 직후라면 파일의 공유 링크를 먼저 생성하고 조회해야 합니다.
공유 링크를 생성하는 메서드는 `sharingCreateSharedLinkWithSettings()` 입니다.

```typescript
async function createSharedLink(dropboxPath: string): Promise<string> {
  ...
  const response = await dbx.sharingCreateSharedLinkWithSettings({
    path: dropboxPath,
    settings: {
      // 접근 권한: 전체 공개(public), 일부 공개(team_only), 비밀번호(password)
      requested_visibility: { '.tag': 'public' },
    },
  });
  return response.result.url;
}
```

불특정 다수가 보는 블로그 이미지 링크이므로 전체 공개해야 합니다.
공유 링크를 생성하면 누구나 볼 수 있는 링크가 반환됩니다.   
(편의 상 오류 처리는 제외하고 보여드립니다.)

하지만, 아래와 같이 조회한 공유 링크는 드롭박스 미리보기로 연결되는 링크일 뿐,
이미지 그 자체에 대한 주소가 아닙니다.

`https://www.dropbox.com/scl/fi/pk4xy0ihcgwwxbk4vnt0e/dropbox-00-cover.webp?rlkey=d7u8bdntnh4c9au6148yw48e9&st=eb8n7o4h&dl=0`

블로그에서 이미지를 표시하려면 이미지로 직접적으로 연결되는 다운로드 링크를 사용해야 합니다.
방법은 간단하게 도메인만 `www.dropbox.com` 에서 `dl.dropboxusercontent.com` 로 바꿔주면 됩니다.

```typescript
const sharedLink = (await createSharedLink(dropboxPath))
  .replace('www.dropbox.com', 'dl.dropboxusercontent.com')
  .replace('&dl=0', '&raw=1');
```

저는 추가로 이미지를 원본으로 표시하기 위해 `raw=1` 파라미터를 더했습니다.

## 이미지 변환 함수 정의하기

이미지 업로드 함수는 `filesUpload()` 메서드를 호출하여 이미지 파일을
드롭박스에 업로드하기 전에 이미지 크기 또는 포맷을 변환합니다.
이러한 변환 작업을 하는 함수가 `convertImage()` 입니다.

이 함수는 `imageProcessor` 모듈에서 정의합니다.
함수에 로컬 이미지 파일 경로, 최대 이미지 크기, 파일 포맷을 전달하면
요청사항에 맞게 이미지 파일을 변환하고 임시 파일로 저장합니다.

```typescript
export async function convertImage(
  inputPath: string,
  targetFormat: string,
  maxSize: number
): Promise<string> {
  ...
  return outputPath;
}
```

크기와 포맷은 사용자 설정에서 읽어옵니다. 둘 다 기본값은 빈 값인데,
값이 설정된 경우만 이미지 변환 함수를 호출합니다.

```typescript
const config = vscode.workspace.getConfiguration('dropboxImageUploader');
const imageFormat = config.get<string>('imageFormat', '');  // 변경할 포맷
const maxImageSize = config.get<number>('maxImageSize', 0); // 최대 크기

if (imageFormat || maxImageSize > 0) {
  processedFilePath = await convertImage(filePath, imageFormat, maxImageSize);
}
```

### ffmpeg 설치하기

이미지 변환은 TypeScript 코드로 구현하지 않고 컴퓨터에 설치된
[ffmpeg](https://ffmpeg.org/)을 사용합니다.
`convertImage()` 함수는 최대 이미지 크기 및 파일 포맷 파라미터로부터
ffmpeg 명령어를 조합하고 명령어를 호출할 뿐입니다.

ffmpeg 설치 방법은 OS마다 다르지만, 대표적으로 Mac에서는
홈브류(Homebrew) 패키지 관리자를 이용합니다.

```bash
brew install ffmpeg
```

윈도우라면 환경 변수까지 설정해야 할 수 있는데,
터미널에서 `ffmpeg -version` 명령어로 설치된 버전이
정상 출력되는지 확인하면 됩니다.

```bash
% ffmpeg -version

ffmpeg version 8.0.1 Copyright (c) 2000-2025 the FFmpeg developers
```

ffmpeg 설치까지 확인했다면
TypeScript 코드로 ffmpeg 명령어를 조합하는 과정을 진행합니다.

### ffmpeg 이미지 변환

먼저, 이미지 파일 경로(`inputPath`)와 변환된 이미지를 저장할 경로(`outputPath`)를
정의합니다.   
그리고, `-i` 옵션으로 이미지 파일 경로를 넣어서 입력 파일을 지정합니다.

```typescript
const inputExt = path.extname(inputPath);
const inputBasename = path.basename(inputPath, inputExt);
const outputExt = targetFormat ? `.${targetFormat}` : inputExt;
const outputPath = path.join(os.tmpdir(), `${inputBasename}${outputExt}`);

let ffmpegCmd = `ffmpeg -y -i "${inputPath}"`;
```

다음으로, 최대 이미지 크기(`maxSize`)가 설정된 경우 이미지 파일의 너비와 높이를 읽고,
두 값 중에서 큰 쪽이 `maxSize` 를 초과하지 않도록 제한합니다.
이미지 크기 조정 시 너비와 높이가 모두 동일 비율로 감소해야 이미지가 망가지지 않습니다.
TypeScript에서 이 비율을 굳이 계산하진 않고 ffmepg이 대신 처리합니다.

ffmpeg에서 이미지 크기, 즉 해상도를 변경하는 건 비디오 필터를 의미하는 `vf` 옵션의
`scale` 필터를 사용합니다.

```typescript
if (maxSize > 0) {
  const { width, height } = await getImageDimensions(inputPath);
  const maxDimension = Math.max(width, height);

  if (maxDimension > maxSize) {
    if (width > height) {
      ffmpegCmd += ` -vf "scale=${maxSize}:-1"`;
    } else {
      ffmpegCmd += ` -vf "scale=-1:${maxSize}"`;
    }
  }
}
```

이미지의 너비와 높이는 `ffprobe` 패키지 명령어를 통한 이미지 분석 결과로부터
추출할 수 있습니다.

```typescript
async function getImageDimensions(filePath: string): Promise<{ width: number; height: number }> {
  const { stdout } = await execAsync(
    `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 "${filePath}"`
  );
  const [width, height] = stdout.trim().split(',').map(Number);
  return { width, height };
}
```

이미지 확장자는 여러가지가 있지만, 일단 이 확장 프로그램은
제 사적 이용 목적으로 만들었기 때문에 3개의 확장자(webp, jpg, png)로의 변환만 지원합니다.

이미지 파일 포맷 변환은 비디오 코덱을 의미하는 `-c:v` 옵션과
비디오 품질을 의미하는 `-q:v` 옵션을 사용합니다.

```typescript
if (targetFormat) {
  const format = targetFormat.toLowerCase();
  if (format === 'webp') {
    ffmpegCmd += ` -c:v libwebp -q:v 90`;
  } else if (format === 'jpg') {
    ffmpegCmd += ` -c:v mjpeg -q:v 2`;
  } else if (format === 'png') {
    ffmpegCmd += ` -c:v png`;
  }
}
```

비디오 코덱 별로 품질 값 범위가 달라 코드로 제어하기엔 복잡하여 고정 품질을 적용했습니다.
- `libwebp` 코덱은 0 에서 100 사이 품질 범위를 가지며, 높을수록 고품질입니다.
- `mjpeg` 코덱은 1 에서 31 사이 품질 범위를 가지며, 낮을수록 고품질입니다.
- `png` 코덱은 무손실 압축이라서 `-q:v` 옵션을 사용하지 않습니다.

이미지 크기와 포맷을 지정했다면 마지막으로 출력 경로를 추가하고
ffmpeg 명령어를 실행합니다.

```typescript
ffmpegCmd += ` "${outputPath}"`;
await execAsync(ffmpegCmd);
```

정상적으로 변환됐다면 오류 없이 출력 경로에 변환된 이미지 파일이 만들어집니다.

## 이미지 업로드 함수 완성하기

이미지를 변환하고 업로드하는 `uploadImageToDropbox()` 함수의
각 부분을 작성했으니 이제 함수를 완성해봅시다.

```typescript
import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { convertImage, cleanupTempFile } from './imageProcessor';

export async function uploadImageToDropbox(filePath: string, targetFolder?: string): Promise<string> {
  const dbx = getDropboxClient();
  let processedFilePath = filePath;
  let isTempFile = false;

  try {
    // 파일 포맷 또는 최대 이미지 크기 설정 불러오기
    const config = vscode.workspace.getConfiguration('dropboxImageUploader');
    const imageFormat = config.get<string>('imageFormat', '');
    const maxImageSize = config.get<number>('maxImageSize', 0);

    // 파일 포맷 또는 최대 이미지 크기 설정이 있으면 이미지 변환
    if (imageFormat || maxImageSize > 0) {
      processedFilePath = await convertImage(filePath, imageFormat, maxImageSize);
      isTempFile = processedFilePath !== filePath;
    }

    // 원본 또는 변환된 이미지 파일을 읽기
    const fileBuffer = fs.readFileSync(processedFilePath);
    const fileName = path.basename(processedFilePath);
    const folder = targetFolder || getUploadPathFromConfig();
    const dropboxPath = `${folder}/${fileName}`;

    // 이미지 업로드
    await dbx.filesUpload({...});

    // 공유 링크 생성 후 반환
    const sharedLink = await createSharedLink(dropboxPath);
    return sharedLink.replace('www.dropbox.com', 'dl.dropboxusercontent.com').replace('&dl=0', '&raw=1');
  } catch (error: any) {
    ...
  } finally {
    // 이미지 변환 시 생성된 임시 파일 삭제
    if (isTempFile) {
      cleanupTempFile(processedFilePath);
      // 내부적으로 파일 존재 확인 후 fs.unlinkSync() 호출
    }
  }
}
```

이렇게 하여 이미지 파일 경로를 전달하면 드롭박스에 업로드하고 공유 링크를 반환하는
`uploadImageToDropbox()` 함수가 완성되었습니다.

## 확장 프로그램 사용하기

확장 프로그램을 사용하는 방법은 간단합니다.

1. **Command Palette 열기**: `Cmd + Shift + P` (Mac) / `Ctrl + Shift + P` (Win)
2. **"Upload Image to Dropbox" 입력**
3. **업로드 경로 입력**: 사용자 설정에 `Upload Path` 를 작성했다면 생략
4. **이미지 파일 선택**: 탐색기에서 이미지 파일을 여러 개 선택 가능
5. **자동으로 마크다운 링크 삽입 완료!**

Command Palette를 거치지 않고 키보드 단축키(`Cmd + Alt + U`)로
명령어를 실행하는 방법도 있습니다.

처음에 확장 프로그램의 동작을 보여드렸는데,
확장 프로그램의 내부 작동 원리를 보고 실제 동작을 다시 보시면 이해가 더 쉽게 되실겁니다.

![Use dropbox-image-uploader for VS Code extension](https://dl.dropboxusercontent.com/scl/fi/k479on0o4k06rm9824hu1/dropbox-00-preview.gif?rlkey=e68aj559ulf8xudc6b0ko6t5g&raw=1)

혹시 텍스트만으로 사용자 설정을 입력하는데 어려움을 겪는 분들이 계실 것 같아
제 설정도 공유드립니다.

저는 개발 과정을 설명하는 글을 주로 작성해서 제 화면을 캡쳐한 PNG 이미지를 원본으로 저장해 놓는데,
아무래도 용량이 크다보니 압축 효율이 좋은 WEBP 포맷 변환과 최대 1920px 크기 제한을 걸었습니다.
(설정에서 "dropbox"를 검색하면 관련 설정을 확인할 수 있습니다.)

![VS Code Settings](https://dl.dropboxusercontent.com/scl/fi/7i53xdjzlees4bqw33h7s/dropbox-06-vscode-settings.webp?rlkey=74byu8c2jllno2famgd89h3ys&raw=1)

## 확장 프로그램 배포하기

VS Code Marketplace에 확장 프로그램을 배포하는 방법은 두 가지입니다.

### 방법 1: 웹 UI에서 직접 업로드

가장 간단하고 확실한 방법입니다. Azure DevOps 설정 없이 바로 배포 가능합니다.

#### 1단계: VSIX 파일 생성

```bash
npm install
npm run compile
npx @vscode/vsce package --allow-missing-repository
```

프로젝트 루트 경로에서 명령어를 실행하면 `.vsix` 파일이 생성됩니다.

#### 2단계: Publisher 등록

1. [marketplace.visualstudio.com/manage](https://marketplace.visualstudio.com/manage) 접속
2. Microsoft 계정으로 로그인
3. **"Create publisher"** 클릭
4. Publisher ID 입력 (package.json의 `publisher` 값과 동일해야 함)
5. 이름, 설명 등 입력 후 생성

![VS Code | Marketplace - Create Pulbisher](https://dl.dropboxusercontent.com/scl/fi/urxj0mea3yr7utvu1wvjl/dropbox-04-create-publisher.webp?rlkey=ch1a5ashypdep1blz99p638lx&raw=1)

#### 3단계: VSIX 업로드

1. Publisher 대시보드에서 **"+ New extension"** 클릭
2. **"Visual Studio Code"** 선택
3. 생성된 `.vsix` 파일을 드래그 앤 드롭 또는 선택
4. **업로드 완료!**

![Manage Publishers & Extensions](https://dl.dropboxusercontent.com/scl/fi/1uuqefaux3v30tua8ltd7/dropbox-05-new-extension.webp?rlkey=el4wlkln4rj49onf8cdz4kl6h&raw=1)

### 방법 2: CLI로 배포

명령어 한 번으로 배포하는 방법입니다. 단, Azure DevOps 설정이 필요합니다.

#### 1단계: Azure DevOps에서 PAT 토큰 발급

1. [dev.azure.com](https://dev.azure.com) 접속
2. **"Start free"** 클릭하여 조직(Organization) 생성
3. 우측 상단 **사람 아이콘** → **Personal access tokens** 클릭
4. **"+ New Token"** 클릭
5. 설정:
   - **Name**: `vsce-publish`
   - **Organization**: `All accessible organizations`
   - **Expiration**: 원하는 기간
   - **Scopes**: `Custom defined` → **Marketplace** → **Manage** 체크
6. **Create** → 토큰 복사 (**다시 볼 수 없음!**)

저는 아쉽게도 새 계정으로 Azure DevOps 조직을 생성하는데 어려움이 있어서
이 과정은 진행하지 못했습니다.

#### 2단계: vsce 설치

```bash
npm install -g @vscode/vsce
```

#### 3단계: 배포

```bash
# 첫 배포
vsce publish -p <복사한_PAT_토큰>

# 버전 자동 증가 후 배포
vsce publish patch -p <PAT_토큰>   # 1.0.0 → 1.0.1
vsce publish minor -p <PAT_토큰>   # 1.0.0 → 1.1.0
vsce publish major -p <PAT_토큰>   # 1.0.0 → 2.0.0
```

## 마치며

VS Code 확장 프로그램 개발이 처음이었지만,
바이브 코딩 덕분에 확장 프로그램에 대한 이해없이
원하는 기능을 만들어 볼 수 있었습니다.
그리고, 이제 블로그 글을 작성하기 위해 AI가 작성한 코드를 분석하면서
확장 프로그램을 어떻게 개발하는지 이해할 수 있었습니다.

코드를 Github에 공개하고 VS Code Marketplace에 배포한 것은
현재 26년 3월 기준에서 불과 며칠되지 않았지만, 이 확장 프로그램 자체는
한 달도 전에 Github 블로그를 시작할 때부터 바이브 코딩으로 만들어서
사용하고 있었습니다.

Github 블로그를 작성하면서 가장 큰 걱정거리가 이미지를
어떻게 편하게 업로드 할 것인지 였는데,
이 확장 프로그램 덕분에 블로그 글 작성 시간의 많은 부분을
절약했습니다.

초기에는 마크다운 파일에 직접 이미지 파일을 드롭다운 하는 방식을
계획했지만 아쉽게도 VS Code에서 이미지를 드롭다운하면 새 창에서
이미지가 표시되는 기존의 동작을 대체하는 방법을 알 수 없어서
드래그 앤 드롭을 구현하지는 못했습니다.

혹시 비슷한 불편함을 느끼셨다면, 이 글이 도움이 되길 바랍니다.
전체 코드는 아래 GitHub 저장소에서 확인하실 수 있습니다.

{{< bookmark "https://github.com/minyeamer/dropbox-image-uploader" >}}

확장 프로그램은 VS Code Marketplace에 배포하였으며,
"Dropbox Image Uploader" 라고 검색하시면 확인 및 설치하실 수 있습니다.

{{< bookmark
  url="https://marketplace.visualstudio.com/items?itemName=minyeamer.dropbox-image-uploader"
  title="Dropbox Image Uploader - Visual Studio Marketplace"
  description="Extension for Visual Studio Code - Upload images to Dropbox and insert shared links into Markdown files"
  image="https://dl.dropboxusercontent.com/scl/fi/gjry70so67eg9ao9fssq5/dropbox-00-logo.webp?rlkey=5vac2tmon2zgkpw4zjhd2vl6r&raw=1"
  fetch="false" >}}

{{< series "Hugo 테마 만들기" >}}
