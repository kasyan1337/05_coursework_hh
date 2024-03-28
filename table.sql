CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    vacancy_id VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    salary_from INTEGER,
    salary_to INTEGER,
    currency VARCHAR(50),
    address TEXT,
    description TEXT,
    url TEXT NOT NULL,
    company_name VARCHAR(255) NOT NULL
);
