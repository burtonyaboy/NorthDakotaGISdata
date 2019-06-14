#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup


def main():
    for i in range(0,34):
        r = requests.get(f'https://gishubdata.nd.gov/search/type/dataset?sort_by=changed&page=0%2C{i}&q=search/type/dataset')
        soup = BeautifulSoup(r.content,'html.parser')
        for link in soup.find_all("h2", class_="node-title"):
            print(link.get_text())
    

if __name__=="__main__":
    main()
