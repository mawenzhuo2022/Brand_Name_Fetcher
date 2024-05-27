# -*- coding: utf-8 -*-
# @Author  : Wenzhuo Ma
# @Time    : 2024/5/27 11:06
# @Function: Fetches brand names in various languages from Wikipedia pages for multiple brands.

import requests
from bs4 import BeautifulSoup
import os
import json


def get_brand_names_from_wikipedia(brand_page_url):
    """
    Fetches the brand names in various languages from a Wikipedia page.
    Parameters:
    - brand_page_url: The URL of the Wikipedia page to fetch.
    Returns:
    A dictionary with language codes as keys and brand names as values.
    """
    response = requests.get(brand_page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    interlanguage_links = soup.find_all('a', class_='interlanguage-link-target')
    brand_names = {}
    for link in interlanguage_links:
        language_code = link['hreflang']
        brand_name = link.text.strip()
        brand_names[language_code] = brand_name
    return brand_names


def main():
    brands = {
        'Cisco': 'https://en.wikipedia.org/wiki/Cisco_Systems',
        'Huawei': 'https://en.wikipedia.org/wiki/Huawei',
        'H3C': 'https://en.wikipedia.org/wiki/H3C_Technologies',
        'HP': 'https://en.wikipedia.org/wiki/HP_Inc.',
        'Microsoft': 'https://en.wikipedia.org/wiki/Microsoft'
    }

    # Create the directory for storing results if it does not exist
    results_dir = '../dat/results'
    os.makedirs(results_dir, exist_ok=True)

    # Fetching the brand names for each brand and save to file
    for brand, url in brands.items():
        print(f"\nFetching names for brand: {brand}")
        brand_names = get_brand_names_from_wikipedia(url)

        # Save results to a JSON file named after the brand
        file_path = os.path.join(results_dir, f'{brand}.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(brand_names, f, ensure_ascii=False, indent=4)

        print(f'Results for {brand} saved to {file_path}')


if __name__ == "__main__":
    main()
