import requests
from bs4 import BeautifulSoup
import json
import xml
from xml.etree import ElementTree
import csv
import os
from datetime import datetime
import pandas as pd
import re
import os.path
import clinics

cookies, headers, all_moscow_clinics = clinics.get_clinics()


def get_data(clinic=422):
    data = {
        'signedParamsString': 'YToxMjp7czoxMToiSVNfSE9TUElUQUwiO3M6MToiTiI7czo5OiJDTElOSUNfSUQiO3M6MzoiNDIyIjtzOjEwOiJDQUNIRV9USU1FIjtpOjg2NDAwO3M6MTM6IklTX1BSSUNFX0xJU1QiO3M6MToiWSI7czo3OiJDSVRZX0lEIjtzOjI6IjI3IjtzOjEwOiJDQUNIRV9UWVBFIjtzOjE6IkEiO3M6MTI6In5JU19IT1NQSVRBTCI7czoxOiJOIjtzOjEwOiJ+Q0xJTklDX0lEIjtiOjA7czoxMToifkNBQ0hFX1RJTUUiO2k6ODY0MDA7czoxNDoifklTX1BSSUNFX0xJU1QiO3M6MToiWSI7czo4OiJ+Q0lUWV9JRCI7czoyOiIyNyI7czoxMToifkNBQ0hFX1RZUEUiO3M6MToiQSI7fQ==.28d5b0761b620bb33be564a242b9c648bc13bcebc1ae040298c32ee4be59f029',
        'clinic': clinic,
    }

    src = 0
    check_file = os.path.exists(f'{clinic}_service.html')
    if check_file is True:
        with open(f'{clinic}_service.html') as file:
            src = file.read()
    else:
        response = requests.post('https://mamadeti.ru/local/components/webprofy/price_list/ajax.php', cookies=cookies,
                                 headers=headers, data=data)
        with open(f'{clinic}_service.html', 'w') as file:
            file.write(response.text)

        with open(f'{clinic}_service.html') as file:
            src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    services_all = {}
    services_selection_category = []
    categories_raw = soup.select('option[value*="section-id-"]')
    for cnt_categories, categories in enumerate(categories_raw):
        current_categories = categories.text
        services_raw = soup.find_all(
            attrs={'class': 'price-list__group', 'data-section-group': f'section-id-{cnt_categories}'})
        for cnt_services, services in enumerate(services_raw):
            current_services = services
            service_article = current_services.find_all(attrs={'class': 'price-list__article'})
            service_name = current_services.find_all(attrs={'class': 'price-list__name'})
            service_price = current_services.find_all(attrs={'class': 'price-list__price-num'})
            article_name_price = []
            for i in range(len(service_article)):
                article_name_price.append({'Код услуги': service_article[i].text, 'Наименования': service_name[i].text,
                                           'Цена': service_price[i].text})
        services_all[current_categories] = article_name_price
    return services_all


def final_file_save(clinic_id, clinic_name, all_sevice):
    with open(f'{clinic_id}_{clinic_name}_full_service.json', 'w') as file:
        file.write(json.dumps(all_sevice, indent=4, ensure_ascii=False))


for i in all_moscow_clinics:
    final_file_save(i, all_moscow_clinics[i],get_data(i))