#!/usr/local/bin/python3

import requests #HTTP requests, used to grab web pages
from bs4 import BeautifulSoup #HTML parser to read web pages
from xlwt import Workbook #Excel utility

def main():
    #Create a workbook
    wb = Workbook()
    #Create a new sheet in workbook
    datasets = wb.add_sheet('ND GIS Datasets')
    #Write the headers
    datasets.write(0,0,"Dataset Title")
    datasets.write(0,1,"Date created")
    datasets.write(0,2,"File Size")
    #Use these for keeping track of which row is being used
    row = 1

    #There are 34 URLs in the search pane that we need to grab
    for i in range(0,34):
        #Grab each web page
        r = requests.get(f'https://gishubdata.nd.gov/search/type/dataset?sort_by=changed&page=0%2C{i}&q=search/type/dataset')
        #Create a soup object so it's really easy to read the web page
        soup = BeautifulSoup(r.content,'html.parser')
        #Search for the links, which are big headers
        for link in soup.find_all("h2", class_="node-title"):
            #Write the title of the dataset to excel sheet
            datasets.write(row,column,link.get_text())
            #Request the webpage for this dataset
            set = requests.get("https://gishubdata.nd.gov" + str(link.a.get('href')))
            #Parse the webpage that was recieved
            tomatosoup = BeautifulSoup(set.content,"html.parser")
            #Grab the field with the 'date modified' info and write that to excel
            datasets.write(row,column+1,tomatosoup.find("div",class_="field-name-field-modified-date").get_text())
            row += 1
    #save the sheet
    wb.save('datasets.xls')

if __name__=="__main__":
    main()
