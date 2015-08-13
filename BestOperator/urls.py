from django.conf.urls import url
from BestOperator import views
from BestOperator.views import MainView

urlpatterns = [
    url(r'^r/$', views.post_results, name='results'),
    url(r'^$', MainView.as_view(), name='index'),
]