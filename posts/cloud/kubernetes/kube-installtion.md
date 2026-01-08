---
title: "쿠버네티스 클러스터 구축하기 - Ubuntu 24.04에서 kubeadm으로 멀티노드 설치"
date: "2025-07-16T23:52:48+09:00"
layout: "post"
description: >
  Ubuntu 24.04에서 쿠버네티스 클러스터 설치 가이드.
  kubeadm, containerd, Calico CNI를 활용한 마스터/워커 노드 구성부터 대시보드 배포까지 단계별로 설명합니다.
  Apple Silicon(ARM64) 환경에서 실습 가능한 완벽한 K8s 설치 튜토리얼입니다.
cover: "https://dl.dropboxusercontent.com/scl/fi/vz7ubvu68l28n2h9m13vc/kubernetes-00-cover.webp?rlkey=62jkzfxluywah0k79039ywve0&raw=1"
thumbnail: "https://dl.dropboxusercontent.com/scl/fi/9itthpgf8xuiogeebvyp9/kubernetes-00-logo.webp?rlkey=g4wrh18mf0tioibm3fij5r54k&raw=1"
categories: ["Cloud", "Kubernetes"]
tags: ["Kubernetes", "쿠버네티스 설치", "Ubuntu 24.04", "kubeadm", "containerd", "Calico", "CNI", "kubectl", "kubelet", "클러스터 구성"]
series: ["Kubernetes 배우기"]
---

{{< series "Kubernetes 배우기" >}}

## 실습 개요

{{% hint warning %}}
쿠버네티스 공식문서 중 시작하기 항목에 있는 [컨테이너 런타임](https://kubernetes.io/ko/docs/setup/production-environment/container-runtimes/)
과 [kubeadm 설치하기](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) 를 따릅니다.
{{% /hint %}}

### OS 선정

관련한 블로그 게시글 중에는 Rocky Linux OS를 사용한 사례가 많았는데,
이미 과거에 [Mac에 Ubuntu Server 24.04 설치하기 (UTM)](/blog/install-ubuntu-server/) 라는 게시글로
Ubuntu Server 가상머신을 생성한 이력이 있어서 Rocky Linux 대신에 Ubuntu Server를 사용할 것입니다.

Ubuntu Server를 선택한 또 다른 이유는,
Rocky Linux의 원본인 RHEL 8버전과 Ubuntu Server의 공식문서를 참고하여 아래와 같이 최소사양을 비교한데 있습니다.
서비스 운영 환경으로 사용할 것이 아니라서 단순히 숫자만 놓고 봤을 때 Ubuntu Server가 더 가벼워서 실습 환경으로 선택했습니다.

|하드웨어|[Ubuntu Server 24.04.2 LTS](https://documentation.ubuntu.com/server/reference/installation/system-requirements/)|[RHEL 8](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/8/html/automatically_installing_rhel/system-requirements-and-supported-architectures_rhel-installer#check-disk-and-memory-requirements_system-requirements-and-supported-architectures)|
|---|---|---|
|CPU|1GHz 이상 64비트|1.5GHz 이상 64비트, 2코어 권장|
|RAM|최소 1.5GB (ISO), 권장 3GB 이상|최소 1.5GiB~3GiB, 권장 1GB/CPU|
|저장공간|최소 5GB, 권장 25GB 이상|최소 10GiB, 권장 20GiB 이상|

Apple Silicon 환경에서 리눅스 가상머신을 실행하기 때문에, OS와 컨테이너 런타임 등은 모두 arm64 호환 버전을 사용합니다.

## 실습 환경

UTM 소프트웨어를 사용해 Ubuntu Server 가상머신이 만들어졌음을 가정하고 진행합니다. 가상머신 생성이 필요한 경우 [이전 게시글](/blog/install-ubuntu-server/)을 참고할 수 있습니다.

![localhost(minyeamer) \subset {UTM \subset {k8s-master, k8s-worker1, k8s-worker2}}](https://dl.dropboxusercontent.com/scl/fi/yohnr0gbnachd0thjabu3/diagram-02-vm.webp?rlkey=heta5zxt7qoomnhwqfh1tvml5&raw=1)

### 가용 자원

M4 Mac Mini 한 대의 자원을 사용할 수 있습니다.

{{% hint info %}}
**M4 Mac mini**

Memory : 16GB
CPU : 10코어
IP Address : 192.168.50.227/24
{{% /hint %}}

### 실습 자원

마스터 노드 1대와 워커 노드 2대로 구성된 쿠버네티스 클러스터를 구성합니다.

{{% hint info %}}
**k8s-master**

Memory : 4GB
CPU : 4코어
IP Address : 192.168.50.13/24
{{% /hint %}}

{{% hint info %}}
**k8s-worker1**

Memory : 4GB
CPU : 4코어
IP Address : 192.168.50.14/24
{{% /hint %}}

{{% hint info %}}
**k8s-worker2**

Memory : 4GB
CPU : 4코어
IP Address : 192.168.50.15/24
{{% /hint %}}

### 네트워크

{{< image
  src="https://dl.dropboxusercontent.com/scl/fi/a74mlztg1okfv44avn46l/diagram-03-network.webp?rlkey=nod84kq0bx9nrb0lhvizjozoo&raw=1"
  alt="{k8s-master, k8s-worker1, k8s-worker2} -> localhost(minyeamer) -> gateway -> internet"
  max-width="691px"
  align="center" >}}

통신 편의성을 위해 가상머신 네트워크는 브릿지 모드로 설정합니다.
Ubuntu Server 설치 시 기본 설정인 DHCP 대신에 Static IP 주소를 설정합니다.

실습 중 `minyeamer` 호스트에서 쿠버네티스 노드로 SSH 연결하여 명령어를 입력합니다.

쿠버네티스 노드는 역할을 명시하기 위해 `k8s-master`, `k8s-worker1`, `k8s-worker2` 호스트로 정의합니다.
`k8s-master` 가 마스터 노드 역할을 하고, 나머지가 워커 노드 역할을 담당합니다.

## 설치하기 (공통)

우선, 마스터 노드와 워커 노드에서 공통적으로 컨테이너 런타임과 쿠버네티스를 설치합니다.

### 1. Ubuntu Server 기본 설정

```bash
echo '===== [1] Ubuntu Server 기본 설정 ====='
echo '===== [1-1] 타임존 설정 ====='
sudo timedatectl set-timezone Asia/Seoul

echo '===== [1-2] hosts 설정 ====='
cat << EOF | sudo tee -a /etc/hosts

192.168.50.13 k8s-master
192.168.50.14 k8s-worker1
192.168.50.15 k8s-worker2
EOF
```

쿠버네티스 노드 간 호스트명으로 통신하기 위해 `/etc/hosts` 에 호스트명과 IP 주소를 맵핑합니다.
맥에서도 쿠버네티스 노드에 SSH로 접근하기 위해 편의상 `/etc/hosts` 를 동일하게 설정했습니다.

### 2. kubeadm 설치 전 사전작업

쿠버네티스 공식문서 [kubeadm 설치하기](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
에 따르면 시작하기 전에,

{{% hint info %}}
- 컴퓨터의 특정 포트들 개방. 자세한 내용은
  [여기](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#check-required-ports)
  를 참고한다.
- 스왑의 비활성화. kubelet이 제대로 작동하게 하려면 반드시 스왑을 사용하지 않도록 설정한다.
{{% /hint %}}

위 사항을 만족해야 한다고 알려줍니다.

쿠버네티스 클러스터 노드 간 다양한 포트를 통해 통신이 이루어지는데,
방화벽 설정에 의해 통신이 차단되어 클러스터 구성이 실패할 수 있습니다. 쿠버네티스 API 서버가 `6443` 포트를 사용하고,
파드 네트워크 플러그인마다 또 필요한 포트가 있습니다. 실습 환경에선 방화벽 자체를 해제합니다.

또한, 쿠버네티스의 구성요소인 Kubelet은 메모리 할당 및 관리를 위해 설계되었는데,
Swap을 사용하게 되면 예상치 못한 성능 저하나 불안정성을 초래할 수 있어 Swap을 해제해야 합니다.

이러한 과정을 아래와 같은 명령어로 처리할 수 있습니다.

```bash
echo '===== [2] kubeadm 설치 전 사전작업 ====='
echo '===== [2-1] 방화벽 해제 ====='
sudo systemctl stop ufw
sudo systemctl disable ufw
sudo ufw disable

echo '===== [2-2] Swap 비활성화 ====='
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

echo '===== [2-3] 필수 패키지 설치 ====='
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg iproute2
```

추가로, 컨테이너 런타임과 쿠버네티스 설치 전 필요한 필수 패키지를 미리 설치합니다.

### 3. 컨테이너 런타임 설치 전 사전작업

컨테이너 런타임과 관련된 쿠버네티스 공식문서의
[IPv4를 포워딩하여 iptables가 브리지된 트래픽을 보게 하기](https://kubernetes.io/ko/docs/setup/production-environment/container-runtimes/#ipv4를-포워딩하여-iptables가-브리지된-트래픽을-보게-하기)
문단에 따라 패킷 포워딩 등의 기능 제공을 위해 iptables 설정을 합니다.

해당 과정은 아래와 같이 공식문서에서 제공됩니다.

```bash
echo '===== [3] 컨테이너 런타임 설치 전 사전작업 ====='
echo '===== [3-1] 필요한 모듈 로드 ====='
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

echo '===== [3-2] iptables 세팅 ====='
sudo tee /etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
EOF

echo '===== [3-3] 설정값 적용 ====='
sudo sysctl --system
```

### 4. 컨테이너 런타임 설치

컨테이너 런타임은 Docker 공식문서 [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
에 따라 도커 엔진을 설치합니다.
도커 엔진을 설치하고 그 안에 포함되는 `containerd` 를 쿠버네티스의 컨테이너 런타임으로 사용합니다.

해당 과정은 아래와 같이 공식문서에서 제공됩니다.

참고로, `containerd` 설치 시 amd64와 arm64 아키텍처 중 하나를 지정해야 하는데,
`$(dpkg --print-architecture)` 명령어로 현재 환경의 아키텍처를 출력하여 변수로 사용합니다.

```bash
echo '===== [4] 컨테이너 런타임 설치 ====='
echo '===== [4-1] 도커 공식 GPG 키 추가 ====='
sudo apt-get update
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo '===== [4-2] 도커 Apt 저장소 추가 ====='
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo '===== [4-3] containerd 설치 ====='
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo '===== [4-4] CRI 활성화 ====='
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml

sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml
sudo systemctl restart containerd
```

컨테이너 런타임과 관련된 쿠버네티스 공식문서의
[containerd](https://kubernetes.io/ko/docs/setup/production-environment/container-runtimes/#containerd)
문단을 보면 아래와 같은 참고사항을 알려줍니다.

{{% hint info %}}
만약 `containerd` 를 패키지(`RPM`, `.deb` 등)를 통해 설치하였다면,
CRI integration 플러그인은 기본적으로 비활성화되어 있다.

쿠버네티스에서 containerd를 사용하기 위해서는 CRI support가 활성화되어 있어야 한다.
cri가 `/etc/containerd/config.toml` 파일 안에 있는 `disabled_plugins` 목록에 포함되지 않도록 주의하자.
만약 해당 파일을 변경하였다면, `containerd` 를 다시 시작한다.
{{% /hint %}}

따라서, `containerd` 설치 후 CRI를 직접 활성화합니다.

컨테이너 런타임을 설치한 후 `containerd` 버전을 확인해보니 1.2.27 버전이 설치되었습니다.

```bash
$ containerd --version
containerd containerd.io 1.7.27 05044ec0a9a75232cad458027ca83437aae3f4da
```

### 5. 쿠버네티스 설치

쿠버네티스 공식문서의
[kubeadm, kubelet 및 kubectl 설치](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#kubeadm-kubelet-및-kubectl-설치)
문단에 따라 쿠버네티스 운영에 필요한 패키지를 설치합니다. 각 패키지에 대해 아래와 같은 설명을 참고할 수 있습니다.

{{% hint info %}}
- `kubeadm` : 클러스터를 부트스트랩하는 명령이다.
- `kubelet` : 클러스터의 모든 머신에서 실행되는 파드와 컨테이너 시작과 같은 작업을 수행하는 컴포넌트이다.
- `kubectl` : 클러스터와 통신하기 위한 커맨드 라인 유틸리티이다.
{{% /hint %}}

해당 과정은 아래와 같이 공식문서에서 제공됩니다.

```bash
echo '===== [5] kubeadm 설치 ====='
echo '===== [5-1] 쿠버네티스 패키지 저장소의 공개키 다운로드 ====='
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.33/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo '===== [5-2] 쿠버네티스 Apt 저장소 추가 ====='
# sudo mkdir -p -m 755 /etc/apt/keyrings << Ubuntu 22.04 이전 버전
echo \
  "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.33/deb/ /" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

echo '===== [5-3] kubelet, kubeadm, kubectl 설치 ====='
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

echo '===== [5-4] kubelet 서비스 활성화 ====='
sudo systemctl enable --now kubelet
```

쿠버네티스를 설치한 후 `kubeadm`, `kubelet`, `kubectl` 버전을 확인했습니다.
모두 동일하게 1.33.2 버전이 설치되었습니다.

```bash
$ kubeadm version
kubeadm version: &version.Info{
Major:"1", Minor:"33", EmulationMajor:"", EmulationMinor:"", MinCompatibilityMajor:"",
MinCompatibilityMinor:"",
GitVersion:"v1.33.2", GitCommit:"a57b6f7709f6c2722b92f07b8b4c48210a51fc40",
GitTreeState:"clean", BuildDate:"2025-06-17T18:39:42Z",
GoVersion:"go1.24.4", Compiler:"gc", Platform:"linux/arm64"}
```

```bash
$ kubelet --version
Kubernetes v1.33.2
```

```bash
$ kubectl version
Client Version: v1.33.2
Kustomize Version: v5.6.0
Server Version: v1.33.2
```

## 설정하기 (마스터 노드)

마스터 노드에서 우선 클러스터 설정을 진행합니다.

### 6. 쿠버네티스 클러스터 설정

쿠버네티스 클러스터를 초기화하면 다양한 쿠버네티스 컴포넌트들이 파드로 만들어집니다.
또한, 실습 과정에서 새로운 파드를 생성하게 됩니다.

컨테이너들 간 통신을 위해 CNI(Container Network Interface)라는 표준 인터페이스가 필요합니다.
쿠버네티스는 기본적으로 Kubelet 이라는 자체적인 CNI 플러그인을 제공하지만 네트워크 기능이 매우 제한적인 단점이 있습니다.

그 단점을 보완하기 위해, 서드파티 플러그인으로 Flannel, Calico 등이 존재합니다.
이 중에서 Calico 네트워크 정책 및 보안, 확장성, 성능 측면에서 뛰어나기 때문에 실전 환경에서 주로 사용됩니다.

Calico를 개발하고 관리하는 Tigera에서 제공하는 공식문서
[Install Calico networking and network policy for on-premises deployments](https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises)
를 참고하여 아래와 같이 Calico를 설치했습니다.

```bash
echo '===== [6] 쿠버네티스 클러스터 설정 ====='
echo '===== [6-1] 클러스터 초기화 ====='
sudo kubeadm init --pod-network-cidr=10.244.0.0/16 --apiserver-advertise-address 192.168.50.13

echo '===== [6-2] kubectl 설정 ====='
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

echo '===== [6-3] Pod Network 설치 (Calico) ====='
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/operator-crds.yaml
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/tigera-operator.yaml

echo '===== [6-4] 사용자 정의 리소스 다운로드 ====='
curl https://raw.githubusercontent.com/projectcalico/calico/v3.30.2/manifests/custom-resources.yaml -O
sed -i 's/192.168.0.0/10.244.0.0/g' custom-resources.yaml

echo '===== [6-5] Calico를 설치하기 위한 manifest 생성 ====='
kubectl create -f custom-resources.yaml
```

설치가 완료되면 `calico-system` 이라는 네임스페이스 아래에 `calico-node` 등의 파드가 만들어집니다.
하지만, 위 명령어 중 사용자 정의 리소스 다운로드 부분에 `calico-node` 를 정의하는
`custom-resources.yaml` 파일의 기본 네트워크 대역이 `192.168.0.0/16` 대역으로 작성되어 있어서 오류가 발생했습니다.

`custom-resources.yaml` 파일 내용에서 기본 네트워크 대역을 클러스터 초기화 시에
입력한 `pod-network-cidr` 대역 `10.244.0.0/16` 으로 변경해줍니다.

```bash
$ kubectl get pods -n calico-system
NAME                                       READY   STATUS        RESTARTS      AGE
calico-kube-controllers-6565cb8dfb-dfb6m   1/1     Running       1 (23h ago)   3d
calico-node-2xznr                          1/1     Running       0             3d
calico-node-7zlgx                          1/1     Running       0             3d
calico-node-jgddh                          0/1     Running       1 (23h ago)   3d
calico-typha-6fd8bff95d-k2bgm              1/1     Running       0             3d
csi-node-driver-2llx6                      2/2     Running       0             3d
csi-node-driver-mj8js                      2/2     Running       0             3d
csi-node-driver-nzr55                      2/2     Running       2 (23h ago)   3d
goldmane-5f56496f4c-5szmn                  1/1     Running       1 (23h ago)   3d
whisker-78db647586-dpsdl                   2/2     Terminating   0             3d
whisker-78db647586-tmbnp                   2/2     Running       0             31m
```

## 설정하기 (워커 노드)

워커 노드에서 마스터 노드에 연결하는 설정을 진행합니다.

### 7. 쿠버네티스 클러스터 연결

마스터 노드에서 쿠버네티스 클러스터를 초기화하고
새 노드가 클러스터에 합류할 수 있도록 아래와 같이 토큰을 생성할 수 있습니다.

```bash
k8s-master$ sudo kubeadm token create --print-join-command > ~/join.sh
k8s-master$ cat join.sh
kubeadm join 192.168.50.13:6443 --token ...
```

마스터 노드에서 `kubeadm token create` 의 출력 결과를 복사해서 워커 노드에서 실행할 수도 있지만,
향후 쿠버네티스 설치 과정을 Ansible 등을 사용해 자동화할 계획이 있어서
GUI를 거치지 않고 SSH 통신을 통해 출력 결과를 전달했습니다.

```bash
k8s-master$ scp ~/join.sh minyeamer@k8s-worker1:/home/minyeamer/
k8s-worker1$ sudo ./join.sh

k8s-master$ scp ~/join.sh minyeamer@k8s-worker2:/home/minyeamer/
k8s-worker2$ sudo ./join.sh
```

마스터 노드로부터 전달받은 `join.sh` 파일, 즉 `kubeadm join` 명령어를
워커 노드에서 실행하고 기다리면 모든 노드가 활성화되는 것을 확인할 수 있습니다.

```bash
k8s-master$ kubectl get nodes
NAME          STATUS     ROLES           AGE   VERSION
k8s-master    Ready      control-plane   29m   v1.33.2
k8s-worker1   NotReady   <none>          16m   v1.33.2
k8s-worker2   NotReady   <none>          15m   v1.33.2
```

```bash
k8s-master$ kubectl get nodes
NAME          STATUS   ROLES           AGE   VERSION
k8s-master    Ready    control-plane   30m   v1.33.2
k8s-worker1   Ready    <none>          16m   v1.33.2
k8s-worker2   Ready    <none>          16m   v1.33.2
```

## 설정하기 (기타)

`kubectl` 명령어를 입력하는 마스터 노드에서 편의를 위한 설정을 진행합니다.

### 8. 쿠버네티스 편의기능 설치

쿠버네티스 공식문서 중 [kubectl 치트 시트](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)
에 따라 `kubectl` 명령어를 `k` 로 단축하는 것과 같은 자동완성 설정을 할 수 있습니다.

```bash
sudo apt-get update
sudo apt-get install bash-completion

echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
source ~/.bashrc
```

### 9. 쿠버네티스 대시보드 배포

쿠버네티스 공식문서 중
[쿠버네티스 대시보드를 배포하고 접속하기](https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/)
에 따르면 아래와 같은 웹 UI(쿠버네티스 대시보드)를 배포할 수 있습니다.

![Kubernetes Dashboard > Workloads > Pods](https://dl.dropboxusercontent.com/scl/fi/25ojg74h2u84k91aluf5k/kubernetes-01-dashboard.webp?rlkey=yp0kbkrle7od4cr1crcb06mm7&raw=1)

쿠버네티스 대시보드 웹 UI에 대한 파드를 생성하고, 파드의 `443` 포트를 호스트의 포트(`8443` 등)에 포워딩하여 웹 UI에 접속할 수 있습니다. 해당 과정은 아래에서 제시합니다.

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.6.1/aio/deploy/recommended.yaml
kubectl create serviceaccount admin-user -n kubernetes-dashboard

kubectl create clusterrolebinding admin-user \
  --clusterrole=cluster-admin \
  --serviceaccount=kubernetes-dashboard:admin-user

kubectl create token admin-user -n kubernetes-dashboard > ~/admin-token

kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard 8443:443 &
```

이제 막 쿠버네티스를 설치한 직후라 그런지, 아니면 사용량이 올바르게 수집되지 않아서인진 모르겠지만 아무런 내용도 나타나지 않습니다. 나중에 쿠버네티스를 충분히 실습하고 나서 대시보드에 대해 다시 알아보겠습니다.

## References

- [https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/](https://kubernetes.io/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)
- [https://kubernetes.io/ko/docs/setup/production-environment/container-runtimes/](https://kubernetes.io/ko/docs/setup/production-environment/container-runtimes/)
- [https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises](https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/onpremises)
- [https://www.inflearn.com/course/쿠버네티스-어나더-클래스-지상편-sprint1](https://www.inflearn.com/course/쿠버네티스-어나더-클래스-지상편-sprint1)
- [https://cafe.naver.com/kubeops/91](https://cafe.naver.com/kubeops/91)
- [https://captcha.tistory.com/78](https://captcha.tistory.com/78)
- [https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/](https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/)
- [https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/](https://kubernetes.io/ko/docs/tasks/access-application-cluster/web-ui-dashboard/)
