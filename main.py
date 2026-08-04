import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def is_status_code_200(url: str):

    try: 
        response = requests.get(url, timeout = 5)
        response.raise_for_status()

        return response
    
    except requests.exceptions.ConnectionError:
        print("There is a connection error (internet, DNS...). Please, try it later.")
        exit()

    except requests.exceptions.Timeout:
        print("Your request tried for so long and got timed out. Plese, try it later.")
        exit()

    except requests.exceptions.HTTPError as error:
        print(f"Your request returned {error}")
        exit()

parser = argparse.ArgumentParser()
parser.add_argument('--option', choices=['laptops', 'tablets', 'phones'], default='laptops')
args = parser.parse_args()

categories = {
    'laptops': 'computers/laptops',
    'tablets': 'computers/tablets',
    'phones': 'phones/touch'
}

category = categories[args.option]

usd_rate = is_status_code_200(url = 'https://api.frankfurter.dev/v2/rates?base=USD&quotes=BRL')
html_doc = is_status_code_200(url = f'https://webscraper.io/test-sites/e-commerce/allinone/{category}')

usd_rate = usd_rate.json()[0]['rate']
html_doc = html_doc.text

soup = BeautifulSoup(html_doc, 'html.parser')
products = soup.find_all(class_='product-wrapper')

if products:
    new_list = []

    for product in products:
        

        price = (product.find(itemprop="price")).text.replace('$', "")
        price_converted = round(float(price) * usd_rate, 2)
        title = (product.find(class_='title')).get('title')
        rating = (product.find(class_='ratings')).find('p', attrs={'data-rating': True}).get('data-rating')
        review = (product.find(class_='review-count')).find(itemprop="reviewCount").text

        new_list.append({'title': title, 'price_usd': price, 'price_brl': price_converted, 'rating': rating, 'reviews': review})

    df = pd.DataFrame(new_list)
    df.to_csv('products.csv', index=False)

    most_expensive_product_line = df.loc[df['price_brl'].idxmax()]
    cheapest_product_line = df.loc[df['price_brl'].idxmin()]

    print("\n\n     SUMMARY     ")
    print("-----------------")
    print(f"Total products: {len(products)}")
    print(f"Most expensive: {most_expensive_product_line['title']} - R${most_expensive_product_line['price_brl']}")
    print(f"Cheapest: {cheapest_product_line['title']} - R${cheapest_product_line['price_brl']}")
    print(f"Average ticket in BRL: {round(df['price_brl'].mean(), 2)}")
    
else:
    print("There are no products in this page.")

