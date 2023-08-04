from django.urls import path

from asset.views import InsertActivityView
from asset import views
from asset.views import ListActivityView, NetAssetHistoryView
from asset.views import InvestmentView


app_name = "asset"

urlpatterns = [
    path("insert-new-activity/", InsertActivityView.as_view(), name="new_activity"),
    path("history-activity/", ListActivityView.as_view(), name="history_activity"),
    path("ajax/load-cities/", views.load_category, name="ajax_load_category"),
    path(
        "asset-liquidation-process",
        views.AssetLiquidationProcessView.as_view(),
        name="asset_liquidation_process",
    ),
    path("net-asset-history", NetAssetHistoryView.as_view(), name="net_asset_history"),
    path("investment", InvestmentView.as_view(), name="investment"),
]
