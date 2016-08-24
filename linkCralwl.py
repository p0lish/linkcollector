#!/usr/bin/python
import requests
import urllib.error
import urllib.request
import urllib.parse
import random
import sys
import argparse
from bs4 import BeautifulSoup

__author__ = "polish"

_description = "Scan and collect all links on a website."
parser = argparse.ArgumentParser(description= _description)

parser.add_argument('--url', metavar='url', type=str, help='The site url for scanning')






ROOT_DIR = "./"
USERAGENTS = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
]


# get contents from url #
def randomUserAgent():
    return random.choice(USERAGENTS)


USERAGENT = randomUserAgent()

def get_content(url):
    try:
        req = requests.get(url, headers={'User-Agent': USERAGENT}, verify=False)
        content = req.content
        return content
    except urllib.error.HTTPError as e:
        print("<--404-->", e)
        return ""
    except requests.exceptions.InvalidSchema as invalidschema:
        collect_wrong_urls(url)
        return ""

def collect_wrong_urls(url):
    f = open("malformed_urls.txt", 'a')
    f.write(url)
    f.close()



def generateFilename(url):
    return url.replace("/", "").replace(":", "")

def apply_link_filter(link):
    if link is '':
        return False
    elif link is "#":
        return False
    elif link is "javascript://":
        return False
    else:
        return True

def get_all_links_from(current_url, m, h):
    content = get_content(current_url)
    soupContent = BeautifulSoup(content, 'html.parser')
    urls=[]
    links = soupContent.findAll(href=True)
    for i in links:
        link = i['href']
        link = create_valid_url(link, m, h)
        if apply_link_filter(link):
            urls.append(link)
    return urls

def write_current_urls_into_file(f, c, l):
    f.write('PARENT URL>>>>' + str(c) + "\n")
    for link in l:
        f.write(link + "\n")

def create_valid_url(url, main_url, http_prefix):
    if url.startswith("//"):
        url = http_prefix + ":" + url
    elif url.startswith("/"):
        url = main_url + url
    elif url.startswith("../"):
        url = main_url+ "/" + url
    elif url.startswith("http"):
        return url
    else:
        url = main_url + "/" + url
    return url



def ready(_url):
    if _url == None:
        print("No url given bye. please use ./lincCrawl --url <siteurl>")
        sys.exit()
    requests.packages.urllib3.disable_warnings()
    COUNTER = 0
    MAIN_URL = _url
    http_prefix = _url.split("://")[0]
    link_pool = []
    visited_links = []
    f_http = open(generateFilename(_url), 'w')
    link_pool.append(_url)

    while len(link_pool) > 0:
        current_url = link_pool.pop(0)
        if current_url not in visited_links:
            COUNTER += 1
            print(current_url, COUNTER, len(link_pool))
            links = get_all_links_from(current_url, MAIN_URL, http_prefix)
            write_current_urls_into_file(f_http, current_url, links)
            link_pool += links
            visited_links.append(current_url)
    f_http.close()

args = parser.parse_args()
ready(args.url)