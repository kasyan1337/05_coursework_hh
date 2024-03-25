import requests


def get_companies_info(company_ids):
    companies_info = []
    for company_id in company_ids:
        response = requests.get(f'https://api.hh.ru/employers/{company_id}')
        if response.status_code == 200:
            companies_info.append(response.json())
    return companies_info



import psycopg2


class DBManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)

    def get_companies_and_vacancies_count(self):
        # SQL-запрос для получения количества вакансий у каждой компании
        pass

    def get_all_vacancies(self):
        # SQL-запрос для получения списка всех вакансий
        pass

    def get_avg_salary(self):
        # SQL-запрос для получения средней зарплаты по вакансиям
        pass

    def get_vacancies_with_higher_salary(self):
        # SQL-запрос для получения списка вакансий с зарплатой выше средней
        pass

    def get_vacancies_with_keyword(self, keyword):
        # SQL-запрос для поиска вакансий по ключевому слову
        pass
