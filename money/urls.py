from django.urls import path
from . import views

app_name = 'money'
urlpatterns = [
        path('', views.MainView.as_view(), name='index'),    #views.indexはまだ作ってないからあとで作る
        path('<int:year>/<int:month>', views.MainView.as_view(), name='index'),
        #path('', views.money_list, name='money_list'),
        ]