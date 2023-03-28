import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_product(product_name):
    # create a dictionary to store product details
    product_dict = {}

    # scrape Amazon
    amazon_url = "https://www.amazon.com/s?k=" + product_name.replace(' ', '+')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    amazon_page = requests.get(amazon_url, headers=headers)
    amazon_soup = BeautifulSoup(amazon_page.content, 'html.parser')
    amazon_results = amazon_soup.find_all(
        'div', {'data-component-type': 's-search-result'})

    # check if there are any results on Amazon
    if len(amazon_results) > 0:
        amazon_first_result = amazon_results[0]
        amazon_product_name = amazon_first_result.find('h2').text.strip()
        amazon_product_price = amazon_first_result.find(
            'span', {'class': 'a-offscreen'}).text.strip()
        amazon_product_rating = amazon_first_result.find(
            'span', {'class': 'a-icon-alt'}).text.strip()
        product_dict['Amazon'] = {'Name': amazon_product_name,
                                  'Price': amazon_product_price, 'Rating': amazon_product_rating}
    else:
        product_dict['Amazon'] = {
            'Name': 'No results found', 'Price': 'N/A', 'Rating': 'N/A'}

    # scrape Best Buy
    bestbuy_url = "https://www.bestbuy.com/site/searchpage.jsp?st=" + \
        product_name.replace(
            ' ', '%20') + "&_dyncharset=UTF-8&_dynSessConf=-959860077563872441"
    bestbuy_page = requests.get(bestbuy_url)
    bestbuy_soup = BeautifulSoup(bestbuy_page.content, 'html.parser')
    bestbuy_results = bestbuy_soup.find_all('div', {'class': 'list-item'})

    # check if there are any results on Best Buy
    if len(bestbuy_results) > 0:
        bestbuy_first_result = bestbuy_results[0]
        bestbuy_product_name = bestbuy_first_result.find('h4').text.strip()
        bestbuy_product_price = bestbuy_first_result.find(
            'div', {'class': 'priceView-hero-price priceView-customer-price'}).text.strip()
        bestbuy_product_rating = bestbuy_first_result.find(
            'span', {'class': 'sr-only'}).text.strip()
        product_dict['Best Buy'] = {'Name': bestbuy_product_name,
                                    'Price': bestbuy_product_price, 'Rating': bestbuy_product_rating}
    else:
        product_dict['Best Buy'] = {
            'Name': 'No results found', 'Price': 'N/A', 'Rating': 'N/A'}

    # scrape Walmart
    walmart_url = "https://www.walmart.com/search/?query=" + \
        product_name.replace(' ', '+')
    walmart_page = requests.get(walmart_url)
    walmart_soup = BeautifulSoup(walmart_page.content, 'html.parser')
    walmart_results = walmart_soup.find_all(
        'div', {'class': 'search-result-gridview-item-wrapper'})

    # check if there are any results on Walmart
    if len(walmart_results) > 0:
        walmart_first_result = walmart_results[0]
        walmart_product_name = walmart_first_result.find(
            'div', {'class': 'search-result-product-title'}).text.strip()
        walmart_product_price = walmart_first_result.find(
            'span', {'class': 'search-result-product-price'}).text.strip()
        walmart_product_rating = walmart_first_result.find(
            'span', {'class': 'stars-container'})['aria-label']
        product_dict['Walmart'] = {'Name': walmart_product_name,
                                   'Price': walmart_product_price, 'Rating': walmart_product_rating}
    else:
        product_dict['Walmart'] = {
            'Name': 'No results found', 'Price': 'N/A', 'Rating': 'N/A'}

    # convert product details dictionary to a pandas dataframe
    product_df = pd.DataFrame.from_dict(product_dict, orient='index')

    # filter out products with no results
    product_df = product_df[product_df['Name'] != 'No results found']

    # convert price column to a numeric data type
    product_df['Price'] = product_df['Price'].str.replace(
        '$', '', regex=True).str.replace(',', '').astype(float)

    # calculate a score for each product based on price and rating
    product_df['Score'] = product_df['Rating'].str.split(
    ).str[0].astype(float) * product_df['Price']

    # recommend the product with the highest score
    # recommended_product = product_df.iloc[product_df['Score'].idxmax()]
    if not product_df.empty:
        recommended_product = product_df.iloc[product_df['Score'].idxmax()]

        # print the product details and recommendation
        print(product_df)
        print('\nRecommended product: ' +
              recommended_product['Name'] + ' from ' + recommended_product.name)
    else:
        print(product_dict)


scrape_product(input('Enter product name: '))
