import os

import DBManager
import functions

# Use environment variables to load database connection params
conn_params = {
    # 'dbname': os.getenv('DB_NAME'),
    'dbname': 'headhunter_vacancies',  # Updated database name
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Choosing random 10 Russian IT companies
russian_it_companies_default = [
    "Yandex", "Kaspersky", "Mail.Ru", "ABBYY", "1C", "Acronis", "Parallels", "Auriga", "EPAM", "Softline"
]

# Iterating over chosen companies above and saving them into database for future use
for company in russian_it_companies_default:
    functions.save_vacancies_for_company(company, conn_params)

# Preparing environment for using the DBManager and filtering vacancies
db_manager = DBManager.DBManager(conn_params)

# DBManager usage
with DBManager.DBManager(conn_params) as manager:
    # print(manager.get_companies_and_vacancies_count()) # Showing vacancies and counting them by company
    # print(manager.get_all_vacancies()) # Showing all vacancies test
    # print(manager.get_avg_salary()) # Getting avg salary test
    # print(manager.get_vacancies_with_higher_salary()) # Getting vacancies with salary higher than average test
    print(manager.get_vacancies_with_keyword('Python'))  # Searching for keyword Python test
