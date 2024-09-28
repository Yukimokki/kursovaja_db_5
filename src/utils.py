import psycopg2


def create_tables(conn):
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    employer_id INT PRIMARY KEY,
                    employer_name VARCHAR(100) NOT NULL
                )
            """)

            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(employer_id),
                    vacancy_name VARCHAR(100) NOT NULL,
                    salary INT NOT NULL,
                    currency VARCHAR(100),
                    requirement TEXT,
                    vacancy_url VARCHAR(100) NOT NULL
                )
            """)


def loads_into_table(conn, vacansies: list) -> None:
    """заполняет таблицу данными о вакансиях"""

    with conn:
        with conn.cursor() as cur:
            for vac in vacansies:
                cur.execute('INSERT INTO employers (employer_id, employer_name) VALUES '
                            '(%s,%s)' 'ON CONFLICT (employer_id) DO NOTHING', (vac.employer_id, vac.employer_name))

                cur.execute(
                    'INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, salary, currency, '
                    'requirement, vacancy_url) VALUES '
                    '(%s,%s,%s,%s,%s,%s, %s)',
                    (vac.vacancy_id, vac.employer_id, vac.vacancy_name, vac.salary, vac.currency,
                     vac.requirement, vac.vacancy_url))


def drop_table(conn, table_name) -> None:
    """удаляет таблицу. по умолчанию соединение закроется. если передать в con_status 1 то останется открытым"""
    with conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            print(f'из базы данных удалена таблица {table_name}')


def creat_db():
    """Создание базы данных"""
    conn = psycopg2.connect(host='localhost', user='postgres', password='12345')
    cursor = conn.cursor()
    conn.autocommit = True
    try:
        sql = "CREATE DATABASE HH"
        cursor.execute(sql)
    except psycopg2.errors.DuplicateDatabase:
        pass
    cursor.close()
    conn.close()