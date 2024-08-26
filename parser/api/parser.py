import time
import json
from datetime import datetime
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from .managers import AdsManager as am
from .models import Imovirtual
from .serializers import ImovirtualSerializer

class ExpiredAd(Exception):
    pass  

options = Options()
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-extensions")
options.add_argument("--dns-prefetch-disable")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-dev-shm-usage")
# options.binary_location = 'home/parsival/google-chrome-stable_current_amd64.deb'
# options.add_argument('--headless')
# options.add_argument("--remote-debugging-pipe")
# options.add_argument("--proxy-server='direct://'")

IMOVIRTUAL_URL = 'https://www.imovirtual.com/en/comprar/apartamento/?locations%5B0%5D%5Bregion_id%5D=11&locations%5B0%5D%5Bsubregion_id%5D=163&locations%5B1%5D%5Bregion_id%5D=11&locations%5B1%5D%5Bsubregion_id%5D=162'
URLS_FILE = 'imovirtual_urls.json'
DATA_FILE = 'imovirtual_data.json'


class Parser:
    source_name = None
    prefix = "https://"
    data_file = None
    urls_file = None

    def __init__(self, url) -> None:
        self.url = url
        self.raw_data = []
        self.data = []
        self.driver = webdriver.Chrome
   


    def add_prefix(self, url):
        if not "https://" in url:
            url = self.prefix + url
        return url

    def raw_data_normalisation_file(self, filepath):
        with open(filepath, 'r') as file:
            urls = json.load(file)

        checked_urls = [self.add_prefix(url) for url in urls]
        self.write_to_file('normalised_data.json', checked_urls)

    def raw_data_normalisation(self):
        urls = [self.add_prefix(url) for url in self.raw_data]
        self.raw_data = urls

    def open_page(self, url=None) -> webdriver:
        url = self.url if not url else url
        driver = webdriver.Chrome()
        return driver.get(url)

    def parse_page(self, page: webdriver.Chrome) -> BeautifulSoup:
        time.sleep(random.randint(4, 10))
        soup = BeautifulSoup(page.page_source, 'html.parser')
        return soup

    def find_many(self, tag, filter, page: BeautifulSoup, **kwargs) -> list:
        res = page.find_all(tag, attrs=filter, **kwargs)
        return res

    def extract_attribute(self, el, attr):
        return el[attr]

    def extract_attributes(self, el, attr):
        res = []
        for _ in el:
            extracted = self.extract_attribute(_, attr)
            res.append(extracted)
        return res

    def combined_extraction(self, tag, filter, attr, page, **kwargs) -> list:
        list_of_tags = self.find_many(tag, filter, page, **kwargs)
        list_of_attributes = self.extract_attributes(list_of_tags, attr)
        return list_of_attributes

    def data_formatter(self, url):
        data = {'date_of_extraction': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'extracted_from': self.source_name,
                'ad_url': url}
        return data

    def remove_double_urls(self):
        data = []
        for url in self.raw_data:
            if not url in data:
                data.append(url)

        self.raw_data = data

    def normalize_ad(self, ad):
        raise NotImplementedError
    
    def adds_extraction(self):
        raise NotImplementedError
    
    def data_extraction(self): 
        raise NotImplementedError

    def insert_to_db(self):
        with open('../extracted_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.data = data

        rng = range(0, len(self.data)+1)
        while True:
            try:
              for i in rng:
                ad = self.normalize_ad(self.data[i])
                type_ = ad['extracted_from']
                model = self.models[type_]
                inst = model(**ad)
                inst.save()
            except IndexError:
                break
            
    def write_to_file(self, filename='extracted_data.json', d=None, mode='w'):
        data = d
        if d == 'data':
            data = self.data
        if d == 'raw':
            data = self.raw_data
        with open(filename, mode, encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Data has been written to {filename}")


class ImovirtualParser(Parser):
    count = 0
    source_name = 'Imovirtual'
    data_file = DATA_FILE
    urls_file = URLS_FILE
    not_provided = 'Not provided'
    charfield_keys = Imovirtual.charfield_keys()

    def click_onetrust_button(self, driver:webdriver.Chrome):
        time.sleep(2.5)
        accept_btn = driver.find_element(
            By.ID, "onetrust-accept-btn-handler")
        if accept_btn:
            accept_btn.click()

    def normalize_imovirtual(self, ad:dict):
        try:
            coord = ad.pop('coordinates')
            ad['coordinates_latitude'] = coord['latitude']
            ad['coordinates_longitude'] = coord['longitude']
            ad['rooms'] = 0 if ad['rooms'] == 'zero' else int(ad['rooms'])
            ad['bathrooms'] = int(''.join(filter(str.isdigit, ad['bathrooms']))) if ad['bathrooms'] else 0
            ad['description'] = BeautifulSoup(ad['description'], 'html.parser').get_text(separator=' ', strip=True)
            
            ad['gross_area'] = self.not_provided if not ad.get('gross_area') else ad['gross_area']
            ad['condition'] = self.not_provided if not ad.get('condition') else ad['condition']
            ad['market_type'] = self.not_provided if not ad.get('market_type') else ad['market_type']
            for key in self.charfield_keys:
                ad[key] = self.not_provided if not ad.get(key) else ad[key]
        except KeyError:
            pass
        return ad
    
    def get_ad_from_props(self, data, props, values):
        int_data = data
        int_props = props
        int_values = values

        for k, v in int_values:
            current_level = int_props
            for key in v:
                try:
                    current_level = current_level[key]
                except (KeyError, TypeError):
                    current_level = None
                    break
            if isinstance(current_level, list):
                int_data[k] = ', '.join(current_level)
            else:
                int_data[k] = current_level

        ad = self.normalize_imovirtual(int_data)
        return ad
    
    def get_and_save_new_ad(self, data, props, values):
        ad = self.get_ad_from_props(data, props, values)

        serializer = ImovirtualSerializer(data=ad)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
        else: 
            print(serializer.errors)
            return
        self.count += 1
        print(f"Extracted ad: {self.count}")

    def get_and_update_existing_ad(self, data, props, values, existing_ad:Imovirtual):
        extracted_ad = self.get_ad_from_props(data, props, values)
        if existing_ad.price != extracted_ad['price']:
            existing_ad.price = extracted_ad['price']
            existing_ad.price_per_sqm = extracted_ad['price_per_sqm']
            existing_ad.save()
            self.data.append(existing_ad)
            self.count += 1
            print(f"Extracted and updated ad: {self.count}")
        else:
            self.count += 1
            print(f"Ad exists and not changed:{self.count}")
        

    def get_page_props(self, driver):
        attrs = {'id': '__NEXT_DATA__'}
        parsed_page = self.parse_page(driver)
        expired_attr = {'data-cy': 'expired-ad-alert'}
        if parsed_page.find('div', expired_attr):
            raise ExpiredAd
        raw_props = parsed_page.find(
                    'script', attrs).string
        if not raw_props:
            time.sleep(2)
            parsed_page = self.parse_page(driver)
            raw_props = parsed_page.find(
                    'script', attrs).string
        props_content = raw_props.replace(
                '{props:', '{').rstrip('</script>').strip()
        props_dict = json.loads(props_content)
        props = props_dict['props']['pageProps']['ad']
        return props

    def urls_extraction(self):
        url = self.url
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        try:
            self.click_onetrust_button(driver)
        except NoSuchElementException:
            pass
        except ElementClickInterceptedException:
            self.click_onetrust_button(driver)

        while True:
            try:
                time.sleep(1.5)
                parsed_page = self.parse_page(driver)
                extracted_data = self.combined_extraction(
                          'a', 
                          {'data-tracking': "click_body", 
                          'data-tracking-data': '{"touch_point_button":"title"}'}, 
                          'href', 
                          parsed_page)
                self.raw_data.extend(extracted_data)
                time.sleep(random.randint(2, 7))
                next_button = driver.find_element(
                    By.CSS_SELECTOR, '[data-dir="next"]')
                if next_button.get_attribute('class') == 'disabled':
                    print('Extraction is ended')
                    break  
                next_button.click()
            except NoSuchElementException:
                print('Extraction is ended')
                break
            except ElementClickInterceptedException:
                self.click_onetrust_button(driver)
                next_button.click()

        driver.quit()
        self.raw_data_normalisation()
        self.remove_double_urls()
        self.write_to_file(self.urls_file, 'raw')

    def data_extraction(self):
        self.urls_extraction()
        with open(self.urls_file, 'r') as file:
            self.raw_data = json.load(file)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        for url in self.raw_data:
            try:
                driver.get(url)
                self.click_onetrust_button(driver)
            except NoSuchElementException:
                pass
            except WebDriverException:
                driver.quit()
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                try:
                    self.click_onetrust_button(driver)
                except NoSuchElementException:
                    pass

            try:
                props = self.get_page_props(driver)
            except AttributeError:
                continue
            except ExpiredAd:
                ad = Imovirtual.get_ad_by_url(url)
                if ad: 
                    ad.delete()
                    print('Inactive ad deleted')
                continue

            data = self.data_formatter(url)         
            ad = Imovirtual.get_ad_by_url(url)
            if ad: 
                values = (('price', ('target', 'Price')),
                          ('price_per_sqm', ('target', 'Price_per_m')))
                self.get_and_update_existing_ad(data, props, values, ad)
                continue

            values = (('title', ('title',)),
                      ('market_type', ('market',)),
                      ('description', ('description',)),
                      ('advert_type', ('advertType',)),
                      ('features', ('features',)),
                      ('area', ('target', 'Area')),
                      ('gross_area', ('target', 'Gross_area')),
                      ('bathrooms', ('target', 'Bathrooms_num')),
                      ('rooms', ('target', 'Rooms_num')),
                      ('condition', ('target', 'Condition')),
                      ('energy_certificate', ('target', 'Energy_certificate')),
                      ('price', ('target', 'Price')),
                      ('price_per_sqm', ('target', 'Price_per_m')),
                      ('property_type', ('target', 'ProperType')),
                      ('owner_name', ('owner', 'name')),
                      ('owner_phones', ('owner', 'phones')),
                      ('agency_name', ('agency', 'name')),
                      ('agency_phones', ('agency', 'phones')),
                      ('city', ('location', 'address', 'city', 'name')),
                      ('county', ('location', 'address', 'county', 'name')),
                      ('province', ('location', 'address', 'province', 'name')),
                      ('coordinates', ('location', 'coordinates'))
                    )
            self.get_and_save_new_ad(data, props, values)

        driver.quit()
        am.create_and_save_history()
        print('End of extraction')

