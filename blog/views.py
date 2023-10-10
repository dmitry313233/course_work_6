from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, DetailView

from blog.forms import BlogForm
from blog.models import Blog


# Create your views here.

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog:blog_list')

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'


    def get_object(self, queryset=None):
        self.object = super().get_object()
        self.object.count_view += 1
        self.object.save()
        return self.object

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog:blog_list')
