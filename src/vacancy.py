class Vacancy:
    """Класс для организации данных по вакансиям в удобном виде. хранит в себе полезные атрибуты по вакансиям"""

    def __init__(self, vacancy_id: str | int, vacancy_name: str, vacancy_url: str, salary: int, currency: int,
                 requirement: str, employer_id: str, employer_name: str):
        """ Конструктор класса """

        self.vacancy_id = vacancy_id
        self.vacancy_name = vacancy_name
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.vacancy_url = vacancy_url
        self.salary = salary
        self.currency = currency
        self.requirement = requirement

    def __lt__(self, other):
        """ Метод сравнения зарплат """
        # if self.salary is not None and other.salary is not None:
        return self.salary < other.salary

    def __str__(self):
        """ Строковое представление вакансии """

        return (f'ID вакансии: {self.vacancy_id}\n'
                f'ID компании: {self.employer_id}\n'
                f'Наименование компании: {self.employer_name}\n'
                f'Наименование вакансии: - {self.vacancy_name}\n'
                f'Ссылка на вакансию {self.vacancy_url}\n'
                f'Зарплата от - {self.salary},\n'
                f'Валюта - {self.currency},\n'
                f'Краткое описание: {self.requirement}\n')