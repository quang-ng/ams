from typing import Any
from django import http
from django.views.generic import TemplateView
from django.shortcuts import redirect


class IndexPageView(TemplateView):
    def get(self, request):
        return redirect("asset:new_activity")


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
