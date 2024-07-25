import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def scrape_jumia_deals():
    names = []
    old_prices = []
    new_prices = []
    review_ratings = []
    review_counts = []
    discounts = []

    for i in range(1, 50):
        url = f"https://www.jumia.co.ke/mlp-top-deals/?page={i}#catalog-listing"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        response = requests.get(url, headers = headers)
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = soup.find_all('article', attrs = {'class': 'prd _fb _p col c-prd'})

        for result in results:
            # Product name
            try:
                names.append(result.find('div', attrs={"class": "info"}).find('h3').text)
            except:
                names.append(None)

            # Old product price
            try:
                original_price = result.find('div', attrs={"class": "old"}).text
                old_prices.append(int(re.sub(r'[^\d]', '', original_price)))
            except:
                old_prices.append(None)

            # New price
            try:
                current_price = result.find('div', class_='info').find('div', class_='prc').text.strip()
                new_prices.append(int(re.sub(r'[^\d]', '', current_price)))
            except:
                new_prices.append(None)

            # Product Discount
            try:
                discounts.append(result.find('div', class_='info').find('div', class_='bdg _dsct _sm').text.strip())
            except:
                discounts.append(None)

            # Product rating
            try:
                rating = result.find('div', class_='info').find('div', class_='rev').find('div').text.strip()
                review_ratings.append(float(re.search(r'\d+\.\d+', rating).group()))
            except:
                review_ratings.append(None)

            # Ratings count
            try:
                ratings_cnt = result.find('div', class_='info').find('div', class_='rev').text.strip()
                match = re.search(r'\((\d+)\)', ratings_cnt)
                review_counts.append(int(match.group(1)))
            except:
                review_counts.append(None)

    return names, old_prices, new_prices, review_ratings, review_counts, discounts

def save_to_csv(names, old_prices, new_prices, review_ratings, review_counts, discounts, filename='Jumia-Deals-2.csv'):
    data = {
        'Product Name': names,
        'Old Price': old_prices,
        'New Price': new_prices,
        'Discount': discounts,
        'Rating': review_ratings,
        'Ratings Count': review_counts
    }

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    names, old_prices, new_prices, review_ratings, review_counts, discounts = scrape_jumia_deals()
    save_to_csv(names, old_prices, new_prices, review_ratings, review_counts, discounts)
    print("Data has been saved to Jumia-Deals-2.csv")