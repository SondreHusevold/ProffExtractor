# ProffExtractor

### DISCLAIMER: This script is made purely for educational purposes and you are solemnly responsible for your use of this python script.

Warning: Systematically copying information from Proff.no is not allowed according to Norwegian copyright law unless you have written permission from Proff A/S. Use at your own risk.

Introduction
------------

Proff.no does not have any form of open API that you can use freely or purchase access to. This script crawls through the webpage and extracts information from a company of your choice making it into a form of "pseudo-API". Simply tell it what company you want information on and it'll spit out a JSON object that contains all the information it could gather from the site.

It uses BeautifulSoup4 to extract information like assets, equity, liquidity, name of the company, operating profits, organisation number, profitability, revenue, revenue before tax, solidity and their value code and parses it into a JSON format.

To extract more specific information it'll use Brønnøysundregisteret's API to extract the organisation number of the company and uses their information to crawl through the Proff.no page, extract the information and printing it out.

It will not extract any information if the company in question does not have any information available on the site.

Dependencies:
-------------

This script requires BeautifulSoup4 and urllib2. Both of these can be installed via python's pip tool.

Instructions:
-------------

Example usage:

`python2.7 ProffExtractor.py --c STATKRAFT_ENERGI_AS`

`python2.7 ProffExtractor.py --c ADECCO`

`python2.7 ProffExtractor.py --c coca_cola`

Can be combined with >> to add it to a text file for example. If you have a list of companies, using a for loop in Bash or Powershell would suffice.

* The company name needs to reflect what Brønnøysundregisteret's database has. 
* Spaces needs to be underscores. 
* It does not need to be the complete name of the company. Thus "coca_cola" would suffice for the Coca-Cola Company. 

Take a look at Brønnøysundregisteret's API for further information. 

Breakage:
------------

Changes to Proff.no or Brønnøysundregisteret might break the script and it would need to be changed to work again.

I am not updating this script. Thus you are on your own if the script breaks.
