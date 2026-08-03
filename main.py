import requests
from bs4 import BeautifulSoup
import csv
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

if not products:
    print("No products were found on the page. The site structure may have changed.")
    exit()

exp_product_value = 0
exp_product_name = ""

che_product_value = 1000000000000
che_product_name = ""

average = 0

with open('products.csv', mode='w', newline='') as archive:

    archive_writer = csv.writer(archive)
    archive_writer.writerow(['title', 'price_usd', 'price_brl', 'rating', 'reviews'])

    if products:
        for product in products:
            new_list = []

            price = (product.find(itemprop="price")).text.replace('$', "")
            price_converted = round(float(price) * usd_rate, 2)
            title = (product.find(class_='title')).get('title')
            rating = (product.find(class_='ratings')).find('p', attrs={'data-rating': True}).get('data-rating')
            review = (product.find(class_='review-count')).find(itemprop="reviewCount").text

            new_list.extend([title, price, price_converted, rating, review])

            archive_writer.writerow(new_list)

            if price_converted >= exp_product_value:
                exp_product_value = price_converted
                exp_product_name = title


            if price_converted <= che_product_value:
                che_product_value = price_converted
                che_product_name = title

            average += price_converted


        print("\n\n     SUMMARY     ")
        print("-----------------")
        print(f"Total products: {len(products)}")
        print(f"Most expensive: {exp_product_name} - R${exp_product_value}")
        print(f"Cheapest: {che_product_name} - R${che_product_value}")
        print(f"Average ticket in BRL: {round(average/len(products), 2)}")
        
    else:
        print("There are no products in this page")

