# ProffExtractor

Introduction
------------

Proff.no does not have any form of open API that you can use freely or purchase access to. This script crawls through the webpage and extracts information from a company of your choice.

It uses BeautifulSoup4 to extract information like assets, equity, liquidity, name of the company, operating profits, organisation number, profitability, revenue, revenue before tax, solidity and their value code and parses it into a JSON format.

It uses Brønnøysundregisteret's API to extract the name of the company and uses their information to crawl through the Proff.no page, extract the information and printing it out.

Dependencies:
-------------

This script requires BeautifulSoup4 and urllib2. Both of these can be installed via python's pip tool.

Instructions:
-------------

Example usage:
`python2.7 ProffExtractor.py --c STATKRAFT_ENERGI_AS`
`python2.7 ProffExtractor.py --c ADECCO`
`python2.7 ProffExtractor.py --c coca_cola`

The company name is how it is written at Brønnøysundregisteret. Spaces needs to be underscores. Take a look at their API for further information.

Breakage:
------------

Changes to Proff.no or Brønnøysundregisteret might break the script and it would need to be changed to work again.

I am not updating this script. Thus you are on your own if the script breaks.


## DISCLAIMER: This script is made purely for educational purposes and you are solemnly responsible for your use of this python script.

Warning: Systematically copying information from Proff.no is not allowed according to Norwegian copyright law unless you have written permission from Proff A/S. Use at your own risk.
