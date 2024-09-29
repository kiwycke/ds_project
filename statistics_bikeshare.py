import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
Plot for Avg. Trip Duration by Month distributed by Gender
----------------------------------------
"""

# define Python user-defined exceptions
class InvalidInput(Exception):
    "Raised when the input is none of the options."
    pass

class StatisticsBikeshare:
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    city_letters = {'c': 'chicago', 'n': 'new york city', 'w': 'washington'}

    months_num = ['1', '2', '3', '4', '5', '6']

    week_days = {'m': 'Monday', 't': 'Tuesday', 'w': 'Wednesday', 'th': 'Thursday', 'f': 'Friday', 's': 'Saturday', 'su': 'Sunday'}

    bulk = False

    def not_bulk(self):
        input("Press Enter to continue...\n\n\n")

    def bulk_check(self):
        """Checks if user want bulk data or not."""
        while True:
            try:
                restart = input('\nDo you want for statistics in bulk? Enter (y)yes or (n)no.\n')
                if restart.lower() == 'yes' or restart.lower() == 'y':
                    self.bulk = True
                    print('Let\'s go with bulk statistics!')
                    print('-'*48+'\n')
                    break
                elif restart.lower() == 'no' or restart.lower() == 'n':
                    print('Let\'s go with statistics sequentially!')
                    print('-'*48+'\n')
                    break
                else:
                    raise InvalidInput
            except InvalidInput:
                print('\n  !! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n')
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

    def col_check(self, df, col_name):
        """Checks if column is part of the data frame."""
        return col_name in list(df.columns)

    def want_filter(self):
        """Checks if user want unique filters."""
        while True:
            try:
                restart = input('\nDo you want to filter data? Enter (y)yes or (n)no.\n')
                if restart.lower() == 'yes' or restart.lower() == 'y':
                    print('Let\'s filter data!')
                    print('-'*48+'\n')
                    return True
                elif restart.lower() == 'no' or restart.lower() == 'n':
                    print('Using default filters (each city, months and days)!')
                    print('-'*48+'\n')
                    return False
                else:
                    raise InvalidInput
            except InvalidInput:
                print('\n  !! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n')
                continue

    def get_filters(self):
        """
        Asks user to specify a cities, months, and days to analyze.

        Returns:
            (set) cites     - first characters of names of the cities to analyze,
                            - 'a' to apply no city filter

            (set) months    - numbers of the months to filter by,
                            - 'a' to apply no month filter

            (set) days      - first letters names of the days of week to filter by,
                            - 'wends' to filter by weekends,
                            - 'wdays' to filter by weekdays,
                            - 'a' to apply no day filter
        """
        print('\n'+'-'*48)
        print('| Hello! Let\'s explore some US bikeshare data! |')
        print('-'*48+'\n\n')

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

                    if not months:
                        raise InvalidInput
                    if 'a' in months:
                        months.remove('a')
                        months.update(self.months_num)
                    if all(e in self.months_num for e in months):
                        break
                    else:
                        raise InvalidInput
                except InvalidInput:
                    print('\n  !! Type valid input please !! (eg.: \'1 2 3 4 5 6\')\n\n')
                    continue
            print('-'*48+'\n')

            # get user input for day of week (all, monday, tuesday, ... sunday)
            while True:
                try:
                    print('Which days\' data are you interested in?')
                    print('Options:\n  - (m)Monday  (t)Tuesday  (w)Wednesday  (th)Thursday  (f)Friday  (s)Saturday  (su)Sunday\n    (wdays)Weekdays  (wends)Weekends  (a)all\n')
                    days = set(input('Type here (separated by space): ').split())
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
                    print('\n  !! Type valid input please !! (eg.: \'m t w th f s su\')\n\n')
                    continue
            print('-'*48+'\n')

        print('Current filters:\n  Cities: {}\n  Months: {}\n  Days: {}'.format(sorted(cities), sorted(months), sorted(days)))
        print('='*48)
        if not self.bulk:
            self.not_bulk()
        return cities, months, days


    def load_data(self, cities, months, days):
        """
        Loads data for the specified cities and filters by month(s) and day(s) if applicable.

        Args:
            (set) cites     - first characters of names of the cities to analyze,
                            - 'a' to apply no city filter

            (set) months    - numbers of the months to filter by,
                            - 'a' to apply no month filter

            (set) days      - first letters names of the days of week to filter by,
                            - 'wends' to filter by weekends,
                            - 'wdays' to filter by weekdays,
                            - 'a' to apply no day filter
        Returns:
            df - Pandas DataFrame containing specified cities data filtered by month(s) and day(s)
        """
        # load data file into a dataframe
        df = pd.concat((pd.read_csv(self.CITY_DATA[city]) for city in list(cities)), ignore_index=True)

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['Month'] = df['Start Time'].dt.month
        df['Day of week'] = df['Start Time'].dt.day_name()

        # getting the corresponding int type numpy array
        months = np.array(list(months)).astype(int)

        # filter by month to create the new dataframe
        df = df[df['Month'].isin(months)]

        # filter by day of week to create the new dataframe
        df = df[df['Day of week'].isin(days)]

        return df


    def time_stats(self, df):
        """Displays statistics on the most frequent times of travel."""

        print('| Calculating The Most Frequent Times of Travel... |\n\n')
        start_time = time.time()

        if self.col_check(df, 'Start Time'):
            # display the most common start hour
            print('Most popular start hour:\n  {}'.format(df['Start Time'].dt.hour.mode()[0]))
            print('-'*10)

            # display the most common month
            print('Most popular months:\n  {}'.format(df['Start Time'].dt.month_name().mode()[0]))
            print('-'*10)
        else:
            print('No start time data to share.')
            print('-'*10)

        if self.col_check(df, 'Day of week'):
            # display the most common day of week
            print('Most popular day:\n  {}'.format(df['Day of week'].mode()[0]))
            print('-'*10)
        else:
            print('No day data to share.')
            print('-'*10)

        print("This took %s seconds." % (time.time() - start_time))
        print('-'*48)
        if not self.bulk:
            self.not_bulk()

    def station_stats(self, df):
        """Displays statistics on the most popular stations and trip."""

        print('| Calculating The Most Popular Stations and Trip... |\n\n')
        start_time = time.time()

        if self.col_check(df, 'Start Station'):
            # display most commonly used start station
            print('Most popular Start Station:\n  {}'.format(df['Start Station'].mode()[0]))
            print('-'*10)
        else:
            print('No start station data to share.')
            print('-'*10)

        if self.col_check(df, 'End Station'):
            # display most commonly used end station
            print('Most popular End Station:\n  {}'.format(df['End Station'].mode()[0]))
            print('-'*10)
        else:
            print('No end station data to share.')
            print('-'*10)

        if self.col_check(df, 'Start Station') and self.col_check(df, 'End Station'):
            # display most frequent combination of start station and end station trip
            print('Most popular Start - End Stations combo:\n  {}'.format((df['Start Station'] + ' - ' + df['End Station']).mode()[0]))
            print('-'*10)
        else:
            print('No start station or end station data to share.')
            print('-'*10)

        print("This took %s seconds." % (time.time() - start_time))
        print('-'*48)
        if not self.bulk:
            self.not_bulk()

    def trip_duration_stats(self, df):
        """Displays statistics on the total and average trip duration."""

        print('| Calculating Trip Duration... |\n\n')
        start_time = time.time()

        if self.col_check(df, 'Trip Duration'):
            # converting seconds to dd:hh:mm:ss
            duration_days = pd.to_timedelta(df['Trip Duration'], unit='s')

            # display total travel time
            print('Total Trip Duration:\n  {}'.format(duration_days.sum()))
            print('-'*10)

            # display mean travel time
            print('Average Trip Duration:\n  {}'.format(duration_days.mean(skipna = True)))
            print('-'*10)

            print("This took %s seconds." % (time.time() - start_time))
            print('-'*48)
        else:
            print('No trip duration data to share.')
            print('-'*10)
        if not self.bulk:
            self.not_bulk()

    def user_stats(self, df):
        """Displays statistics on bikeshare users."""

        print('|  Calculating User Stats...  |\n')
        start_time = time.time()

        # Display counts of user types
        if self.col_check(df, 'User Type'):
            print('Counts of User Types:\n  {}'.format(df.groupby(['User Type'])['User Type'].count()))
            print('-'*10)
        else:
            print('No user type data to share.')
            print('-'*10)

        # Display counts of gender
        if self.col_check(df, 'Gender'):
            print('Counts of Gender:\n  {}'.format(df.groupby(['Gender'])['Gender'].count()))
            print('-'*10)
        else:
            print('No gender data to share.')
            print('-'*10)


        # Display earliest, most recent, and most common year of birth
        if self.col_check(df, 'Birth Year'):
            print('Earliest year of birth among participants:\n  {}'.format(df['Birth Year'].min()))
            print('-'*10)
            print('Most recent year of birth among participants:\n  {}'.format(df['Birth Year'].max()))
            print('-'*10)
            print('Most common year of birth among participants:\n  {}'.format(df['Birth Year'].mode()[0]))
            print('-'*10)
        else:
            print('No birth year data to share.')
            print('-'*10)

        if self.col_check(df, 'Gender') and self.col_check(df, 'Trip Duration') and self.col_check(df, 'Month'):
            # Average trip duration by month distributed by gender
            print('Avg. Trip Duration by Month distributed by Gender:\n  {}'.format(df.groupby(['Gender', 'Month'])['Trip Duration'].mean()))
            print('-'*10)

            # Creating new DataFrame for transparency 
            df_gender = pd.DataFrame(df.groupby(['Gender', 'Month'])['Trip Duration'].mean()).reset_index()

            # Plot for Avg. Trip Duration by Month distributed by Gender
            plt.plot(df_gender['Month'].loc[df_gender['Gender'] == 'Female'], df_gender['Trip Duration'].loc[df_gender['Gender'] == 'Female'], 'g.-', label = 'Female')
            plt.plot(df_gender['Month'].loc[df_gender['Gender'] == 'Male'], df_gender['Trip Duration'].loc[df_gender['Gender'] == 'Male'], 'b.-', label = 'Male')
            plt.title('Avg.Trip Duration by Month\nFemale vs Male')
            plt.ylabel('Trip Duration')
            plt.xlabel('Months')
            plt.legend()
            plt.show()
        else:
            print('No gender or trip duration or month data to share.')
            print('-'*10)

        print("This took %s seconds." % (time.time() - start_time))
        print('-'*48+'\n')

    def menu(self):
        cities, months, days = self.get_filters()
        df = self.load_data(cities, months, days)
        self.time_stats(df)
        self.station_stats(df)
        self.trip_duration_stats(df)
        self.user_stats(df)
        while True:
            try:
                restart = input('\nWould you like to restart? Enter (y)yes or (n)no.\n')
                if restart.lower() == 'yes' or restart.lower() == 'y':
                    print('\nRestart.')
                    print('-'*48+'\n')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.menu()
                elif restart.lower() == 'no' or restart.lower() == 'n':
                    print('\nExit.')
                    print('='*48+'\n')
                    exit()
                else:
                    raise InvalidInput
            except InvalidInput:
                print('\n  !! Type valid input please !! (eg.: \'y\' | \'yes\' | \'n\' | \'no\')\n\n')
                continue

if __name__ == "__main__":
    bike_stat = StatisticsBikeshare()
    bike_stat.menu()