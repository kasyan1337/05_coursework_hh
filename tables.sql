CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    logo URL
);

CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    title TEXT NOT NULL,
    salary TEXT,
    url TEXT NOT NULL
);
