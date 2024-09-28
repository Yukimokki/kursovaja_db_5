import time
import psycopg2
from src.api import HH
from src.dbmanager import DBManager
from src.utils import create_tables, drop_table, loads_into_table, creat_db


def main():
    creat_db()
    conn = psycopg2.connect(host='localhost', database='hh', user='postgres', password='12345') # устанавливаем соединение с конфиг файлом
    drop_table(conn, 'vacancies')  # удаляем таблицу vacancies
    drop_table(conn, 'employers')  # удаляем таблицу employers

    hh_api_instance = HH()  # экземляр класса HH

    # Проверка на кол-во введеных страниц, не больше 20, иначе выведем 2 по умолчанию
    page_quantity = input('Введите количество запрашиваемых страниц от 1 до 20: ')
    if page_quantity.isdigit() and 0 < int(page_quantity) <= 20:
        hh_api_instance.load_vacancies(int(page_quantity))
    else:
        print(f'вы ввели неверный параметр, по умолчанию будет загружено 2 страницы')
        time.sleep(1)
        hh_api_instance.load_vacancies()  # запрос через апи

    vacancies_list = hh_api_instance.vacancies
    vacancies_inst_list = hh_api_instance.parse_vacancies(vacancies_list)
    create_tables(conn)
    loads_into_table(conn, vacancies_inst_list)
    db_man_inst = DBManager(conn)

    while True:

        print('''1 - вывести на экран список всех компаний и количество вакансий у каждой компании
2 - вывести на экран список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
3 - вывести на экран среднюю зарплату по вакансиям. (по умолчанию RUR)
4 - вывести на экран список всех вакансий, у которых зарплата выше средней по всем вакансиям. (по умолчанию "RUR")
5 - вывести на экран список всех вакансий, в названии которых содержится ключевое слово.
0 - завершение программы
    ''')

        choice_number = ['1', '2', '3', '4', '5', '0']
        user_choice = input(f"{'*' * 50}\nВведите номер и нажмите 'enter' для пуска действия: ")

        if user_choice and user_choice == '1' and user_choice in choice_number:
            db_man_inst.get_companies_and_vacancies_count()

        elif user_choice and user_choice == '2' and user_choice in choice_number:
            db_man_inst.get_all_vacancies()

        elif user_choice and user_choice == '3' and user_choice in choice_number:
            user_input = input('введите валюту(только RUR): ')
            if user_input.isalpha():
                db_man_inst.get_avg_salary(user_input.upper())

        elif user_choice and user_choice == '4' and user_choice in choice_number:
            user_input = input('введите валюту(только RUR): ')
            if user_input.isalpha():
                db_man_inst.get_vacancies_with_higher_salary(user_input.upper())

        elif user_choice and user_choice == '5' and user_choice in choice_number:
            user_input = input('введите ключевое слово: ')
            db_man_inst.get_vacancies_with_keyword(user_input)

        elif user_choice and user_choice == '0' and user_choice in choice_number:
            db_man_inst.conn_close()
            break


if __name__ == '__main__':
    main()