#!/usr/local/bin/python3

import requests #HTTP requests, used to grab web pages
import bs4 #HTML parser to read web pages
from xlwt import Workbook #Excel utility
import re #Regular expressions
import threading #Multithreading for that $p33D

def indexer(link, datasets, row):
    
    #A couple variables to store file sizes, cause some datasets
    #   have multiple sets of the same file type
    csv_size = 0
    xml_size = 0

    #Write the title of the dataset to excel sheet
    datasets.write(row,0,link.get_text())
    #Request the webpage for this dataset
    set = requests.get("https://gishubdata.nd.gov" + str(link.a.get('href')))
    #Parse the webpage that was recieved
    tomatosoup = bs4.BeautifulSoup(set.content,"html.parser")

    #Grab the field with the 'date modified' info and write that to excel
    modified_date = tomatosoup.find("div",class_="field-name-field-release-date").get_text()
    #Find all 'a' tags in webpage, use regex to find links that end with "csv"
    csv_link_elements = tomatosoup.find_all("a", {"href" : re.compile("csv$")})
    #Same as above but with XML
    xml_link_elements = tomatosoup.find_all("a", {"href" : re.compile("xml$")})

    #Request the headers for each CSV link
    for file in csv_link_elements:
        if file is not None:
            #Grad the headers
            he = requests.head(file.get("href"))
            try:
                #If there is a content-length header, we use that
                csv_size += int(he.headers['Content-Length']) 
            except KeyError as e:
                #For now a file without the header will just be 0
                #Later it'll download a file and get the size
                #with curl or something
                csv_size += 0

    #Same as above but for xml links
    for file in xml_link_elements:
        if file is not None:
            he = requests.head(file.get("href"))
            try:
                xml_size += int(he.headers['Content-Length'])
            except KeyError as e:
                xml_size += 0

    #Write the data to excel file
    datasets.write(row,1,modified_date)
    datasets.write(row,2,csv_size)
    datasets.write(row,3,xml_size)

def main():
    #Create a workbook
    wb = Workbook()
    #Create a new sheet in workbook
    datasets = wb.add_sheet('ND GIS Datasets')

    #Write the headers
    datasets.write(0,0,"Dataset Title")
    datasets.write(0,1,"Date created")
    datasets.write(0,2,"CSV File Size")
    datasets.write(0,3,"XML File Size")
    #Use these for keeping track of which row is being used
    row = 1

    #There are 34 URLs in the search pane that we need to grab
    for i in range(0,34):
        threads = []
        #url = f'https://gishubdata.nd.gov/search/type/dataset?sort_by=changed&page=0%2C{i}&q=search/type/dataset'
        
        #Grab each web page
        r = requests.get(f'https://gishubdata.nd.gov/search/type/dataset?sort_by=changed&page=0%2C{i}&q=search/type/dataset')
        #Create a soup object so it's really easy to read the web page
        soup = bs4.BeautifulSoup(r.content,'html.parser')
        
        #Search for the links, which are big headers
        #Loop through them
        for link in soup.find_all("h2", class_="node-title"):
            t = threading.Thread(target=indexer,args=(link,datasets,row))
            threads.append(t)
            t.start()
            #Move to next row
            row += 1

        for thread in threads:
            thread.join()

    #save the sheet
    wb.save('datasets.xls')

if __name__=="__main__":
    main()
