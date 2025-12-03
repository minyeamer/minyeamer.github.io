---
title: "[Python] uv 프로젝트 구성하고 배포하기"
date: "2025-07-23T00:47:11+09:00"
layout: "post"
description: >
  uv를 활용한 Python 프로젝트 구성 및 배포 가이드.
  Rust 기반 고속 패키지 관리자로 프로젝트 초기화, 가상환경 생성, 의존성 추가부터 PyPI 배포까지 단계별로 안내합니다.
  pip보다 빠른 uv로 효율적인 개발 환경을 구축하세요.
cover: "https://dl.dropboxusercontent.com/scl/fi/jj13nbquunpa7gfeok7qf/uv-00-cover.png?rlkey=fwjnzqzt94gdmu25brus4cwfa&st=escdsoau&dl=0"
categories: ["Project", "Tools"]
tags: ["uv", "Python", "프로젝트 관리", "가상환경", "PyPI", "배포", "패키지 관리", "Rust", "Python 패키지"]
---

Python으로 새로운 프로젝트를 시작하려고 하는데 uv가 프로젝트 관리에 좋다는 얘기를 들어서 어떻게 활용할 수 있을지 찾아보았습니다.
단순히 프로젝트 의존성을 빠르게 설치해줄 뿐 아니라 가상환경과 PyPI 배포까지 지원해줘서 사용해보려고 합니다.

## uv

{{< bookmark "https://github.com/astral-sh/uv" >}}

uv는 Rust로 작성된 매우 빠른 Python 패키지 및 프로젝트 관리자라고 설명합니다.
Rust 기반으로 만들어져서 그런지 `pip` 나 `poetry` 와 비교했을 때 굉장히 빠른 속도를 보여줍니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/nw5qz64i85snrbm7ocir9/uv-01-fast.webp?rlkey=gwy75efcl9clbyzdenfq2z8eb&dl=0"
  alt="uv 0.06s, poetry 0.99s, pdm 1.90s, pip-sync 4.63s"
  max-width="691px"
  align="center" >}}

## 설치하기

설치 스크립트를 내려받아 설치할 수 있습니다.

```bash
# macOS 또는 Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

또는, 간단하게 PyPI를 통하거나 맥에서는 brew를 통해 설치할 수 있습니다.

```bash
pip install uv
```

```bash
brew install uv
```

설치한 후 버전을 조회하여 정상적으로 설치되었는지 확인할 수 있습니다.

```bash
% uv --version
uv 0.8.0 (Homebrew 2025-07-17)
```

## 프로젝트 시작하기

`uv init` 명령어를 통해 기본적인 프로젝트 구조를 생성할 수 있습니다.
프로젝트명은 "linkmerce", 파이썬 버전은 3.10으로 설정하여 프로젝트를 시작했습니다.

```bash
% uv init linkmerce --python 3.10
Initialized project `linkmerce` at `{$root}/linkmerce`
```

`uv init` 명령어를 통해 생성되는 프로젝트 구조는 아래와 같습니다.

```
./
├── .git/
├── .gitignore
├── .python-version
├── main.py
├── README.md
└── pyproject.toml
```

이 중에서 `pyproject.toml` 파일은 프로젝트명 또는 패키지 의존성과 같은 메타데이터를 명시하는 설정 파일입니다.
프로젝트를 초기화하면서 만들어진 `pyproject.toml` 의 내용을 살펴보면 아래와 같습니다.

```
[project]
name = "linkmerce"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []
```

초기 버전은 "0.1.0"으로 권장하고, 앞에서 설정한 파이썬 3.10 버전이 최소 요구사항으로 명시되어 있습니다.

## 가상환경 생성하기

`uv venv` 명령어를 통해 `.venv/` 위치에 가상환경을 생성할 수 있습니다.
`--name` 옵션을 주어 가상환경 이름을 변경할 수 있습니다.

```bash
% uv venv --python 3.10
Using CPython 3.10.18
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

가상환경 실행은 출력 결과에서 설명하듯이 `source .venv/bin/activate` 명령어를 입력하면 됩니다.

## 의존성 추가하기

`uv add` 명령어를 통해 패키지 의존성을 설치할 수 있습니다.
개발할 때만 사용하고 배포할 때는 활용하지 않을 경우 `--dev` 옵션을 추가할 수 있습니다.

의존성을 고려하지 않고 가상환경에만 패키지를 설치하고 싶은 경우엔 `uv pip install` 명령어를 사용할 수 있습니다.

```bash
% uv add requests
Using CPython 3.10.18
Creating virtual environment at: .venv
Resolved 6 packages in 158ms
Prepared 5 packages in 101ms
Installed 5 packages in 5ms
 + certifi==2025.7.14
 + charset-normalizer==3.4.2
 + idna==3.10
 + requests==2.32.4
 + urllib3==2.5.0
```

가벼운 패키지이긴 하지만 `pip` 로 설치했을 때 대비해서 훨씬 빠른 속도를 체감합니다.
`uv add` 명령어로 패키지 의존성을 설치하면 `pyproject.toml` 설정 파일에 자동으로 의존성이 추가됩니다.

```bash
[project]
name = "linkmerce"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.32.4",
]
```

또한, 동시에 생성되는 `uv.lock` 파일에는 패키지 의존성에 대한 바이너리 경로가 추가되어 있습니다.
의존성의 버전을 정확히 잠가버리기 때문에 다른 환경에서도 일관된 개발 및 배포 환경을 유지할 수 있습니다.

```bash
version = 1
revision = 2
requires-python = ">=3.10"

...

[[package]]
name = "linkmerce"
version = "0.1.0"
source = { virtual = "." }
dependencies = [
    { name = "requests" },
]

[package.metadata]
requires-dist = [{ name = "requests", specifier = ">=2.32.4" }]

[[package]]
name = "requests"
version = "2.32.4"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    { name = "certifi" },
    { name = "charset-normalizer" },
    { name = "idna" },
    { name = "urllib3" },
]
sdist = { url = "https://files.pythonhosted.org/packages/e1/0a/929373653770d8a0d7ea76c37de6e41f11eb07559b103b1c02cafb3f7cf8/requests-2.32.4.tar.gz", hash = "sha256:27d0316682c8a29834d3264820024b62a36942083d52caf2f14c0591336d3422", size = 135258, upload-time = "2025-06-09T16:43:07.34Z" }
wheels = [
    { url = "https://files.pythonhosted.org/packages/7c/e4/56027c4a6b4ae70ca9de302488c5ca95ad4a39e190093d6c1a8ace08341b/requests-2.32.4-py3-none-any.whl", hash = "sha256:27babd3cda2a6d50b30443204ee89830707d396671944c998b5975b031ac2b2c", size = 64847, upload-time = "2025-06-09T16:43:05.728Z" },
]
```

## 패키지 배포하기

### 프로젝트 구성하기

패키지를 배포하기에 앞서 프로젝트와 관련된 폴더를 생성하고 간단한 모듈을 추가했습니다.

```bash
./
├── .git/
├── src/
│   └── linkmerce/
│       ├── auth/
│       ├── collect/
│       ├── parse/
│       └── utils/
├── .gitignore
├── .python-version
├── main.py
├── README.md
├── pyproject.toml
└── uv.lock
```

### 패키지 빌드하기

`twine` 으로 패키지를 빌드할 때는 패키지 루트 경로를 변경하는 기능이 없어서
프로젝트 명칭의 폴더 아래에 패키지를 놓아야 했던 것으로 기억합니다.

`uv build` 명령어로 패키지를 빌드할 때는 `pyproject.toml` 설정 파일에서
`module-root` 값에 루트 경로를 지정할 수 있습니다.
해당 값을 명시하지 않으면 기본 루트 경로로 `src/` 가 적용되고 이는 uv에서 권장하는 사항입니다.

```bash
[build-system]
requires = ["uv_build>=0.8.0,<0.9.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "linkmerce"
module-root = "src"
```

`uv build` 와 관련한 자세한 내용은 [공식 문서](https://docs.astral.sh/uv/concepts/build-backend/)를 참고할 수 있습니다.

`uv build` 명령어로 패키지를 빌드하면 `dist/` 경로에 `.whl` 파일이 생성됩니다.

```bash
 % uv build
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built dist/linkmerce-0.1.0.tar.gz
Successfully built dist/linkmerce-0.1.0-py3-none-any.whl
```

### PyPI에 배포하기

PyPI에 배포하기 전에 먼저 API 토큰을 생성해야 합니다.
자세한 내용은 [안내 문서](https://pypi.org/help/#apitoken)를 참고할 수도 있습니다.

과거에 아래와 같이 PyPI에 패키지를 등록한 적이 있는데, 이번에 새로운 패키지를 등록해봅니다.

![PyPI > Your projects (2)](https://dl.dropboxusercontent.com/scl/fi/5g23hk24yl9rtn1o5r1h8/uv-02-pypi-list.webp?rlkey=laccd47zg8gr644ach7uke5iy&dl=0)

Account settings 페이지의 API tokens 항목에서 API 토큰을 발급받을 수 있습니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/wfto4binkivlk9qcdwp4d/uv-03-pypi-token.webp?rlkey=jiwgu55kust02dpigbvxxx22i&dl=0"
  alt="API tokens > Name = minyeamer, Scope = All projects"
  max-width="691px"
  align="center" >}}

API 토큰은 `pypi-*` 형식을 가지는데, 해당 토큰 값을 `uv publish` 명령어로
배포할 때 추가하면 PyPI 인증을 처리하고 PyPI에 패키지를 배포할 수 있습니다.

```bash
% uv publish --token pypi-*
Publishing 2 files https://upload.pypi.org/legacy/
Uploading linkmerce-0.1.0-py3-none-any.whl (7.8KiB)
Uploading linkmerce-0.1.0.tar.gz (5.5KiB)
```

PyPI 프로젝트 페이지를 확인해보면 방금 배포한 패키지가 올라온 것을 볼 수 있습니다.

![PyPI > Your projects (3)](https://dl.dropboxusercontent.com/scl/fi/fh8dfopuws8ub83wmlldo/uv-04-pypi-add.webp?rlkey=wpe4wkbusikljdedt0k80ji99&dl=0)

매번 `uv publish` 명령어를 작성하는 것은 불편하기 때문에
`dist.sh` 스크립트 파일로 명령어를 내보내서 간단하게 호출할 수 있습니다.

```bash
echo "uv publish --token pypi-*" >> dist.sh
chmod 755 dist.sh
```

```bash
# 다음에 배포할 떄는 간단하게 uv publish 명령어 호출
./dist.sh
```
