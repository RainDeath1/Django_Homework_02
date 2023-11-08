from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import models
from django.views.generic import TemplateView



class LoginRequiredMixin:
    login_url = 'login/'

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super().as_view(*args, **kwargs)
        return login_required(view)


class BaseMixin:
    base_context = {
        'localhost': 'Список задач',
        'footer_text': 'Copyright 2023 by My Website',
    }

    def get_base_context(self):
        return self.base_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
        return context


class MenuMixin(BaseMixin):
    menu_items = []

    def get_menu_items(self):
        return self.menu_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = self.get_menu_items()
        return context


class HomePageView(MenuMixin, TemplateView):
    template_name = 'home.html'
    menu_items = [
        {'name': 'Home', 'url': 'task-list/'},
        {'name': 'About', 'url': 'user_list/'},
    ]


