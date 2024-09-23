from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, FormView, ListView
from posts.forms import AddCommentForm, AddPostForm

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
        cache_key = f"posts_{order_by}_{query}"

        posts = cache.get(cache_key)
        if posts is None:
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

            cache.set(cache_key, posts, 60 * 15)
        return posts


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная Страница"
        return context



class PostsView(DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = Comment.objects.filter(post=post, parent__isnull=True).order_by('created_at')

        paginator = Paginator(comments, 25)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context["title"] = "Комментарии"
        context['form'] = AddCommentForm()
        context['messages'] = messages.get_messages(self.request)
        return context


class CreatePostView(LoginRequiredMixin, FormView):
    form_class = AddPostForm
    template_name = 'posts/create_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddPostForm()
        context['title'] = 'Добавить пост'
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'user': self.request.user}
        return kwargs

    def form_valid(self, form):
        post = Post.objects.create(
            user=self.request.user,
            title=form.cleaned_data['title'],
            body=form.cleaned_data['body'],
            url=form.cleaned_data['url']
        )

        messages.success(self.request, 'Ваш пост был создан успешно.')
        return redirect(reverse('posts:post_detail', args=[post.id]))


    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{error}')
        return self.render_to_response(self.get_context_data(form=form))



class AddCommentToPostView(LoginRequiredMixin, FormView):

    def post(self, request, *args, **kwargs):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        form = AddCommentForm(request.POST, request.FILES, initial={'user': request.user})

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.url = form.cleaned_data["home_page"]
            comment.body = form.cleaned_data["text"]
            comment.image = form.cleaned_data.get("image") 
            comment.file = form.cleaned_data.get("file")
            comment.save()

            messages.success(request, 'Ваш комментарий добавлен.')
            return JsonResponse({
                'success': True,
                'user': str(request.user),
                'comment': comment.body,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        errors = {field: errors for field, errors in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)
    


class AddCommentToCommentView(LoginRequiredMixin, FormView):

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        form = AddCommentForm(request.POST, request.FILES, initial={'user': request.user})

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.url = form.cleaned_data["home_page"]
            comment.body = form.cleaned_data["text"]
            comment.image = form.cleaned_data.get("image") 
            comment.file = form.cleaned_data.get("file")
            comment.parent = parent_comment
            comment.save()

            messages.success(request, 'Ваш комментарий добавлен.')
            return JsonResponse({
                'success': True,
                'user': str(request.user),
                'comment': comment.body,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })


        errors = {field: errors for field, errors in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_id = self.kwargs.get('post_id')
        comment_id = self.kwargs.get('comment_id')

        context['post'] = get_object_or_404(Post, pk=post_id)
        context['comment'] = get_object_or_404(Comment, pk=comment_id)
        context['title'] = 'Ответить на комментарий'
        return context


class DeletePostView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:main')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Пост успешно удалён.')
        return HttpResponseRedirect(self.get_success_url())
    

class DeleteCommentView(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user or self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, 'Комментарий успешно удалён.')
        return redirect(request.META["HTTP_REFERER"])
