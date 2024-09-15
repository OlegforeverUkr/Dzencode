from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, FormView, ListView
from posts.forms import AddCommentForm

from posts.models import Comment, Post
from posts.search import search_posts


class MainView(ListView):
    model = Post
    template_name = 'base/main_page.html'
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
            if order_by == "username":
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
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        comments = Comment.objects.filter(post=post).order_by('created_at')

        paginator = Paginator(comments, 25)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context["title"] = "Комментарии"
        return context


class AddCommentView(LoginRequiredMixin, FormView):
    form_class = AddCommentForm
    template_name = 'posts/add_comment.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs


    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])

        parent_comment = None
        if form.cleaned_data['parent_id']:
            parent_comment = get_object_or_404(Comment, pk=form.cleaned_data['parent_id'])

        Comment.objects.create(
            post=post,
            user=self.request.user,
            url=form.cleaned_data['home_page'],
            body=form.cleaned_data['text'],
            parent=parent_comment
        )
        messages.success(self.request, 'Ваш комментарий был добавлен успешно.')
        return redirect(reverse('posts:post_detail', args=[post.id]))


    def form_invalid(self, form):
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(self.request, f'{error}')

        return self.render_to_response(self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        context['post'] = Post.objects.get(pk=post_id)
        context['title'] = 'Добавить комментарий'
        context['parent_id'] = self.request.GET.get('parent_id')
        return context
