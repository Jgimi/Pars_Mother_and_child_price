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


def get_clinics():
    cookies = {
        'BX_USER_ID': 'a90b5a7aba829c33aefd9920776e9106',
        '_ym_d': '1654696605',
        '_ym_uid': '1654696605762207720',
        '_ga': 'GA1.2.1414753695.1654696606',
        'tmr_lvid': 'e755bb672d412a544e32923913d51d34',
        'tmr_lvidTS': '1654696605736',
        '_ct': '200000002264555195',
        '_ct_client_global_id': '456deb13-d619-53c3-aa8d-1a9db907969a',
        'cookies-message-hidden': 'Y',
        'menu-tab-active-id': 'f435494cb8875e97b6001bf671e8684f',
        '_gid': 'GA1.2.1739357815.1655932508',
        'PHPSESSID': 'XopnNNSO3ncXvv10rXFGHspElTcGCEqn',
        'cted': 'modId%3D814cd09b%3Bclient_id%3D1414753695.1654696606%3Bya_client_id%3D1654696605762207720',
        '_ym_isad': '1',
        '_gat_UA-56244691-1': '1',
        '_ym_visorc': 'b',
        '_ct_ids': '814cd09b%3A17324%3A3842715676',
        '_ct_session_id': '3842715676',
        '_ct_site_id': '17324',
        'tmr_detect': '1%7C1656004952111',
        'call_s': '%3C!%3E%7B%22814cd09b%22%3A%5B1656006753%2C3842715676%2C%7B%22215545%22%3A%22736768%22%7D%5D%2C%22d%22%3A2%7D%3C!%3E',
        'tmr_reqNum': '148',
    }

    headers = {
        'authority': 'mamadeti.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'BX_USER_ID=a90b5a7aba829c33aefd9920776e9106; _ym_d=1654696605; _ym_uid=1654696605762207720; _ga=GA1.2.1414753695.1654696606; tmr_lvid=e755bb672d412a544e32923913d51d34; tmr_lvidTS=1654696605736; _ct=200000002264555195; _ct_client_global_id=456deb13-d619-53c3-aa8d-1a9db907969a; cookies-message-hidden=Y; menu-tab-active-id=f435494cb8875e97b6001bf671e8684f; _gid=GA1.2.1739357815.1655932508; PHPSESSID=XopnNNSO3ncXvv10rXFGHspElTcGCEqn; cted=modId%3D814cd09b%3Bclient_id%3D1414753695.1654696606%3Bya_client_id%3D1654696605762207720; _ym_isad=1; _gat_UA-56244691-1=1; _ym_visorc=b; _ct_ids=814cd09b%3A17324%3A3842715676; _ct_session_id=3842715676; _ct_site_id=17324; tmr_detect=1%7C1656004952111; call_s=%3C!%3E%7B%22814cd09b%22%3A%5B1656006753%2C3842715676%2C%7B%22215545%22%3A%22736768%22%7D%5D%2C%22d%22%3A2%7D%3C!%3E; tmr_reqNum=148',
        'referer': 'https://mamadeti.ru/clinics/',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    clinics_raw_file = 'clinics.html'
    check_file = os.path.exists(clinics_raw_file)
    src = 0

    if check_file is True:
        with open('clinics.html') as file:
            scr = file.read()

    else:
        response = requests.get('https://mamadeti.ru/price-list/', cookies=cookies, headers=headers)
        with open('clinics.html', 'w') as file:
            file.write(response.text)
        with open('clinics.html') as file:
            scr = file.read()

    all_moscow_clinics = {}
    soup = BeautifulSoup(scr, 'lxml')
    all_moscow_clinics_row = soup.find_all(value=re.compile('clinic-id-'))
    for clinic in all_moscow_clinics_row:
        all_moscow_clinics[clinic["value"].replace('clinic-id-', '')] = clinic.text.replace(u'\xa0', ' ')

    return cookies,headers,all_moscow_clinics
