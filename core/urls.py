from django.urls import path
from . import views
from .views import *
from .rest_apis import PointhautsnbrApi,DepenseRecetteChartApi
# Routers provide an easy way of automatically determining the URL conf.

urlpatterns = [
    path('budgetjour/<int:id>',views.etat_budgets),
    path('apiis', DepenseRecetteChartApi.as_view()),
]