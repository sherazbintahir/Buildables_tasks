from bs4 import BeautifulSoup
import os
import pandas as pd

d = {'title': [], 'price': [], 'link': []}

for file in os.listdir('selenium/data'):
    try:
        with open(f"selenium/data/{file}", encoding="utf-8") as f:
            html_doc = f.read()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        cards = soup.find_all("div", class_="puis-card-container")
        
        for card in cards:
            # Extract title
            title_tag = card.find("h2")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            link_tag = card.find("a", class_="a-link-normal")
            link = "https://www.amazon.com" + link_tag['href'] if link_tag else "N/A"
            
            price_tag = card.find("span", class_="a-price-whole")
            price = price_tag.get_text(strip=True) if price_tag else "N/A"
            
            d['title'].append(title)
            d['price'].append(price)
            d['link'].append(link)    
    except Exception as e:
        print(e)

df = pd.DataFrame(d)
df.to_csv('selenium/data/amazon_products.csv')
print("Data collection complete. CSV file created.")

