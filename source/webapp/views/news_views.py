from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import News


class NewsView(ListView):
    model = News
    template_name = 'news/news.html'
    context_object_name = 'news_list'
    ordering = ['-created_at']


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'


class NewsAddView(UserPassesTestMixin, CreateView):
    model = News
    template_name = 'base_CRUD/add.html'
    fields = ('title', 'text', 'photo')
    success_url = reverse_lazy('webapp:news')

    def test_func(self):
        user = self.request.user
        return user.is_staff


class NewsEditView(UserPassesTestMixin, UpdateView):
    template_name = 'base_CRUD/edit.html'
    model = News
    fields = ('title', 'text', 'photo')
    context_object_name = 'news'

    def test_func(self):
        user = self.request.user
        return user.is_staff

    def get_success_url(self):
        return reverse('webapp:news')


class NewsDeleteView(UserPassesTestMixin, DeleteView):
    model = News
    template_name = 'base_CRUD/delete.html'
    context_object_name = 'news'
    success_url = reverse_lazy('webapp:news')

    def test_func(self):
        user = self.request.user
        return user.is_staff




