#!/usr/bin/env python

import json
import os
import time

import requests


TITLE_JSON_URL = 'http://chroniclingamerica.loc.gov/lccn/'

if __name__ == '__main__':
    s = requests.Session()
    lccns = set()
    for date in os.listdir('dates'):
        print('date:', date)
        files = os.listdir('dates/%s' % date)
        for f in [f for f in files if f.endswith('.txt')]:
            lccn = f[:f.index('-')]
            lccns.add(lccn)
        print('lccn len:', len(lccns))
    for lccn in lccns:
        json_url = '%s%s.json' % (TITLE_JSON_URL, lccn)
        print('fetch: %s' % json_url)
        r = s.get(json_url)
        with open('titles/%s.json' % lccn, 'wt') as fp:
            json.dump(r.json(), fp)
        time.sleep(0.2)
