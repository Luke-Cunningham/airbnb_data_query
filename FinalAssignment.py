"""
Final Assignment by
    Lukas Cunningham
    7/26/2021
    Prepare DataBase to load data from a csv file and run advanced
    unit testing.
"""

import csv
from enum import Enum


class EmptyDatasetError(Exception):
    pass


class NoMatchingItems(Exception):
    pass


filename = './AB_NYC_2019.csv'

conversions = {
    "USD": 1,
    "EUR": .84,
    "CAD": 1.23,
    "GBP": .72,
    "CHF": .92,
    "NZD": 1.41,
    "AUD": 1.32,
    "JPY": 110.8
}

home_currency = ''


class DataSet:
    """ the DataSet class will present summary tables based on
    information imported from a .csv file
    """

    copyright = "No copyright has been set"

    class Categories(Enum):
        LOCATION = 1
        PROPERTY_TYPE = 2

    class Stats(Enum):
        MIN = 0
        AVG = 1
        MAX = 2

    def __init__(self, header=""):
        self._data = None
        try:
            self.header = header
        except ValueError:
            self._header = ""

        self._labels = {
            self.Categories.LOCATION: set(),
            self.Categories.PROPERTY_TYPE: set()
        }

    def load_file(self):
        """ Load data into self._data """
        with open(filename, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            self._data = [(item[1], item[2], int(item[3]))
                          for item in csv_reader]
            print(len(self._data))

        self._initialize_sets()
        # return len(self._data)

    def _initialize_sets(self):
        if self._data is None:
            raise EmptyDatasetError

        for item in self._data:
            (self._labels[self.Categories.LOCATION].add(item[0]))
            (self._labels[self.Categories.PROPERTY_TYPE].add(item[1]))

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header: str):
        if len(header) <= 30:
            self._header = header
        else:
            raise ValueError

    def _cross_table_statistics(self,
                                descriptor_one: str, descriptor_two: str):
        """ Given a label from each category, calculate summary
        statistics for the items matching both labels.

        Keyword arguments:
            descriptor_one -- the label for the first category
            descriptor_two -- the label for the second category

        Returns a tuple of min, average, max from the matching rows.
        """
        if not self._data:
            raise EmptyDatasetError

        my_rents = [item[2] for item in self._data if
                    descriptor_one == item[0] and
                    descriptor_two == item[1]]

        if len(my_rents) == 0:
            raise NoMatchingItems

        return float(min(my_rents)), float(sum(my_rents) / len(my_rents)),\
            float(max(my_rents))

    def display_cross_table(self, stat: Stats):
        """
        Print a table of rent statistics
        :param stat: Enum for Min, Avg, Max Rents
        """
        if not self._data:
            raise EmptyDatasetError

        properties = list(self._labels[DataSet.Categories.PROPERTY_TYPE])
        locations = list(self._labels[self.Categories.LOCATION])

        print(20 * " ", end="")
        for header in properties:
            print(f"{header:<22}", end="")
        print()

        for row in locations:
            print(f"{row:<20}", end="")
            for col in properties:
                try:
                    prices = self._cross_table_statistics(row, col)[stat.value]
                    print(f"$ {prices:<20.2f}", end="")
                except NoMatchingItems:
                    na = "N/A"
                    print(f"$ {na:<20}", end="")
            print()


def print_menu():
    """ Display the main menu text. """
    print("Main Menu")
    print("1 - Print Average Rent by Location and Property Type")
    print("2 - Print Minimum Rent by Location and Property Type")
    print("3 - Print Maximum Rent by Location and Property Type")
    print("4 - Load Data")
    print("9 - Quit")


def currency_converter(source_curr: str, target_curr: str, quantity: float):
    """ Convert from one unit of currency to another.

    Keyword arguments:
        quantity -- a float representing the amount of currency to be
                    converted.
        source_curr -- a three letter currency identifier string from
                       the conversions dictionary
        target_curr -- a three letter currency identifier string from
                       the conversions dictionary
    """
    if quantity < 0:
        raise ValueError
    return (quantity / (conversions[source_curr])) * conversions[target_curr]


def currency_options(base_curr: str):
    """ Present a table of common conversions from base_curr to other
    currencies.
    """
    currency_list = []

    print(f"Options for converting from {home_currency}:")

    print(f"{base_curr:10}", end="")
    for item in conversions:
        if item != base_curr:
            currency_list.append(item)
            print(f"{item:10}", end="")
    print()

    for row in range(10, 100, 10):
        print(f"{row:<10.2f}", end="")
        for column in currency_list:
            print(f"{currency_converter(base_curr, column, row):<10.2f}",
                  end="")
        print()
    print()


def menu(dataset: DataSet):
    """ present user with options to access the Airbnb dataset """

    currency_options(home_currency)

    print(dataset.copyright)

    while True:
        print(dataset.header)
        print_menu()

        try:
            user_choice = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number")
            continue

        if user_choice == 1:
            try:
                dataset.display_cross_table(DataSet.Stats.AVG)
            except EmptyDatasetError:
                print("Please load a DataSet first")

        elif user_choice == 2:
            try:
                dataset.display_cross_table(DataSet.Stats.MIN)
            except EmptyDatasetError:
                print("Please load a DataSet first")

        elif user_choice == 3:
            try:
                dataset.display_cross_table(DataSet.Stats.MAX)
            except EmptyDatasetError:
                print("Please load a DataSet first")

        elif user_choice == 4:
            dataset.load_file()

        elif user_choice == 9:
            print("Goodbye!  Thank you for using the database")
            break

        else:
            print("Please enter a valid number")


def main():
    global home_currency
    DataSet.copyright = "copyright 2021 Luke Cunningham"
    air_bnb = DataSet()

    user_name = input("Please enter your name: ")
    print(f"Hi {user_name}, welcome to Foothill's database project.")

    while home_currency not in conversions:
        home_currency = input("What is your home currency? ")

        if home_currency not in conversions:
            print(f"Please enter AUD, USD, EUR, CAD, GBP, CHF, NZD or JPY")

    while True:
        try:
            air_bnb.header = input("Enter a header for the menu:\n")
            break
        except ValueError:
            print("Header must be a string less than or equal to thirty "
                  "characters long")

    menu(air_bnb)


if __name__ == "__main__":
    main()


"""
Please enter your name: Luke
Hi Luke, welcome to Foothill's database project.
What is your home currency? USD
Enter a header for the menu:
AirBNB 2021
Options for converting from USD:
USD       EUR       CAD       GBP       CHF       NZD       AUD       JPY       
10.00     8.40      12.30     7.20      9.20      14.10     13.20     1108.00   
20.00     16.80     24.60     14.40     18.40     28.20     26.40     2216.00   
30.00     25.20     36.90     21.60     27.60     42.30     39.60     3324.00   
40.00     33.60     49.20     28.80     36.80     56.40     52.80     4432.00   
50.00     42.00     61.50     36.00     46.00     70.50     66.00     5540.00   
60.00     50.40     73.80     43.20     55.20     84.60     79.20     6648.00   
70.00     58.80     86.10     50.40     64.40     98.70     92.40     7756.00   
80.00     67.20     98.40     57.60     73.60     112.80    105.60    8864.00   
90.00     75.60     110.70    64.80     82.80     126.90    118.80    9972.00   

copyright 2021 Luke Cunningham
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 1
Please load a DataSet first
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 2
Please load a DataSet first
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 3
Please load a DataSet first
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 4
48895
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 1
                    Private room          Shared room           Entire home/apt       
Bronx               $ 66.79               $ 59.80               $ 127.51              
Queens              $ 71.76               $ 69.02               $ 147.05              
Staten Island       $ 62.29               $ 57.44               $ 173.85              
Brooklyn            $ 76.50               $ 50.53               $ 178.33              
Manhattan           $ 116.78              $ 88.98               $ 249.24              
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 2
                    Private room          Shared room           Entire home/apt       
Bronx               $ 0.00                $ 20.00               $ 28.00               
Queens              $ 10.00               $ 11.00               $ 10.00               
Staten Island       $ 20.00               $ 13.00               $ 48.00               
Brooklyn            $ 0.00                $ 0.00                $ 0.00                
Manhattan           $ 10.00               $ 10.00               $ 0.00                
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 3
                    Private room          Shared room           Entire home/apt       
Bronx               $ 2500.00             $ 800.00              $ 1000.00             
Queens              $ 10000.00            $ 1800.00             $ 2600.00             
Staten Island       $ 300.00              $ 150.00              $ 5000.00             
Brooklyn            $ 7500.00             $ 725.00              $ 10000.00            
Manhattan           $ 9999.00             $ 1000.00             $ 10000.00            
AirBNB 2021
Main Menu
1 - Print Average Rent by Location and Property Type
2 - Print Minimum Rent by Location and Property Type
3 - Print Maximum Rent by Location and Property Type
4 - Load Data
9 - Quit
What is your choice? 9
Goodbye!  Thank you for using the database
"""