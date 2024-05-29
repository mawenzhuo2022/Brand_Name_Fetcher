# -*- coding: utf-8 -*-
# @Author  : Wenzhuo Ma
# @Time    : 2024/5/27 11:06
# @Function: Fetches brand names in various languages from Wikipedia pages for multiple brands.

import requests
from bs4 import BeautifulSoup
import spacy
import os
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载NLP模型
nlp = spacy.load('en_core_web_sm')
logging.info("NLP model loaded.")


def fetch_page(url):
    """获取指定URL的HTML内容"""
    try:
        response = requests.get(url)
        logging.info(f"Successfully fetched page: {url}")
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching page {url}: {e}")
        return None


def extract_ner(text):
    """使用spaCy从文本中提取专有名词"""
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ == 'ORG']
    logging.info(f"Extracted {len(entities)} organizations.")
    return entities


def find_language_versions(name, languages=['en', 'zh']):
    """查找维基百科中给定名称的不同语言版本的链接及其翻译"""
    try:
        search_url = f"https://en.wikipedia.org/wiki/{name.replace(' ', '_')}"
        content = fetch_page(search_url)
        if content:
            soup = BeautifulSoup(content, 'html.parser')
            versions = {}
            for lang in languages:
                lang_link = soup.find('a', class_='interlanguage-link-target', hreflang=lang)
                if lang_link:
                    lang_page = fetch_page(lang_link['href'])
                    if lang_page:
                        lang_soup = BeautifulSoup(lang_page, 'html.parser')
                        lang_title = lang_soup.find('h1', id='firstHeading').text
                        versions[lang] = {'url': lang_link['href'], 'title': lang_title}
            logging.info(f"Found language versions for {name}: {versions}")
            return versions
        return {}
    except Exception as e:
        logging.error(f"Error processing {name}: {e}")
        return {}

def main():
    brands = {
        'Cisco': 'https://en.wikipedia.org/wiki/Cisco_Systems',
        # 添加其他品牌如需要
    }

    results_dir = '../dat/fetched'
    os.makedirs(results_dir, exist_ok=True)
    logging.info("Results directory checked/created.")

    for brand, url in brands.items():
        logging.info(f"Starting processing for brand: {brand}")
        html_content = fetch_page(url)
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text()
            entities = extract_ner(text)

            results = {}
            for entity in entities:
                links = find_language_versions(entity)
                if links:
                    results[entity] = links

            file_path = os.path.join(results_dir, f'{brand}.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            logging.info(f"Results for {brand} saved to {file_path}")

if __name__ == '__main__':
    main()
