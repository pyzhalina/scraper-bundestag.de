import json
import random
import time

import requests
from bs4 import BeautifulSoup


def get_persons_urls():
    persons_url_list = []

    for i in range(0, 736, 20):
        url = f"https://www.bundestag.de/ajax/filterlist/de/abgeordnete/862712-862712?limit=20&noFilterSet=true&offset={i}"
        q = requests.get(url)
        result = q.content

        soup = BeautifulSoup(result, 'lxml')
        persons = soup.find_all(class_='bt-open-in-overlay')

        for person in persons:
            person_page_url = 'https://www.bundestag.de' + person.get('href')
            persons_url_list.append(person_page_url)

        time.sleep(random.randrange(2, 4))

    with open('persons_url_list.txt', 'a', encoding="utf-8-sig") as file:
        for line in persons_url_list:
            file.write(f"{line}\n")

def get_data():
    with open('persons_url_list.txt', encoding="utf-8-sig") as file:
        lines = [line.strip() for line in file.readlines()]

        data_dict = []

        for line in lines:
            q = requests.get(line)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')
            try:
                person = soup.find(class_='bt-biografie-name').find('h3').text
                person_name_company = person.strip().split(',')
                person_name = person_name_company[0]
                person_company = person_name_company[1].strip()

                social_networks = soup.find_all(class_="bt-link-extern")

                social_networks_urls = []
                for item in social_networks:
                    social_networks_urls.append(item.get('href'))
            except Exception:
                person_name = 'None'
                person_company = 'None'
                social_networks_urls = 'None'

            data = {
                'Personal_name': person_name,
                'Company_name': person_company,
                'Social_networks': social_networks_urls
            }

            data_dict.append(data)

            with open('data.json', 'w', encoding="utf-8-sig") as json_file:
                json.dump(data_dict, json_file, indent=4)

def main():
    get_persons_urls()
    get_data()

if __name__ == '__main__':
    main()
