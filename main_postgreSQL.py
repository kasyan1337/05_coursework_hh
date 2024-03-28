import psycopg2
import requests


def save_vacancies_for_company(company_name, conn_params):
    base_url = 'https://api.hh.ru/vacancies'
    params = {'text': f'компания:{company_name}'}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        vacancies_data = response.json()
        vacancies = vacancies_data.get('items', [])

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**conn_params)
        cur = conn.cursor()

        for vacancy in vacancies:
            vacancy_id = vacancy.get('id')
            name = vacancy.get('name')
            salary_info = vacancy.get('salary')
            salary_from = salary_info.get('from') if salary_info else None
            salary_to = salary_info.get('to') if salary_info else None
            currency = salary_info.get('currency') if salary_info else None
            address_info = vacancy.get('address')
            address = address_info.get('raw') if address_info else None
            snippet_info = vacancy.get('snippet')
            description = "; ".join(filter(None, [snippet_info.get('requirement') if snippet_info else None,
                                                  snippet_info.get('responsibility') if snippet_info else None]))
            url = vacancy.get('url')
            employer_info = vacancy.get('employer')
            employer_name = employer_info.get('name') if employer_info else 'Unknown'

            # Ensure all required fields are available before attempting to insert
            if vacancy_id and name and url and employer_name:
                # Insert data into the database
                cur.execute("""
                    INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, currency, address, description, url, company_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id) DO NOTHING;
                """, (vacancy_id, name, salary_from, salary_to, currency, address, description, url, employer_name))

        conn.commit()

        cur.close()
        conn.close()

        print(f"Saved {len(vacancies)} vacancies for {company_name} in the database.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


conn_params = {
    'dbname': 'headhunter_vacancies',
    'user': 'postgres',
    'password': '1337',
    'host': 'localhost',
    'port': '5433'
}


# First example
# save_vacancies_for_company("Yandex", conn_params)

# Random Russian IT companies
# russian_it_companies_default = [
#     "Yandex", "Kaspersky", "Mail.Ru", "ABBYY", "1C", "Acronis", "Parallels", "Auriga", "EPAM", "Softline"
# ]
#
# for company in russian_it_companies_default:
#     save_vacancies_for_company(company, conn_params)


class DBManager:
    def __init__(self, db_config):
        self.conn = psycopg2.connect(**db_config)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT company_name, COUNT(id) 
                FROM vacancies 
                GROUP BY company_name;
            ''')
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT company_name, name, salary_from, salary_to, url 
                FROM vacancies;
            ''')
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT AVG((salary_from + salary_to) / 2) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            ''')
            return cur.fetchone()

    def get_vacancies_with_higher_salary(self):
        with self.conn.cursor() as cur:
            cur.execute('''
                WITH avg_salary AS (
                    SELECT AVG((salary_from + salary_to) / 2) AS avg 
                    FROM vacancies 
                    WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
                )
                SELECT vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.url 
                FROM vacancies, avg_salary 
                WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > avg_salary.avg;
            ''')
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT name, salary_from, salary_to, url, description
                FROM vacancies 
                WHERE name ILIKE %s OR description ILIKE %s;
            ''', ('%' + keyword + '%', '%' + keyword + '%'))
            return cur.fetchall()


db_manager = DBManager(conn_params)

# print(db_manager.get_companies_and_vacancies_count())
# print(db_manager.get_all_vacancies())
# print(db_manager.get_avg_salary())
# print(db_manager.get_vacancies_with_higher_salary())
print(db_manager.get_vacancies_with_keyword('Python'))
