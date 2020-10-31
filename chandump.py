#!/usr/bin/env python3
from sys import argv
import re
import urllib.request
from threading import Thread

import requests
import bs4


def getfname(link):
    pattern = re.compile(r'.*/(.*\..*)')
    r = pattern.findall(link)
    return r[0]


def run():
    threads = []
    r = requests.get(argv[1])
    soup = bs4.BeautifulSoup(r.content)
    thumbs = soup.findAll('a', {'class': 'fileThumb'})
    for thumb in thumbs:
        link = 'https:' + thumb['href']
        #link = 'https:' + thumb.find('img')['src']
        fname = getfname(link)
        dl_f = lambda: urllib.request.urlretrieve(link, fname)
        print('Downloading', fname)
        thread = Thread(target=dl_f)
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    print('Done!')


if __name__ == '__main__':
    if len(argv) != 2:
        print('python chandump.py [THREAD URL]')
        exit()
    run()
