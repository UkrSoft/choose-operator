from django.conf.urls import url
from BestOperator import views
from BestOperator.views import MainView

urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),
    url(r'^$/results', views.get_results, name='get_results'),
]