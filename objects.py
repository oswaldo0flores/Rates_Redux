# HW6 - Rates Redux    Oswaldo Flores
"""
To handle a single country and a list of countries.

The SingleCountry represents a single country. The class contains an init to
initialize the class, a str to set what the user is allowed to see, a method
to get country currency description, a method to get the exchange rate, a method
to get a record date, a method to calculate exchange rate with is this class
exchange rate to a given value, and a method to load in a single country from
the database module.
The Countries represent a list of country names only. The class contains an init to
initialize the class, a len to get the length of the list, an iter to iterate over the list,
a str to set what the data should look like to the user, a contains to find a country with a
given value, a get countries to get the whole list, and get countries count to get how many countries
should be in the list.
"""

from dal import CountriesCountAdapter, CountriesAdapter, CountryAdapter
from dataclasses import dataclass, field


@dataclass
class Countries:
    __countries: list = field(default_factory=list)

    def __init__(self) -> None:
        """
        To initialize this class.

        To initialize this class with an empty list. This class should have a mutable list because
        at the start of this application I do not know how many countries I am getting.
        """
        self.__countries = []

    def __len__(self) -> int:
        """
        To get the length of the list.

        To get the length of the list.

        :return: Length of the list.
        """
        return len(self.__countries)

    def __iter__(self):
        """
        To iterate over the list.

        To iterate over the list. Yields every country name in the list.

        :yield: A country name.
        """
        for country in self.__countries:
            yield country

    def __str__(self) -> str:
        """
        To display what data the user is allowed to see.

        To display what data the user is allowed to see. This method can
        also format the data to make it more readable.

        :return: The formatted data that is display to the user.
        """
        return '\n'.join(map(str, self.__countries))

    def __contains__(self, country: str) -> str:
        """
        To find a country.

        To find a country if it exists within the list.

        :param country: The name of a country.
        :type country: str
        :return: The name of the country that exists within the list.
        """
        if country in self.__countries:
            return country

    @staticmethod
    def get_count_adapter(callback: any) -> None:
        """
        To get the countries count from an API call.

        To get the countries count from an API call. This method is static because
        I should not create an instance of this class to determine how many countries
        I am getting. I use a call back because I do not know how long the API call
        will last for.

        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        countries_count_adapter = CountriesCountAdapter(callback)
        countries_count_adapter.get_countries_count()

    @staticmethod
    def get_countries_adapter(countries_count: int, callback: any) -> None:
        """
        To get countries from an API call.

        To get countries from an API call. This method is static because I should not create
        an instance of this class to get countries. I use a call back because I do not know
        how long the API call will last for.

        :param countries_count: The amount of countries I am getting.
        :type countries_count: int
        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        countries_adapter = CountriesAdapter(countries_count, callback)
        countries_adapter.get_countries()


@dataclass
class SingleCountry:
    __currency: str
    __exchange_rate: float
    __record_date: str

    def __init__(self, currency: str = '', exchange_rate: float = 0.0,
                 record_date: str = '') -> None:
        """
        To initialize the class.

        To initialize the class with a given currency, exchange rate, and
        a record date. I assume the data is valid because data validation should not happen
        here. All three fields in this class can have a default value of an empty string or
        a zero.

        :param currency: The currency of a country.
        :type currency: str
        :param exchange_rate: The exchange rate for a country's currency.
        :type exchange_rate: float
        :param record_date: The date of the exchange rate.
        :type record_date: str
        """
        self.__currency = currency
        self.__exchange_rate = exchange_rate
        self.__record_date = record_date

    def __str__(self) -> str:
        """
        To display what data the user is allowed to see.

        To display what data the user is allowed to see if the user decides to print out the object
        of this class. This method also formats the data to make it more readable.

        :return: The formatted data that is display to the user.
        """
        return f'{self.__currency}, {self.__exchange_rate}, {self.__record_date}'

    def get_currency(self) -> str:
        """
        To get currency.

        To get currency. It can contain an empty string or a country currency.

        :return: An empty string or a country currency.
        """
        return self.__currency

    def get_exchange_rate(self) -> float:
        """
        To get the exchange rate.

        To get the exchange rate of a currency. It can contain a rate of 0.0 or a country's
        exchange rate.

        :return: A rate of 0.0 or a country's exchange rate.
        """
        return self.__exchange_rate

    def get_record_date(self) -> str:
        """
        To get the record date.

        To get the record date of the exchange rate. It can contain an empty string
        or a date of the exchange rate.

        :return: An empty string or a date.
        """
        return self.__record_date

    def calculate_exchange_rate(self, value: float or int) -> float or int:
        """
        To calculate the exchange rate.

        To calculate the exchange rate with a given value. Validating the value
        should not happen here, it should happen in the ui module. Multiply the
        value with this class exchange rate to get this class country's currency
        amount.

        :param value: The amount of currency in USD.
        :type value: float or int
        :return: This class country's currency amount.
        """
        return value * self.__exchange_rate

    @staticmethod
    def get_country_adapter(country_name: str, callback: any) -> None:
        """
        To get a country data.

        To get a country data. This method is static because I should not create an instance of
        this class to get a country's data. I use a call back because I do not know
        how long the API call will last for.

        :param country_name: The name of the country.
        :type country_name: str
        :param callback: To determine if the API call was successful.
        :type callback: any
        """
        country_adapter = CountryAdapter(country_name, callback)
        country_adapter.get_country()
