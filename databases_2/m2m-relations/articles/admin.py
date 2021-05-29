from django.contrib import admin
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import Relationship, Article, Tag


class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        is_main_count = 0
        topics = []
        for form in self.forms:
            is_main = form.cleaned_data.get("is_main")
            topic = form.cleaned_data.get("topic")
            if is_main == 1 and is_main_count == 1:
                raise ValidationError('Основным может быть только один раздел')
            if is_main == 1:
                is_main_count = 1
            if topic in topics:
                raise ValidationError('Раздел не может повторяться')
            topics.append(form.cleaned_data.get("topic"))

        if is_main_count != 1:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = Relationship
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]
