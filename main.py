import requests
import datetime as dt
import json
import sys
from os.path import dirname, join, getmtime,exists
from os import listdir


class WeatherForecast:

    def date_(self):
        print('Enter the date to check rain probability (YYYY-MM-DD)')
        date_input = input(
            "Press enter key to to get Tomorrows data, type (today) for today's date or (exit) to quit: ")
        if not date_input:
            date = dt.date.today() + dt.timedelta(1)
            date_format = date.strftime('%Y-%m-%d')
            print(f'No date given, checking for tomorrow: {date_format}')
            return date_format
        elif date_input == 'today':
            date = dt.date.today()
            date_format = date.strftime('%Y-%m-%d')
            print(f"Using today's date: {date_format}")
            return date_format
        elif date_input == 'exit':
            sys.exit()
        else:
            try:
                date_input = dt.datetime.strptime(date_input, '%Y-%m-%d')
                date_format = date_input.strftime('%Y-%m-%d')
                return date_format
            except ValueError:
                print('Invalid date or format entered')
                self.date_()

    def weather(self,search_date):
        latitude, longitude = 52.13776120092765, -7.936540192825734
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=precipitation_probability_max&timezone=Europe%2FLondon&start_date={search_date}&end_date={search_date}'
        response = requests.get(url)
        return response.text

    def weather_cached(self,search_date):
        use_cache = True
        file_path = join('cache', search_date)
        if not exists(file_path):
            use_cache = False
        elif dt.datetime.fromtimestamp(getmtime(file_path)) < dt.datetime.now() - dt.timedelta(hours=24):
            use_cache = False
        if use_cache:
            print('Cache used')
            print()
            with open(file_path) as file:
                return float(file.read())
        weather_txt = self.weather(search_date)
        precipitation = json.loads(weather_txt)
        precipitation_probability = float(precipitation["daily"]["precipitation_probability_max"][0])
        self[search_date] = precipitation_probability

    def __getitem__(self, item):
        try:
            return self.weather_cached(item)
        except KeyError:
            return None

    def __setitem__(self, item, value):
        file_path = join('cache', item)
        with open(file_path, 'w') as file:
            file.write(str(value))


wf = WeatherForecast()
date_entered = wf.date_()
print('Probability of rain:', wf[date_entered], '%')
print()
print('files cached: ')
for file in listdir('cache'):
    print(file)