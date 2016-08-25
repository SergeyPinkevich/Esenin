import requests
import sqlite3
import re
from bs4 import BeautifulSoup

url = 'http://slova.org.ru'


class Poem:
    title = ""
    text = ""
    year = 0

    def set_title(self, title):
        self.title = title

    def set_text(self, text):
        self.text = text

    def set_year(self, year):
        self.year = year


def create_db():
    con = sqlite3.connect('texts.db', timeout=10)
    cur = con.cursor()
    cur.execute('CREATE TABLE texts (id INTEGER PRIMARY KEY, title VARCHAR(200), text TEXT, year INTEGER)')
    con.commit()
    con.close()


def update_db(poem):
    con = sqlite3.connect('texts.db', timeout=10)
    cur = con.cursor()
    cur.execute('INSERT INTO texts(title, text, year) VALUES (?, ?, ?)', (poem.title, poem.text, poem.year))
    con.commit()
    con.close()


def get_html(url):
    response = requests.get(url)
    return response.text


def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    list = soup.find("div", {"id": "stihi_list"})
    for link in list.find_all("a"):
        page_link = url + link['href']
        parse_page(get_html(page_link))


def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    block = soup.find("div", class_="list_columns2")

    title = block.find("h3").text
    temp = block.find("pre")
    try:
        text = re.findall(r'<pre>(.*?)<i>', str(temp), re.DOTALL)[0].strip()
        if text == "":
            text = re.findall(r'</i>(.*?)<i>', str(temp), re.DOTALL)[0].strip()
        year = block.find_all("i")
        year = int(re.findall(r'(\d{4})', str(year))[0])
    except IndexError:
        text = re.findall(r'</i>(.*?)<i>', str(temp), re.DOTALL)[0].strip()
    if title == "x x x":
        title = re.split('\n', text)[0]

    print(title)
    # print(text)
    # print(year)

    create_poem(title, text, year)


def create_poem(title, text, year):
    poem = Poem()

    poem.set_title(title)
    poem.set_text(text)
    poem.set_year(year)

    update_db(poem)


if __name__ == '__main__':
    # create_db()
    for i in range(0, 6):
        parse(get_html(url + "/esenin/div" + str(i)))
    # parse_page(get_html(url + "/esenin/vhate/"))
    # print()
    # parse_page(get_html(url + "/esenin/ahkakmnogo/"))

