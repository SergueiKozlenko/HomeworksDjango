from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article, Tag, Relationship


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def create_tags_view(request):
    template = 'articles/tags.html'
    fixture = [
        {'id': 1, 'topic': 'Культура'},
        {'id': 2, 'topic': 'Город'},
        {'id': 3, 'topic': 'Здоровье'},
        {'id': 4, 'topic': 'Наука'},
        {'id': 5, 'topic': 'Космос'},
        {'id': 6, 'topic': 'Международные отношения'}
    ]
    for tag in fixture:
        Tag.objects.update_or_create(defaults=tag, **tag)

    for article in Article.objects.all():
        if article.id == 1:
            Relationship.objects.update_or_create(title_id=article.id, topic_id=1, is_main=True)
            Relationship.objects.update_or_create(title_id=article.id, topic_id=2, is_main=False)
        if article.id == 2:
            Relationship.objects.update_or_create(title_id=article.id, topic_id=3, is_main=True)
            Relationship.objects.update_or_create(title_id=article.id, topic_id=4, is_main=False)
        if article.id == 3:
            Relationship.objects.update_or_create(title_id=article.id, topic_id=5, is_main=True)
            Relationship.objects.update_or_create(title_id=article.id, topic_id=6, is_main=False)
            Relationship.objects.update_or_create(title_id=article.id, topic_id=4, is_main=False)

    context = {'scopes': Relationship.objects.all()}

    return render(request, template, context=context)
