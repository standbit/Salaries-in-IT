import os
import time
from itertools import count

import ciso8601
import requests
from dotenv import load_dotenv
from terminaltables import SingleTable


def get_hh_vacancies(language):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    published_from_date = "2022-02-07"
    for page in count(0):
        payload = {
            "text": f"Программист {language}",
            "area": 1,
            "date_from": published_from_date,
            "page": page
            }
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()
        page_content = page_response.json()
        page_limit = page_content["pages"] - 1
        if page >= page_limit:
            break
        all_vacancies.append(page_content)
    return all_vacancies


def get_sj_vacancies(language):
    secret_key = os.getenv("SUPERJOB_KEY")
    url = "https://api.superjob.ru/2.0/vacancies/"
    all_vacancies = []
    published_from_date = "2022-02-07"
    converted_date = ciso8601.parse_datetime(published_from_date)
    unix_time = int(time.mktime(converted_date.timetuple()))
    for page in count(0):
        header = {
            "X-Api-App-Id": secret_key
        }
        payload = {
            "date_published_from": unix_time,
            "town": 4,
            "catalogues": 48,
            "keyword": language,
            "page": page,
            }
        page_response = requests.get(url, headers=header, params=payload)
        page_response.raise_for_status()
        page_content = page_response.json()
        page_limit = page_content["more"]
        if not page_limit:
            break
        all_vacancies.append(page_content)
    return all_vacancies


def predict_salary(salary_from, salary_to):
    if salary_from == 0 and salary_to == 0:
        return
    elif salary_from == 0 or salary_from is None:
        predict_salary = salary_to * 0.8
        return predict_salary
    elif salary_to == 0 or salary_to is None:
        predict_salary = salary_from * 1.2
        return predict_salary
    else:
        predict_salary = (salary_from + salary_to)/2
        return predict_salary


def predict_hh_salary(vacancy):
    if vacancy["salary"]:
        if vacancy["salary"]["currency"] != "RUR":
            return
        else:
            salary_from = vacancy["salary"]["from"]
            salary_to = vacancy["salary"]["to"]
            predicted_salary = predict_salary(salary_from, salary_to)
            return predicted_salary


def predict_sj_salary(vacancy):
    if vacancy["currency"] != "rub":
        return
    else:
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
        predicted_salary = predict_salary(salary_from, salary_to)
        return predicted_salary


def get_hh_salary_statistics():
    languages = [
        "Java",
        "C++",
        "Python",
        "Javascript",
        "Go",
        "Ruby",
        "Swift",
        "PHP"
        ]
    salary_statistics = {}
    for language in languages:
        response = get_hh_vacancies(language)
        if not response:
            salary_statistics[language] = {
                "vacancies_found": 0,
                "vacancies_processed": 0,
                "average_salary": 0
                }
        else:
            vacancies_found = response[0]["found"]
            salary_sum = 0
            vacancies_processed = 0
            for page in response:
                for vacancy in page["items"]:
                    salary = predict_hh_salary(vacancy)
                    if salary:
                        salary_sum += salary
                        vacancies_processed += 1
                average_salary = int(salary_sum/vacancies_processed)
                salary_statistics[language] = {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": vacancies_processed,
                    "average_salary": average_salary
                    }
    return salary_statistics


def get_sj_salary_statistics():
    languages = [
        "Java",
        "C++",
        "Python",
        "Javascript",
        "Go",
        "Ruby",
        "Swift",
        "PHP"
        ]
    salary_statistics = {}
    for language in languages:
        response = get_sj_vacancies(language)
        if not response:
            salary_statistics[language] = {
                "vacancies_found": 0,
                "vacancies_processed": 0,
                "average_salary": 0
                }
        else:
            vacancies_found = response[0]["total"]
            salary_sum = 0
            vacancies_processed = 0
            for page in response:
                for vacancy in page["objects"]:
                    salary = predict_sj_salary(vacancy)
                    if salary:
                        salary_sum += salary
                        vacancies_processed += 1
                average_salary = int(salary_sum/vacancies_processed)
                salary_statistics[language] = {
                    "vacancies_found": vacancies_found,
                    "vacancies_processed": vacancies_processed,
                    "average_salary": average_salary
                    }
    return salary_statistics


def create_table(company_salaries, title):
    data = []
    data.append([
        "Язык программирования",
        "Вакансий найдено",
        "Вакансий обработано",
        "Средняя зарплата"])
    for key, value in company_salaries.items():
        data.append([
            key,
            value["vacancies_found"],
            value["vacancies_processed"],
            value["average_salary"]
            ])
    table_instance = SingleTable(data, title)
    return table_instance


def main():
    load_dotenv()
    hh_salary_statistics = get_hh_salary_statistics()
    hh_title = "HeadHunter Moscow"
    table_instance = create_table(hh_salary_statistics, hh_title)
    print(table_instance.table)
    print()
    sj_salary_statistics = get_sj_salary_statistics()
    sj_title = "SuperJob Moscow"
    table_instance = create_table(sj_salary_statistics, sj_title)
    print(table_instance.table)


if __name__ == "__main__":
    main()
