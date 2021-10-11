from django.shortcuts import render
from .models import Article
from .parsers import parse_data_navbar


def main(request, page_id=1, topic='All'):
    currencies = parse_data_navbar.get_data()
    articles = Article.objects.order_by('-datePublication')
    if topic == 'All':
        result = setTables(articles, page_id)
    else:
        articles_topic = articles.filter(category=topic)
        result = setTables(articles_topic, page_id)
    return render(request, 'main/base.html',
                  {'article_table': [result[2], result[3], result[4]],
                   'currencies': currencies,
                   'list_pages': range(result[0], result[1]),
                   'current_page': page_id,
                   'topic': topic,
                   'search': 0})


def setTables(articles, page_id):
    count_pages = len(articles[(page_id - 1) * 27:]) // 27 + 1
    last_page = page_id + 3 if (page_id + 2) <= count_pages else page_id + count_pages
    start_page = page_id - 2 if page_id >= 3 else page_id - page_id + 1
    articles_for_left_table = articles[(page_id - 1) * 27:(page_id - 1) * 27 + 27:3]
    articles_for_center_table = articles[(page_id - 1) * 27 + 1:(page_id - 1) * 27 + 27:3]
    articles_for_right_table = articles[(page_id - 1) * 27 + 2:(page_id - 1) * 27 + 27:3]
    return start_page, last_page, articles_for_left_table, articles_for_center_table, articles_for_right_table



def search(request, page_id=1):
    search_article = request.GET.get('searched-article', '')
    currencies = parse_data_navbar.get_data()
    try:
        search_article.strip()
        articles_search = Article.objects.filter(title__icontains=search_article)
        if len(articles_search) > 0:
            result = setTables(articles_search, page_id)
            return render(request, 'main/base.html',
                          {'article_table': [result[2], result[3], result[4]],
                           'currencies': currencies,
                           'list_pages': range(result[0], result[1]),
                           'current_page': page_id,
                           'topic': 'All',
                           'search': 1})
        else:
            return render(request, 'main/base.html',
                          {'currencies': currencies, 'notSearchedArticle': 0, 'search': search_article})
    except (Exception.MultipleObjectsReturned, Article.DoesNotExist):
        return render(request, 'main/base.html',
                      {'currencies': currencies, 'notSearchedArticle': 0, 'search': search_article})
