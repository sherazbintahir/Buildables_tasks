import asyncio
import json
import pandas as pd
import os
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

async def extract_amazon_products():
    url = "https://www.amazon.com/s?k=iphone"
    pages = 26

    browswer_config = BrowserConfig(browser_type="chromium", headless=True)

    crawler_config = CrawlerRunConfig(
        extraction_strategy=JsonCssExtractionStrategy(
            schema={
                "name": "Amazon product search result",
                "baseSelector": "[data-component-type='s-search-result']",
                "fields": [
                    {"name": "title", "selector": "h2 span", "type": "text"},
                    {"name": "image", "selector": ".s-image", "type": "attribute", "attribute": "src"},
                    {"name": "rating", "selector": ".a-icon-alt", "type": "text"},  # <-- fixed
                    {"name": "reviews_count", "selector": ".s-link-style .s-underline-text", "type": "text"},
                    {"name": "price", "selector": ".a-price .a-offscreen", "type": "text"},
                ]
            }
        )
    )

    all_products = []

    async with AsyncWebCrawler(config=browswer_config) as crawler:
        for page in range(1, pages + 1):
            page_url = f"{url}&page={page}"
            print(f"\n Scraping page {page}: {page_url}")

            result = await crawler.arun(url=page_url, config=crawler_config, cache_mode=CacheMode.BYPASS)

            if result and result.extracted_content:
                try:
                    products = json.loads(result.extracted_content)
                    print(f" Found {len(products)} products on page {page}")
                    all_products.extend(products)
                except json.JSONDecodeError:
                    print(f" Failed to parse page {page}")

    os.makedirs("dt", exist_ok=True)

    df = pd.DataFrame(all_products)
    df.to_csv("dt/amazon_products.csv", index=False, encoding="utf-8")
    print(" Data saved to dt/amazon_products.csv")

    for product in all_products[:3]:
        print("\n Product Details:")
        print(f"Title:  {product.get('title')}")
        print(f"Price: {product.get('price')}")
        print(f"Rating: {product.get('rating')}")
        print(f"Image: {product.get('image')}")
        print(f"Review Count: {product.get('reviews_count')}")
        print("-" * 80)


if __name__ == "__main__":
    asyncio.run(extract_amazon_products())
