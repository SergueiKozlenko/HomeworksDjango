from django.views.generic import ListView

from .models import Student


class StudentListView(ListView):
    model = Student

    def get_queryset(self):
        return Student.objects.prefetch_related("teachers").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
