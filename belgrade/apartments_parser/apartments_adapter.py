from typing import Iterator

import requests
from bs4 import BeautifulSoup, PageElement
from datetime import date, timedelta


class Apartment:
    id: str
    title: str
    description: str
    link: str
    placement: str
    price: str
    owner: str
    date_published: str
    features: list[str]


class ApartmentsAdapter:
    def __init__(self):
        self.processed_apartments_ids: dict[str, bool] = {}
        self.request_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ('
                                              'KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
        self.max_pages = 100

    def get_apartments(self) -> Iterator[list[Apartment]]:
        processed_ids: list[str] = []
        apartments: list[Apartment] = []

        current_date = date.today().strftime('%d.%m.%Y')
        date_before = (date.today() - timedelta(days=1)).strftime('%d.%m.%Y')

        for page in range(1, self.max_pages):
            apartments.clear()
            response = None

            try:
                response = requests.get(
                    'https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd?page=' + str(page),
                    headers=self.request_headers,
                    timeout=15)
            except Exception as e:
                print('An error occurred while getting page: ' + str(e))

            bs = BeautifulSoup(response.text, 'html.parser')

            for apart_block in bs.find_all('div', {'class': 'product-item'}):
                apartment = Apartment()

                try:
                    apartment_id = self.__get_apartment_id(apart_block)
                    date_published = self.__get_apartment_publish_date(apart_block)

                    if date_published != current_date and date_published != date_before:
                        continue

                    if self.processed_apartments_ids.get(apartment_id):
                        continue

                    apartment.id = apartment_id
                    apartment.date_published = date_published
                    apartment.title = self.__get_apartment_title(apart_block)
                    apartment.description = self.__get_apartment_description(apart_block)
                    apartment.placement = self.__get_apartment_placement(apart_block)
                    apartment.price = self.__get_apartment_price(apart_block)
                    apartment.owner = self.__get_apartment_owner(apart_block)
                    apartment.features = self.__get_apartment_features(apart_block)
                    apartment.link = self.__get_apartment_link(apart_block)

                    if len(self.processed_apartments_ids.keys()) != 0:
                        apartments.append(apartment)

                    processed_ids.append(apartment_id)
                except Exception as err:
                    print('An error occurred while parsing page: ' + str(err))

            print('Processed page #{0}'.format(page))
            yield apartments

        new_processed_ids = (processed_ids + list(self.processed_apartments_ids.keys()))[:3000]
        self.processed_apartments_ids.clear()

        for processed_id in new_processed_ids:
            self.processed_apartments_ids[processed_id] = True

    @staticmethod
    def __get_apartment_id(apart_block: PageElement) -> str:
        return apart_block.attrs["data-id"]

    @staticmethod
    def __get_apartment_title(apart_block: PageElement) -> str:
        title_wrapper = apart_block.find_all_next('h3')[0]
        return title_wrapper.find_all_next('a')[0].text

    @staticmethod
    def __get_apartment_description(apart_block: PageElement) -> str:
        description_wrapper = apart_block.find_all_next('p', {'class': 'product-description'})[0]
        return description_wrapper.text

    @staticmethod
    def __get_apartment_link(apart_block: PageElement) -> str:
        title_wrapper = apart_block.find_all_next('h3')[0]
        link_wrapper = title_wrapper.find_all_next('a')[0]

        return 'https://www.halooglasi.com' + link_wrapper['href']

    @staticmethod
    def __get_apartment_placement(apart_block: PageElement) -> str:
        places_list_wrapper = apart_block.find_all_next('ul', {'class': 'subtitle-places'})[0]
        places_list = places_list_wrapper.findChildren()
        places = map(lambda place: place.text.strip(), places_list)

        return ', '.join(places)

    @staticmethod
    def __get_apartment_price(apart_block: PageElement) -> str:
        price_wrapper = apart_block.find_all_next('div', {'class': 'central-feature-wrapper'})[0]
        price = price_wrapper.find_all_next('i')[0]

        return price.text

    @staticmethod
    def __get_apartment_owner(apart_block: PageElement) -> str:
        owner_wrapper = apart_block.find_all_next('span', {'data-field-name': 'oglasivac_nekretnine_s'})[0]
        return owner_wrapper.text.strip()

    @staticmethod
    def __get_apartment_publish_date(apart_block: PageElement) -> str:
        date_wrapper = apart_block.find_all_next('span', {'class': 'publish-date'})[0]
        return date_wrapper.text.strip('.')

    @staticmethod
    def __get_apartment_features(apart_block: PageElement) -> list[str]:
        res: list[str] = []

        features_wrapper = apart_block.find_all_next('ul', {'class': 'product-features'})[0]
        features = features_wrapper.findChildren(recursive=False)

        for feature in features:
            res_feature = ''

            value_wrapper = feature.find_all_next('div', {'class': 'value-wrapper'})

            if len(value_wrapper) == 0:
                continue

            value = value_wrapper[0].text
            legend = value_wrapper[0].find_all_next('span', {'class': 'legend'})[0]

            res_feature += legend.text
            res_feature += ': '
            res_feature += value.replace(legend.text, '')

            res.append(res_feature)

        return res
