import csv

import self
from django.conf.urls import url
from django.template.response import TemplateResponse

from .parsers.main import main
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.translation import ngettext
from import_export.admin import ImportExportModelAdmin

from .models import Article


def delete_duplicate(modeladmin, request, queryset):
    count_articles_before = len(queryset)
    for title in queryset.values_list('title', flat=True).distinct():
        queryset.filter(pk__in=queryset.filter(title=title).values_list('id', flat=True)[1:]).delete()
    count_articles_after = len(queryset.values_list('title', flat=True).distinct())
    count_delete_duplicate = count_articles_before - count_articles_after
    modeladmin.message_user(request, ngettext(
        '%d duplicate story was successfully deleted .',
        '%d duplicate stories were successfully deleted.',
        count_delete_duplicate,
    ) % count_delete_duplicate, messages.SUCCESS)


delete_duplicate.short_description = "Delete duplicate"


class ArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    # article = Article(title='')
    change_list_template = "admin/model_change_list.html"

    def get_urls(self):
        urls = super(ArticleAdmin, self).get_urls()
        custom_urls = [
            url('^import/$', self.process_import, name='process_import'), ]
        return custom_urls + urls

    def process_import(self, request):
        if request.POST.get('post') == 'yes':
            # count_articles = main()
            # print(count_articles)
            # self.message_user(request, ngettext(
            #     '%d article was successfully parsed.',
            #     '%d articles were successfully parsed.',
            #     count_articles,
            # ) % count_articles, messages.SUCCESS)
            with open('articles.csv', 'r', encoding='utf-8') as File:
                reader = csv.reader(File)
                flag = False
                count = -1
                for row in reader:
                    count += 1
                    if flag:
                        article = Article(id=row[0], title=row[1], imageUrl=row[2], category=row[3],
                                          datePublication=row[4],
                                          articleUrl=row[5])
                        article.save()
                    else:
                        flag = True
                        continue
                self.message_user(request, ngettext(
                    '%d article was successfully added.',
                    '%d articles were successfully added.',
                    count,
                ) % count, messages.SUCCESS)

        else:
            if request.POST.get('post') == 'no':
                return HttpResponseRedirect("../")
            return TemplateResponse(request, "admin/my_action_confirmation.html")
        return HttpResponseRedirect("../")

    list_display = ['title', 'datePublication']
    search_fields = ('title',)
    actions = [delete_duplicate]


admin.site.register(Article, ArticleAdmin)
