import re
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook


def build_search_url(query: str) -> str:
    params = {
        "where": "nexearch",
        "sm": "top_hty",
        "fbm": "0",
        "ie": "utf8",
        "query": query,
    }
    return "https://search.naver.com/search.naver?" + urlencode(params)


def get_soup(url: str) -> BeautifulSoup:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.naver.com/",
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_news_items(soup: BeautifulSoup):
    card_selectors = [
        # New Naver news portal desktop structure
        "div.fender-news-portal-container-desk div.fds-news-item-list-desk > div.sds-comps-vertical-layout.sds-comps-full-layout",
        # Legacy / fallback structures
        "div.group_news li.bx",
        "ul.list_news > li",
        "div.news_area",
        "div.news_wrap.api_ani_send",
    ]

    cards = []
    for selector in card_selectors:
        found = soup.select(selector)
        if found:
            cards = found
            break

    results = []

    for card in cards:
        title_tag = (
            card.select_one("a[data-heatmap-target='.tit']")
            or card.select_one("a.news_tit")
            or card.select_one("a.api_txt_lines.total_tit")
            or card.select_one("a[href]")
        )
        if not title_tag:
            continue

        title = title_tag.get_text(" ", strip=True)
        link = title_tag.get("href", "").strip()

        desc_tag = (
            card.select_one("a[data-heatmap-target='.body']")
            or card.select_one("div.news_dsc .dsc_txt_wrap")
            or card.select_one("a.api_txt_lines.dsc_txt_wrap")
            or card.select_one("div.dsc_wrap")
            or card.select_one("div.news_dsc")
        )
        summary = desc_tag.get_text(" ", strip=True) if desc_tag else ""

        press = ""
        date = ""

        info_tags = card.select(
            "span.sds-comps-profile-info-subtext, "
            "div.news_info div.info_group span.info, "
            "div.news_info div.info_group a.info, "
            "span.info"
        )
        info_texts = [tag.get_text(" ", strip=True) for tag in info_tags if tag.get_text(" ", strip=True)]

        press_tag = (
            card.select_one("a[data-heatmap-target='.prof'] span")
            or card.select_one(".sds-comps-profile-info-title-text span")
            or card.select_one("a.info.press, span.press, a.news_office")
        )
        if press_tag:
            press = press_tag.get_text(" ", strip=True)
        elif info_texts:
            press = info_texts[0]

        for text in info_texts:
            if re.search(r"(전$|\\d{4}\\.\\d{1,2}\\.\\d{1,2}\\.?$)", text):
                date = text
                break

        if press == "네이버뉴스":
            press = ""

        results.append(
            {
                "title": title,
                "link": link,
                "press": press,
                "date": date,
                "summary": summary,
            }
        )

    dedup = {}
    for item in results:
        if item["link"]:
            dedup[item["link"]] = item

    return list(dedup.values())


def main():
    query = "반도체"
    url = build_search_url(query)

    soup = get_soup(url)
    news_items = extract_news_items(soup)

    print(f"[검색어] {query}")
    print(f"[수집 건수] {len(news_items)}")
    print("-" * 80)

    for index, item in enumerate(news_items, 1):
        print(f"{index}. 제목: {item['title']}")
        print(f"   링크: {item['link']}")
        print(f"   언론사: {item['press']}")
        print(f"   날짜: {item['date']}")
        print(f"   요약: {item['summary']}")
        print("-" * 80)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "news"

    headers = ["title", "link", "press", "date", "summary"]
    sheet.append(headers)

    for item in news_items:
        sheet.append([
            item.get("title", ""),
            item.get("link", ""),
            item.get("press", ""),
            item.get("date", ""),
            item.get("summary", ""),
        ])

    workbook.save("naver_result.xlsx")

    print("엑셀 저장 완료: naver_result.xlsx")


if __name__ == "__main__":
    main()
