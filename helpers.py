import os
from bs4 import BeautifulSoup
from urllib.parse import unquote

html_cache = {}


def get_order(article, target, articles_path):
    print(article)
    if article not in html_cache:
        filepath = os.path.join(articles_path, article[0].lower(), f"{article}.htm")
        with open(filepath, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            links = soup.find_all(
                "a", href=lambda href: href and href.startswith("../../wp/")
            )
            # links_a = [(tag, tag['href']) for tag in soup.find_all('a', href=lambda href: href and href.startswith("../../wp/"))]
            # links_area = [(tag, tag['href']) for tag in soup.find_all('area', href=lambda href: href and href.startswith("../../wp/"))]
            # all_links = sorted(links_a + links_area, key=lambda x: soup.encode_contents(x[0]))
            html_cache[article] = links

    order = [
        i
        for i, link in enumerate(html_cache[article], start=1)
        if target.lower() in unquote(link["href"].lower())
    ]

    return int(order[0]) if order else None
