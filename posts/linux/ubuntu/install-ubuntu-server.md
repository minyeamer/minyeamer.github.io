---
title: "Mac에서 UTM으로 Ubuntu Server 24.04 설치하기"
date: "2025-07-06T15:47:47+09:00"
layout: "post"
description: >
  Mac에서 UTM 가상화 소프트웨어를 사용하여 Ubuntu Server 24.04 LTS를 가상머신으로 설치하는 가이드를 제공합니다.
  ARM64 이미지 다운로드, 네트워크 구성, SSH 접속 설정까지 단계별로 안내합니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/cw0ng73mwxr7yd0pgutnf/ubuntu-00-cover-2404.jpg?rlkey=y1b4ptay54ln84xn06spxi6w4&st=pu2ctpn3&dl=0"
categories: ["Linux", "Ubuntu"]
tags: ["Ubuntu", "Ubuntu Server", "UTM", "Virtual Machine", "Mac", "Linux", "우분투 설치하기", "가상머신", "SSH"]
---

리눅스 개발 환경이 필요해졌는데 단순 테스트를 위해 새로운 PC를 사거나
기존에 사용하는 Mac에 직접 설치하는건 비용이나 리스크가 있어 간단하게 가상환경을 이용하려 합니다.

Mac에서 무료로 이용할 수 있는 가상화 소프트웨어인 UTM을 사용해 우분투 서버를 설치하는 과정을 진행합니다.

## 1. Ubuntu 이미지 다운로드

Ubuntu Server 24.04.2 LTS 이미지를 다운로드 받습니다. (이미지 클릭 시 다운로드 경로로 이동)

{{% hint danger %}}
주의할 점은, 기본 다운로드 경로인 [https://ubuntu.com/download/server](https://ubuntu.com/download/server)로
접속하면 x86 아키텍처와 호환되는 amd64 이미지로 연결되기 때문에,
애플 실리콘 기반의 Mac이라면 다운로드 받는 파일이 arm64 이미지인지 확인해야 합니다.
{{% /hint %}}

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/oceh3he8l3sdtym9thmgm/ubuntu-01-download-arm.webp?rlkey=7v481x1bntmgbe1ulnahmonmu&dl=0"
  alt="Downloads > Ubuntu Server for ARM"
  href="https://ubuntu.com/download/server/arm" >}}

또는 터미널에서 내려받을 수도 있습니다.

```bash
curl -O -L https://cdimage.ubuntu.com/releases/24.04/release/ubuntu-24.04.2-live-server-arm64.iso
```

```bash
% ls -la ubuntu-24.04.2-live-server-arm64.iso
-rw-r--r--@ 1 user  group  2922393600 Jul  6 11:29 ubuntu-24.04.2-live-server-arm64.iso
```

## 2. UTM 설치하기

UTM 최신 버전(작성일 기준 4.6.5)을 설치합니다. (이미지 클릭 시 다운로드 경로로 이동)

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/08wbq1ughueuppsalapz8/utm-00-download.webp?rlkey=tljmi68xpg0nlfjurj2viccpa&dl=0"
  alt="UTM Download > Securely run operating systems on your Mac"
  href="https://mac.getutm.app/" >}}

앱스토어에서도 설치할 수 있는데 $9.99를 지불해야 합니다.

UTM을 실행하면 다음과 같은 화면이 나타납니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/e1fjmfsn0id95xkrpjwvg/utm-01-create-vm.webp?rlkey=fayvfsb1rtej0wrjhds1na5l6&dl=0"
  alt="Welcome to UTM"
  max-width="691px"
  align="center" >}}

## 3. 가상머신 생성하기

새 가상머신 만들기를 선택합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/jssht9bq4ghahyhu36x8q/utm-01-create-vm-guide.webp?rlkey=n05rhgb2akmyf2af3gqpzv3oz&dl=0"
  alt="Create a New Virtual Machine"
  max-width="691px"
  align="center" >}}

Start 화면에서 Virtualize를 선택합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/4cqnht6i802ict7ejq0tf/utm-02-start-virtualize-guide.webp?rlkey=5f3bz7prft1luehm9gef1dduq&dl=0"
  alt="Start > Virtualize (Faster, but can only run the native CPU architecture.)"
  max-width="691px"
  align="center" >}}

운영체제는 Linux를 선택합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/0zsipmeuxd76aarzmzbao/utm-03-os-linux-guide.webp?rlkey=jjx99y67zj5cvz0y65yumfh1i&dl=0"
  alt="Operating System > Linux"
  max-width="691px"
  align="center" >}}

### 이미지 파일 추가

Boot ISO Image에 앞에서 다운로드 받았던 Ubuntu 이미지 파일을 추가합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/t3cyt6s98f2iukzkcncgr/utm-04-boot-iso-image-guide.webp?rlkey=1b2j2trhax5h2py8z4zakpy01&dl=0"
  alt="Linux > Boot ISO Image > ubuntu-24.04.2-live-server-arm64.iso"
  max-width="691px"
  align="center" >}}

### 하드웨어 설정

메모리와 CPU 크기는 목적에 맞게 설정합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/c4i1o2auh3382l6156aaf/utm-05-hardware-4g-guide.webp?rlkey=k0d4nyq0w6tolp6ermwasmb72&dl=0"
  alt="Hardware > Memory 4096 MiB, CPU Cores 2"
  max-width="691px"
  align="center" >}}

저장공간도 목적에 맞게 설정합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/hthm6z1y5nm83anw3n65r/utm-06-storage-40g-guide.webp?rlkey=3h0m3gzz2q6yhtz4gydp6w22g&dl=0"
  alt="Storage > Specify the size of the drive where data will be stored into, 40 GiB"
  max-width="691px"
  align="center" >}}

### 가상머신 이름 설정

저장공간 설정 후에 나오는 공유폴더 설정은 무시합니다.
마지막으로 요약 화면이 나오는데 가상머신 이름을 설정합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/1659cvqcr1lct2x0cxsya/utm-07-summary-guide.webp?rlkey=xczccbzy4qqc6zxbff3gm3048&dl=0"
  alt="Summary > Name: k8s-master"
  max-width="691px"
  align="center" >}}

저장을 누르면 가상머신이 생성된 것을 확인할 수 있습니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/ao4ebm7s6ivuv56ehy0s1/utm-08-k8s-master.webp?rlkey=m6oni31rids7s6pte576nzg71&dl=0"
  alt="UTM > k8s-master"
  max-width="691px"
  align="center" >}}

### 가상머신 네트워크 설정

추가로, Ubuntu를 설치하기 전에 가상머신에서 네트워크 설정을 적용했습니다.
향후 여러 대의 가상머신과 Mac 간의 통신을 원활히 하기 위해 브릿지 모드를 선택했습니다.
이러한 경우가 아니라면 기본 설정인 Shared Network(NAT) 모드를 사용해도 됩니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/5hl5w2730xxzhzy99i73p/utm-09-network-bridge.webp?rlkey=ukq4ocs4eqsc6rtx5m0qzp5cd&dl=0"
  alt="Settings > Devices > Network > Network Mode: Bridged (Advanced)"
  max-width="691px"
  align="center" >}}

## 4. Ubuntu 설치하기

앞에서 생성한 가상머신을 실행합니다.
"Try or Install Ubuntu Server" 를 선택합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/5667kbl3ff7vba3y49fwc/ubuntu-02-install-init.webp?rlkey=dfi2ae1p0gy3rz13ptc90fasl&dl=0"
  alt="GNU GRUB version 2.12 > Try or Install Ubuntu Server"
  max-width="691px"
  align="center" >}}

### 언어 및 설치 유형

언어 및 키보드 레이아웃은 기본값인 "English" 를 선택합니다.

![Select your language](https://dl.dropboxusercontent.com/scl/fi/d7zwy8tealp6rry2vul8g/ubuntu-03-install-language.webp?rlkey=n10agxhqfdk3bogwnz0wqiqcy&dl=0)

![Keyboard configuration](https://dl.dropboxusercontent.com/scl/fi/1ipgx5ir7ph6qjm75wa4u/ubuntu-04-install-keyboard.webp?rlkey=rgk99m147moiagqqpiomamwjl&dl=0)

설치 유형은 기본값인 "Ubuntu Server" 를 선택합니다.

![Choose the type of installation](https://dl.dropboxusercontent.com/scl/fi/k03fkjunxnjrzhn7n84m9/ubuntu-05-install-type.webp?rlkey=3ylc7nzokh3jdpm833b3ne5g7&dl=0)

### 네트워크 설정

네트워크 설정에선 기본적으로 DHCP를 통한 동적 IP 주소가 적용되어 있습니다.

![Network configuration > DHCPv4](https://dl.dropboxusercontent.com/scl/fi/e00fwy4sp2n56jxmnmolx/ubuntu-06-install-network-dhcp.webp?rlkey=adruzzoo35ki9xrxakcrkthf3&dl=0)

향후 여러 가상머신 간 고정된 IP 주소를 가지고 통신할 필요가 있기 때문에 정적으로 IP 주소를 지정하겠습니다.
이러한 경우가 아니라면 DHCP를 유지한채 넘어가도 무방합니다.

가상머신을 실행하기 전에 [네트워크 설정](#가상머신-네트워크-설정)에서
브릿지 모드로 변경했기 때문에 맥의 네트워크와 동일한 대역을 사용할 수 있습니다.
NAT 모드로 가상머신을 실행 중이라면 DHCP를 통해 배정된 IP 주소를 바탕으로 대역을 추정해 IP 주소를 지정해야 합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/f6xmbgh8zd413oees8yv9/ubuntu-07-install-ipv4-method.webp?rlkey=xdyg9og782d0rbojyxo8gvyvp&dl=0"
  alt="Edit enp0s1 IPv4 configuration > IPv4 Method: Manual"
  max-width="604px"
  align="center" >}}

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/xv50tlt58s6vp7bgzcqfl/ubuntu-08-install-ipv4-info.webp?rlkey=nphq16at79pqy2hbisnb5i0an&dl=0"
  alt="Edit enp0s1 IPv4 configuration > Address: 192.168.50.13/24"
  max-width="604px"
  align="center" >}}

정적 IP 주소를 할당했다면 다음과 같이 `static` 으로 표시됩니다.

![Network configuration > static](https://dl.dropboxusercontent.com/scl/fi/x9o3auu74yky1j10zqgpj/ubuntu-09-install-network-static.webp?rlkey=xgobkkx4dxrj63779x3afe54s&dl=0)

### 프록시 및 미러 서버 설정

프록시 서버는 기본값으로 무시합니다.

![Proxy configuration](https://dl.dropboxusercontent.com/scl/fi/ljzwgqwr3xjprhyvf1154/ubuntu-10-install-proxy.webp?rlkey=a6cak9r5z5nlzw6zplp8ifziu&dl=0)

미러 서버는 소프트웨어 패키지를 다운로드 받는 공식 서버의 복제본입니다.
보통 패키지를 다운로드 받을 때 미러 서버를 통해 받습니다.
기본값으로는 "kr.ports.ubuntu.com/ubuntu-ports" 로 지정되어 있는데,
속도가 더 빠른 카카오 미러 서버 "mirror.kakao.com" 로 변경했습니다.

![Ubuntu archive mirror configuration](https://dl.dropboxusercontent.com/scl/fi/8dlnyvjnvpmp4tkjoyooz/ubuntu-11-install-mirror.webp?rlkey=tpr0bfb2vnrwabyzru91g2th2&dl=0)

### 저장공간 설정

저장공간도 기본 설정인 "Use an entire disk" 를 적용합니다.
목적에 따라 파티션을 분리할 수도 있지만, 현재는 파티션을 나눌 필요가 없습니다.

![Guided storage configuration](https://dl.dropboxusercontent.com/scl/fi/9zur6f4harksj7l4fwv6y/ubuntu-12-install-storage.webp?rlkey=y2nqz2lqhgsmiv8j8ahzyba0s&dl=0)

![Storage configuration](https://dl.dropboxusercontent.com/scl/fi/tl76ovh807ku0lsmvaumj/ubuntu-13-install-partitions.webp?rlkey=ynw1afjnwwiig8je100ecyabz&dl=0)

설치를 진행하게 되면 디스크 포맷을 통해 저장된 데이터가 삭제될 수 있다고 경고하는데 그대로 진행합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/eodlicwk3z1f0o86yv59j/ubuntu-14-install-confirm-format.webp?rlkey=3u7tfyely8c8lh2c762jyidkr&dl=0"
  alt="Confirm destructive action"
  max-width="518px"
  align="center" >}}

### 프로필 설정

사용자 이름, 서버 이름 등을 설정합니다.

- Your name : 이름 정보 (서버 운영과 무관)
- Your server's name : 서버 호스트명
- Pick a username : 로그인 사용자 이름
- Choose a password : 로그인 사용자 비밀번호
- Confirm your password : 로그인 사용자 비밀번호 확인

![Profile configuration](https://dl.dropboxusercontent.com/scl/fi/c52zlcqmwyqj6tvkr57bo/ubuntu-14-install-profile.webp?rlkey=vemzosrmklwpc5bu9lwre06rg&dl=0)

### 기타 설정 및 설치

Ubuntu Pro 업그레이드 여부를 묻는데 사용하지 않으므로 넘어갑니다.

![Upgrade to Ubuntu Pro](https://dl.dropboxusercontent.com/scl/fi/25lzrdly77ezor8ymimu7/ubuntu-15-install-pro.webp?rlkey=7jckd8j22wqxi7sh9d69igevc&dl=0)

OpenSSH 서버 설치를 묻는데 SSH 서버를 사용하기 위해 체크합니다.

![SSH configuration](https://dl.dropboxusercontent.com/scl/fi/0ygvff9bbsdzu28wewgrp/ubuntu-16-install-ssh.webp?rlkey=gkbo5r5931a3du7l27flkicmy&dl=0)

설치 패키지 선택창이 나오는데 필요한건 직접 설치할 것이기 때문에 다음으로 넘어갑니다.

![Featured server snaps](https://dl.dropboxusercontent.com/scl/fi/tvnk5ree5zrurackvhh8a/ubuntu-17-install-snaps.webp?rlkey=9dn87gplvyyvq8jn1droedzkz&dl=0)

설치가 진행되고, 설치가 완료되면 "Reboot Now" 선택지가 생깁니다. 재부팅을 수행합니다.

![Installation complete! > Reboot Now](https://dl.dropboxusercontent.com/scl/fi/4tjsn92sa3vx7vyh6ljz0/ubuntu-18-install-complete.webp?rlkey=vmqjh9s2pacsx15sd13xe3m5v&dl=0)

## 5. Ubuntu 접속

최초 설치 후 재부팅하면 더이상 진행되지 않고 커서만 깜빡이는데, 일단 종료하고 UTM 화면으로 돌아갑니다.
가상머신에서 부팅용 이미지 파일을 초기화한 후 다시 실행합니다.

{{< img
  src="https://dl.dropboxusercontent.com/scl/fi/rnys091je3c9wb5yhgfm6/utm-10-clear-cd-dvd-guide.webp?rlkey=veuxjlfig9prmveyi6e9eu0c1&dl=0"
  alt="UTM > CD/DVD > Clear"
  max-width="691px"
  align="center" >}}

가상머신을 실행하면 로그인 화면이 나타납니다.
프로필 설정에 지정한 사용자 이름과 비밀번호를 순차적으로 입력합니다.

![k8s-master login: _](https://dl.dropboxusercontent.com/scl/fi/rzz4jyys1ohzy3t9f91oe/ubuntu-19-k8s-master-login.webp?rlkey=7u5jdnih08dxv1ojaik3igmdl&dl=0)

정상적으로 로그인되었다면 아래와 같이 명령어를 입력할 수 있는 프롬프트가 나타납니다.

![minyeamer@k8s-master:~$ _](https://dl.dropboxusercontent.com/scl/fi/282q7vu1a47miepep6pq3/ubuntu-20-k8s-master-home.webp?rlkey=td0jrflmlulh3p71ejpbg1tyb&dl=0)

## 참고 자료

- [https://ubuntu.com/download/server/arm](https://ubuntu.com/download/server/arm)
- [https://mac.getutm.app/](https://mac.getutm.app/)
- [https://gymdev.tistory.com/75](https://gymdev.tistory.com/75)
- [https://moneymentors.tistory.com/entry/우분투Ubuntu-22042-LTS-서버-설치-방법](https://moneymentors.tistory.com/entry/우분투Ubuntu-22042-LTS-서버-설치-방법)
- [https://mirror.kakao.com/](https://mirror.kakao.com/)
