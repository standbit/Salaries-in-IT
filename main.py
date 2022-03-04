import requests
from pprint import pprint
import json


def get_it_vacancies():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Программист",
        "text": "Разработчик",
        "area": 2
    }
    response = requests.get(url, params=params)
    print(response.url)
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


def main():
    job_response = get_it_vacancies()
    write_json_file(job_response)


if __name__ == "__main__":
    main()
