#!/usr/bin/env python3
# coding: utf-8

import logging
import time
from datetime import datetime

import requests
from wild.eastmoney import get_core_conception
from db import col_stock_profile, col_subject


def pull_and_save(session, code, name):
    cc = get_core_conception(session, code)
    doc = {
        'name': name,
        'core': [],
        'detail': []
    }
    for i in cc:
        if i['gjc'] == '所属板块':
            doc['core'] = i['ydnr'].split(' ')
            continue
        doc['detail'].append({
            'title': i['gjc'],
            'content': i['ydnr']
        })
    col_subject.update_one(
        {'_id': code},
        {'$set': doc},
        upsert=True
    )


s = requests.Session()
stock_profile_docs = col_stock_profile.find(projection=['name'])
for d in stock_profile_docs:
    try:
        pull_and_save(s, d['_id'], d['name'])
    except Exception as e:
        logging.warning(d['_id'], e)
        continue
