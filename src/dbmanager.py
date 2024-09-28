class DBManager:
    """для организации подключения и вывода различной информации из БД по определенным критериям"""

    def __init__(self, conn):
        self.conn = conn

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute('SELECT  employers.employer_name, COUNT(*) FROM vacancies '
                            'JOIN employers USING(employer_id)'
                            'GROUP BY employers.employer_name')
                rows = cur.fetchall()
                for i in rows:
                    print(f"компания - {(i[0])}, количество вакансий - {i[1]}")

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute('SELECT * FROM vacancies')
                rows = cur.fetchall()

                for i in rows:
                    print(f'{i} \n {"-" * 200}')

    def get_avg_salary(self, currency: str = "RUR"):
        """получает среднюю зарплату по вакансиям. по умолчанию "RUR" """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT AVG(salary) "
                            f"FROM vacancies "
                            f"WHERE vacancies.currency = %s", (currency,))
                rows = cur.fetchall()
                decimal_value = rows[0][0]
                if decimal_value is not None:
                    print(f"средняя зарплата - {int(decimal_value)} {currency}")

    def get_vacancies_with_higher_salary(self, currency: str = "RUR"):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. по умолчанию "RUR" """
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies WHERE currency = %s "
                            f"AND salary > (SELECT AVG(salary) "
                            f"FROM vacancies "
                            f"WHERE currency = %s)", (currency, currency))
                rows = cur.fetchall()
                for i in rows:
                    print(f'{i} \n {"-" * 200}')

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        with self.conn:
            with self.conn.cursor() as cur:
                like_pattern = f'%{keyword.lower()}%'
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE LOWER(vacancy_name) LIKE %s", (like_pattern,))
                rows = cur.fetchall()
                for i in rows:
                    print(f'{i} \n {"-" * 200}')

    def conn_close(self):
        """закрывает соединение с БД"""
        if self.conn:
            self.conn.close()