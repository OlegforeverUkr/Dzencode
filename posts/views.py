from django.shortcuts import render
from django.views.generic import ListView

from posts.models import Post


class MainView(ListView):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'main_page.html', {'posts': posts, 'title': 'Главная страница'})


class PostView(ListView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, 'post_page.html', {'post': post, 'title': post.title})