#!/usr/bin/env python

import argparse
import gzip
import json
import os
from pprint import pprint
import shutil
import time

import requests


CHRONAM_SEARCH_URL = 'http://chroniclingamerica.loc.gov/search/pages/results/'

s = requests.Session()
titles = {}


def handle_items(d):
    items = d['items']
    for page in items:
        if 'ocr_eng' not in page:
            continue
        print(page['id'])
        dirname = 'dates/%s' % page['date']
        os.makedirs(dirname, exist_ok=True)
        lccn = page['lccn']
        id = page['id']
        ed_seq = id[id.index('1916') + 11:-1].replace('/', '_')
        txt_filename = '%s/%s-%s.txt' % (dirname, lccn, ed_seq)
        with open(txt_filename, 'wt') as fp:
            print(page['ocr_eng'], file=fp)
        ocr_url = page['url'].replace('.json', '/ocr.xml')
        ocr_filename = '%s/%s-%s.xml.gz' % (dirname, lccn, ed_seq)
        time.sleep(0.1)
        r = s.get(ocr_url, stream=True)
        if r.status_code == 200:
            with open(ocr_filename, 'wb') as fp:
                shutil.copyfileobj(r.raw, fp)
        handle_title(page)


def handle_title(d):
    lccn = d.get('lccn')
    if not lccn:
        print('title keys:', d.keys())
        return
    if lccn in titles:
        if not d['batch'] in titles[lccn]['batches']:
            titles[lccn]['batches'].append(d['batch'])
        return
    titles[lccn] = {
            'title': d['title'],
            'title_normal': d['title_normal'],
            'country': d['country'],
            'state': d['state'],
            'city': d['city'],
            'place': d['place'],
            'frequency': d['frequency'],
            'batches': [d['batch']]
    }


def fetch_text(args, page=1):
    print('page:', page)
    params = {'format': 'json', 'dateFilterType': 'yearRange', 'page': page,
              'sort': 'date', 'language': 'eng', 'rows': 50}
    if args.year:
        params['date1'] = args.year
        params['date2'] = args.year
    if args.pageone:
        params['sequence'] = 1
    req = s.get(CHRONAM_SEARCH_URL, params=params)
    d = req.json()
    handle_items(d)
    end_index = d['endIndex']
    if end_index >= args.limit:
        return
    page = end_index // d['itemsPerPage']
    fetch_text(args=args, page=page + 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch text from Chronam')
    parser.add_argument('-y', '--year', type=int, required=False,
                        help='fetch text for a specific year')
    parser.add_argument('--limit', type=int, default=100,
                        help='limit total pages (default 100)')
    parser.add_argument('--pageone', default=False, action='store_true',
                        help='fetch only front pages')
    args = parser.parse_args()

    if args.year and (args.year < 1836 or args.year > 1922):
        parser.error('Year must be between 1836-1922')

    fetch_text(args)
    pprint(titles)
    json.dump(titles, open('titles.json', 'w'))
