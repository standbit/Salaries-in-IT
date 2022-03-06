from urllib import response
import requests
from pprint import pprint
import json


def get_it_vacancies(language):
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Программист",
        "text": language,
        "area": 1,
        "date_from": "2022-02-07"    
    }
    response = requests.get(url, params=params)
    converted_response = response.json()
    return converted_response


def write_json_file(response):
    with open("response.json", "w") as outfile:
        json.dump(response, outfile, indent=4, ensure_ascii=False)


def read_json_file(json_file):
    with open(json_file, "r") as file:
        file_contents = file.read()
        content = json.loads(file_contents)
        return content


def show_vacancies_num():
    languages = ["Java", "C++", "Python", "Javascript", "Go", "Ruby", "Swift", "PHP"]
    vacancies_num = {}
    for language in languages:
        response = get_it_vacancies(language)
        vacancies_num[language] = response["found"]
    pprint(vacancies_num)
    return


def show_python_salaries(response):
    for counter, vacancy in enumerate(response["items"]):
        print(counter, vacancy["salary"])
    return 


def main():
    response = get_it_vacancies("python")
    write_json_file(response)
    show_python_salaries(response)


if __name__ == "__main__":
    main()
