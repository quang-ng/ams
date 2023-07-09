from django.urls import path

from asset.views import InsertActivityView
from asset import views


app_name = 'asset'

urlpatterns = [
    path('insert-new-activity/', InsertActivityView.as_view(), name='new_activity'),
    path('ajax/load-cities/', views.load_category, name='ajax_load_category'),
]