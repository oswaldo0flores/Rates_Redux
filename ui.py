# HW6 - Rates Redux    Oswaldo Flores
"""
Handles the input and output.

The ui module will create a GUI class that the user can interact with. The init
method will initialize the GUI class and will load the GUI with country names
in the combo box. The run method will start and run the GUI.The create widgets
method will create every single widget in the GUI form. The convert click will
convert the user amount with a country's currency. The is amount valid method will
determine if the user amount is valid. The is countries count method will determine
if it has an integer or None. The is countries will determine if it has a list of
country or None. The is country method will determine if it has a list of the same
country or None. The display converted amount method will display the converted
amount to the user. The error message will display an error message to the user
about the connection to the database. The invalid amount will display an error
message to the user that they enter an invalid amount. The display loading data
will display what data is going to be loading. Every method that requires an
API call will communicate through the objects module to the dal module.
"""
import tkinter as tk
from objects import Countries, SingleCountry
from tkinter import ttk, messagebox


class CurrencyConverterForm:

    def __init__(self, root) -> None:
        """
        To initialize the GUI class.

        To initialize the GUI with a given root. This method must create widgets and this
        will be its own method. This method will load country names from an API call. Calling
        the API directly does not happen here. It happens in the dal module. This method
        will communicate through the objects module to the dal module because it requires an
        API call.
        :param root: A root to run the GUI.
        """
        self._root = root
        self._root.title('Currency Converter')
        self._root.geometry('500x250')
        self.create_widgets()
        Countries.get_count_adapter(self.is_countries_count)
        self.display_loading_data(f'Loading countries count: ')

    @staticmethod
    def run() -> None:
        """
        To start the GUI application.

        To start the GUI application. This method is static because you should not
        have an instance of this class to create an instance of this class.
        """
        root = tk.Tk()
        form = CurrencyConverterForm(root)
        root.mainloop()

    def create_widgets(self) -> None:
        """
        To create widgets for a GUI application.

        To create widgets for a GUI application. All widgets should be set to private.
        The GUI should have a set of list to store all country names, a text box to enter
        an amount in USD, a convert button to convert the amount, and a result text box to
        display the result with a given country name and an amount.
        """
        self._currency_label = ttk.Label(self._root, text='Select Currency:')
        self._currency_label.grid(row=0, column=0, pady=5)
        self._currency_combo_box = ttk.Combobox(self._root)
        self._currency_combo_box.grid(row=0, column=1)
        self._currency_combo_box.config(state='readonly')

        self._amount_label = ttk.Label(self._root, text='Enter an amount in USD:')
        self._amount_label.grid(row=1, column=0)
        self._amount_entry = ttk.Entry(self._root)
        self._amount_entry.grid(row=1, column=1)

        self._convert_button = ttk.Button(self._root, text='Convert', command=self.convert_click)
        self._convert_button.grid(row=2, column=1, pady=5)
        self._convert_button.config(state='disabled')

        self._result_label = ttk.Label(self._root, text='Result')
        self._result_label.grid(row=3, column=0)
        self._result_text = tk.Text(self._root, height=5, width=40)
        self._result_text.grid(row=3, column=1)
        self._result_text.config(state='disabled')

    def convert_click(self) -> None:
        """
        When the user clicks the covert button.

        When the user clicks the convert button. The button and combo box must be disabled to
        not interfere the thread api call in the dal module. Validate if the amount the user enter.
        If the amount is invalid, prompt an error message to the user and enable the button and combo
        box. If the amount is valid, make an API call. This method will communicate through the
        objects module to the dal module because it requires an API call. I do not validate the country's
        name because I know it is already valid. Since I loaded the data in the init method.
        """
        self._convert_button.config(state='disabled')
        self._currency_combo_box.config(state='disabled')
        amount = self._amount_entry.get()
        self._amount_entry.config(state='disabled')
        amount = self.is_amount_valid(amount)
        if amount is not False:
            self.display_loading_data('Loading country data')
            SingleCountry.get_country_adapter(self._currency_combo_box.get(), self.is_country)
        else:
            self.invalid_amount()
            self._amount_entry.config(state='normal')
            self._convert_button.config(state='normal')
            self._currency_combo_box.config(state='normal')

    def is_amount_valid(self, amount: str) -> float or None:
        """
        To validate the given amount.

        To validate the given amount. The amount must be a positive number.

        :param amount: An unvalidated amount given by the user.
        :type amount: str
        :return: Float if the amount is a positive number. False if the amount
        is not positive or a number.
        """
        if amount.isdigit() and float(amount) > 0.0:
            return float(amount)
        return False

    def is_countries_count(self, countries_count: int or None) -> None:
        """
        Determine if the countries count API call was successful.

        Determine if the countries count API call was successful. If the countries count
        API call was not successful, display an error message to the user. If the countries
        count API call was successful, let the user know and make another API call to get
        country names. This method will communicate through the objects module to the dal
        module because it requires an API call. If countries count is None, I will not enable,
        normal, the convert button because I will not have any data in the combo box. The user
        must reset the application.

        :param countries_count: The amount of countries to display or None.
        :type countries_count: int or None
        """
        self.display_loading_data(f'{countries_count} countries found')
        if countries_count is not None:
            self.display_loading_data(f'Loading countries')
            Countries.get_countries_adapter(countries_count, self.is_countries)
        else:
            self.error_message_reset()

    def is_countries(self, countries: list or None) -> None:
        """
        Determine if the countries name API call was successful.

        Determine if the countries name API call was successful. If the countries name
        API call was not successful, display an error message to the user. If the countries
        name API call was successful, let the user know and display the country names to the user.
        If countries is None, I will not enable, normal, the convert button because I will
        not have any data in the combo box. The user must reset the application.

        :param countries: A list of country names or None.
        :type countries: list or None
        """
        if countries is not None:
            self._currency_combo_box['values'] = countries
            self._currency_combo_box.current(0)
            self._convert_button.config(state='normal')
        else:
            self.error_message_reset()

    def is_country(self, country_data: list or None) -> None:
        """
        Determine if the country data API call was successful.

        Determine if the country data API call was successful. If the country data
        API call was not successful, display an error message to the user. If the country
        data API call was successful, let the user know and display the data to the user.
        If country data is None, I will enable, normal, the convert button because I will
        have data in the combo box. The user does not have to reset this application.
        Even though I am getting a country's data, that country can have many exchange rate
        in a given day.

        :param country_data: A single country with their exchange rate(s) or None.
        :type country_data: list or None
        """
        if country_data is not None:
            self._result_text.config(state='normal')
            self._result_text.delete(1.0, tk.END)
            self.display_convert_amount(country_data)
            self._result_text.config(state='disabled')
        else:
            self.error_message()
        self._amount_entry.config(state='normal')
        self._convert_button.config(state='normal')
        self._currency_combo_box.config(state='normal')

    def display_convert_amount(self, country_data: list) -> None:
        """
        Display the exchange rate.

        Display the exchange rate with this form amount. Validating the user amount
        does not happen here because validation already happen in another method.
        When display the user amount and the converted amount, both need to have two
        decimal places because we are dealing with currency. Since a country can have
        many exchange rate, display those exchange rates.

        :param country_data: A single country with their exchange rate(s).
        :type country_data: list
        """
        amount = float(self._amount_entry.get())
        for country in country_data:
            convert_amount = country.calculate_exchange_rate(amount)
            result = f'{amount:.02f} USD = {convert_amount:.02f} {country.get_currency()}'
            self._result_text.insert(tk.END, f'{result}\n')

    def error_message_reset(self) -> None:
        """
        Display an error message.

        Display an error message. This is a server error and this tells the user to reset
        the application.
        """
        tk.messagebox.showerror(title='Server Error', message='An Error has occur! Please reset.')

    def error_message(self) -> None:
        """
        Display an error message.

        Display an error message. This is a server error and this tells the user to try again.
        This will not tell the user to reset the application.
        """
        tk.messagebox.showerror(title='Server Error', message='An Error has occur! Try again.')

    def invalid_amount(self) -> None:
        """
        Display an error message.

        Display an error message. This is a user error and this tells the user they
        enter an invalid amount.
        """
        tk.messagebox.showerror(title='User Error', message='Invalid amount')

    def display_loading_data(self, loading_data: str) -> None:
        """
        Tells the user what is being loaded.

        Tells the user what is being loaded. This will let the user know that the application is
        still running. Without this method, I assume the user might think the application has crash
        because loading the data might take a long time.

        :param loading_data: What data is being loaded.
        :type loading_data: str
        """
        self._result_text.config(state='normal')
        self._result_text.insert(tk.END, f'{loading_data}\n')
        self._result_text.config(state='disabled')
