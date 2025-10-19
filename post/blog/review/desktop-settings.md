---
layout: post
title: 가벼운 딥러닝용 조립PC 후기
date: 2022-09-01 19:58:46 +0900
categories: [Blog, Review]
tags: [Desktop, i5-12600K, RTX 3060, Fractal Design, 컴퓨존]
---

# 구매 계기

매번 딥러닝 모델을 학습하는 실험을 하면서 Colab에 의존하는 방식에 불편함을 느꼈는데,   
결국 190발을 사용해서 RTX 3060이 포함된 조립 PC를 구매했습니다.

이번 기회에 혼자서 컴퓨터를 조립해봤으면 좋았겠지만,   
여기에 많은 시간을 쏟을만한 상황도 아니었고 이쪽이 고장날 일도 없어서 맡겼습니다.

컴퓨터 조립 업체로 다나와, 피씨팩토리 등을 고려했는데,   
현금 결제를 권장하는 부분이 미심쩍었고 컴퓨존의 평이 좋아 믿고 맡겼습니다.

# 부품 선정

## 그래픽 카드

처음엔 약 100만원을 얹어서 RTX 3090Ti을 구매할 생각이었지만,   
당시 소득이 없는 상황이라 저렴한 가격의 RTX 3060을 구매했습니다.   
Colab에서 RoBERTa 등의 모델을 돌리면서 15GB의 VRAM이 고갈되어 배치 사이즈를 줄인 경험이 있어   
상대적으로 적은 12GB VRAM의 RTX 3060 제품이 불안하긴 했습니다.   
하지만, 당장엔 큰 모델을 돌릴 예정이 없고 그래픽 카드를 교체하는게 어렵지는 않기 때문에   
향후 확장성을 고려하는 방향으로 저사양의 제품을 구매했습니다.

## 파워

다만, 파워의 경우 교체가 쉽지 않기 때문에 향후 그래픽 카드를 교체할 것을 고려해 850W로 선택했고,   
WiFi 보드, 강화유리가 없는 케이스를 필수 요건으로 삼아   
퀘이사존을 통해 부품에 대한 정보를 탐색했습니다.

## 메인보드

메인보드로는 인텔용 B660 보드를 선택했는데,   
구매하고 보니 썬더볼트 독과 연결할만한 고속 포트가 존재하지 않아 아쉬웠습니다.   
이점은 충분히 고려하지 못하고 결정한 문제입니다.

## 케이스

케이스는 프랙탈 디자인 사의 Torrent Compact 제품을 구매했는데,   
강화유리가 안달린 제품들의 가격이 대체로 비싼 편이어서 이왕이면 취향에 맞는 제품으로 선택했습니다.   

## 기타 부품

게임이 목적은 아니었기 때문에 CPU는 적당한 인텔 사 제품을 골랐고,   
관리의 불편함 때문에 CPU용 쿨러로 DEEPCOOL 사의 공랭 쿨러를 선택했습니다.

램, SSD, HDD는 각각 마이크론, 하이닉스, WD 사의 제품을 선택했습니다.   
마찬가지로 크게 중요한 부품은 아니었기 때문에 유명한 것으로 골랐습니다.

# 컴퓨존 조립

컴퓨존에 견적 신청을 한 후 당일날 조립이 완료되었다는 답변을 받았습니다.   
용산에서 택배가 발송되고 다음날 아래와 같은 사진을 전달받았습니다.

![compuzone-1](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/compuzone-1.jpg?raw=true)

|||
|:-:|:-:|
|![compuzone-2](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/compuzone-2.jpg?raw=true)|![compuzone-3](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/compuzone-3.jpg?raw=true)|

제품 배송도 주문 후 하루 내지 이틀 사이에 도착한 것으로 기억합니다.   
컴퓨터 자체도 스티로폼이랑 완충재로 단단히 감싸져 있어 배송 상태에 만족했습니다.

# 제품 수령 및 확인

각 제품의 박스는 찌그러짐 없이 잘 배송되었는데, 겉박스가 살짝 과대포장이 아닌가 생각했습니다.   
컴퓨터는 아래 사진과 같이 내부까지 완충재로 보호된 상태로 배송되었습니다.

|||
|:-:|:-:|
|![desktop-1](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/desktop-1.jpg?raw=true)|![desktop-2](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/desktop-2.jpg?raw=true)|

완충재를 걷어내니 그래픽 카드의 아름다운 자태가 눈에 들어왔습니다.   
개인적으로 RGB를 선호하지는 않기 때문에 제품 그 자체를 보는 것만으로 행복감을 느꼈습니다.

![desktop-3](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/desktop-3.jpg?raw=true)

케이스도 개인 취향에 살짝 비싼 제품을 구매했는데 이렇게 다시 보니 잘 샀다고 생각합니다.   
특히 케이스 정면의 Y자 형태의 디자인이 매력적입니다.

![desktop-4](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/desktop-4.jpg?raw=true)

별도의 수작업 없이 바로 컴퓨터를 실행시켰는데 한가지 아쉬웠던 점은 쿨러 소리가 너무 시끄러웠던 것입니다.   
특별히 불량이 있는 것은 아니고 단순히 쿨러의 RPM이 높게 느껴졌던 건데   
메인보드에서 CPU 쿨러의 속도를 조절해도 변화가 없어 각각의 쿨러를 확인해보니   
케이스 쿨러에서 제어가 이루어지지 않는 문제가 있었습니다.

제가 조립한 제품이 아니어서 다 뜯어보기도 난감했는데   
다행히 가장 의심쩍었던 팬 허브와 관련해 찾아보면서 메인보드와 연결 문제가 있을 것이라 짐작하게 되었고,   
팬 허브의 PWM 포트가 메인보드가 아닌, 동일 허브의 FAN4 포트에 연결되어 있었습니다.   
황당하긴 하지만 정상적으로 연결 후 조용히 돌아가는 모습을 보니 만족했습니다.

![fan-hub](https://github.com/minyeamer/til/blob/main/.media/blog/review/desktop-settings/fan-hub.jpg?raw=true)

현재는 우분투를 탑재해 장남감으로서 재밌게 가지고 놀고 있습니다.   
M1 맥북을 유일한 PC로 사용하면서 가끔씩 호환성에 불편함을 느꼈었는데   
리눅스 시스템과 함께 VMware 상에서 윈도우를 운영하면서 더이상 그러한 걱정을 할 필요가 없어졌습니다.   
무엇보다 가장 만족스러운건 터미널에서 `nvidia-smi` 명령어를 입력했을 때   
표시되는 그래픽 카드의 상태를 확인하는 것입니다.

적지않은 지출이었지만 그 이상으로 만족한 경험이었습니다.
