import requests
import json
from bs4 import BeautifulSoup
from pprint import pprint


def information_about_job_vacancies(job_title, numb_pages):
    vacancies_list = list()
    base_url = 'https://hh.ru'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    url = f'{base_url}/search/vacancy'
    for page in range(numb_pages):
        params = {'text': job_title,
                  'page': page}
        response = requests.get(url, headers=headers, params=params)
        dom = BeautifulSoup(response.text, 'html.parser')
        vacancies = dom.find_all('div', {'class': 'vacancy-serp-item vacancy-serp-item_redesigned'})
        for vacancy in vacancies:
            vacancies_data = {}
            info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            title_vacancy = info.getText()
            link_job = info['href']
            info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            site_from_vacancy = base_url + info['href']
            info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if info == None:
                salary_list = [None, None, None]
            else:
                salary_list = converting_str_to_list_salary(info.getText())
            vacancies_data['title_vacancy'] = title_vacancy
            vacancies_data['salary_list'] = salary_list
            vacancies_data['link_job'] = link_job
            vacancies_data['site_from_vacancy'] = site_from_vacancy
            vacancies_list.append(vacancies_data)
    return vacancies_list


def converting_str_to_list_salary(str_salary):
    salary_l = str_salary.split(' ')
    if salary_l[0] == 'от':
        return [int(salary_l[1].replace('\u202f', '')) , None, salary_l[2]]
    elif salary_l[0] == 'до':
        return [None, int(salary_l[1].replace('\u202f', '')), salary_l[2]]
    else:
        return [int(salary_l[0].replace('\u202f', '')), int(salary_l[2].replace('\u202f', '')), salary_l[3]]


if __name__ == '__main__':
    name_job = input('Введите название вакансии: ')
    try:
        page_site = int(input('Введите количество страниц: '))
    except ValueError:
        print(f'Вы ввели не число!!!')
    else:
        list_vacancies = information_about_job_vacancies(name_job, page_site)
        pprint(list_vacancies)
        with open('data_task2_1.json', 'w') as f:
            json.dump(list_vacancies), f)
