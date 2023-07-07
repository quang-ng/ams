from datetime import datetime
from typing import Any
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, FormView
from django.shortcuts import get_object_or_404, redirect

from asset.forms import InsertActivityForm
from asset.models import Asset, Liability, ActivityCategory

# Create your views here.
class InsertActivityView(LoginRequiredMixin, FormView):
    template_name = "asset/new_activity.html"
    form_class = InsertActivityForm


    def get_initial(self):
        user = self.request.user
        initial = super().get_initial()
        initial['category'] = ActivityCategory.objects.all()
        initial['asset'] = Asset.objects.all()
        initial['liability'] = Liability.objects.all()
        initial['input_date'] = datetime.now()

        
        return initial

    def form_valid(self, form):
        user = self.request.user

        print("form.cleaned_data: ", form.cleaned_data)

        return redirect("asset:new_activity")
