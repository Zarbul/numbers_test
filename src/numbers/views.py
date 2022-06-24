from django.views.generic import ListView

from . import models


class Index(ListView):
    """
    Отображает страницу с данными из базы
    """
    model = models.Order
    template_name = 'index.html'


