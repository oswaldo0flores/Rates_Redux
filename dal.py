# HW6 - Rates Redux    Oswaldo Flores
"""
To handle API calls.

The CountriesCount class will handle the API call for getting the countries count.
The CountriesCountAdapter will wrap the CountriesCount into a thread API call with
a callback. The Countries class will handle the API call for getting a list
of countries. The CountriesAdapter will wrap the Countries class into a threaded API
call with a callback. The Country class will handle the API call for getting a single
country's data. The CountryAdapter will wrap the Country class into a threaded API call
with a callback.

BASE_URL: The base URL in an API operation.
END_POINT: The end part of the URL in an API operation.
COUNTRY_FIELD: Data to get during an API GET operations. I should get country.
DATE: The date we get our data from.
FORMAT: How should the data be formatted.
META_KEY: Key part for a key value pair. The key is meta.
TOTAL_COUNT_KEY: Key part for a key value pair. The key is total-count.
OK_CODE: The API call was successful.
DATA_KEY: Key part for a key value pair. The key is data.
COUNTRY_KEY: Key part for a key value pair. The key is country.
CURRENCY: The data I should be getting when making an API call. I should get currency.
EXCHANGE_RATE: The data I should be getting when making an API call. I should get exchange rate.
RECORD_DATE: The data I should be getting when making an API call. I should get record date.
COUNTRY_FILTER: Data to filter during any API operations. I should filter a country.
"""

import objects
import requests
import threading


class CountriesCount:
    BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
    END_POINT = 'v1/accounting/od/rates_of_exchange'
    COUNTRY_FIELD = 'country'
    DATE = 'record_date:eq:2022-12-31'
    FORMAT = 'json'
    META_KEY = 'meta'
    TOTAL_COUNT_KEY = 'total-count'
    OK_CODE = 200

    def get_countries_count(self) -> int or None:
        """
        To get a countries count through an API call.

        To get a countries count through an API call. This API call will not be threaded because
        I might what to call an API call un-threaded. For this API call to be successful, the status code
        must be ok.

        :return: The countries count if the API call was successful. None if the API call
        was unsuccessful.
        """
        request_url = f'{self.BASE_URL}{self.END_POINT}'
        params = {
            'fields': self.COUNTRY_FIELD,
            'filter': self.DATE,
            'format': self.FORMAT
        }
        try:
            response = requests.get(request_url, params=params)
            if response.status_code == self.OK_CODE:
                json = response.json()
                return json[self.META_KEY][self.TOTAL_COUNT_KEY]
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as err:
            return None


class CountriesCountAdapter:
    def __init__(self, callback: any) -> None:
        """
        To initialize the class.

        To initialize the class with a callback. I use a callback because I am using a threaded GUI
        application. I do not want my application to freeze since I do not know how long the
        API call will take.

        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        self._callback = callback

    def get_countries_count(self) -> None:
        """
        To get a countries count with a thread.

        To get a countries count with a thread. This method will spawn a thread to get
        a countries count.
        """
        thread = threading.Thread(target=self.make_countries_count_api_call)
        thread.start()

    def make_countries_count_api_call(self) -> None:
        """
        To make an API call.

        To make an API call to get countries count. This method will be in a thread that
        already exist from another method, get_countries_count of this class. The countries count
        will be put into this class callback field.
        """
        countries_count = CountriesCount().get_countries_count()
        self._callback(countries_count)


class Countries:
    BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
    END_POINT = 'v1/accounting/od/rates_of_exchange'
    COUNTRY_FIELD = 'country'
    DATE = 'record_date:eq:2022-12-31'
    DATA_KEY = 'data'
    COUNTRY_KEY = 'country'
    OK_CODE = 200

    def __init__(self, countries_count: int):
        """
        To initialize the class with a countries count.

        To initialize the class with a countries count.

        :param countries_count: The amount of countries to get.
        :type countries_count: int
        """
        self._countries_count = countries_count

    def get_countries(self) -> list or None:
        """
        To get countries through an API call.

        To get countries through an API call. This API call will not be threaded because
        I might what to call an API call un-threaded. For this API call to be successful, the status code
        must be ok.

        :return: A countries list if the API call was successful. None if the API call
        was unsuccessful.
        """
        request_url = f'{self.BASE_URL}{self.END_POINT}'
        params = {
            'fields': self.COUNTRY_FIELD,
            'page[size]': self._countries_count,
            'filter': self.DATE
        }
        try:
            response = requests.get(request_url, params=params)
            if response.status_code == self.OK_CODE:
                json = response.json()
                countries = []
                for period in json[self.DATA_KEY]:
                    countries.append(period[self.COUNTRY_KEY])
                return countries
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as err:
            return None


class CountriesAdapter:

    def __init__(self, countries_count: int, callback: any) -> None:
        """
        To initialize the class.

        To initialize the class with a callback and a countries count. I use a callback because
        I am using a threaded GUI application. I do not want my application to freeze since I do
        not know how long the API call will take.

        :param countries_count:
        :type countries_count: int
        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        self._countries_count = countries_count
        self._callback = callback

    def get_countries(self) -> None:
        """
        To get countries with a thread.

        To get countries with a thread. This method will spawn a thread to get
        countries.
        """
        thread = threading.Thread(target=self.make_countries_api_call)
        thread.start()

    def make_countries_api_call(self):
        """
        To make an API call.

        To make an API call to get countries. This method will be in a thread that
        already exist from another method, get_countries of this class. The countries
        will be put into this class callback field.
        """
        countries = Countries(self._countries_count).get_countries()
        self._callback(countries)


class Country:
    BASE_URL = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/'
    END_POINT = 'v1/accounting/od/rates_of_exchange'
    CURRENCY = 'currency'
    EXCHANGE_RATE = 'exchange_rate'
    RECORD_DATE = 'record_date'
    COUNTRY_FILTER = 'country:eq:'
    DATE = 'record_date:eq:2022-12-31'
    DATA_KEY = 'data'
    OK_CODE = 200

    def __init__(self, country_name: str) -> None:
        """
        To initialize the class with a country's name.

        TO initialize the class with a country's name.

        :param country_name: The name of a country.
        :type country_name: str
        """
        self._country_name = country_name

    def get_single_country(self) -> list or None:
        """
        To get a country's data through an API call.

        To get a country's data through an API call. This API call will not be threaded because
        I might what to call an API call un-threaded. For this API call to be successful, the status code
        must be ok.

        :return: A country's data if the API call was successful. None if the API call
        was unsuccessful.
        """
        request_url = f'{self.BASE_URL}{self.END_POINT}'
        params = {
            'fields': f'{self.CURRENCY},{self.EXCHANGE_RATE},'
                      f'{self.RECORD_DATE}',
            'filter': f'{self.COUNTRY_FILTER}{self._country_name},{self.DATE}'
        }
        try:
            response = requests.get(request_url, params=params)
            if response.status_code == self.OK_CODE:
                json = response.json()
                country_currency = ''
                exchange_rate = 0.0
                record_date = ''
                country = []
                for period in json[self.DATA_KEY]:
                    country_currency = period[self.CURRENCY]
                    exchange_rate = float(period[self.EXCHANGE_RATE])
                    record_date = period[self.RECORD_DATE]
                    country.append(objects.SingleCountry(country_currency, exchange_rate, record_date))
                return country
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as err:
            return None


class CountryAdapter:

    def __init__(self, country_name: str, callback: any) -> None:
        """
        To initialize the class.

        To initialize the class with a callback and a country's name. I use a callback because
        I am using a threaded GUI application. I do not want my application to freeze since I do
        not know how long the API call will take.

        :param country_name: The name of a country.
        :type country_name: str
        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        self._country_name = country_name
        self._callback = callback

    def get_country(self) -> None:
        """
        To get a country's data with a thread.

        To get a country's data with a thread. This method will spawn a thread to get
        a country's data.
        """
        thread = threading.Thread(target=self.make_country_api_call)
        thread.start()

    def make_country_api_call(self) -> None:
        """
        To make an API call.

        To make an API call to get a country's data. This method will be in a thread that
        already exist from another method, get_country of this class. The country
        will be put into this class callback field.
        """
        country = Country(self._country_name).get_single_country()
        self._callback(country)
