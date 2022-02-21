import json
import requests


user_name = input('Введите имя пользователя: ')
#user_name = 'Microsoft'
url = f'https://api.github.com/users/{user_name}/repos'
response = requests.get(url)
if response.status_code == 200:
    with open('data_task1_1.json', 'w') as f:
        json.dump(response.json(), f)
    for i in response.json():
        print(i['name'])
