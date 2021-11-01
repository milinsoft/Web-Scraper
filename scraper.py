import string
import os
import os.path

import requests
from bs4 import BeautifulSoup


class NatureScraper:
    def __init__(self, _last_page, _article_type):
        self._curr_page_num = 1
        self._url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={self._curr_page_num}'
        self._last_page = _last_page
        self._article_type = _article_type
        self._page_source = None
        self._articles = []
        self._saved_articles = []

    def get_page_source(self):
        r = requests.get(self._url)
        if r.status_code == requests.codes.ok:
            self._page_source = BeautifulSoup(r.content, 'html.parser')
            return self._page_source

    def get_articles(self) -> list:
        self._articles = self._page_source.find_all('article')
        return self._articles

    def find_news_articles(self) -> list:
        for article in self._articles:
            article_type_span = article.find('span', attrs={'data-test': 'article.type'})
            if article_type_span:
                if article_type_span.contents[1].get_text() == self._article_type:
                    article_title = article.find('a').get_text()
                    for p in string.punctuation:
                        article_title.maketrans(p, ' ')
                    article_title = '_'.join(article_title.split(' '))
                    link_info = {'title': article_title,
                                 'link': article.find('a')['href']}
                    self._saved_articles.append(link_info)
        return self._saved_articles

    def save_news_articles(self):
        for article in self._saved_articles:
            filename = article['title'] + '.txt'
            file = open(filename, 'wb')
            r = requests.get('https://nature.com' + article['link'])
            if r.status_code == requests.codes.ok:
                soup = BeautifulSoup(r.content, 'html.parser')
                file.write(bytes(soup.find('div', 'c-article-body').get_text().strip(), 'utf-8'))
            file.close()

    def page_switch(self):
        self._curr_page_num += 1


def folder_maker():
    def wrapper():
        ...
    ...


def main():
    try:
        scraper = NatureScraper(int(input("How many pages scrapper should look for?\n")), input("What article type are you looking for?\n").capitalize())

    except ValueError:
        print("Only integers accepted as a page numbers")
        return main()

    while scraper._curr_page_num <= scraper._last_page:

        main_directory = os.getcwd()
        # print("you currently in:", main_directory)
        # create new folder:
        subfolder = "Page_" + str(scraper._curr_page_num)
        try:
            os.mkdir(subfolder)
            os.chdir(os.path.join(main_directory, subfolder))
        except FileExistsError:
            os.chdir(os.path.join(main_directory, subfolder))
        # print("you switched to:", os.getcwd())
        scraper.get_page_source()
        scraper.get_articles()
        articles = scraper.find_news_articles()
        titles = []
        for a in articles:
            titles.append(a['title'])
        scraper.save_news_articles()
        print('Saved articles:')
        print(titles)

        os.chdir(main_directory)
        scraper.page_switch()


if __name__ == '__main__':
    main()
