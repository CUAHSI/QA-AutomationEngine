# auction_page/urls.py
from django.conf.urls import url
from auction_page import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'auctions-view/$', views.AuctionsPageView.as_view()),
    url(r'auctions-coord/$', views.AuctionsCoordPageView.as_view())
]
