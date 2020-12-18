#!/usr/bin/env python3

import sys
import datetime
import requests

from bs4 import BeautifulSoup
import json
import yaml

url = 'https://wg21.link/index'

dates = {}
for elem in BeautifulSoup(requests.get(url + '.html').text, 'lxml').find_all('li'):
  date = elem.find(class_='date')
  if date is not None:
    dates[elem['id']] = date.get_text()

index_yaml = yaml.safe_load(requests.get(url + '.yaml').text)['references']
for item in index_yaml:
  if item.pop('issued', None) is not None:
    date = datetime.date.fromisoformat(dates[item['id']])
    item['issued'] = { 'date-parts' : [[ date.year, date.month, date.day ]] }

json.dump(index_yaml, sys.stdout, ensure_ascii=False, indent=2)
