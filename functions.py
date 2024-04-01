import psycopg2
import requests


def save_vacancies_for_company(company_name, conn_params):
    """
    Loads the vacancies to PostgreSQL database from HH.ru; saves them for future use
    :param company_name:
    :param conn_params:
    :return:
    """
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
