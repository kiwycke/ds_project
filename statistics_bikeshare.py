import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, date

"""
Statistics Computed

#1 Popular times of travel (i.e., occurs most often in the start time)

most common month
most common day of week
most common hour of day
----------------------------------------

#2 Popular stations and trip

most common start station
most common end station
most common trip from start to end (i.e., most frequent combination of start station and end station)
----------------------------------------

#3 Trip duration

total travel time
average travel time
----------------------------------------

#4 User info

counts of each user type
counts of each gender (only available for NYC and Chicago)
earliest, most recent, most common year of birth (only available for NYC and Chicago)
average trip duration by month distributed by gender
plot for Avg. Trip Duration by Month distributed by Gender
earliest, most recent, and most common year of birth
plot for Avg. Trip Duration distributed by age groups
----------------------------------------
"""

class InvalidInput(Exception):
    "Raised when the input is none of the options."
    msg = 'InvalidInput'
    def __str__(self):
        return self.msg

class StatisticsBikeshare:
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    city_letters = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}

    months_num = ['1', '2', '3', '4', '5', '6']

    week_days = {'m': 'Monday', 't': 'Tuesday', 'w': 'Wednesday', 'th': 'Thursday', 'f': 'Friday', 's': 'Saturday', 'su': 'Sunday'}

    bulk = False

    df = pd.DataFrame()

    start = 0

    stop = 5

    def not_bulk(self):
        input("Press Enter to continue...\n\n\n")

    def bulk_check(self):
        """Checks if user want statistics in bulk or sequentially."""
        while True:
            try:
                inp = input('\nDo you want for statistics in bulk? Enter (y)yes or (n)no.\n')
                if inp.lower() == 'yes' or inp.lower() == 'y':
                    self.bulk = True
                    print('Let\'s go with bulk statistics!\n'+'-'*48+'\n')
                    break
                elif inp.lower() == 'no' or inp.lower() == 'n':
                    self.bulk = False
                    print('Let\'s go with statistics sequentially!\n'+'-'*48+'\n')
                    break
                else:
                    raise InvalidInput
            except InvalidInput:
                print('\n!! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n'+'-'*48+'\n')
                continue
    
    def map_input_to_days(self, days):
        """Filter helper function (replaces 'a', 'wdays' and 'wends' inputs to days' keys)"""
        if 'a' in days:
            days.remove('a')
            days.update(self.week_days.keys())
        if 'wdays' in days:
            days.remove('wdays')
            days.update(list(self.week_days.keys())[:5])
        if 'wends' in days:
            days.remove('wends')
            days.update(list(self.week_days.keys())[5:])
        return days

    def col_check(self, col_name):
        """Checks if column is part of the dataframe."""
        return col_name in list(self.df.columns)

    def want_filter(self):
        """Checks if user want unique filters."""
        while True:
            try:
                inp = input('\nDo you want to filter data? Enter (y)yes or (n)no.\n')
                if inp.lower() == 'yes' or inp.lower() == 'y':
                    print('Let\'s filter data!\n'+'-'*48+'\n')
                    return True
                elif inp.lower() == 'no' or inp.lower() == 'n':
                    print('Using default filters (each city, months and days)!\n'+'-'*48+'\n')
                    return False
                else:
                    raise InvalidInput
            except InvalidInput:
                print('\n!! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n'+'-'*48+'\n')
                continue

    def to_age(self, birth_year):
        """Converts birth year to age"""
        return datetime.today().year - birth_year

    def secure_input(self, input_set):
        return set(input_set.lower() for input_set in input_set)

    def get_filters(self):
        """
        Asks user
            - if they want to see statistics in bulk or sequentially
            - if they want to specify filters for a cities, months, and days to analyze
                - if they don't than statistics will be shown for each city, month and day
                - otherwise they can specify unique filters

        Returns:
            (set) cites     - names of the cities to analyze,

            (set) months    - numbers of the months to filter by,

            (set) days      - names of the days to filter by
        """
        print('\n'+'-'*48+'\n| Hello! Let\'s explore some US bikeshare data! |\n'+'-'*48+'\n')


        self.bulk_check()
        if not self.want_filter():
            # set default values for cities, months, days
            cities = set(self.city_letters.values())
            months = set(self.months_num)
            days = self.week_days.values()
        else:
            # get user input for filters (cities, months, days).
            while True:
                try:
                    print('Which cities\' data are you interested in?\n  - (c)Chicago,\n  - (n)New York City,\n  - (w)Washington\n  - (a)All\n')
                    cities = set(input('Type here (separated by space): ').split())
                    cities = self.secure_input(cities)

                    tmp = set()
                    if not cities:
                        raise InvalidInput
                    if 'a' in cities:
                        cities.remove('a')
                        cities.update(self.city_letters.keys())
                    if all(e in self.city_letters.keys() for e in cities):
                        for val in cities:
                            tmp.add(self.city_letters[val])
                        cities = tmp
                        break
                    else:
                        raise InvalidInput
                except InvalidInput:
                    print('\n  !! Type valid input please !! (eg.: \'c n w\')\n\n')
                    continue
            print('-'*48+'\n')

            # get user input for month (all, january, february, ... , june)
            while True:
                try:
                    print('Which months\' data are you interested in?\n  - (a)All  (1)Jan  (2)Feb  (3)March  (4)Apr  (5)May  (6)June\n')
                    months = set(input('Type here (separated by space): ').split())
                    months = self.secure_input(months)

                    if not months:
                        raise InvalidInput
                    if 'a' in months:
                        months.remove('a')
                        months.update(self.months_num)
                    if all(ch in self.months_num for ch in months):
                        break
                    else:
                        raise InvalidInput
                except InvalidInput:
                    print('\n!! Type valid input please !! (eg.: \'1 2 3 4 5 6\')\n\n'+'-'*48+'\n')
                    continue
            print('-'*48+'\n')

            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                try:
                    print('Which days\' data are you interested in?')
                    print('Options:\n  - (m)Monday  (t)Tuesday  (w)Wednesday  (th)Thursday  (f)Friday  (s)Saturday  (su)Sunday\n    (wdays)Weekdays  (wends)Weekends  (a)all\n')
                    days = set(input('Type here (separated by space): ').split())
                    days = self.secure_input(days)
                    days = self.map_input_to_days(days)

                    tmp = set()
                    if not days:
                        raise InvalidInput
                    if all(e in self.week_days.keys() for e in days):
                        for val in days:
                            tmp.add(self.week_days[val])
                        days = tmp
                        break
                    else:
                        raise InvalidInput
                except InvalidInput:
                    print('\n!! Type valid input please !! (eg.: \'m t w th f s su\')\n\n'+'-'*48+'\n')
                    continue
            print('-'*48+'\n')

        print('Current filters:\n  Cities: {}\n  Months: {}\n  Days: {}\n'.format(sorted(cities), sorted(months), sorted(days))+'='*48+'\n')
        if not self.bulk:
            self.not_bulk()
        return cities, months, days


    def load_data(self, cities, months, days):
        """
        Loads data for the specified cities and filters by month(s) and day(s) if applicable.

        Parameters:
            (set) cites     - names of the cities to analyze,

            (set) months    - numbers of the months to filter by,

            (set) days      - names of the days to filter by

        Returns:
            df - Pandas DataFrame containing specified cities' data filtered by month(s) and day(s)
        """
        # load data file into a dataframe
        self.df = pd.concat((pd.read_csv(self.CITY_DATA[city]) for city in list(cities)), ignore_index=True)

        if self.col_check('Start Time'):
            # convert the Start Time column to datetime
            self.df['Start Time'] = pd.to_datetime(self.df['Start Time'])

            # extract Month and Day of Week from Start Time to create new columns
            self.df['Month'] = self.df['Start Time'].dt.month
            self.df['Day of week'] = self.df['Start Time'].dt.day_name()

        if self.col_check('Birth Year'):
            # extract Age from Birth Year to create new column
            self.df['Age'] = self.df['Birth Year'].astype('Int64').apply(self.to_age)

        # getting the corresponding int type numpy array
        months = np.array(list(months)).astype(int)

        # filter by month to create the new dataframe
        self.df = self.df[self.df['Month'].isin(months)]

        # filter by day of week to create the new dataframe
        self.df = self.df[self.df['Day of week'].isin(days)]

        return self.df


    def time_stats(self):
        """Displays statistics on the most frequent times of travel."""

        print('| Calculating The Most Frequent Times of Travel... |\n\n')
        start_time = time.time()

        if self.col_check('Start Time'):
            # display the most common start hour
            print('Most popular start hour:\n  {}\n'.format(self.df['Start Time'].dt.hour.mode()[0])+'-'*10)

            # display the most common month
            print('Most popular months:\n  {}\n'.format(self.df['Start Time'].dt.month_name().mode()[0])+'-'*10)
        else:
            print('No start time data to share.\n'+'-'*10)

        if self.col_check('Day of week'):
            # display the most common day of week
            print('Most popular day:\n  {}\n'.format(self.df['Day of week'].mode()[0])+'-'*10)
        else:
            print('No day data to share.\n'+'-'*10)

        print("This took %s seconds.\n" % (time.time() - start_time)+'-'*48)
        if not self.bulk:
            self.not_bulk()

    def station_stats(self):
        """Displays statistics on the most popular stations and trip."""

        print('| Calculating The Most Popular Stations and Trip... |\n\n')
        start_time = time.time()

        if self.col_check('Start Station'):
            # display most commonly used start station
            print('Most popular Start Station:\n  {}\n'.format(self.df['Start Station'].mode()[0])+'-'*10)
        else:
            print('No start station data to share.\n''-'*10)

        if self.col_check('End Station'):
            # display most commonly used end station
            print('Most popular End Station:\n  {}\n'.format(self.df['End Station'].mode()[0])+'-'*10)
        else:
            print('No end station data to share.\n'+'-'*10)

        if self.col_check('Start Station') and self.col_check('End Station'):
            # display most frequent combination of start station and end station trip
            print('Most popular Start - End Stations combo:\n  {}\n'.format((self.df['Start Station'] + ' - ' + self.df['End Station']).mode()[0])+'-'*10)
        else:
            print('No start station or end station data to share.\n'+'-'*10)

        print("This took %s seconds.\n" % (time.time() - start_time)+'-'*48)
        if not self.bulk:
            self.not_bulk()

    def trip_duration_stats(self):
        """Displays statistics on the total and average trip duration."""

        print('| Calculating Trip Duration... |\n\n')
        start_time = time.time()

        if self.col_check('Trip Duration'):
            # converting seconds to dd:hh:mm:ss
            duration_days = pd.to_timedelta(self.df['Trip Duration'], unit='s')

            # display total travel time
            print('Total Trip Duration:\n  {}\n'.format(duration_days.sum())+'-'*10)

            # display mean travel time
            print('Average Trip Duration:\n  {}\n'.format(duration_days.mean(skipna = True))+'-'*10)
        else:
            print('No trip duration data to share.\n'+'-'*10)

        print("This took %s seconds.\n" % (time.time() - start_time)+'-'*48)
        if not self.bulk:
            self.not_bulk()

    def user_stats(self):
        """Displays statistics on bikeshare users."""

        print('|  Calculating User Stats...  |\n')
        start_time = time.time()

        if self.col_check('User Type'):
            # display counts of user types
            print('Counts of User Types:\n  {}\n'.format(self.df.groupby(['User Type'])['User Type'].count())+'-'*10)
        else:
            print('No user type data to share.\n'+'-'*10)

        if self.col_check('Gender'):
            # display counts of gender
            print('Counts of Gender:\n  {}\n'.format(self.df.groupby(['Gender'])['Gender'].count())+'-'*10)
        else:
            print('No gender data to share.\n'+'-'*10)


        if self.col_check('Birth Year'):
            # display earliest, most recent, and most common year of birth
            print('Earliest year of birth among participants:\n  {}\n'.format(self.df['Birth Year'].min())+'-'*10)
            print('Most recent year of birth among participants:\n  {}\n'.format(self.df['Birth Year'].max())+'-'*10)
            print('Most common year of birth among participants:\n  {}\n'.format(self.df['Birth Year'].mode()[0])+'-'*10)

            # creating new DataFrame for transparency 
            df_age = pd.DataFrame(self.df.groupby(['Age', 'Month'])['Trip Duration'].mean()).reset_index()
            print('Average trip duration among participants\' younger than 20 years\':\n {}\n'.format(df_age[['Age', 'Trip Duration', 'Month']].loc[df_age['Age'] < 20])+'-'*10)

            # plot for Avg. Trip Duration distributed by age groups
            plt.plot(df_age['Month'].loc[(df_age['Age'] < 30)], df_age['Trip Duration'].loc[(df_age['Age'] < 30)], 'm.', label = 'age < 30')
            plt.plot(df_age['Month'].loc[(df_age['Age'] > 30) & (df_age['Age'] < 60)],
                     df_age['Trip Duration'].loc[(df_age['Age'] > 30) & (df_age['Age'] < 60)], 'b.', alpha = 0.5, label = '30 < age < 60')
            plt.plot(df_age['Month'].loc[(df_age['Age'] > 60) & (df_age['Age'] < 90)],
                     df_age['Trip Duration'].loc[(df_age['Age'] > 60) & (df_age['Age'] < 90)], 'g.', alpha = 0.5, label = '60 < age < 90')
            plt.plot(df_age['Month'].loc[(df_age['Age'] > 90)], df_age['Trip Duration'].loc[(df_age['Age'] > 90)], 'r.', alpha = 0.5, label = 'age > 90')
            plt.title('Avg.Trip Duration by Month and Age groups\n age < 30, 30 < age < 60, 60 < age < 90, 90 < age')
            plt.ylabel('Trip Duration')
            plt.xlabel('Months')
            plt.legend()
            plt.show()
        else:
            print('No birth year data to share.\n'+'-'*10)

        if self.col_check('Gender') and self.col_check('Trip Duration') and self.col_check('Month'):
            # average trip duration by month distributed by gender
            print('Avg. Trip Duration by Month distributed by Gender:\n  {}\n'.format(self.df.groupby(['Gender', 'Month'])['Trip Duration'].mean())+'-'*10)

            # creating new DataFrame for transparency 
            df_gender = pd.DataFrame(self.df.groupby(['Gender', 'Month'])['Trip Duration'].mean()).reset_index()

            # plot for Avg. Trip Duration by Month distributed by Gender
            plt.plot(df_gender['Month'].loc[df_gender['Gender'] == 'Female'], df_gender['Trip Duration'].loc[df_gender['Gender'] == 'Female'], 'g.-', label = 'Female')
            plt.plot(df_gender['Month'].loc[df_gender['Gender'] == 'Male'], df_gender['Trip Duration'].loc[df_gender['Gender'] == 'Male'], 'b.-', label = 'Male')
            plt.title('Avg.Trip Duration by Month\nFemale vs Male')
            plt.ylabel('Trip Duration')
            plt.xlabel('Months')
            plt.legend()
            plt.show()
        else:
            print('No gender or trip duration or month data to share.\n'+'-'*10)

        print("This took %s seconds.\n" % (time.time() - start_time)+'-'*48)

    default_input_msg = '\nDo you want to check the first 5 rows of the dataset related to the chosen city?\nEnter (y)yes or (n)no.\n'
    default_print_msg = '\nFirs 5 rows of dataset:\n{}\n'

    def show_five_rows(self):
        next_five_input_msg = '\nDo you want to check another 5 rows of the dataset?\nEnter (y)yes or (n)no.\n'
        next_five_print_msg = '\n Next 5 rows of dataset:\n{}\n'
        while True:
            try:
                check_five_rows = input(self.default_input_msg)
                if check_five_rows.lower() == 'yes' or check_five_rows.lower() == 'y':
                    self.default_input_msg = next_five_input_msg
                    print(self.default_print_msg.format(self.df.iloc[self.start:self.stop])+'-'*48+'\n')
                    self.default_print_msg = next_five_print_msg
                    self.start += 5
                    self.stop += 5
                    self.show_five_rows()
                elif check_five_rows.lower() == 'no' or check_five_rows.lower() == 'n':
                    print('\nShowing no more of dataset\n'+'-'*48+'\n')
                    self.restart_kernel()
                else:
                    raise InvalidInput
            except InvalidInput:
                print('!! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n'+'-'*48+'\n')
                continue

    def restart_kernel(self):
        self.start = 0
        self.stop = 5
        self.default_input_msg = '\nDo you want to check the first 5 rows of the dataset related to the chosen city?\nEnter (y)yes or (n)no.\n'
        self.default_print_msg = '\nFirs 5 rows of dataset:\n{}\n'
        while True:
            try:
                restart = input('\nWould you like to restart the kernel? Enter (y)yes or (n)no.\n')
                if restart.lower() == 'yes' or restart.lower() == 'y':
                    print('\nRestart.\n'+'-'*48+'\n')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.menu()
                elif restart.lower() == 'no' or restart.lower() == 'n':
                    print('\nExit.\n'+'='*48+'\n')
                    exit()
                else:
                    raise InvalidInput
            except InvalidInput:
                print('!! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n'+'-'*48+'\n')
                continue

    def menu(self):
        cities, months, days = self.get_filters()
        self.df = self.load_data(cities, months, days)
        self.time_stats()
        self.station_stats()
        self.trip_duration_stats()
        self.user_stats()
        self.show_five_rows()
        

if __name__ == "__main__":
    bike_stat = StatisticsBikeshare()
    bike_stat.menu()