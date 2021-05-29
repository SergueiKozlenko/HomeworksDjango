from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Article.objects.select_related('author', 'genre').\
            only('author__name', 'genre__name', 'title', 'image', 'text')
