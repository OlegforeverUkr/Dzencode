from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.shortcuts import redirect
from django.contrib import auth, messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserAuthForm, UserProfileForm, UserRegistrationForm


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy('posts:main')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        auth.login(self.request, user)
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class UserLoginView(LoginView):
    form_class = UserAuthForm
    template_name = "login.html"
    success_url = reverse_lazy('posts:main')

    def form_valid(self, form):
        messages.success(self.request, f"{form.cleaned_data['username']}, вы вошли в свой аккаунт.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy('posts:main')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context



class UserLogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.warning(request=request, message="Вы вышли из аккаунта.")
        return redirect('posts:main')


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                error_messages.append(error)
        messages.warning(self.request, " ".join(error_messages))
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Кабинет'
        return context