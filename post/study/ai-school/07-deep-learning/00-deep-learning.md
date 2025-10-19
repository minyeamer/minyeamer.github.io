---
layout: post
title: "[AI SCHOOL 5기] 딥러닝"
date: 2022-04-14 17:20:00 +0900
categories: [Study, AI SCHOOL]
tags: [AI SCHOOL, 멋쟁이사자처럼, 코드라이언, Deep Learning]
slug: aischool-07-00-deep-learning
draft: true
---

# Deep Learning
- 아주 많은 데이터를 이용한 학습
- 머신러닝의 Feature Engineering 과정을 컴퓨터가 진행 (Feature Extraction)
- 데이터가 많아질수록 시간이 늘어나지만 학습의 깊이도 증가
- Data Augmentation: 부족한 데이터를 일부 변형하여 데이터의 수 증가

---

# Perceptron
- Threshold를 넘기면 다음 뉴런에게 전기신호를 보내는 뉴런을 본딴 인공신경망
- 데이터가 들어오면 내부적으로 연산을 진행해 하나의 값으로 다음 퍼셉트론에게 전달
- 깊이 (층의 개수), 너비 (하나의 층에 있는 퍼셉트론 수)
- 퍼셉트론을 연결하는 선 하나하나가 `θ`를 의미
- 제일 좋은 `θ` 값의 조합을 찾는 것이 목적

## Single-Layer Perceptron
- 뉴런을 본따 만든 알고리즘 하나의 단위
- 데이터와 `θ`의 선형 결합을 계산하고 결과에 Activation Function 적용
- Activaiton Function은 선형 결과를 꺾는 비선형 함수   
  (단순 선형 회귀로는 아무리 많은 Layer를 쌓아도 같은 선형 회귀 결과가 나옴)
- XOR 문제의 경우 Linearly Inseparable하여 하나의 퍼셉트론으로 풀 수 없음

## Multi-Layer Perceptron
- 복수의 퍼셉트론을 연결한 구조
- 단층 퍼셉트론에서 풀 수 없었던 XOR 문제를 and 연산 뉴런과 or 연산 뉴런의 조합으로 해결

## (Artificial) Neural Network
- 퍼셉트론을 모은 레이어를 깊이 방향으로 쌓아나가면서 만들어낸 인공 신경망 모델
- Input Layer: 외부로부터 데이터를 입력 받는 신경망 입구
- Hidden Layer: Input Layer와 Output Layer 사이의 모든 레이어 (Learnable Kernel)
- Output Layer: 모델의 최종 연산 결과를 내보내는 신경망 출구
- 결과값을 그대로 받으면 Regression
- 결과값에 Sigmoid를 거치면 Binary Classification
- 결과값에 Softmax를 거치면 K-Class Classificiation

## Back Propagation Algorithm
- 오차 역전파 알고리즘 (신경망의 효율적인 학습)
- 학습된 출력 값과 실제 값과의 오차를 계산하여 Feedforward 반대인 역방향으로 전파하는 알고리즘
- Forward 방향으로 한번 연산을 한 다음 그 결과값(Cost)를 역방향으로 전달해가면서 Parameter를 Update
- 모델이 틀린 정도를 역방향으로 전달하며 미분하고 곱하고 더하는 것을 반복하여 `θ`를 갱신
- Vanishing Gradient: 레이어가 깊어질수록 앞선 오차 값이 역방향으로 뒤까지 전달이 되지 않는 문제
- Activation Function(ReLu Function)을 적용하여 문제 해결

---

# Activation Function
- 선형 결합 결과에 대한 출력 값을 다음 레이어로 전달하는 비선형 함수
- 마지막 결과에 대한 MSE를 최소화하기 위해 Gradient Descent를 진행하는데,   
  이전 층의 `θ`에 대해서는 미분을 통해 한단계 전의 상태로 되돌려 수행 (Back Propagation Algorithm)

## Step Function
- 0보다 크면 1, 0보다 작으면 0을 반환하는 함수
- 미분 시 0이 되어 결과를 이전 상태로 되돌릴 수 없는 문제로 사용하지 않음

## Sigmoid Function
- Step Function과 유사한 형태의 지수 함수
- `tanh`: Sigmoid Function은 나올 수 있는 y 값이 양수 영역에 한정되기 때문에   
  그래프를 내려서 -1에서 1 사이 범위로 변환
- 가장 큰 기울기 값이 0.25에 불과하기 때문에 결과 값을 5단계만 이전으로 되돌려도   
  0.001에 근접한 의미없는 값이 됨

## ReLu Function
- 0보다 크면 x 값, 0보다 작으면 0을 반환하는 꺾인 형태의 함수
- `Leaky ReLU`: 출력이 0일 경우 어떤 것을 곱해도 0이 되어버리는 Bad Neuron이 발생하기 떄문에   
  0보다 작은 값에 대해 미세한 음수 결과 값(y=⍺x)을 반환하도록 한 함수
- `PReLU`: 컴퓨터가 에러를 줄이는 방향으로 `⍺` 값을 조정하는 함수 (Parametric ReLU)

---

# Neural Network Optimization
- Gradient Descent를 활용한 신경망 학습
- (1)모든 Parameter `θ`를 초기화, (2)Cost Function 상의 가장 낮은 지점으로 이동, (3)`θ`를 Update

## Weight Initialization
- Gradient Descent를 적용하기 위해 Parameter `θ`를 초기화하는 것
- Xavier Initialization: Sigmoid 또는 tanh 함수를 사용할 떄 적용, 표준편차가 sqrt(1/n)인 정규분포를 따르도록 가중치 초기화
- He Initialization: ReLu 함수를 사용할 때 적용, 표준편차가 sqrt(2/n)인 정규분포를 따르도록 가중치 초기화

## Weight Regularization
- Gradient Descent 계산 시 Cost Function은 Tradining Data에 대해 모델이 발생시키는 에러 값의 지표
- Training Data만 고려된 Cost Function을 기준으로 Gradient Descent를 적용하면 Overfitting 우려
- 모델이 복잡해질수록 모델 속에 숨어있는 `θ`의 개수가 증가하고 절대값이 커짐
- `θ`에 대한 함수(Regularization Term)를 기존의 Cost Function에 더하여 Trade-off 관계 속에서 최적값을 찾음

## Regularization Term
- `J(θ) = MSE + λR(θ)`, Weight Decay
- L1 Regularization: 가중치의 절대값의 합에 비례하여 가중치에 패널티 (Lasso, 마름모꼴),   
  관련성이 없거나 매우 낮은 특성의 가중치를 정확히 0으로 유도하여 모델에서 해당 특성 배제
- L2 Regularization: 가중치의 제곱의 합에 비례하여 가중치에 패널티 (Ridge, 원의 방정식),   
  큰 값을 가진 가중치를 더욱 제약하는 효과
- Regularization Rate: 스칼라 값 (Lambda, L1/L2 도형의 크기),   
  정규화 함수의 상대적 중요도 지정, 정규화율을 높이면 과적합이 감소하지만 모델의 정확성이 떨어짐

## Advanced Gradient Descent Algorithms
- Stochastic Gradient Descent: 하나의 Training Data 마다 Cost를 계산하고 Gradient Descent 적용,   
  매번 weight를 갱신하기 때문에 신경망의 성능이 불안정, 수렴조건을 조정해야할 필요
- Mini-Batch Stochasitc Gradient Descent: Training Data에서 일정한 크기(Batch Size)의 데이터 선택,   
  설계자의 의도에 따라 속도와 안정성을 동시에 관리, GPU 기반의 효율적인 병렬 연산 가능
- Epoch: 전체 학습 데이터를 한 번씩 모두 학습시킨 횟수(iteration)
- Adam Optimizer: Momentum과 AdaGrad/RMSProp의 이점을 조합, Adaptive Learning Rate가 적용

## Dropout
- 신경망에 적용할 수 있는 효율적인 Overfitting 회피 방법 중 하나
- Training을 진행할 때 매 Batch 마다 레이어 단위로 일정 비율 만큼의 뉴런을 꺼뜨림
- Test/Inference 단계에는 Dropout을 걷어내어 전체 뉴런이 살아있는 채로 Inference를 진행
- 랜덤하게 뉴런을 꺼뜨려 학습을 방해함으로써 모델의 학습이 Training Data에 편향되는 것을 방지
- 동일한 데이터에 대해 매번 다른 모델을 학습시키는 것과 같은 효과를 발생시켜 Model Ensemble 효과를 얻을 수 있음
- 가중치 값이 큰 특정 뉴런의 영향력이 커져 다른 뉴런들의 학습 속도에 문제를 발생시키는 Co-Adaptation 회피

## Batch Normalization
- 입력값에 Standardization과 같은 Normalization을 적용하면 전반적으로 모델의 성능 증가
- Normalization이 제대로 적용되지 못할 경우 최적의 Cost 지점으로 가는 길을 빠르게 찾지 못함
- Batch Normalization은 입력값 뿐만 아니라 Hidden Layer에 있는 Input에도 Normalization을 적용
- Activation Function을 적용하기 전에 Batch Normalization을 먼저 적용
- Standardization 적용 시 Sigmoid의 선형 부분에서만 값이 나와 비선형 함수의 역할 상실
- Non-linearity: 열에 `λ`를 곱하고 `β`를 더함 (오차역전파를 통해 학습하는 `θ`), Scaling 및 Shifting 적용
- 학습 속도 및 학습 결과 개선, 가중치 초기값 의존도가 낮음, Overfitting 억제 효과, **학습 속도 향상이 주목적**

---

# Draft

http://playground.tensorflow.org/

> spiral 예시
https://goo.gl/vvea3e , https://goo.gl/yfLEHq , https://goo.gl/jqVgr9

> 12p

클래스 불균형 - SMOTE

* Introducing the NVIDIA DPU @ https://j.mp/2GjQRBL
* Mythbusters Demo GPU vs CPU @ https://j.mp/3abWFb2
* Somethings about TPU (Google I/O) : https://goo.gl/JSTbDv
* 구글, AI로 AI칩 개발 시도..."사람보다 나아“ @ http://j.mp/2vbQ545 
* Colab-specific TPU examples (Fashion-MNIST, LSTM, BERT) @ https://goo.gl/DTTR31
* (CodeLab) TPU-speed data pipelines: tf.data.Dataset and TFRecords @ http://j.mp/2XF2Ccx
* Colossus Mk2 by Graphcore beating Nvidia's flagship A100 (UK startup)@ https://j.mp/3iig0Ke

> 39p

* Active Learning : ALiPy @ http://j.mp/2Q1EdYo
* model interpretability vs model explainability @ https://j.mp/2AUy4df 
* 데이터 라벨링 너무 귀찮아요: 컨센서스 라벨링 도입기 (DEVIEW2020) @ https://j.mp/38AYUnC
* LIME (python library for model explanation & interpretable model) @ https://goo.gl/5JcZFY
* 정형데이터를 위한 인공신경망 모델, TabNet (Google Cloud AI, feature selection & interpretability) @ https://j.mp/38ABU8e

> 모델 해석 가능성 vs 설명 가능성

> active learning
10만장 중 만장을 선택해 정답을 달 때 어떤 애들을 달아줄지

> 41p
선형대수, 행렬 잘 표현하는 유튜브 >   
Essence of linear algebra @ https://goo.gl/O79Wsx   
Essence of calculus @ https://goo.gl/3KHqk6

* 3Blue1Brown 한국어 번역 시리즈 @ https://j.mp/3939TGO
* 수학전공자가 추천하는 유튜브 수학 강의 목록 @ http://j.mp/2QiFDj5
* 머신러닝 & 딥러닝 분야별 추천 서적 리스트 @ https://j.mp/3q1CGCV
* Statistics 110 : Probability from Harvard (커넥트 재단, 한글) @ https://j.mp/3uhcOVp
* Introduction to linear algebra for ML (Matrix Factorization, SVD, Embedding, 추천시스템, PCA +@) @ https://j.mp/2UGa0EM
* Machine Learning Roadmap 2020 (분석 프로세스별 노하우/정의/자료링크 등) @ https://j.mp/335sVeg & https://j.mp/3hMY9Li

* 데이터과학자와 데이터엔지니어를 위한 인터뷰 문답집 (책, 매우 세부적인 MLDL 관련 Q&A) @ https://j.mp/2ZX7wAV

> 논문 자료
* PR12 (Youtube, 논문읽기모임) @ https://j.mp/2FDR6Xz
* Papers You Must Read (by 고려대 Data Science & Business Analytics 연구실)@ https://j.mp/3259sIy -> 고려대 석사 들어오자마자 읽어야할 논문

> 45p
* 모두를 위한 머신러닝/딥러닝 강의
* 머신러닝 용어집 (Google ML Crash course) @ https://goo.gl/Q4bYbz

> 70p
* XOR solvable activation function helps DNNs @ http://j.mp/2ZSz0ar
* Dendritic action potentials and computation in human layer 2/3 cortical neurons @ http://j.mp/2ZQbnPC

* http://playground.tensorflow.org/

* Deep learning에서의 Kernel trick, Feature crosses @ http://j.mp/2p5CbO2

* RAdam (Rectified-Adam) @ http://j.mp/2qzRjUa & http://j.mp/2N322hu
* AdaBound (using dynamic bound of learning rate) @ http://j.mp/2VAo3Lz
* AdaBelief (Adapting stepsizes by the belief in observed gradients) @ https://j.mp/3iQEBaL

* ONNX (Open Neural Network Exchange Format) @ https://goo.gl/nvJ8TH & https://goo.gl/GYJze7 + ONNX 첫걸음 (eBook) @ https://j.mp/2ZLJwkK
* How to run PyTorch models in the browser with ONNX.js @ https://j.mp/3bP8qFf
오닉스: 인공신경망 모델을 pytorch에서 tensorflow, keras로 끌고와서 사용할 수 있게

* 우리가 볼 수 없는 데이터로 모델을 학습시킬 수 있을까?(DEVIEW2020, Privacy preserving AI / PySyft / Federated Learning) @ https://j.mp/2LVNyD0

* 얼굴 탐지 Android 앱 개발 (TF Lite & ML Kit) @ https://j.mp/2SKkbaB
* TF Lite Model Maker Examples (이미지분류, 텍스트분류, BERT QA) @ https://j.mp/3xly26w
* On-Device ML Examples by Google (세부 과제별 Android/iOS/tf.js 소스 코드 포함) @ https://j.mp/3chnMDC

* Papers with Code: Methods (딥러닝 관련 기법 분야별 논문 & 구현 모음) @ https://j.mp/329FcxD   
-> 이미지에 자막 등 과제 별로 구현된 코드 모음

* Deep Learning State of the Art (MIT, 2019) @ http://j.mp/2vhAkF3
* AI 기능구현 웹사이트 & 생활 속 AI 사례 모음 @ https://j.mp/2XWYDpN

> 인공지능 분야
1. CV(Computer Vision)
2. NLP(자연어)
3. Audio
+ RL (강화학습)

사물 검출   
후보 영역 추출 > CNN   
이미지를 픽셀 단위로 하면 너무 큼 > CNN이 대안

> CNN
* 이미지에 (세타) 필터(3x3) > 같은 위치(픽셀)에 있는 것들끼리 곱함
* 곱해진 값을 더함 > 새 도화지 위에 더한 값을 넣어줌
* 필터를 한칸씩 이동시키며 더한 값으로 도화지 채움 > 이미지의 특징을 찾아냄
* 필터 결과 도화지를 Feature Map
* 서로 다른 특징을 잡아놓은 이미지가 64장 > 픽셀을 줄여줌
* <<< Convolutional Layer

* Pooling Layer >>>
* Feature Map을 그대로 가져가지 않고 4칸 지정해서 최댓값만 살림
* Max(Average)-Pooling

* 하나의 세트로 구성된 레이어

* CPR -> FC(Fully-Connected == Dense) -> Output Layer

* Transpool Learning 할 때 FC 전까지만 가져옴

* 3x3: 필터 사이즈 (지정)   
* 필터를 이동시키는 작업: 윈도우 슬라이딩
* 이미지 바깥쪽에 0을 채우고 필터 >
* 원본이랑 feature map의 크기가 동일하게 유지: zero padding

# CNN 링크
* https://yceffort.kr/2019/01/29/pytorch-3-convolutional-neural-network  (상단 이미지)
https://towardsdatascience.com/intuitively-understanding-convolutions-for-deep-learning-1f6f42faee1 (중반부 * 필터 이미지)
* http://taewan.kim/post/cnn/ (필터 계산 예시, RGB 채널 적용 예시, Pooling 계산 예시 <- 쉬운 한글 설명)
* https://setosa.io/ev/image-kernels/ (필터별 적용 결과 예시)

* https://poloclub.github.io/cnn-explainer/ (필터 & 풀링 구체적인 계산 예시 <- 구체적인 계산)
* https://www.slideshare.net/yongho/ss-79607172 (개념 이해용 자료)
* https://www.youtube.com/playlist?list=PLl1irxoYh2wzOOU9hvJqMYc215wAlxrpp (개념 이해용 자료)

* CNN 네모가 크기 때문에 픽셀 단위로
* -> Image Segmentation

* HuggingFace (Pytorch, Tensorflow)

> BERT

* 한국언론진흥재단, 빅카인즈 기사 기반 AI 언어모델 ‘KPF-BERT’ 공개 (2022) @ https://bit.ly/35uBdQC
* 금융 언어 이해를 위해 개발된 ALBERT 톺아보기 with Transformers (KB-ALBERT, PyCon Korea 2020) @ https://j.mp/2G3y0dO

> GPT
* Transformer 모델
* https://blog.naver.com/PostView.nhn?blogId=krugmanpaul&logNo=222218829812
* 텍스트가 들어오면 내부적으로 학습하여 번역된 결과 내보냄
* 크게 두쪽(전반부: encoder, 후반부: decoder)
* encoder: 문장을 이해하기 위해 학습
* decoder: 이해한 문장을 바탕으로 문장 생성

* The Illustrated GPT-2 (Visualizing Transformer Language Models) @ http://j.mp/2Mx4f74 + GPT-2-simple @ http://j.mp/32DOhN8
* KoGPT(KakaoBrain) @ https://j.mp/3qXZpmL + KoGPT2 (SKT) @ http://j.mp/3bp5378 & http://j.mp/2uzUxJv & https://j.mp/3aYYTct

* Awesome GPT-3 (a collection of demos and articles about the OpenAI GPT-3 API) @ https://j.mp/2ELqjbv + GPT Crush @ https://gptcrush.com/
* GPT-3 based Text2Code examples : (React-app) @ https://j.mp/2WALBhN / (LaTeX) @ https://j.mp/2WBnRdA / (JSX) @ https://j.mp/3jiKsoX
* (new & advanced) Screenshot-to-code @ https://goo.gl/tmMJSj & https://goo.gl/xKoQaw + AlphaCode Attention Visualization @ https://bit.ly/3rneqyf

> VSCode
* Serenade Voice 말하면 코드를 짤 수 있게

* Github Copilot

* OpenAI Codex (the model that powers GitHub Copilot) @ https://j.mp/3tP1qB5
* (OpenAI) DALL·E 2 @ https://t.ly/LjMf

* 세상에 없는 사람들 - 인간을 대체할 디지털 인간 @ https://j.mp/3hHgxos

* AI-Colorized Korea, 1900 @ https://bit.ly/37xJJzj
* AI-Colorized Atomic Bomb Cannon test @ https://j.mp/3k7dTK2

* U-GAT-IT: Unsupervised Generative Attentional Networks with Adaptive Layer-Instance Normalization for Image-to-Image Translation @ https://j.mp/3hP5xWa

* 네이버웹툰, AI 자동채색 서비스 출시 @ https://j.mp/3q2Gc2Q

* Nvidia Inpainting Demo @ https://bit.ly/3rL5LWe
* Adobe Remove objects with Content-Aware Fill @ https://j.mp/2HiB8mx
* Photoshop’s AI neural filters can tweak age and expression with a few clicks @ https://j.mp/34iPInc

* Super resolution 구현 파이썬 라이브러리 Image Super-Resolution (ISR)@ http://j.mp/2PPCwOR

* A Deeper Look Into The Life of An Impressionist (deepfakes of celebrities) @ http://j.mp/2NsDHll
* Fake video of President Barack Obama @ https://goo.gl/xU1jTc + Very realistic Tom Cruise Deepfake @ https://j.mp/3zO6JTH

* 20 different ways AI could be used by criminals over the next 15 years @ https://j.mp/2EYL3ML
* Thieves are now using AI deepfakes to trick companies into sending them money @ http://j.mp/2PB8MpQ
* How to recognize fake AI-generated images @ http://j.mp/2H5NNqi & http://j.mp/2H7C7DE & http://j.mp/2H5RFru
* Fakebox (Detector for fake news) @ https://machinebox.io/docs/fakebox

* Soundraw (AI Music Generator for creators) @ https://j.mp/3biJhTH
* OpenAI Jukebox (genre/artist/lyrics -> generates music with singing & raw audio, PyTorch) @ https://j.mp/2W94HvN

* Soundraw: 저작권 회파하기 위해 비슷한 음악을 작곡

* 립싱크만으로 말 알아듣는 AI, 음성인식 넘어 무성인식 @ https://j.mp/2GNOx67
* 머스크의 뇌과학 스타트업 '뉴럴링크', 생각만으로 비디오 게임 하는 원숭이 공개 @ https://j.mp/3ebOduA
* Neural networks translated a paralyzed man’s brainwaves into conversational phrases @ https://j.mp/3wTRMgh

* FastAutoAugment by Kakao brain @ https://bit.ly/3K8wRga

* Albumentations 라이브러리
* Augment 작업 편하게

* Albumentations (fast augmentations based on highly-optimized OpenCV library) @ https://goo.gl/GYKK4y & https://j.mp/2J7Enej

* CutMix (data augmentation method proposed by Clova AI Research) @ http://j.mp/2Q0hBaA & http://j.mp/2WhJSjD
* Test Time Augmentation and how to perform it with Keras @ http://j.mp/2NtlVli & http://j.mp/2NqVVXH (+ http://j.mp/2Nnu8an)

> 실습 5-1

* Conv2D -> Condulutional Layer 2D
* input_shape: 한 장 이미지에 대한 차원
* flatten 쓰면 input_shape가 필요 없음
* 컬러 이미지: (28,28,3) -> 3채널
* (3,3) -> kernel size
* (kernel_regularizer -> L1,L2 규제)

* tf.keras preprocessing layers (with examples) @ https://j.mp/3ksCIl8

* Label smoothing, When Does Label Smoothing Help? @ https://j.mp/337naLv & https://j.mp/3lYi1Oq

> `validation_data=test_generator`
- 데이터가 다 나눠져 있다면 train data는 놔두고 validation_data를 따로 넣어줌
