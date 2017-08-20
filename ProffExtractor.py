# -*- coding: utf-8 -*-
import sys
import json
from collections import defaultdict
from urllib2 import urlopen, URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
# Usage: "python ProffExtractor.py --u STATKRAFT_ENERGI_AS"
#        "python ProffExtractor.py --u ADECCO"
#          "python ProffExtractor.py --u coca_cola"

# A simple company object. Makes it easier to parse it to a JSON object.
class Company(object):
    def __init__(self, name, orgnumber, liquidity, profitability, solidity, revenue, operatingProfit, revenueBeforeTax, assets, equity, valuecode):
        self.name = name
        self.orgnumber = orgnumber
        self.profitability = profitability
        self.solidity = solidity
        self.liquidity = liquidity
        self.revenue = revenue
        self.operatingProfit = operatingProfit
        self.revenueBeforeTax = revenueBeforeTax
        self.assets = assets
        self.equity = equity
        self.valuecode = valuecode

# Parses the arguments the script gets.
# This is typically --u to get a certain name out.
# Spaces in the name needs to be replaced with underscores.

def parse_arguments():
    """ Process command line arguments """
    parser = ArgumentParser(description='Grabs information located at Proff.no. Use cat (>>) to make the text into an JSON.')
    parser.add_argument('--c', help='Use --c and the name of the company. Company names with spaces needs underscores _', required=True)
    args = parser.parse_args()

    # Brønnøysunregistret search API
    completeString = "http://data.brreg.no/enhetsregisteret/enhet.json?$filter=startswith(navn,'" + args.c.decode() + "')"

    return completeString


# Parses the rows from the table it gets.
def parse_rows(rows):
    """ Get data from rows """
    results = []
    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            datalength = len(table_data)
            for index, data in enumerate(table_data):
                if(index % (datalength / 6) == 0):
                    results.append(data.get_text().strip())
    return results

# Creates a company object by getting name and organization number as parameters.
def create_company(name, orgNumber):
    getProffString = 'http://www.proff.no/bransjesøk?q=' + str(orgNumber)

    # Make soup of Proff search query
    try:
        resp = urlopen(getProffString)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (url, e.reason))
        return 1

    linkSoup = BeautifulSoup(resp.read(), 'html.parser')
    try:
        y = linkSoup.find(class_='addax-cs_hl_hit_company_name_click').get('href')
    except AttributeError as e:
        return 1

    # Let's extract the Proff identificator.
    proffURL = y.rsplit('/', 2)[-2]

    # Proff does not care about the information from /selskap/ and out until the identificator.
    profflink = 'http://www.proff.no/selskap/afwfwaf/afwfafwf/asfjawgj/' + proffURL

    # Make soup of the company's main view.
    try:
        resp = urlopen(profflink)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (url, e.reason))
        return 1

    proffSoup = BeautifulSoup(resp.read(), 'html.parser')

    # Read the "total-account-table" table from the HTML. This contains most of the information.
    
    try:
        table = proffSoup.find_all(class_='total-account-table ui-wide', limit=1)
    except AttributeError as e:
        # Something is wrong with the tables.
        return 1

    # Information from the header charts from the site which tells us about the
    # company's liquidity, solidity and profitability. 
    infoFromHeader = []
    topstatistics = proffSoup.find_all(class_='chart-value', limit=3)
    for i in topstatistics:
        try:
            infoFromHeader.append(i.span.get_text().strip().replace("(","").replace(")",""))
        except AttributeError as e:
            # If the value is "Kan ikke beregnes" it will set it as zero.
            try:
                if(i.get_text() == "Kan ikke beregnes"):
                    infoFromHeader.append(0)
            except AttributeError as g:
                # Some unknown strange attribute. Skip the firm.
                return 1
        except UnicodeEncodeError as r:
            try:
                # Might be encoding error due to strange characters in the extracted text. Try without stripping the text.
                infoFromHeader.append((i.span.get_text().replace("(","").replace(")","")))
            except UnicodeError as r:
                # Unicode error again. Skip company.
                return 1

    # Table generation.
    table_data = parse_rows(table)

    if(len(table_data) >= 5):
        companyObject = Company(name, orgNumber, infoFromHeader[0], infoFromHeader[1], infoFromHeader[2], table_data[0], table_data[1], table_data[2], table_data[3], table_data[4], table_data[5])
        # Check for encoding error by parsing it without printing. 
        json.dumps(companyObject.__dict__, ensure_ascii=False)
        # Encoding accepted. Add to list.
        listOfCompanies.append(companyObject)
        return companyObject
    else:
        # Not enough information is in the tables. There's most likely no info here.
        return 1

def main():
    # Get arguments
    url = parse_arguments()

    # List of the company objects. Will be JSONed in the end.
    global listOfCompanies
    listOfCompanies = []

    try:
        resp = urlopen(url)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (url, e.reason))
        return 1

    # Load Brønnøysundregistret information about the company.
    x = json.load(resp)

    for index, company in enumerate(x["data"]):
        name = x["data"][index]["navn"]
        orgNo = x["data"][index]["organisasjonsnummer"]
        create_company(name, orgNo)

    # Print the list of companies as a JSON array with JSON objects.
    print (json.dumps([ob.__dict__ for ob in listOfCompanies], sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))

if __name__ == '__main__':
    status = main()
    sys.exit(status)