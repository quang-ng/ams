from django.urls import path

from asset.views import InsertActivityView


app_name = 'asset'

urlpatterns = [
    path('insert-new-activity/', InsertActivityView.as_view(), name='new_activity'),
]