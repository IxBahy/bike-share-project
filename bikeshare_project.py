
import pandas as pd
import numpy as np
# reading the csv files into variables:
chicago_data = pd.read_csv("F:\programming projects\chicago.csv")
nyc_data = pd.read_csv("F:\programming projects\\new_york_city.csv")
washington_data = pd.read_csv("F:\programming projects\washington.csv")
# creating a dict with the variables we made
City_Data = {'chicago': chicago_data,
             'new york': nyc_data, 'washington': washington_data}

# making a check functions to make sure that the values user enter are correct


def check_value(value, type):
    while True:
        try:
            if value in ['chicago', 'new york', 'washington'] and type == 'city':
                break
            elif value in ['january', 'february', 'march', 'april', 'may', 'june', 'all'] and type == 'month':
                break
            elif value in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'] and type == 'day':
                break
            else:
                if type == 'city' and value not in ['chicago', 'new york', 'washington']:
                    print('wrong city value')
                    get_inputs()
                if type == 'day' and value not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
                    print('wrong day value')
                    get_inputs()
                if type == 'month' and value not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                    print('wrong month value')
                    get_inputs()

        except ValueError:
            print('Invalid input')
    return value

# getting values from user with the function while also calling the check function


def get_inputs():
    city = check_value(input
                       ('pleas select what city you want the data from: chicago, new york, Washington \n').lower(), 'city')

    format_type = (
        input('do you want data shown by the : month, day, both \n').lower())
    if format_type == 'both':
        month = check_value(input
                            ('pleas select what month you want the data from \n note: form january till june\n').lower(), 'month')
        day = check_value(input
                          ('pleas select what day you want the data from \n').lower(), 'day')

    elif format_type == 'day':
        day = input('pleas select what day you want the data from \n').lower()
        check_value(day, 'day')
        month = None
    elif format_type == 'month':
        month = input(
            'pleas select what month you want the data from \n note: form january till june\n').lower()
        check_value(month, 'month')
        day = None
    print('_'*40)
# return checked values
    return city, month, day


def load_data(city, month=None, day=None):
    # load data file into a dataframe
    df = (City_Data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month is None:
        for month in df['month']:
            month = None
    elif month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day == None:
        for day in df['day_of_week']:
            day = None
    elif day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

# calculate the time statistics (most common month,day,duration)


def Travel_Time_stats(df):
    print('Travel Time stats are : \n')
    if df['month'] is not None:
        print('most common month is ', df['month'].mode()[0])
    if df['day_of_week'] is not None:
        print('most common day is ', df['day_of_week'].mode()[0])
    print('most common duration is ', df['hour'].mode()[0])
    print('_'*40)

# calculate the stations statistics(most common start,end,trip)


def Travel_Stations_stats(df):
    print('Travel Stations stats are : \n')
    print('most common start stations is :', df['Start Station'].mode()[0])
    print('most common end stations is :', df['End Station'].mode()[0])
    print('most common trip is', df.groupby('Start Station')
          ['End Station'].agg(pd.Series.mode))
    print('_'*40)

# calculate the user statistics (user type,gender,BD)


def Traveller_stats(df, city):
    print('Traveller stats are : \n')
    print('types of users are \n ', df['User Type'].value_counts())
    if city != 'washington':
        print('count of each gender is\n ', df['Gender'].value_counts())
        print("birth_date stats are :")
        print('minimum date is : ', df['Birth Year'].min())
        print('maximum date is : ', df['Birth Year'].max())
        print('most common date is : ', df['Birth Year'].mode()[0])

    print('_'*40)

# calculate the total time for trips statistics (total,average time taken)


def Travel_durations_stats(df):
    print('Travel durations  stats are : \n')
    print('total duration time is ', df['Trip Duration'].sum())
    print('average duration time is \n', df['Trip Duration'].mean())
    print('_'*40)


def main():
    # a loo[ so the user can use the program until he is done ]
    while True:
        # assigning the values returned froma the get_input functions as a tuple into single variables
        city, month, day = get_inputs()
        # creating th data frame and calling the other functions to print the calculations
        df = load_data(city, month, day)
        Travel_Time_stats(df)
        Travel_Stations_stats(df)
        Traveller_stats(df, city)
        Travel_durations_stats(df)
        view_data = input(
            'do you want to see 5 rows of individual trip data? \n Enter yes or no : ').lower()
        index = 0
        while view_data == 'yes':
            print(df.iloc[index:index+5])
            index += 5
            view_data = input(
                'do you wish to continue? \n Enter yes or no : ').lower()
            if view_data == 'no':
                break
        # making an exit option to the user
        exit = input("do you want to exit the programm\n").lower()
        if exit == 'yes':
            break


if __name__ == "__main__":
    main()
