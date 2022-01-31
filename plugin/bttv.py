import requests

BASE_URL = 'https://api.betterttv.net/3/emotes/shared/'
SEARCH_ENDPOINT = 'search'
TOP_ENDPOINT = 'top'
CDN_URL = 'https://cdn.betterttv.net/emote/{id}/{size}.{ext}'
MIN_QUERY_LEN = 3


def get_img_url(emote, size='1x'):
    """
    Return emote image url
    """
    return CDN_URL.format(id=emote['id'], ext=emote['imageType'], size=size)

def _request(endpoint, **kwargs):
    url = BASE_URL + endpoint
    headers = {
        'accept': 'json',
        'accept-language': 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=headers, **kwargs)
    data = response.json()
    if isinstance(data, dict):
        return []
    return response.json()

def search_emotes(search_term, limit=25):
    params = (
        ('query', search_term),
        ('limit', limit),
    )
    return _request(SEARCH_ENDPOINT, params=params)

def top_emotes(limit=25):
    params = (
        ('offset', '0'),
        ('limit', limit),
    )
    return _request(TOP_ENDPOINT, params=params)
