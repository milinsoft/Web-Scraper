import string
import os

import requests
from bs4 import BeautifulSoup


class NatureScraper:
    def __init__(self, last_page, _article_type):
        self.curr_page_num = 1
        self._url = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={self.curr_page_num}'
        self.last_page = last_page
        self._article_type = _article_type
        self._page_source = None
        self._articles = []
        self._saved_articles = []
        self.main_directory = os.getcwd()
        self.subfolder = None

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
        self.curr_page_num += 1

    def make_subfolder(self):
        self.subfolder = "Page_" + str(self.curr_page_num)
        try:
            os.mkdir(self.subfolder)
        except FileExistsError:
            pass


def main():
    try:
        scraper = NatureScraper(int(input("How many pages scrapper should look for?\n")), input("What article type are you looking for?\n").capitalize())
    except ValueError:
        print("Only integers accepted as a page numbers")
        return main()

    while scraper.curr_page_num <= scraper.last_page:
        scraper.make_subfolder()
        os.chdir(scraper.subfolder)
        scraper.get_page_source()
        scraper.get_articles()
        articles = scraper.find_news_articles()
        titles = [article['title'] for article in articles]
        scraper.save_news_articles()
        print('Saved articles:\n', titles)
        scraper.page_switch()
        os.chdir(scraper.main_directory)


if __name__ == '__main__':
    main()
