from django.urls import path, include
from django.conf import settings
from articles.views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='articles'),
]

if settings.DEBUG:
    import debug_toolbar

urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
