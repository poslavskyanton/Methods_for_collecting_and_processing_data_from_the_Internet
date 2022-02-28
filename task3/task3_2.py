from pprint import pprint
from pymongo import MongoClient


def max_salary_job_search(db_v, salary, currency):
    for doc in db_v.find({'salary_list.2': currency,'$or':
                          [{'$and': [{'salary_list.0': {'$lt': salary}}, {'salary_list.1': None}]},
                           {'$and': [{'salary_list.1': {'$gt': salary}}, {'salary_list.0': None}]},
                           {'$and': [{'salary_list.0': {'$ne': None}}, {'salary_list.1': {'$gt': salary}}]}]}):
        pprint(doc)


if __name__ == '__main__':
    currency_inp = input('Введите валюту("руб.", "USD"): ')
    try:
        salary_inp = int(input('Введите зарплату: '))
    except ValueError:
        print(f'Вы ввели не число!!!')
    else:
        client = MongoClient('127.0.0.1', 27017)
        db = client['vacations_db']
        vacations = db.vacations
        max_salary_job_search(vacations, salary_inp, currency_inp)
