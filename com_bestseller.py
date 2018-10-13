import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.com/gp/bestsellers/books/ref=zg_bs_pg_1?ie=UTF8&pg="


def proc(item):
    name = item.find_all("img")
    name = name[0]['alt']

    auth = item.find_all("div", "a-row a-size-small")
    auth = auth[0].string

    price = item.find_all("span", "p13n-sc-price")
    price = price[0]
    price = price.contents[0].string
    price = ' '.join(price.split())

    numberOfRatings = item.find_all("a", "a-size-small a-link-normal")
    if len(numberOfRatings) > 0:
        numberOfRatings = numberOfRatings[0].string
    else:
        numberOfRatings = "Not available"

    rating = item.find_all("span", "a-icon-alt")

    if rating[0].string == "Prime":
        rating = "Not available"
    else:
        rating = rating[0].string

    suburl = item.find_all("div", "a-section a-spacing-none p13n-asin")
    suburl = suburl[0]['data-p13n-asin-metadata']
    suburl = dict(i.split(':') for i in suburl.split(','))
    suburl = suburl['"asin"'].replace('"', '').replace('}', '')
    item_url = "https://www.amazon.com/dp/" + suburl + "/"

    writer.writerow([name, item_url, auth, price, numberOfRatings, rating])


csvfile = open("output/com_book.csv", "w")
writer = csv.writer(csvfile, delimiter=';',
                    quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Name", "URL", "Author", "Price",
                 "Number of Ratings", "Average Rating"])
for i in range(5):
    page = requests.get(url + str(i + 1))
    page = BeautifulSoup(page.text)
    list = page.find_all("div", "zg_itemWrapper")
    for item in list:
        proc(item)
