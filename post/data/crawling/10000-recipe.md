---
layout: post
title: "[Python] 만개의 레시피 데이터 수집"
date: 2023-03-26 18:52:14 +0900
categories: ["Data", "Crawling"]
tags: ["Crawling", "Python", "requests", "만개의레시피"]
---

최근 레시피 생성을 목적으로 한 사이드 프로젝트에 참여하게 되었는데   
모델 학습을 위한 만개의 레시피 데이터 크롤링을 진행해보았습니다.

# 스키마 구성

기존엔 레시피 명칭과 음식 재료 정보만을 수집할 계획이었지만,   
만개의 레시피의 각 페이지를 살펴보면서 추가적으로 가져갈만한 데이터가 있음을 확인하여   
우선적으로 테이블 관계 및 스키마를 구성해보았습니다.

![schema](https://github.com/minyeamer/til/blob/main/.media/data/crawling/10000-recipe/schema.png?raw=true)

초기에 만개의 레시피와 공공데이터를 데이터 소스로 삼았기 때문에,   
만개의 레시피에 대한 DB `_10000`, 공공데이터에 대한 DB `food`로 구성했습니다.

`_10000` DB 내 테이블은 만개의 레시피 내 각각의 페이지에서 가져온 데이터로 구성되며,   
크게 카테고리, 레시피, 사용자 단위로 구분할 수 있습니다.

# 만개의 레시피 데이터 수집

크롤링에서 데이터 요청 및 가공을 위해 정의된 유틸리티 함수들이 있는데,   
별도로 코드를 보여주지는 않고 해당 함수가 호출될 때 간단히 어떤 동작을 하는지만 전달드립니다.

## 카테고리 추출

만개의 레시피 카테고리는 레시피 검색 페이지에서 간단하게 추출할 수 있으므로,   
개발자 도구 또는 requests에 대한 응답에서 카테고리에 해당하는 부분을 가져옵니다.   
여기서 `get_headers()` 함수는 `User-Agent` 등 기본적인 브라우저 정보가 담긴 헤더를 반환합니다.

```python
url = "https://www.10000recipe.com/recipe/list.html"
headers = get_headers(url, referer=url)
headers["upgrade-insecure-requests"] = '1'
response = session.get(url, params=params, headers=headers)
source = BeautifulSoup(response.text, "html.parser")

cate_list = source.select_one("div.cate_list")
pattern = "javascript:goSearchRecipe([\d\w()',]+)"
raw_cat = [(re_get(pattern, cat.attrs["href"]),cat.text) for cat in cate_list.select("a") if "href" in cat.attrs]
cat_map = lambda catType, catId, catName: {"categoryId":catId, "categoryType":catType, "categoryName":catName}
categories = [cat_map(*literal_eval(data), name) for data, name in raw_cat]
categories = pd.DataFrame(categories)
categories = categories[categories["categoryId"]!='']
categories.head()
```

데이터 수집 결과 아래와 같은 구조의 데이터를 획득할 수 있습니다.

|categoryId|categoryType|categoryName|
|:-:|:-:|:-:|
|63|cat4|밑반찬|
|56|cat4|메인반찬|
|54|cat4|국/탕|
|55|cat4|찌개|
|60|cat4|디저트|

## 레시피 목록 추출

레시피 검색 페이지는 검색어, 정렬 기준, 페이지, 카테고리를 쿼리로 받습니다.   
레시피 목록을 추출하는데 검색어나 카테고리는 필요하지 않고 동일한 정렬 기준에서 수집하기 때문에   
데이터 수집 시에는 페이지에 반복문을 적용하여 데이터가 존재하는 범위를 가져올 것입니다.

```python
ORDER_MAP = {"정확순":"accuracy", "최신순":"date", "추천순":"reco"}
get_params = lambda **kwargs: {k:v for k,v in kwargs.items() if v}
uri = "https://www.10000recipe.com/recipe/"

def fetch(session: requests.Session, query=str(), sortType="추천순", page=1,
        cat1=str(), cat2=str(), cat3=str(), cat4=str(), **kwargs) -> List[str]:
    url = uri+"list.html"
    params = get_params(q=query, order=ORDER_MAP[sortType], page=page,
                        cat1=cat1, cat2=cat2, cat3=cat3, cat4=cat4)
    headers = get_headers(url, referer=url)
    headers["upgrade-insecure-requests"] = '1'
    response = session.get(url, params=params, headers=headers)
    return parse(response.text, **kwargs)

def parse(response: str, **kwargs) -> List[str]:
    source = BeautifulSoup(response, 'html.parser')
    uris = source.select("a.common_sp_link")
    ids = [uri.attrs["href"].split('/')[-1] for uri in uris if "href" in uri.attrs]
    return ids
```

데이터 수집 결과로는 문자열 타입의 레시피 ID 목록을 획득할 수 있습니다.

## 레시피 정보 추출

레시피 ID로 접근할 수 있는 레시피 상세 정보 페이지에서   
레시피 정보에 대한 데이터를 추출합니다.
소스코드 내에서 레시피 정보가 JSON 형식으로 존재하기 때문에   
일일히 HTML 태그를 파싱할 필요 없이 데이터를 한번에 JSON 오브젝트로 가져올 수 있습니다.

데이터를 가공하는 `map_recipe()` 함수 내에서   
`cast_int()`는 데이터를 정수형으로 변환할 때 에러가 발생하면 기본값 0을 반환하는 함수이고,   
`hier_get()`은 중첩 딕셔너리의에 단계별 키 목록에 대한 값을 안전하게 가져오기 위한 함수입니다.

```python
uri = "https://www.10000recipe.com/recipe/"

def fetch(session: requests.Session, recipeId: str, **kwargs) -> Dict:
    url = uri+recipeId # https://www.10000recipe.com/recipe/6997297
    headers = get_headers(url, referer=uri+"list.html")
    headers["upgrade-insecure-requests"] = '1'
    response = session.get(url, headers=headers)
    return parse(response.text, recipeId, **kwargs)

def parse(response: str, recipeId: str, **kwargs) -> Dict:
    source = BeautifulSoup(response, 'html.parser')
    raw_json = source.select_one("script[type=\"application/ld+json\"]").text
    try: data = json.loads(raw_json)
    except: data = literal_eval(raw_json)
    return map_recipe(data, recipeId, source, **kwargs)

def map_recipe(data: Dict, recipeId: str, source=None, **kwargs) -> Dict:
    recipe_info = {"recipeId": recipeId}
    recipe_info["name"] = data.get("name")
    recipe_info["author"] = hier_get(data, ["author","name"])
    recipe_info["ratingValue"] = cast_int(hier_get(data, ["aggregateRating","ratingValue"]))
    recipe_info["reviewCount"] = cast_int(hier_get(data, ["aggregateRating","reviewCount"]))
    recipe_info["totalTime"] = data.get("totalTime")
    recipe_info["recipeYield"] = data.get("recipeYield")
    try: recipe_info["recipeIngredient"] = ','.join(data["recipeIngredient"])
    except: recipe_info["recipeIngredient"] = extract_ingredient(source, **kwargs)
    recipe_info["recipeInstructions"] = '\n'.join(
        [step.get("text",str()) for step in data.get("recipeInstructions",list())
            if isinstance(step, dict)])
    recipe_info["createDate"] = data.get("datePublished")
    return recipe_info

def extract_ingredient(source: Tag, **kwargs) -> str:
    cont_ingre = source.select_one("div.cont_ingre")
    if cont_ingre:
        return [ingre.split() for ingre in cont_ingre.select_one("dd").text.split(',')]
    else: return str()
```

데이터 수집 결과 아래와 같이 정리된 딕셔너리를 얻을 수 있습니다.

```python
{
    "recipeId": "6997297",
    "name": "두부짜조",
    "author": "호이호이",
    "ratingValue": 5,
    "reviewCount": 1,
    "totalTime": "PT20M",
    "recipeYield": "1 servings",
    "recipeIngredient": "두부 30g,라이스페이퍼 2장,돼지고기 5g,...",
    "recipeInstructions": "부위는 상관없지만 저는 저렴하고...",
    "createDate": "2023-02-19T13:37:04+09:00"
}
```

실질적으로 활용할 데이터는 레시피명 `name`과 재료명인 `recipeIngredient`이며,   
평점, 리뷰 수, 조리순서 등도 추가적인 분석을 통해 활용성을 기대해볼 수 있습니다.

## 요리 후기 추출

동일한 레시피 상세 정보 페이지에서 요리 후기에 대한 데이터를 추출할 수 있습니다.

단, 요리 후기는 JSON 형식으로 정리되어 있지 않기 때문에   
HTML 소스를 파싱하여 대상 문자열을 추출해야 합니다.

데이터를 가공하는 `map_review()` 함수 내에서   
`re_get()`은 정규표현식 패턴에 매칭되는 문자열을 추출하는 함수이고,   
`select_text()`는 BeautifulSoup 태그에서   
CSS Selector로 안전하게 문자열을 추출하는 함수입니다.

```python
GENDER = {"info_name_m":"M", "info_name_f":"F"}
uri = "https://www.10000recipe.com/recipe/"
rid_ptn = "replyReviewDiv_(\d+)"
uid_ptn = "/profile/review.html\?uid=([\d\w]+)"
date_ptn = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"

def fetch(session: requests.Session, recipeId: str, **kwargs) -> List[Dict]:
    url = uri+recipeId
    headers = get_headers(url, referer=uri+"list.html")
    headers["upgrade-insecure-requests"] = '1'
    response = session.get(url, headers=headers)
    return parse(response.text, recipeId, **kwargs)

def parse(response: str, recipeId: str, **kwargs) -> List[Dict]:
    source = BeautifulSoup(response, 'html.parser')
    reply_divs = source.select("div.view_reply")
    review_div = [div for div in reply_divs if div.select_one("div.reply_tit").text.strip().startswith("요리 후기")]
    if review_div:
        review_list = review_div[0].select("div.reply_list")
        return [map_review(review, recipeId, **kwargs) for review in review_list]
    else: return list()

def map_review(data: Tag, recipeId: str, **kwargs) -> Dict:
    review_info = dict()
    review_info["reviewId"] = re_get(rid_ptn, data.select("div")[-1].attrs.get("id"))
    review_info["recipeId"] = recipeId
    review_info["userId"] = re_get(uid_ptn, data.select_one("a").attrs.get("href"))
    review_info["contents"] = select_text(data, "p.reply_list_cont")
    detail = data.select_one("h4.media-heading")
    if detail:
        review_info["userName"] = select_text(detail, "b")
        gender = detail.select_one("b").attrs.get("class")
        review_info["userGender"] = GENDER.get(gender[0]) if gender else None
        review_info["createDate"] = re_get(date_ptn, detail.text)
    return review_info
```

데이터 수집 결과 아래와 같이 정리된 딕셔너리를 얻을 수 있습니다.

여기서 요리 후기와 별도로 사용자 명칭과 성별을 추출할 수 있습니다.

```python
{
    "reviewId": "395018",
    "recipeId": "6843136",
    "userId": "58031746",
    "contents": "정말 간단한데 중불로하니 좀 태워먹었... 맛은 있네욬ㅋㅋㅋㅋㅋ다음엔 중불이랑 약불 사이로 함 더해바야겠어욬ㅋㅋㅋㄱㅋㅋ감삼둥..♡♡",
    "userName": "나찡as",
    "userGender": "F",
    "createDate": "2020-11-09 17:14:02"
}
```

## 댓글 추출

레시피 상세 정보 페이지에서 댓글은 미리보기만이 제공되며   
전체 댓글을 확인하기 위해서는 별도의 페이지에 접속해야 합니다.

해당 페이지의 출력 결과에서도 요리 후기와 같은 방식으로   
HTML 소스를 파싱하여 대상 문자열을 추출해야 합니다.

```python
GENDER = {"info_name_m":"M", "info_name_f":"F"}
uri = "https://www.10000recipe.com/recipe/"
cid_ptn = "replyCommentDiv_(\d+)"
uid_ptn = "/profile/recipe_comment.html\?uid=([\d\w]+)"
date_ptn = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2})"

def fetch(session: requests.Session, recipeId: str, page=1, **kwargs) -> List[Dict]:
    url = uri+"ajax.html"
    params = dict(q_mode="getListComment", seq=recipeId, page=page)
    headers = get_headers(url, referer=uri+recipeId)
    headers["upgrade-insecure-requests"] = '1'
    response = session.get(url, params=params, headers=headers)
    return parse(response.text, recipeId, **kwargs)

def parse(response: str, recipeId: str, **kwargs) -> List[Dict]:
    source = BeautifulSoup(response, 'html.parser')
    comment_list = source.select("div.reply_list")
    return [map_comment(comment, recipeId, **kwargs) for comment in comment_list]

def map_comment(data: Tag, recipeId: str, **kwargs) -> Dict:
    comment_info = dict()
    comment_info["commentId"] = re_get(cid_ptn, data.select("div")[-1].attrs.get("id"))
    comment_info["recipeId"] = recipeId
    comment_info["userId"] = re_get(uid_ptn, data.select_one("a").attrs.get("href"))
    comment_info["contents"] = select_text(data, "div.media-body").split('|')[-1]
    detail = data.select_one("h4.media-heading")
    if detail:
        comment_info["userName"] = select_text(detail, "b")
        gender = detail.select_one("b").attrs.get("class")
        comment_info["userGender"] = GENDER.get(gender[0]) if gender else None
        comment_info["createDate"] = re_get(date_ptn, detail.text)
    return comment_info

review = fetch(session, "6843136")
review[0]
```

데이터 수집 결과 아래와 같이 정리된 딕셔너리를 얻을 수 있습니다.

데이터 구조는 요리 후기와 동일합니다.

```python
{
    "commentId": "39693405",
    "recipeId": "6843136",
    "userId": "89382542",
    "contents": "신고그러네여..재료양이..ㅜ",
    "userName": "휘아여",
    "userGender": "F",
    "createDate": "2022-03-18 00:02"
}
```
