from abc import ABC, abstractmethod
import requests
from src.vacancy import Vacancy


class Parser(ABC):
    @abstractmethod
    def load_vacancies(self):
        pass


employers_ids = {
    6093775: 'Aston',
    15478:'VK',
    78638:'T-bank',
    67611:'Tensor',
    1740:'Yandex_team',
    733:'Lanit',
    41144:'Askon',
    9418714:'LaModa_tech',
    10711119:'CosmoMedia',
}


class HH(Parser):
    employers_data = employers_ids

    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': 'Python',
                       'employer_id': '',
                       'page': 0,
                       'only_with_salary': True,
                       'per_page': 100,
                       'area': 113,}
        self.vacancies = []

    def load_vacancies(self, page_quantity: int = 2):
        """загружает данные c АПИ по определенным параметрам"""
        self.params['employer_id'] = self.employers_data
        while self.params.get('page') != page_quantity:
            response = requests.get(self.url, headers=self.__headers, params=self.params)
            response.raise_for_status()
            vacancy = response.json()['items']
            self.vacancies.extend(vacancy)
            self.params['page'] += 1

    @staticmethod
    def parse_vacancies(vacancies: list[dict]) -> list[dict]:
        """ Метод фильтрует с API по заданным ключам и возвращает список экз. класса """

        items = []
        for i in vacancies:
            vacancy_id = i.get('id')
            vacancy_name = i.get('name')
            vacancy_url = i.get('alternate_url')

            salary_dict = i.get('salary')
            salary_from = salary_dict.get('from')
            if salary_from is None:
                salary_from = 0

            if salary_dict:
                salary_dict = i.get('salary')
                currency = salary_dict.get('currency')
            else:
                currency = ''

            snippet_dict = i.get('snippet')
            snippet_requirement = snippet_dict.get('requirement')
            if snippet_requirement:
                snippet_requirement = snippet_requirement.replace('<highlighttext>', '').replace('</highlighttext>', '')
            else:
                snippet_requirement = 'нет требований'

            employer = i.get('employer')
            employer_id = employer.get('id')
            employer_name = employer.get('name')

            vacancy_object = Vacancy(vacancy_id, vacancy_name, vacancy_url, salary_from, currency, snippet_requirement,
                                     employer_id, employer_name)

            items.append(vacancy_object)
        return items