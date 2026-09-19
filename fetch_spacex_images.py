import requests


api_url = "https://commons.wikimedia.org/w/api.php"

params = {
    "action": "query",
    "generator": "search",
    "gsrsearch": "Starlink 17-38",
    "gsrnamespace": 6,
    "gsrlimit": 10,
    "prop": "imageinfo",
    "iiprop": "url",
    "format": "json",
}

proxies = {
    "http": "socks5h://127.0.0.1:10808",
    "https": "socks5h://127.0.0.1:10808",
}

headers = {
    "User-Agent": "space-photos-training-project/1.0"
}

response = requests.get(
    api_url,
    params=params,
    proxies=proxies,
    headers=headers,
)
response.raise_for_status()

response_data = response.json()

pages = response_data["query"]["pages"].values()

image_urls = []

for page in pages:
    image_url = page["imageinfo"][0]["url"]
    image_urls.append(image_url)

print(image_urls)