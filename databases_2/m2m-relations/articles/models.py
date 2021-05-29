from django.db import models


class Article(models.Model):
    """
    Модель Статья
    """
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение', )

    tags = models.ManyToManyField('Tag', related_name='tags', through='Relationship')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Модель Раздел
    """
    topic = models.CharField(max_length=128, verbose_name='Раздел')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.topic


class Relationship(models.Model):
    """
    Модель Статьи-Разделы
    """
    title = models.ForeignKey(Article, related_name='scopes', verbose_name="Статья", on_delete=models.CASCADE)
    topic = models.ForeignKey(Tag, related_name='scopes', verbose_name="Тематики статьи", default=False,
                              on_delete=models.CASCADE)
    is_main = models.BooleanField(verbose_name="Основной", default=False)

    def __str__(self):
        return f"{self.title} | {self.topic} | {self.is_main}"
