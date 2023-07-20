import requests
from bs4 import BeautifulSoup
import time
import random
import os
import pandas
class parser():
    def __init__(self):
        self.url = "https://www.olx.pl/muzyka-edukacja/ksiazki/q-python/?page="
    # headers = {
    #     f'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    # }
    # r = requests.get(url)#, headers=headers)
    # soup = BeautifulSoup(r.text, "lxml")
    # book = {}
    # error=True
    # while error==True:
    #     try:    
    #         book["block"] = soup.find("a", class_='css-rc5s2u')
    #         book["url"] = "https://www.olx.pl" + str(book["block"].get("href"))
    #         book["title"] = book["block"].find("div", class_="css-u2ayx9").find("h6", class_="css-16v5mdi er34gjf0").text
    #         book["price"] =  book["block"].find("div", class_="css-u2ayx9").find("p", class_="css-10b0gli er34gjf0").text
    #         book["condition"] = book["block"].find("span", class_="css-3lkihg").get("title") #.find("div", class_="css-u2ayx9").find("div", class_="css-112xsl6")
    #         book["location_and_refresh_time"] = book["block"].find("p", class_="css-veheph er34gjf0").text
    #         book["location"] = book["location_and_refresh_time"][0:book["location_and_refresh_time"].find("-")]
    #         book["refresh_time"] = book["location_and_refresh_time"][book["location_and_refresh_time"].find("-")+2:]
    #         error = False
    #     except Exception as ex:
    #         print("Something went wrong... ", ex)
    #         time.sleep(random.randint(1,5))
    # print("url:\n"+ book["url"])
    # print("title:\n"+ book["title"])
    # print("price:\n"+ book["price"])
    # print("condition:\n"+ book["condition"])
    # print("seller location:\n"+ book["location"])
    # print("seller last refresh timr:\n"+ book["refresh_time"])

        self.books = []
    # book_list = soup.findAll("a", class_='css-rc5s2u')
    #print(len(book_list))
    def find_all_on_pages(self, pages):    
        for i in range(0, pages):
            r = requests.get(self.url+str(i))
            soup = BeautifulSoup(r.text, "lxml")
            book_list = soup.findAll("a", class_='css-rc5s2u')
            print(f"There're {len(book_list)} books on page №{i}.")
            for one_book in book_list:
                try:
                    book = {}
                    book["url"] = "https://www.olx.pl" + str(one_book.get("href"))
                    book["title"] = one_book.find("div", class_="css-u2ayx9").find("h6", class_="css-16v5mdi er34gjf0").text
                    book["price"] =  one_book.find("div", class_="css-u2ayx9").find("p", class_="css-10b0gli er34gjf0").text
                    if "do negocjacji" in book["price"]:
                        book["price"] = book["price"][:-len("do negocjacji")]
                    book["condition"] = one_book.find("span", class_="css-3lkihg").get("title") #.find("div", class_="css-u2ayx9").find("div", class_="css-112xsl6")
                    book["location_and_refresh_time"] = one_book.find("p", class_="css-veheph er34gjf0").text
                    book["location"] = book["location_and_refresh_time"][0:book["location_and_refresh_time"].find("-")]
                    book["refresh_time"] = book["location_and_refresh_time"][book["location_and_refresh_time"].find("-")+2:]
                    self.books.append(book)
                except Exception as ex:
                    print("Something went wrong... ", ex)
    def show_all(self, books):    
        for one_book in self.books:
            try:
                print(f'''
                        url:
                            {one_book["url"]}
                        title:
                            {one_book["title"]}
                        price:
                            {one_book["price"]}
                        condition:
                            {one_book["condition"]}
                        seller location:
                            {one_book["location"]}
                        seller last refresh time:
                            {one_book["refresh_time"]}
                        '''+ "-"*80)
            except Exception as ex:
                print("Something went wrong... ", ex)
    def make_a_table(self, list, columns, name):
        header = columns #["title", "url", "price", "condition", "location", "refresh_time"]
        datafile = pandas.DataFrame(list, columns=header) #self.books,
        file_path = os.path.join(os.path.dirname(__file__), "data")
        datafile.to_csv(os.path.join(file_path, f"{name}.csv"), sep=";", encoding="utf8")       
# max_price = 60
# url_with_add_par = f"https://www.olx.pl/muzyka-edukacja/ksiazki/ksiazki-naukowe/q-python/?search%5Bfilter_float_publishyear:from%5D=2020&view=list&search%5Bfilter_float_price:to%5D={max_price}"
# books_with_changed_par = []
# r = requests.get(url_with_add_par)
# soup = BeautifulSoup(r.text, "lxml")
# book_list = soup.findAll("a", class_='css-rc5s2u')
# for one_book in book_list:
#     try:
#         book = {}
#         book["url"] = "https://www.olx.pl" + str(one_book.get("href"))
#         book["title"] = one_book.find("div", class_="css-u2ayx9").find("h6", class_="css-16v5mdi er34gjf0").text
#         book["price"] =  one_book.find("div", class_="css-u2ayx9").find("p", class_="css-10b0gli er34gjf0").text
#         book["condition"] = one_book.find("span", class_="css-3lkihg").get("title") #.find("div", class_="css-u2ayx9").find("div", class_="css-112xsl6")
#         book["location_and_refresh_time"] = one_book.find("p", class_="css-veheph er34gjf0").text
#         book["location"] = book["location_and_refresh_time"][0:book["location_and_refresh_time"].find("-")]
#         book["refresh_time"] = book["location_and_refresh_time"][book["location_and_refresh_time"].find("-")+2:]
#         books_with_changed_par.append(book)
#     except Exception as ex:
#         print("Something went wrong... ", ex)

# header = ["title", "url", "price", "condition", "location", "refresh_time"]
# datafile = pandas.DataFrame(books_with_changed_par, columns=header)
# file_path = os.path.join(os.path.dirname(__file__), "data")
# datafile.to_csv(os.path.join(file_path, "olx_2020+.csv"), sep=";", encoding="utf8")