from urllib import response
import requests
from pprint import pprint
import json
from itertools import count
import os
from dotenv import load_dotenv


def get_it_vacancies(language):
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []
    for page in count(0):
        payload = {
            "text": "Программист",
            "text": language,
            "area": 1,
            "date_from": "2022-02-07",
            "page": page
            }
        page_response = requests.get(url, params=payload)
        page_response.raise_for_status()
        page_content = page_response.json()
        page_limit = page_content["pages"] -1 
        if page >= page_limit:    # потому что вылазила ошибка, когда page=100
            break
        all_vacancies.append(page_content)
    return all_vacancies


# def write_json_file(response):
#     with open("response.json", "w") as outfile:
#         json.dump(response, outfile, indent=4, ensure_ascii=False)


# def read_json_file(json_file):
#     with open(json_file, "r") as file:
#         file_contents = file.read()
#         content = json.loads(file_contents)
#         return content


# def show_vacancies_num():
#     languages = ["Java", "C++", "Python", "Javascript", "Go", "Ruby", "Swift", "PHP"]
#     vacancies_num = {}
#     for language in languages:
#         response = get_it_vacancies(language)
#         vacancies_num[language] = response["found"]
#     pprint(vacancies_num)
#     return


# def show_python_salaries(response):
#     for counter, vacancy in enumerate(response["items"]):
#         print(counter, vacancy["salary"])
#     return 


def predict_rub_salary(vacancy):
    if vacancy["salary"]:
        if vacancy["salary"]["currency"] != "RUR":
            return None
        elif vacancy["salary"]["from"] and vacancy["salary"]["to"]:
            predict_salary = (int(vacancy["salary"]["from"]) + int(vacancy["salary"]["to"]))/2
            return predict_salary
        elif vacancy["salary"]["from"]:
             predict_salary = int(vacancy["salary"]["from"]) * 1.2
             return predict_salary
        else:
            predict_salary = int(vacancy["salary"]["to"]) * 0.8
            return predict_salary
    return


def main():
    # languages = ["Java", "C++", "Python", "Javascript", "Go", "Ruby", "Swift", "PHP"]
    # salary_resume = {}
    # for language in languages:
    #     response = get_it_vacancies(language)
    #     vacancies_found = response[0]["found"]
    #     salary_sum = 0
    #     vacancies_processed = 0
    #     for page in response:
    #         for vacancy in page["items"]:
    #             salary = predict_rub_salary(vacancy)
    #             if salary:
    #                 salary_sum += salary
    #                 vacancies_processed += 1
    #         average_salary = int(salary_sum/vacancies_processed)
    #         salary_resume[language] = {
    #             "vacancies_found": vacancies_found,
    #             "vacancies_processed": vacancies_processed,
    #             "average_salary": average_salary
    #             }
    # pprint(salary_resume)
    load_dotenv()
    secret_key = os.getenv("SUPERJOB_KEY")
    print(secret_key)


if __name__ == "__main__":
    main()
