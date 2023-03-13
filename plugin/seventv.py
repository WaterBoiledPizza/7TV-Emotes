import requests

GQL_URL = "https://7tv.io/v3/gql"
REST_URL = "https://7tv.io/v3/emotes/{id}"
CDN_URL = 'https://cdn.7tv.app/emote/{id}/{size}.{ext}'
EMOTE_URL = 'https://7tv.app/emotes/{id}'
MIN_QUERY_LEN = 1


def get_img_url(emote, size='1x'):
    """
    Return emote image url
    """
    file_ext = "webp"
    return CDN_URL.format(id=emote['id'], ext=file_ext, size=size)

def get_emote_url(emote, size='1x'):
    """
    Return emote url
    """
    return EMOTE_URL.format(id=emote['id'])

def _request(search="", category="TOP", limit=30):
    query = {
        "operationName": "SearchEmotes",
        "variables": {
            "query": search,
            "limit": limit,
            "page": 1,
            "sort": {
                "value": "popularity",
                "order": "DESCENDING"
            },
            "filter": {
                "category": category,
                "exact_match": False,
                "case_sensitive": False,
                "ignore_tags": True,
                "zero_width": False,
                "animated": False,
                "aspect_ratio": ""
            }
        },
        "query": "query SearchEmotes($query: String!, $page: Int, $sort: Sort, $limit: Int, $filter: EmoteSearchFilter) {\n  emotes(query: $query, page: $page, sort: $sort, limit: $limit, filter: $filter) {\n    count\n    items {\n      id\n      name\n      state\n      trending\n      owner {\n        id\n        username\n        display_name\n        style {\n          color\n          paint_id\n          __typename\n        }\n        __typename\n      }\n      flags\n      host {\n        url\n        files {\n          name\n          format\n          width\n          height\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }

    response = requests.post(GQL_URL, json=query)
    data = response.json()
    data = data['data']['emotes']['items']
    if isinstance(data, dict):
        return []
    return data


def search_emotes(search_term):
    return _request(search=search_term)


def trending_emotes():
    return _request(category="TRENDING_DAY")


if __name__ == "__main__":
    # result = search_emotes("Fridge")
    # result = isAnimated("61fc0f1123f0a55b0ba8313d")
    result = trending_emotes()
    print(result)
