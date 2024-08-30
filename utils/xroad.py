import requests
import pprint
import json
import copy
from collections import OrderedDict
import pandas as pd
import numpy as np
from PIL import Image
import io
import statistics as st

URL = 'https://road-structures-db-bridge.mlit.go.jp/xROAD/api/v1/bridges/'

from dotenv import load_dotenv
import os
load_dotenv(os.path.join(os.path.dirname(__file__), '../', '.env'))
API_HEAD = {
    'API-key': os.environ.get('XROAD_API_KEY')
}

def get_bridge_name(bridge_loc, year):
    # bridge_loc : '35.79640,139.68538'

    api_obtaining_report = 'tenken/report/'
    youshiki = 0
    youshiki_name = 'c' + str(youshiki)

    url_obtaining_report = URL + api_obtaining_report + str(year) + '/' + bridge_loc + '/' + str(youshiki)
    r = requests.get(url_obtaining_report, headers=API_HEAD)
    json_data = r.json()
    name = json_data['result'][0]['basicinfo']['bridge_name']
    return name


def get_bridge_diameters(bridge_loc, year):
    api_obtaining_report = 'tenken/report/'
    youshiki = 2
    youshiki_name = 'c' + str(youshiki)

    url_obtaining_report = URL + api_obtaining_report + str(year) + '/' + bridge_loc + '/' + str(youshiki)
    r = requests.get(url_obtaining_report, headers=API_HEAD)
    json_data = r.json()
    print(json_data)
    info = json_data['result'][0][youshiki_name]

    diameters = []
    for i in range(len(info)):
        diameters.append(info[i]['diameter'])
    return diameters


### DaCS用のテスト


# def get_bridges_by_start_addr(start_addr, year):
#     api_part = 'tenken/list/'
#     url = URL + api_part + str(year)
#     params = {
#         "querys":[
#             {
#                 "key": "start_addr",
#                 "value": start_addr,
#                 "op": 7
#             }
#         ],
#         "limit": 500,
#         "offset": 0
#         }
#     r = requests.post(url, json=params, headers = API_HEAD)
#     json_data = r.json()
#     return json_data['result']


def fetch_by_url(url, json=None):
    if json:
        r = requests.post(url, json=json, headers=API_HEAD)
    else:
        r = requests.get(url, headers=API_HEAD)
    # print(r.status_code)
    json_data = r.json()
    return json_data


def fetch_img(img_url):
    r = requests.get(img_url, headers=API_HEAD)
    return r.content


def save_77_excel(loc, year, save_path):
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}.")
        return True
    
    url = f'{URL}report77/{loc}/{year}'
    response = requests.get(url, headers=API_HEAD)
    print(response.text)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        return True
    else:
        return False


def get_damage_diagrams(bridge_loc, year, diam):
    elem_num_img_list = []
    # 画像名を取得
    url_obtaining_report = URL + 'tenken/report/' + str(year) + '/' + bridge_loc + '/' + str(5)  # 2004年以降　その5
    r_report = requests.get(url_obtaining_report, headers=API_HEAD)
    json_data = r_report.json()
    for data in json_data["result"][0]['c4']:
        if data['diameter'] == str(diam):
            elem_num_img_list = data['inspect_figs']

    # 画像を取得
    contents = []
    if elem_num_img_list:
        for i in range(len(elem_num_img_list)):
            url_obtaining_img = URL + 'tenken/image/' + str(year) + '/' + bridge_loc + '/' + str(4) + '/' + elem_num_img_list[i]
            r_image = requests.get(url_obtaining_img, headers=API_HEAD)
            contents.append(r_image.content)
    
    return contents