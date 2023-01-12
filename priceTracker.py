from bs4 import BeautifulSoup
import csv
import html5lib
import requests
import numpy as np 
from datetime import datetime

LINK = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=250+gb+ssd+m.2+crucial&_sacat=0&LH_TitleDesc=0&_odkw=250+gb+ssd+m.2&_osacat=0"

def getPriceByLink(link):
    # get source
    r = requests.get(link)
    # parse source 
    page_parse = BeautifulSoup(r.text, 'html.parser')
    # find all list items from search result
    search_result = page_parse.find("ul", {"class":"srp-results"}).find_all("li", {"class":"s-item"})

    item_prices = []

    for result in search_result:
        price_as_text = result.find("span", {"class": "s-item__price"}).text
        if "to" in price_as_text:
            continue
        price = float(price_as_text[1:].replace(",", ""))
        item_prices.append(price)
    return item_prices


def remove_outliners(prices, m=2):
    data = np.array(prices)
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def get_average(prices):
    return np.mean(prices)


def save_to_file(prices):
    fields = [datetime.today().strftime("%B-%D-%Y"), np.around(get_average(prices), 2)]
    with open('prices.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)


if __name__ == "__main__":
    prices = (getPriceByLink(LINK))
    price_without_outliners = remove_outliners(prices)
    print(get_average(price_without_outliners))
    save_to_file(prices)


