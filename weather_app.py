import requests
from unidecode import unidecode
import csv
import sys
import pandas as pd
from tabulate import tabulate

# Language-specific messages
messages = {
    'en': {
        'city_prompt': 'City name: ',
        'language_prompt': 'Select a language (en or pt): ',
        'city_error': "City name might be incorrect. Please try again.",
        'more_details_prompt': 'Do you want to see more details? (y or n): ',
        'more_details_invalid': 'Invalid input',
        'weather_title': 'Current Weather',
        'detailed_weather_title': 'Detailed Current Weather',
        'short_csv_headers': ['Country', 'City', 'Temperature', 'Weather'],
        'detailed_csv_headers': ['Country', 'City', 'Temperature', 'Feels like', 'Wind', 'Humidity', 'Weather'],
    },
    'pt': {
        'city_prompt': 'Localidade: ',
        'language_prompt': 'Escolha uma linguagem (en ou pt): ',
        'city_error': 'Cidade desconhecida. Tente outra vez.',
        'more_details_prompt': 'Pretende mais detalhes? (s ou n): ',
        'more_details_invalid': 'Input inválido',
        'weather_title': 'Tempo atual',
        'detailed_weather_title': 'Tempo Atual Detalhado',
        'short_csv_headers': ['País', 'Localidade', 'Temperatura', 'Tempo'],
        'detailed_csv_headers': ['País', 'Localidade', 'Temperatura', 'Sensação térmica', 'Vento', 'Humidade', 'Tempo'],
    }
}

#constants
api_key = "69838aec6b6172080b855b05971723fc"

def main():
    title0 = 'Weather App'
    banner(title0)
    choose_language()
    choose_city()
    weather()

def choose_language():
    while True:
        global language
        language = input(messages['en']['language_prompt']).strip().lower()
        if language in ['en', 'english', 'inglês', 'ingles']:
            language = 'en'
            break
        elif language in ['pt', 'português', 'portugues','portuguese']:
            language = 'pt'
            break
        else:
            print('Choose a language: En or Pt | Escolha uma linguagem: En ou Pt')

def choose_city():
    while True:
        global city
        city = input(messages[language]['city_prompt'])
        url = f"http://api.openweathermap.org/data/2.5/weather?q={unidecode(city)}&appid={api_key}&lang={language}&units=metric"
        response = requests.get(url)
        if response.status_code != 200:
            print(messages[language]['city_error'])
            print('\n')
        else:
            global data
            data = response.json()
            print('\n')
            break  

def banner(title):
    print('\n','=' * 95,sep='')
    print(title.center(95))
    print('=' * 95)
    print('\n')


def weather():
   
    # Data storage
    with open('weather_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(messages[language]['short_csv_headers'])
        writer.writerow([data['sys']['country'],
                         unidecode(city).title(),
                         f"{round(data['main']['temp'],1)} °C",
                         data['weather'][0]['description']])

    # Data visualization
    title1 = messages[language]['weather_title']
    banner(title1)

    df = pd.read_csv('weather_data.csv', encoding='ISO-8859-1')
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False), '\n', sep='')

    # See more details (new data collection, storage, and visualization)
    while True:
        more_details = input(messages[language]['more_details_prompt']).strip().lower()
        print('\n')
        if more_details in ['n', 'no', 'nao', 'não']:
            sys.exit()
        elif more_details in ['s', 'sim', 'y', 'yes']:
            with open('weather_detailed_data.csv', mode='w', newline='') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow(messages[language]['detailed_csv_headers'])
                writer2.writerow([data['sys']['country'],
                                  unidecode(city).title(),
                                  f"{round(data['main']['temp'],1)} °C",
                                  f"{round(data['main']['feels_like'],1)} °C",
                                  f"{round(data['wind']['speed'],1)} m/s",
                                  f"{data['main']['humidity']} %",
                                  data['weather'][0]['description']])
            
            title2 = messages[language]['detailed_weather_title']
            banner(title2)
            df2 = pd.read_csv('weather_detailed_data.csv', encoding='ISO-8859-1')
            print(tabulate(df2, headers='keys', tablefmt='pretty', showindex=False), '\n', sep='')
            break
        else:
            print(messages[language]['more_details_invalid'])

if __name__ == '__main__':
    main()
