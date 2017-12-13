from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
        def get(self, request, **kwargs):
                return render(request, 'index.html', context=None)

class AuctionsPageView(TemplateView):
        def get(self, request, **kwargs):
                return render(request, 'auctions.html', context=None)

class AuctionsCoordPageView(TemplateView):
        def get(self, request, **kwargs):
                return render(request, 'auctions.xml', content_type='application/xml')
