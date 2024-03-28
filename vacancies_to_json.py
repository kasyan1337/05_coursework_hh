import requests
import os
import json


def fetch_vacancies_for_company(company_name):
    base_url = 'https://api.hh.ru/vacancies'

    params = {
        'text': f'компания:{company_name}'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises an error for HTTP errors

        # Parse the JSON response
        vacancies_data = response.json()

        # Path
        save_dir = 'data'
        os.makedirs(save_dir, exist_ok=True)  # Create the directory if it does not exist
        file_path = os.path.join(save_dir, f'{company_name}.json')

        # Write the data to a JSON file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

        print(f"Saved vacancies for {company_name} in {file_path}")

    except requests.RequestException as e:
        print(f"Error fetching vacancies for {company_name}: {e}")


russian_it_companies_default = [
    "Yandex",
    "Kaspersky",
    "Mail.Ru",
    "ABBYY",
    "1C",
    "Acronis",
    "Parallels",
    "Auriga",
    "EPAM",
    "Softline"
]

# for company in russian_it_companies_default:
#     fetch_vacancies_for_company(company)

fetch_vacancies_for_company('Peptides')