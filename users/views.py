from django.shortcuts import render
from django.views import View


class MainView(View):
    def get(self, request):
        return render(request, context={"title": "Dzencode"}, template_name='base.html')
