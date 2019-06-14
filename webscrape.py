#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
from xlwt import Workbook

def main():

    wb = Workbook()
    datasets = wb.add_sheet('ND GIS Datasets')
    datasets.write(0,0,"Dataset Title")
    datasets.write(0,1,"Date created")
    datasets.write(0,2,"File Size")
    row = 1
    column = 0

    for i in range(0,34):
        r = requests.get(f'https://gishubdata.nd.gov/search/type/dataset?sort_by=changed&page=0%2C{i}&q=search/type/dataset')
        soup = BeautifulSoup(r.content,'html.parser')
        for link in soup.find_all("h2", class_="node-title"):
            datasets.write(row,column,link.get_text())
            set = requests.get("https://gishubdata.nd.gov" + str(link.a.get('href')))
            tomatosoup = BeautifulSoup(set.content,"html.parser")
            datasets.write(row,column+1,tomatosoup.find("div",class_="field-name-field-modified-date").get_text())
            row += 1

    wb.save('datasets.xls')

if __name__=="__main__":
    main()
