import time
import re
import pandas as pd
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
xt = ['q', 'quit', 'exit', 'done', 'end', 'stop', 'bye', 'x', 'xt', 'die',
      'leave', 'no', 'kill', 'over', 'break', 'nope', 'nada', 'none']
q = False
rep = False
city = None
month = 'all'
mi = None
day = 'all'


def get_city():
    """
    Asks user to specify a city to analyze.
    Returns: (str) city - name of the city to analyze
    Displays: intro + welcome image
    """
    global q
    global city
    print('\n\n\n\n\n\nHello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    while (city not in CITY_DATA.keys()) and (q is not True):
        incity = input("Are you interested in bikeshare data from Chicago, "
                       "New York City, or Washington DC?\n" +
                       '(At any prompt, type q to quit)\n\n')
        incity = str.lower(incity)
        if re.match('chi', incity) or re.match('windy', incity):
            city = 'chicago'
        elif re.match('new york', incity) or incity in ['nyc', 'ny']:
            city = 'new york city'
        elif re.match('washington', incity) or re.match('d?.c?.$', incity):
            city = 'washington'
        elif incity in xt:
            q = True
            return None, None, None
        else:
            print('\nSorry. Our database only covers Chicago, NYC, and DC')
            time.sleep(2)
    else:
        plt.ion()
        print('\nWelcome to ' + str.capitalize(city) + '!')
#        time.sleep(1)
        plt.figure(figsize=(14, 10), frameon=False)
        plt.rcParams['axes.labelpad'] = 2
        plt.rcParams['axes.titlepad'] = 3
        plt.axis('off')
        plt.imshow(CITY_DATA[city][1], aspect='equal')
        plt.autoscale(tight=True)
        plt.show()
#       plt.pause(3)
        plt.close()

    print("\nWe have access to bikeshare data from " + str.capitalize(city) +
          ' for January through June of 2017.')
#    time.sleep(3)
    print("Over the course of those six months, city residents took " +
          str(CITY_DATA[city][2]) + " rides on bikeshare bicycles.\n")
    if not rep:
#        time.sleep(3)
        print("Every one of those rides was logged in detail as part of the "
              "program's data collection efforts.\n")
#        time.sleep(3)
        if city != 'washington':
            print("For each trip, the program tracked start and end times, "
                  "duration, start and end station (location), users' status "
                  "(subscription or single-ride customer), age, and gender.\n")
        else:
            print("For each trip, the program tracked start and end times, "
                  "duration, start and end station (location), and user type "
                  "(service subscriber or single-use customer).\n")
#        time.sleep(4)
        print("If you'd like, you can choose to look at ride data from a "
              "single month only and/or a specific day of the week.")
    return city


def get_filters():
    # Choose filter(s) or no filter
    global q
    selection = None
    while (not q) and (month not in months) and (day not in days):
        time.sleep(2)
        selection = input("Would you like to filter by (M)onth, (D)ay of "
                          "week, (B)oth month AND day of week, or return "
                          "(A)ll results?\n(type q to quit)\n\n")
        selection = str.lower(selection)
        if selection in xt:
            q = True
            return None, None, None
        elif selection == 'a':
            break
        if selection in ['m', 'b']:
            get_month()
            if (selection == 'm') or q:
                break
        if selection in ['d', 'b']:
            if q:
                break
            get_day()
            break
        else:
            print("That is not a valid selection.\n")
            time.sleep(1)
            print("Please choose from the following or press q to quit")
            continue
        print("\nFetching the data you specified.")
    print('-'*40)
#    time.sleep(4)
    return month, mi, day


def get_month():
    global month
    global mi
    global q
    while month not in months[:6]:
        time.sleep(1)
        month = input("Choose a month from January through June.\n")
        month = str.lower(month)
        if month in xt:
            q = True
            return None, None, None
        elif month[0:3] in [m[0:3] for m in months] or month.isdigit():
            for i, m in enumerate(months):
                if (month[0:3] == m[0:3]) or (month == str(i+1)):
                    if 0 <= i <= 5:
                        month = m
                        mi = i + 1
                        break
                    elif i > 5:
                        print("We only have data for January through "
                              "June")
        else:
            print("That isn't a valid month")
    print("You chose " + month.capitalize())
    time.sleep(1)


def get_day():
    global day
    global q
    while day not in days:
        time.sleep(1)
        day = input("Choose a day of the week. i.e. Sunday, Monday, "
                    "etc.\n")
        day = str.lower(day)
        if day in xt:
            q = True
            return None, None, None
        elif day[0:3] in [d[0:3] for d in days]:
            day = [d for i, d in enumerate(days) if day[0:3] == d[0:3]][0]
            break
        print("That is not a valid day of the week.")
    print("You chose " + day.capitalize())
    time.sleep(1)


def load_data(city, month='all', mi=None, day='all'):
    """
    Loads data for the specified city and filters by month and/or day(optional)

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all"
        (int) mi - index of filter month or None
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
    dfull = df.copy()
    # filter by month if applicable
    if month != 'all':
        df = df[df['month'] == mi]
    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df, dfull


def time_stats(df, dfull):
    # Displays statistics on the most frequent times of travel.
    print('\nCalculating The Most Frequent Times of Travel...\n')
    time.sleep(1)
    print('\nReady....')
#    time.sleep(2)
    print('\n\nGO!\n\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: " +
          months[dfull['month'].mode()[0] - 1].title())
    # display the most common day of week
    print("The most common day is: " + dfull['day_of_week'].mode()[0])
    # display the most common start hour
    print("The most common hour is: " +
          str(dfull['Start Time'].dt.hour.mode()[0]))
    if month != 'all':
        dfmonth = dfull[dfull['month'] == mi]
        print("The most common day in " + month.title() + " is: " +
              str(dfmonth['day_of_week'].mode()[0]))
        print("The most common hour in " + month + " is: " +
              str(dfmonth['Start Time'].dt.hour.mode()[0]))
    if day != 'all':
        dfday = dfull[dfull['day_of_week'] == day.capitalize()]
        print("the most common hour on " + day + " is: " +
              str(dfday['Start Time'].dt.hour.mode()[0]))
        if month != 'all':
            print("The most common hour on " + day + " during the month of " +
                  month + " is: " + str(df['Start Time'].dt.hour.mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, dfull):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station


    # display most commonly used end station


    # display most frequent combination of start station and end station trip


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, dfull):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time


    # display mean travel time


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, dfull):
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
        global city, month, day, rep
        city = get_city()
        month, mi, day = get_filters()
        if q:
            print("Bye!")
            break
        df, dfull = load_data(city, month, mi, day)
        if q:
            print("Bye!")
            break
        time_stats(df, dfull)
        station_stats(df, dfull)
        trip_duration_stats(df, dfull)
        user_stats(df, dfull)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ['yes', 'y']:
            print("Bye!")
            break
        city = None
        month = 'all'
        day = 'all'
        rep = True


if __name__ == "__main__":
    main()
