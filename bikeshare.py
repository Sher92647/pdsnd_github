import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze the bikeshare data.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). Code will ask for user input again if input is invalid.
    while True:
        city = input('Would you like to see data for Chicago, New York City, or Washington?: ').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('Sorry, that city input was invalid. Please try again.')
            continue


    # get user input for month (all, january, february, ... , june). Code will ask for user input again if input is invalid.
    while True:
        month = input('Which month? January, February, March, April, May, or June? Type \"all\" for all months: ').lower()
        if month in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            break
        else:
            print('Sorry, that month input was invalid. Please try again.')
            continue


    # get user input for day of week (all, monday, tuesday, ... sunday). Code will ask for user input again if input is invalid.
    while True:
        day = input('Which day? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday. Type \"all\" for all days of the week: ').lower()
        if day in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            break
        else:
            print('Sorry, that month input was invalid. Please try again.')
            continue


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city]) # load data file into dataframe
    df['Start Time'] = pd.to_datetime(df['Start Time']) # convert the Start Time column to datetime
    df['month'] = df['Start Time'].dt.month_name() # create a new column with the start time month
    df['day_of_week'] = df['Start Time'].dt.day_name() # create a new column with the start time day

    if month != 'all':
        df = df[df['month'] == month.title()]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most popular month for travel was:', popular_month)


    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day for travel was:', popular_day)


    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular start hour for travel was:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().idxmax()
    print('The most commonly used start station was:', popular_start)


    # display most commonly used end station
    popular_end = df['End Station'].value_counts().idxmax()
    print('\nThe most commonly used end station was:', popular_end)


    # display most frequent combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).count()
    combination_station = combination_station.sort_values(['Start Station', 'End Station'], ascending = False)
    print('\nThe most popular trip from start to end was:', combination_station.iloc[:1, :1])

    # display most uncommon combination of start station and end station trip
    combination_station = df.groupby(['Start Station', 'End Station']).count()
    combination_station = combination_station.sort_values(['Start Station', 'End Station'], ascending = True)
    print('\nThe most uncommon trip from start to end was:', combination_station.iloc[:1, :1])
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time was:', round(total_travel_time/86400), 'Days')


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The average travel time was:', round(mean_travel_time/60), 'Minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('What was the breakdown of users?\n', user_types)


    # Display counts of gender
    print('\nWhat is the breakdown of gender?\n')
    
    try:
        gender_types = df['Gender'].value_counts()
        print('Gender breakdown:\n', gender_types)

    except:
        print('Sorry! No data on gender available for this city\n')


    # Display earliest, most recent, and most common year of birth
    print('\nWhat was the oldest, youngest, and most popular year of birth?\n')

    try:
        oldest_birth_year = df['Birth Year'].min()
        print('Oldest birth year:\n', round(oldest_birth_year))

        youngest_birth_year = df['Birth Year'].max()
        print('\nYoungest birth year\n', round(youngest_birth_year))

        popular_birth_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost popular birth year:\n', round(popular_birth_year))

    except:
        print('Sorry! No data on birth year available for this city\n')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw(df):
    counter = 0

    while True:
        if counter == 0:
            user_input = input('Would you like to see 5 lines of the raw data? ').lower()
        else:
            user_input = input('Would you like to see the next 5 lines of the raw data? ').lower()

        if user_input == 'yes':
            start_position = 5 * counter
            end_position = min(start_position + 5, len(df))

            print(df[start_position: end_position])
            counter += 1

            continue
        elif user_input == 'no':
            break
        else:
            print('Sorry, that is not a valid input. Please try again.')
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
