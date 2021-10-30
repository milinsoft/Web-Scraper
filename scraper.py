import string

import requests
from bs4 import BeautifulSoup


class NatureScraper:
    def __init__(self):
        self._url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3'
        self._page_source = None
        self._articles = []
        self._saved_articles = []

    def get_page_source(self):
        r = requests.get(self._url)
        if r.status_code == requests.codes.ok:
            self._page_source = BeautifulSoup(r.content, 'html.parser')
            return self._page_source

    def get_articles(self):
        self._articles = self._page_source.find_all('article')
        return self._articles

    def find_news_articles(self):
        for article in self._articles:
            article_type_span = article.find('span', attrs={'data-test': 'article.type'})
            if article_type_span is not None:
                if article_type_span.contents[1].get_text() == 'News':
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


def main():
    scraper = NatureScraper()
    scraper.get_page_source()
    scraper.get_articles()
    articles = scraper.find_news_articles()
    titles = []
    for a in articles:
        titles.append(a['title'])
    scraper.save_news_articles()
    print('Saved articles:')
    print(titles)


if __name__ == '__main__':
    main()
