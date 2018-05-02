import urllib2
from bs4 import BeautifulSoup

from scrapy.selector import Selector
from scrapy.http import HtmlResponse

quote_page = "http://www.bloomberg.com/quote/SPX:IND"
cric_buzz = "http://www.cricbuzz.com/live-cricket-scorecard/19873/indw-vs-engw-6th-match-womens-t20i-triseries-in-india-2018"
page = urllib2.urlopen(cric_buzz)
soup = BeautifulSoup(page, 'html.parser')
    
def getMatchName(soup):
    name_box = soup.find('div', attrs={'class': 'cb-mtch-info-itm'})
    return name_box


def scrapy(url):
    response = fetch(url)
    view(response)
    
scrapy(cric_buzz)
