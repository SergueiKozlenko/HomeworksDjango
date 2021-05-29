from django.urls import path

from articles.views import create_tags_view, ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
    path('tags/', create_tags_view, name='tags-view')
]
