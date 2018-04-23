import time
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib


ny = plt.imread(urllib.request.urlopen('https://media-cdn.tripadvisor.com/'
                'media/photo-s/0e/9a/e3/1d/freedom-tower.jpg'), format='jpg')

chi = plt.imread(urllib.request.urlopen('http://www.essexinn.com/d/essexinn/'
                'media/Attractions/__thumbs_1600_714_crop/ChicagoSkyline'
                '.jpg.jpg?1427109369'), format='jpg')

dc = plt.imread(urllib.request.urlopen('http://diningoutfree.com/wp-content/'
                'uploads/2014/06/Washington-DC-City.jpg'), format='jpg')

CITY_DATA = {'chicago': ['data/chicago.csv', chi, 2577936],
             'new york city': ['data/new_york_city.csv', ny, 2641886],
             'washington': ['data/washington.csv', dc, 2100005]}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday']

xt = ['q', 'quit', 'exit', 'done', 'end', 'stop', 'bye',
      'leave', 'no', 'kill', 'over', 'break', 'nope', 'nada', 'none']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"
    """
    city = None
    print('\n\n\n\n\n\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while (city not in CITY_DATA.keys()) and (city not in xt):
        incity = input("Are you interested in bikeshare data from Chicago, "
                       "New York City, or Washington DC?\n" +
                       '(Type q to quit)\n\n')
        incity = str.lower(incity)
        if re.match('^chi', incity) or re.match('^windy', incity):
            city = 'chicago'
        elif re.match('^new york', incity) or incity == 'nyc':
            city = 'new york city'
        elif re.match('^washington', incity) or re.match('d?.c?.$', incity):
            city = 'washington'
        elif incity in xt:
            city = incity
        else:
            print('\nSorry. Our database only covers Chicago, NYC, and DC')
    if incity in xt:
        print('\n OK! Seeya later!')
    else:
        plt.ion()
        print('\nWelcome to ' + str.capitalize(city) + '!')
        time.sleep(1)
        plt.figure(figsize=(14, 10), frameon=False)
        plt.rcParams['axes.labelpad'] = 2
        plt.rcParams['axes.titlepad'] = 3
        plt.axis('off')
        plt.imshow(CITY_DATA[city][1], aspect='equal')
        plt.autoscale(tight=True)
        plt.show()
        plt.pause(3)
        plt.close()

    # get user input for month (all, january, february, ... , june)
    print("\nWe have access to bikeshare data from " + str.capitalize(city) +
          ' for January through June of 2017.')
    time.sleep(2)
    print("Over the course of those six months, city residents took " +
          str(CITY_DATA[city][2]) + " rides on bikeshare bicycles.\n")
    time.sleep(2)
    print("Every one of those rides was logged in detail as part of the "
          "program's data collection efforts so that analysts could use the "
          "information to guide future decisions about bikesharing\n")
    time.sleep(2)
    if city != 'washington':
        print("For each trip, the program tracked start and end times, "
              "duration, start and end station (location), user type (service "
              "subscriber or single-use customer, and rider age and gender.\n")
    else:
        print("For each trip, the program tracked start and end times, "
              "duration, start and end station (location), and user type "
              "(service subscriber or single-use customer.\n")
    time.sleep(1)
    print("Would you like to take a look at all the data or would you rather"
          " limit your view to a single month's rides?")
#    input("(press ))

    # get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*40)
    return city, 'all', 'all'  # , month, day


def load_data(city, month='all', day='all'):
    """
    Loads data for the specified city and filters by month and day (optional)

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (str) day - name of the day of week to filter by, or "all"

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city][0])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = list(i+1 for i in range(len(months)) if months[i] == month)[0]
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    # display the most common day of week

    # display the most common start hour

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types


    # Display counts of gender


    # Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
#       df = load_data(city, month, day)
#
#       time_stats(df)
#       station_stats(df)
#       trip_duration_stats(df)
#       user_stats(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
