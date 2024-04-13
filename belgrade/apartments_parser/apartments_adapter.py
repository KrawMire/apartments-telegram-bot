import requests
from bs4 import BeautifulSoup, PageElement


class Apartment:
    title: str
    description: str
    link: str
    placement: str
    price: str
    owner: str
    date_published: str
    features: list[str]


class ApartmentsAdapter:
    def get_apartments(self) -> list[Apartment]:
        response = requests.get('https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd',
                                headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'})
        bs = BeautifulSoup(response.text, 'html.parser')
        apartments: list[Apartment] = []

        for apart_block in bs.find_all('div', {'class': 'product-item'}):
            apartment = Apartment()

            apartment.title = self.__get_apartment_title(apart_block)
            apartment.description = self.__get_apartment_description(apart_block)
            apartment.placement = self.__get_apartment_placement(apart_block)
            apartment.price = self.__get_apartment_price(apart_block)
            apartment.owner = self.__get_apartment_owner(apart_block)
            apartment.date_published = self.__get_apartment_publish_date(apart_block)
            apartment.features = self.__get_apartment_features(apart_block)
            apartment.link = self.__get_apartment_link(apart_block)

            apartments.append(apartment)

        return apartments

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
