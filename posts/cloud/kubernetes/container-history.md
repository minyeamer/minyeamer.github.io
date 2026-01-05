---
title: "컨테이너의 역사와 쿠버네티스 등장 배경 - LXC에서 containerd까지"
date: "2025-07-15T01:55:24+09:00"
layout: "post"
description: >
  쿠버네티스 등장 배경과 컨테이너의 역사를 다룬 가이드.
  LXC, Docker, containerd부터 CRI, OCI까지 컨테이너 기술의 진화를 단계별로 설명하며,
  Kubernetes의 핵심 개념을 이해하세요. 클라우드 네이티브 환경 구축에 필수적인 지식입니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/vz7ubvu68l28n2h9m13vc/kubernetes-00-cover.webp?rlkey=62jkzfxluywah0k79039ywve0&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/9itthpgf8xuiogeebvyp9/kubernetes-00-logo.webp?rlkey=g4wrh18mf0tioibm3fij5r54k&raw=1"
categories: ["Cloud", "Kubernetes"]
tags: ["Kubernetes", "Container", "컨테이너 역사", "Docker", "LXC", "containerd", "CRI", "OCI", "kubelet", "컨테이너 런타임", "클라우드 네이티브", "오케스트레이션"]
---

## Study Overview

{{% hint warning %}}
1. [쿠버네티스 어나더 클래스 (지상편) - Sprint 1, 2](https://www.inflearn.com/course/쿠버네티스-어나더-클래스-지상편-sprint1) 과정을 따릅니다.
2. [[따배쿠] 쿠버네티스 시리즈](https://www.youtube.com/playlist?list=PLApuRlvrZKohaBHvXAOhUD-RxD0uQ3z0c) 과정(유튜브 공개 영상)을 따릅니다.
{{% /hint %}}

### 목적

- 쿠버네티스가 무엇이고, 쿠버네티스로 어떤 것을 할 수 있는지 알기 위해 학습합니다.
- 두 가지 커리큘럼을 참고하지만, 그대로 따라하지 않고 개발 환경에 맞춰서 설치 버전 등을 변경합니다.
- 이론보다는 실습 위주로 직접 명령어를 입력하고 결과를 보면서 쿠버네티스를 익힙니다.

## Container History

![chroot -> cgroup -> namespace -> lxc -> docker -> containerd + Cloud Orchestration](https://dl.dropboxusercontent.com/scl/fi/68zs362oo5yfcc4q7vt3b/diagram-00-container-history.webp?rlkey=l0wyexrgbiugt67y6telphnwe&raw=1)

### LXC

컨테이너의 역사는 `chroot` 를 발표한 것으로 시작합니다. `chroot` 는 "change root"의 약자로,
프로세스의 root 디렉터리를 변경하는 기능입니다. 해당 프로세스가 지정된 디렉터리 이하로만 접근할 수 있도록 하여 격리시킬 수 있습니다.

`cgroup` 은 "control group"의 약자로, 프로세스의 리소스 사용량(CPU, 메모리 등)을 제한 또는 격리할 수 있습니다.
시스템 관리자는 `cgroup` 을 통해 특정 프로세스 그룹에 할당할 수 있는 리소스의 양을 제한하거나,
우선순위를 지정하고, 리소스 사용 현황을 모니터링할 수 있습니다.
컨테이너 환경에서 여러 프로세스가 실행될 때 각 컨테이너별로 자원을 분리하고 관리하는 데 핵심적으로 사용됩니다.

`namespace` 는 시스템 리소스(프로세스, 네트워크 등)를 서로 독립적으로 분리해서 사용할 수 있게 만듭니다.
컨테이너 기술의 핵심 기반으로, 각각의 컨테이너가 독립된 환경처럼 동작할 수 있게 해줍니다.

`LXC` 또는 리눅스 컨테이너는 `cgroup`, `namesapce` 와 같은 리눅스 커널의 기능을 활용하여
하나의 리눅스 시스템에서 여러 개의 격리된 리눅스 환경(컨테이너)을 실행할 수 있게 해주는 운영체제 수준의 가상화 기술입니다.

Red Hat의 토픽 [Linux 컨테이너란?](https://www.redhat.com/ko/topics/containers/linux-keonteineolan)
에 따르면, `LXC` 이전에 `FreeBSD Jail` 이라고,
FreeBSD 시스템에서 여러 개의 독립적인 환경을 실행할 수 있게 해주는 컨테이너의 시초가 있었다고 합니다.
이후에 VServer 프로젝트를 통해 Linux에 격리된 환경이 구현되었습니다.

### Docker

`Docker` 는 `LXC` 에서 출발한 상위 레벨의 컨테이너 기술로, 간편한 CLI와 서버 데몬,
사전 쿠축된 컨테이너 이미지 라이브러리 및 레지스트리 서버의 개념 등 여러 가지의 새로운 개념과 툴을 선보였습니다.

`rkt` 는 `Docker` 이후에 등장한, 보안과 표준 준수를 중시한 컨테이너 런타임입니다.
`rkt` 는 CoreOS에서 개발한 오픈소스 컨테이너 런타임이었는데,
CoreOS가 Red Hat에 인수되면서 Fedora CoreOS로 이름이 바뀌었습니다.
Red Hat의 토픽 [rkt란 무엇일까요?](https://www.redhat.com/ko/topics/containers/what-is-rkt)
에 따르면, `rkt` 의 핵심 실행 단위가 `pod` 인데,
공유 컨텍스트에서 실행되는 하나 이상의 애플리케이션(컨테이너) 집합을 의미하며, 쿠버네티스의 최소 배포 단위로 사용되는 개념입니다.

### Kubernetes

`Docker` 가 나온 이후 `Kubernetes`, `Docker Swarm` 등 컨테이너 오케스트레이션이라는 컨테이너의
배포, 관리, 확장 및 네트워킹을 자동화하는 프로세스가 만들어졌습니다. 현재는 `Kubernetes` 가 주로 사용됩니다.

따라서, `Kubernetes` 와 호환성이 좋은지가 컨테이너를 선택하는 중요한 결정요소가 되었는데,
`Docker` 는 컨테이너 런타임 뿐 아니라 빌드, CLI, 데몬 등 여러 구성요소를 포함해
`Kubernetes` 의 런타임으로 `Docker` 를 사용할 때 불필요한 오버헤드와 복잡성이 발생했습니다.

`Kubernetes` 는 다양한 컨테이너 런타임과의 호환을 위해 CRI(Container Runtime Interface)라는
표준을 도입했습니다. `Docker` 는 CRI를 준수하지 않아 `Dockershim` 이라는 별도의 계층을 만들어야 했습니다.

### containerd

`containerd` 는 `Docker` 에서 불필요한 기능을 제거한 경량 런타임으로, 리소스 사용량이 적고 성능이 뛰어납니다.
따라서, `Docker` 를 런타임으로 쓸 떄보다 CPU나 메모리 사용량이 줄고 관리 포인트가 단순화됩니다.
`container` 는 CNCF(Cloud Native Computing Foundation)에 기부되어 관리되며,
OCI(Open Container Initiative) 표준을 준수합니다.
`Kubernetes` 내부에서 컨테이너를 실행하는 엔진으로 `containerd` 가 사용됩니다.

`Kubernetes` 와 `Docker` 의 관계에 대한 자세한 내용은 쿠버네티스 블로그의 게시글
[당황하지 마세요. 쿠버네티스와 도커](https://kubernetes.io/ko/blog/2020/12/02/dont-panic-kubernetes-and-docker/)
를 참고할 수 있습니다.

`CRI-O` 는 CNCF에서 관리되는 `containerd` 와 달리, Red Hat 등이 관리하며 엔터프라이즈
`Kubernetes` 환경에서 널리 사용됩니다. 범용 컨테이너 런타임 목적의 `containerd` 와 다르게,
`CRI-O` 는 `Kubernetes` 와의 통합만을 목적으로 불필요한 기능을 배제한 최소한의 런타임입니다.

`CRI-O` 에 대한 자세한 설명은 Red Hat의 공식문서
[CRI-O Runtime](https://docs.redhat.com/en/documentation/openshift_container_platform/3.11/html-single/cri-o_runtime/index)
을 참고할 수 있습니다.

## Kubernetes History

![docker (v1.0 ~ v1.20) -> dockershim (v1.5 ~ v1.23) -> cri-dockerd (v1.24 ~ )](https://dl.dropboxusercontent.com/scl/fi/brv7o8znyu6xcxgqvqge1/diagram-01-kubernetes-history.webp?rlkey=zw7bi3tdisijvxjarcfmf2v0x&raw=1)

### Docker

`LXC` 는 리눅스 커널의 기능을 가지고 만든 Low Level 컨테이너 런타임입니다.
`Docker` 는 `LXC` 를 기반으로 `libcontainer` 라는 Low Level 컨테이너 런타임을 만들었습니다.
`Docker` 는 `libcontainer` 를 기반으로 사용자 친화적으로 만든 High Level 컨테이너 런타임입니다.

`Docker` 에는 CLI, 로그 관리, 저장공간, 네트워크 등의 부가 기능이 많아 사용자 편의가 좋지만,
이 중에서 컨테이너를 만드는 역할은 `containder` 가 담당하며 `libcontainer` 를 이용합니다.

### kubelet

`Kubernetes` 는 `kube-apiserver` 와 `kubelet` 이라는 컴포넌트가 있습니다.
`Kubernetes` 에는 컨테이너를 만드는 명령어는 없지만, Pod 안에 컨테이너를 하나 이상 명시할 수 있습니다.

`kube-apiserver` 가 Pod를 생성해달라는 호출을 받으면 `kubelet` 에게 전달하고,
`kubelet` 은 컨테이너 런타임한테 컨테이너를 생성해달라는 요청을 보냅니다.
그러면, 컨테이너 런타임이 직접적으로 컨테이너를 생성합니다.

`kubelet` 은 Pod의 생성부터 실행, 상태 관리, 리소스 모니터링을 담당합니다.
`kubelet` 이 중단되면 해당 노드에서 Pod의 생성 및 관리가 불가능해져, 클러스터의 정상 운영에 큰 영향을 미칩니다.

### CRI

`kubelet` 은 `Docker` 또는 다른 컨테이너 런타임에 알맞은 API를 호출합니다.
하지만, `containerd` 가 분리되고 `CRI-O` 가 추가되는 등 컨테이너 런타임이 늘어나게 되면서
다양한 컨테이너 런타임과 통신하기 위한 표준이 필요했습니다.

CRI는 다양한 컨테이너 런타임과 표준화된 방식으로 통신할 수 있게 해주는 핵심 인터페이스입니다.
CRI는 gRPC 프로토콜을 사용하여 `kubelet` 과 컨테이너 런타임이 효율적으로 명령과 상태 정보를 주고받도록 합니다.
CRI를 통해 컨테이너 런타임 종류에 관계없이 일관된 방식으로 컨테이너와 이미지를 관리할 수 있게 되었습니다.

### OCI

컨테이너의 종류가 많아지면서 컨테이너 런타임과 관련 업계 개방형 표준을 만들기 위해 Red Hat과 Docker 등
여러 기업에 의해 설립된 단체가 OCI입니다. OCI는 컨테이너 런타임과 이미지 포맷의 업계 표준을 정의하여,
다양한 플랫폼과 도구 간의 호환성을 마련하는 것이 핵심 목적입니다.

`Docker` 는 OCI 규격을 맞추기 위해 Low Level로 `runC` 를 만들고 `containerd` 에서도
`runC` 를 사용하게 됩니다. `runC` 가 기존 `libcontainer` 와의 차이점은 `LXC` 를 이용하지 않고
바로 커널 레벨의 가상화 기술을 사용한다는 것입니다.

### CRI-Plugin

`Docker` 와 같은 컨테이너 런타임에 새 기능이 생기면 쿠버네티스도 같이 패치를 해야합니다.
이때마다 CRI를 수정하기 위해 쿠버네티스를 패치해야 하는 구조를,
`kubelet` 에서 컨테이너 런타임으로 바로 받을 수 있게 구조를 바꿉니다.

이런 구조를 지원하기 위해 `containerd` 에서는 `CRI-Plugin` 이라는 기능을 추가했습니다.
`CRI-Plugin` 은 `kubelet` 과 다양한 컨테이너 런타임 사이의 표준 통신을 가능하게 해주는
플러그인 형태의 구현체로, CRI 명세를 실제로 구현한 모듈입니다.

해당 과정에서 `Docker` 를 지원하던 `dockershim` 은 관리가 잘 안되는 문제로
1.24 버전부터 제거되었습니다. 1.24 버전부터는 Mirantis가 `Docker` 를 인수하여 `cri-dockerd` 라는
어댑터를 만들고 Mirantis Container Runtime이란 이름으로 `Docker` 를 지원합니다.

## References

- [https://www.inflearn.com/course/쿠버네티스-어나더-클래스-지상편-sprint1](https://www.inflearn.com/course/쿠버네티스-어나더-클래스-지상편-sprint1)
- [https://www.redhat.com/ko/topics/containers/linux-keonteineolan](https://www.redhat.com/ko/topics/containers/linux-keonteineolan)
- [https://www.redhat.com/ko/topics/containers/what-is-rkt](https://www.redhat.com/ko/topics/containers/what-is-rkt)
- [https://kubernetes.io/ko/blog/2020/12/02/dont-panic-kubernetes-and-docker/](https://kubernetes.io/ko/blog/2020/12/02/dont-panic-kubernetes-and-docker/)
- [https://docs.redhat.com/en/documentation/openshift_container_platform/3.11/html-single/cri-o_runtime/index](https://docs.redhat.com/en/documentation/openshift_container_platform/3.11/html-single/cri-o_runtime/index)
