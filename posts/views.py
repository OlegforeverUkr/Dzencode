from django.shortcuts import render
from django.views.generic import DetailView, ListView

from posts.models import Post
from posts.search import search_posts


class MainView(ListView):
    model = Post
    template_name = 'main_page.html'
    context_object_name = "posts"
    paginate_by = 3
    allow_empty = True

    def get_queryset(self):
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if query:
            posts = search_posts(query)
        else:
            posts = super().get_queryset()

        if order_by:
            if order_by == "user":
                posts = posts.order_by("user__username")
            elif order_by == "email":
                posts = posts.order_by("user__email")
            elif order_by == "news":
                posts = posts.order_by("-created_at")
            elif order_by == "oldest":
                posts = posts.order_by("created_at")

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная Страница"
        return context



class PostView(DetailView):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        return render(request, 'post_page.html', {'post': post, 'title': post.title})
