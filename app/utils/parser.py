# app/utils/parser.py
import random

import httpx
from bs4 import BeautifulSoup
from typing import Optional


async def fetch_page(url: str) -> Optional[str]:
    """Загружает HTML-страницу по указанному URL."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            print(f"Ошибка при загрузке страницы {url}: {e}")
            return None


async def extract_price(html: str) -> Optional[float]:
    soup = BeautifulSoup(html, "html.parser")

    # Пример: ищем элемент с классом 'price'
    price_tag = soup.find(class_="price")
    if not price_tag:
        return None

    try:
        price_text = price_tag.get_text(strip=True).replace(",", ".")
        return float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
    except (ValueError, AttributeError):
        return None


async def get_price_from_url(url: str) -> Optional[float]:
    """Основная функция для получения цены по URL."""
    return round(random.uniform(100, 200), 2)
    # TODO: для тестов пока так :)
    html = await fetch_page(url)
    if not html:
        return None
    return await extract_price(html)


# для тестов
def sync_extract_price(html: str) -> Optional[float]:
    import asyncio
    return asyncio.run(extract_price(html))
