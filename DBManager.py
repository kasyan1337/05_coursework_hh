import psycopg2


class DBManager:
    """
    Manages database operations for storing and querying job vacancies.
    """

    def __init__(self, db_config):
        """
        Initializes the DBManager with the database configuration.
        :param db_config:
        """
        self.db_config = db_config

    def __enter__(self):
        """
        Opens the connection
        :return:
        """
        self.conn = psycopg2.connect(**self.db_config)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the connection
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Funtion to retrieve vacancies and count it by company
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT company_name, COUNT(id) 
                FROM vacancies 
                GROUP BY company_name;
            ''')
            return cur.fetchall()

    def get_all_vacancies(self):
        """
        Function to show all vacancies
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT company_name, name, salary_from, salary_to, url 
                FROM vacancies;
            ''')
            return cur.fetchall()

    def get_avg_salary(self):
        """
        Function to go over all vacancies and output average salary
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT AVG((salary_from + salary_to) / 2) 
                FROM vacancies 
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
            ''')
            return cur.fetchone()

    def get_vacancies_with_higher_salary(self):
        """
        Function to show vacancies that are higher than average salary
        :return:
        """
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
        """
        Search vacancies by keyword
        :param keyword: string
        :return:
        """
        with self.conn.cursor() as cur:
            cur.execute('''
                SELECT name, salary_from, salary_to, url, description
                FROM vacancies 
                WHERE name ILIKE %s OR description ILIKE %s;
            ''', ('%' + keyword + '%', '%' + keyword + '%'))
            return cur.fetchall()
