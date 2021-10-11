from bs4 import BeautifulSoup as bs
import requests as req
import csv
from prettytable import PrettyTable
import random
import threading
import logging
import string
import time

HABR = 'https://habr.com/'
DEVBY = 'https://dev.by/news'
ONLINER = 'https://tech.onliner.by/'
RT = 'https://russian.rt.com/tag/sport'
PRIME = 'https://1prime.ru/world/'
IZ = 'https://iz.ru/rubric/nauka'

FILENAME = "articles.csv"
ARTICLES_HABR = []
ARTICLES_DEVBY = []
ARTICLES_ONLINER = []
ARTICLES_RT = []
ARTICLES_PRIME = []
ARTICLES_IZ = []

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}


def parseHabrCategory(link):
    response = req.get(HABR + link, headers=header)
    soup = bs(response.text, 'lxml')
    articles = soup.find(
        'div', class_='tm-articles-list').find_all('article', class_='tm-articles-list__item')
    parsed_articles = []
    for article in articles:
        try:
            date_article = article.find('div', class_='tm-article-snippet__meta').find(
                'span', class_='tm-article-snippet__datetime-published').find('time').get('title')[:10]
        except:
            continue

        title_article = article.find(
            'h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').text
        url_article = HABR + article.find(
            'h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').find('a')['href'][1:]
        imageurl_article = article.find('div', class_='tm-article-body tm-article-snippet__lead').find(
            'div', class_='tm-article-snippet__cover tm-article-snippet__cover_cover')

        if None == imageurl_article:
            imageurl_article = article.find('div', class_='tm-article-body tm-article-snippet__lead').find(
                'div', class_='article-formatted-body article-formatted-body_version-1')
            if imageurl_article != None:
                imageurl_article = imageurl_article.find('div')
                if imageurl_article != None:
                    try:
                        imageUrl = imageurl_article.find('img')['src']
                    except TypeError as e:
                        logging.error(e)
            else:
                imageUrl = 'https://mirpozitiva.ru/wp-content/uploads/2019/11/1479734077_kofe10.jpg'
        else:
            imageUrl = imageurl_article.find(
                'img', class_='tm-article-snippet__lead-image')['src']
        ARTICLES_HABR.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": imageUrl, "category": "Tech", "datePublication": date_article, "articleUrl": url_article})


def parseHabr():
    start = time.monotonic()
    response = req.get(HABR, headers=header)
    soup = bs(response.text, 'lxml')
    categories = soup.find(
        'nav', class_='tm-main-menu__section-content').find_all('a', class_="tm-main-menu__item")[1:]
    links_categories = list(['ru' + category['href'][3:]
                             for category in categories])
    for link in links_categories:
        parseHabrCategory(link)
    response.close()
    end = time.monotonic()


def parseDevby():
    start = time.monotonic()
    response = req.get(DEVBY, headers=header)
    soup = bs(response.text, 'lxml')
    articles = soup.find(
        'div', class_='cards-group cards-group_list').find_all('div', class_='card card_media card_col-mobile')

    for article in articles:
        article_url = article['data-vr-contentbox-url']
        res = req.get(article_url, headers=header)
        soup = bs(res.text, 'lxml')
        date_article = soup.find('article', class_='article').find('div', class_='article__header').find('div',
                                                                                                         class_='article__container').find(
            'div', class_='article-meta article-meta_semibold').find_all('span', class_='article-meta__item')[-1][
            'data-published-at']
        res.close()
        imageurl_article = DEVBY[:14] + article.find(
            'div', class_='card__img-wrap').find('img', class_='card__img')['src']
        title_article = article.find('div', class_='card__info').find('div', class_='card__body').find(
            'div', class_='card__title card__title_text-crop').text.strip()
        ARTICLES_DEVBY.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": imageurl_article, "category": "Tech", "datePublication": date_article,
             "articleUrl": article_url})
    response.close()
    end = time.monotonic()


def parseOnlinerCategory(category):
    response = req.get(ONLINER + category, headers=header)
    soup = bs(response.text, 'lxml')
    articles = soup.find('div', class_='news-grid__part news-grid__part_1').find('div', class_='news-tidings').find(
        'div', class_='news-tidings__list').find_all('div', class_='news-tidings__item_condensed')
    for article in articles:
        url_article = article.find('a')['href'][1:]
        res = req.get(ONLINER + url_article, headers=header)
        soup = bs(res.text, 'lxml')

        urlimage_article = soup.find(
            'div', class_='news-content js-scrolling-area').find('div', class_='news-header__image')['style'][23:-3]
        title_article = article.find('div', class_='news-tidings__clamping').find(
            'span', class_='news-helpers_show_mobile-small').text
        date_article = url_article[0:10].replace('/', '-')
        ARTICLES_ONLINER.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": urlimage_article, "category": "Tech", "datePublication": date_article,
             "articleUrl": ONLINER + url_article})


def parseOnliner():
    start = time.monotonic()
    response = req.get(ONLINER, headers=header)
    soup = bs(response.text, 'lxml')
    categories = soup.find('div', class_='news-content js-scrolling-area').find('div',
                                                                                class_='news-grid__flex news-grid__flex_alter').find(
        'div', class_='news-grid__part news-grid__part_1').find('div', class_='news-rubrics').find('ul',
                                                                                                   class_='news-rubrics__list').find_all(
        'li', class_='news-rubrics__item')[5::3]
    links_categories = list([category.find('a')['href'][1:]
                             for category in categories])
    for link in links_categories:
        parseOnlinerCategory(link)
    end = time.monotonic()


def parseRT():
    start = time.monotonic()
    response = req.get(RT, headers=header)
    soup = bs(response.text, 'lxml')
    items = soup.find('ul', class_='listing__rows listing__rows_js').find_all(
        'li', class_='listing__column listing__column_all-new listing__column_js')
    for item in items:
        if item.find('div', class_='listing__card').find('div', class_='card card_all-new').find('div',
                                                                                                 class_='card__cover card__cover_all-new') == None:
            continue
        url_article = RT[0:-10] + item.find('div', class_='listing__card').find(
            'div', class_='card card_all-new').find('a')['href']
        res = req.get(url_article, headers=header)
        soup = bs(res.text, 'lxml')
        image_url = soup.find('div', class_='layout__wrapper layout__wrapper_article-page').find('div',
                                                                                                 class_='layout__content').find(
            'div', class_='article article_article-page').find('div',
                                                               class_='article__cover article__cover_article-page').find(
            'img')['src']
        title_article = item.find('div', class_='listing__card').find(
            'div', class_='card card_all-new').find('a').get_text().strip()
        date_article = item.find('div', class_='listing__card').find(
            'div', class_='card card_all-new').find('div', class_='card__date-time card__date-time_all-new_cover').find(
            'time')['datetime'][0:9]
        ARTICLES_RT.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": image_url, "category": "Sport", "datePublication": date_article, "articleUrl": url_article})
    end = time.monotonic()


def parsePrime():
    start = time.monotonic()
    response = req.get(PRIME, headers=header)
    soup = bs(response.text, 'lxml')
    items = soup.find('div', class_='rubric-list__articles').find_all('article',
                                                                      class_='rubric-list__article rubric-list__article_default')
    for item in items:
        date_article = item.find('time')['datetime'][0:10]
        title_article = item.find('h2').get_text()
        url_article = PRIME[0:-7] + item.find('h2').find('a')['href']
        res = req.get(url_article, headers=header)
        soup = bs(res.text, 'lxml')
        image_url = PRIME[0:-7] + soup.find('div', class_='page').find('main', class_='main').find('div',
                                                                                                   class_='infinite__article-content').find(
            'div', class_='article-header').find('figure', class_='article-header__media').find('div',
                                                                                                class_='article-header__media-wrapper').find(
            'img')['src']
        ARTICLES_PRIME.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": image_url, "category": "Economics", "datePublication": date_article,
             "articleUrl": url_article})
    end = time.monotonic()


def parseIz():
    start = time.monotonic()
    response = req.get(IZ, headers=header)
    soup = bs(response.text, 'lxml')
    items = soup.find('div', class_='page-content inside_page active only_left_side').find('div',
                                                                                           class_='four-col-news__list__row').find_all(
        'div', class_='node__cart__item show_views_and_comments')
    for item in items:
        if item.find('div', class_='node__cart__item__category_news rubric-box')['data-type'] != 'news':
            continue
        url_article = IZ[0:13] + \
                      item.find('a', class_='node__cart__item__inside')['href']
        title_article = item.find('a', class_='node__cart__item__inside').find('div',
                                                                               class_='node__cart__item__inside__info').find(
            'div', class_='node__cart__item__inside__info__title small-title-style1').get_text().strip()
        date_article = \
            item.find('a', class_='node__cart__item__inside').find('div', class_='node__cart__item__inside__info').find(
                'div', class_='node__cart__item__inside__info__time small-gray').find('time')['datetime'][0:10]
        res = req.get(url_article, headers=header)
        soup = bs(res.text, 'lxml')
        image_url = 'https:' + \
                    soup.find('div', class_='big_photo__img').find('link')['href']
        ARTICLES_IZ.append(
            {"id": int(''.join(random.choice(string.digits) for _ in range(10))), "title": title_article,
             "imageUrl": image_url, "category": "Science", "datePublication": date_article, "articleUrl": url_article})
    end = time.monotonic()


def csv_write():
    with open(FILENAME, "w", newline="", encoding='utf-8') as file:
        columns = ["id", "title", "imageUrl",
                   "category", "datePublication", "articleUrl"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(ARTICLES_HABR)
        writer.writerows(ARTICLES_DEVBY)
        writer.writerows(ARTICLES_ONLINER)
        writer.writerows(ARTICLES_IZ)
        writer.writerows(ARTICLES_PRIME)
        writer.writerows(ARTICLES_RT)


def main():
    logging.basicConfig(level=logging.INFO)
    print(time.ctime())
    start = time.monotonic()
    th1 = threading.Thread(target=parseHabr)
    logging.info("Data collection starting...")
    th1.start()
    th2 = threading.Thread(target=parseDevby)
    th2.start()
    th3 = threading.Thread(target=parseOnliner)
    th3.start()
    th4 = threading.Thread(target=parseIz)
    th4.start()
    th5 = threading.Thread(target=parsePrime)
    th5.start()
    th6 = threading.Thread(target=parseRT)
    th6.start()
    th6.join()
    th5.join()
    th4.join()
    th3.join()
    th2.join()
    th1.join()
    end = time.monotonic()
    csv_write()
    print('Total execution time: {:>9.4f}'.format(end - start))
    return len(ARTICLES_HABR) + len(ARTICLES_DEVBY) + len(ARTICLES_ONLINER) + len(ARTICLES_IZ) + len(
        ARTICLES_PRIME) + len(ARTICLES_RT)
