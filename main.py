"""
Программа включает в себя следующие функции:
- read_data(filename: str) -> List[Dict[str, str]]:
  Читает данные из CSV-файла и возвращает список словарей.

- display_hierarchy(data: List[Dict[str, str]]):
  Выводит иерархию команд на экран.

- gen_department_report(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
  Генерирует сводный отчёт по департаментам на основе входных данных.

- print_department_report(report: List[Dict[str, str]]) -> None:
  Печатает сводный отчёт о департаментах в виде таблицы.

- save_report_to_csv(report: List[Dict[str, str]], filename: str):
  Сохраняет сводный отчёт в CSV-файл.

- main() -> None:
  Главная функция для взаимодействия с пользователем через командное меню
"""

import csv
from typing import List, Dict


def read_data(filename: str) -> List[Dict]:
    """
    Читает данные из CSV-файла и возвращает список словарей.

    :param filename: Имя CSV-файла.
    :return: Список словарей с данными.
    """
    data = []
    with open(filename, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            data.append(row)
    return data


def display_hierarchy(data: List[Dict]):
    """
    Выводит иерархию команд на экран.

    :param data: Список словарей с данными.
    """
    departments = set()
    teams = {}  # type: ignore
    for entry in data:
        department = entry['Департамент']
        team = entry['Отдел']
        departments.add(department)
        if department in teams:
            teams[department].add(team)
        else:
            teams[department] = {team}

    print('Иерархия команд:')
    for department in sorted(departments):
        print(f'- {department}')
        if department in teams:
            for team in sorted(teams[department]):
                print(f'  - {team}')


def gen_department_report(data: List[Dict]) -> List[Dict]:
    """
    Генерирует сводный отчёт по департаментам на основе входных данных.

    :param data: Список словарей с данными о сотрудниках.
    :return: Список словарей с отчётом по департаментам.
    """
    department_report = []
    departments = set()
    for entry in data:
        department = entry['Департамент']
        departments.add(department)

    for depart in sorted(departments):
        depart_data = [ent for ent in data if ent['Департамент'] == depart]
        salaries = [int(entry['Оклад']) for entry in depart_data]
        min_salary = min(salaries)
        max_salary = max(salaries)
        salary_range = f'{min_salary} – {max_salary}'

        report_entry = {
            'Департамент': depart,
            'Численность': len(depart_data),
            'Вилка зарплат': salary_range,
            'Средняя зарплата': sum(salaries) / len(salaries)
        }

        department_report.append(report_entry)

    return department_report


def print_department_report(report: List[Dict]) -> None:
    """
    Печатает сводный отчёт о департаментах в виде таблицы.

    :param report: Список словарей с отчётом.
    """
    if not report:
        print('Отчёт пуст.')
        return

    table_headers = report[0].keys()
    table_data = [entry.values() for entry in report]

    column_widths = [max(len(str(header)), max(len(str(entry[header]))
                                               for entry in report))
                     for header in table_headers]

    for header, width in zip(table_headers, column_widths):
        print(f'{header:{width}}', end=' | ')
    print()

    for width in column_widths:
        print('-' * width, end=' | ')
    print()

    for row in table_data:
        for item, width in zip(row, column_widths):
            print(f'{item:{width}}', end=' | ')
        print()


def save_report_to_csv(report: List[Dict], filename: str):
    """
    Сохраняет сводный отчёт в CSV-файл.

    :param report: Список словарей с отчётом.
    :param filename: Имя CSV-файла для сохранения.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        fieldnames = report[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for row in report:
            writer.writerow(row)


def main() -> None:
    """
    Главная функция для взаимодействия с пользователем через командное меню.

    Функция запрашивает у пользователя файл с данными и предоставляет
    следующие опции:
    1. Вывести иерархию команд.
    2. Вывести сводный отчёт по департаментам.
    3. Сохранить сводный отчёт в CSV-файл.

    :return: None
    """
    filename = input('Название файла с данными (Enter: Corp_Summary.csv): ')
    if filename == '':
        filename = '../Corp_Summary.csv'
    department_report = None

    try:
        data = read_data(filename)
    except FileNotFoundError as file_exception:
        print(str(file_exception))
        return
    while True:
        print("""Меню:
        1. Вывести иерархию команд
        2. Вывести сводный отчёт по департаментам
        3. Сохранить сводный отчёт в CSV-файл
        Чтобы выйти введите 'exit'
        """)
        choice = input('Выберите пункт меню: ')
        if choice == '1':
            display_hierarchy(data)
        elif choice == '2':
            department_report = gen_department_report(data)
            print_department_report(department_report)
        elif choice == '3':
            if department_report is not None:
                out_filename = input('Название отчёта (Enter: report.csv): ')
                if out_filename == '':
                    out_filename = '../report.csv'
                save_report_to_csv(department_report, out_filename)
                print(f'Отчёт сохранён в файл {out_filename}')
            else:
                out_filename = input('Название отчёта (Enter: report.csv): ')
                if out_filename == '':
                    out_filename = '../report.csv'
                department_report = gen_department_report(data)
                save_report_to_csv(department_report, out_filename)
                print(f'Отчёт сохранён в файл {out_filename}')
        elif choice == 'exit':
            break
        else:
            print('Неверный выбор. Попробуйте снова.')


if __name__ == '__main__':
    main()
