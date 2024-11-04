import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options
import os
import random
import tldextract
from tqdm import tqdm


class WebScraper:
    def __init__(self, saving_path, get_subdomain=True):
        self.saving_path = saving_path
        self.get_subdomain = get_subdomain
        self.chrome_options = Options()

        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument("--no-sandbox")
        # self.chrome_options.add_argument("--disable-dev-shm-usage")

    def _get_text(self, url, id, index):
        try:
            driver = webdriver.Chrome(self.chrome_options)  
            driver.get(url)

            full_html = driver.execute_script("return document.documentElement.outerHTML;")
            soup = BeautifulSoup(full_html, 'html.parser')

            # Loại bỏ tất cả các thẻ HTML, chỉ giữ lại nội dung văn bản
            text_only = soup.get_text()
            text_only = ' '.join(text_only.split(' '))
            cleaned_text = '\n'.join(filter(None, text_only.split('\n')))

            # Save the text to a file
            output_file = f"{self.saving_path}/{id}/{index}.txt"
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

            print(f"url: {url} \n Saved: {output_file}")

        except requests.exceptions.RequestException as e:
            driver.quit()
            print(f"Error fetching the page: {e}")

    def _find_subdomains(self, url):
        try:
            try:
                response = requests.get(url)
                response.raise_for_status()
            
                soup = BeautifulSoup(response.text, 'html.parser')
                sub_link = set()

                for link in soup.find_all('a', href=True):
                    if len(link['href']) > 1:
                        link_url = link['href']
                        if "http" in link_url:
                            sub_link.add(link_url)
                        if link_url.startswith("/"):
                            path_url = f'{url}{link_url[1:]}'
                            sub_link.add(path_url)

                return sub_link
            except:
                driver = webdriver.Chrome(self.chrome_options)  
                driver.get(url)

                full_html = driver.execute_script("return document.documentElement.outerHTML;")
                soup = BeautifulSoup(full_html, 'html.parser')

                sub_link = set()

                for link in soup.find_all('a', href=True):
                    if len(link['href']) > 1:
                        link_url = link['href']
                        if "http" in link_url:
                            sub_link.add(link_url)
                        if link_url.startswith("/"):
                            path_url = f'{url}{link_url[1:]}'
                            sub_link.add(path_url)
                return sub_link

        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return set()

    def process_url_subdomain(self, url, id):
        # Get sub-domains from main domain
        sub_link = self._find_subdomains(url)
        sub_link = [x for x in sub_link if len(x) > 0]
        random.shuffle(sub_link)

        extracted_info = tldextract.extract(url)
        main_domain = extracted_info.domain

        print("url: ", url)
        print("sub_domains in url: ", len(sub_link))

        count = 0
        # Get text from the main domain
        self._get_text(url, id, count)
        count += 1
        
        if self.get_subdomain:
            process_sub_link = [i for i in sub_link if tldextract.extract(i).domain == main_domain]

            if len(process_sub_link) > 0:
                for path_url in process_sub_link:
                    if count <= 6:
                        try:
                            self._get_text(path_url, id, count)
                            count += 1
                        except:
                            continue
                    else:
                        break

            print("=" * 50)

    def process_url(self, url, id, count):
        print("url: ", url)
        # Get text from the main domain
        self._get_text(url, id, count)
