from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

class PromoappView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'promoapp/promo_index.html')
    
class PromoappNewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'promoapp/news.html')

class IndexView(TemplateView):
    template_name = 'promoapp/index.html'

class FiveView(TemplateView):
    template_name = 'promoapp/5.html'

class SixView(TemplateView):
    template_name = 'promoapp/6.html'

class SevenView(TemplateView):
    template_name = 'promoapp/7.html'

class EightView(TemplateView):
    template_name = 'promoapp/8.html'

class NineView(TemplateView):
    template_name = 'promoapp/9.html'

class TenView(TemplateView):
    template_name = 'promoapp/10.html'

class ElevenView(TemplateView):
    template_name = 'promoapp/11.html'

class TwelveView(TemplateView):
    template_name = 'promoapp/12.html'

class ContactView(TemplateView):
    template_name = 'promoapp/contact.html'

class DiningView(TemplateView):
    template_name = 'promoapp/dining.html'

class GreetingView(TemplateView):
    template_name = 'promoapp/greeting.html'

class IndexEnView(TemplateView):
    template_name = 'promoapp/index_en.html'

class NewsView(TemplateView):
    template_name = 'promoapp/News.html'

class Nouka1View(TemplateView):
    template_name = 'promoapp/nouka1.html'

class Nouka2View(TemplateView):
    template_name = 'promoapp/nouka2.html'

class Resipi1View(TemplateView):
    template_name = 'promoapp/resipi.html'

class Resipi2View(TemplateView):
    template_name = 'promoapp/resipi2.html'

class Resipi3View(TemplateView):
    template_name = 'promoapp/resipi3.html'

class Resipi4View(TemplateView):
    template_name = 'promoapp/resipi4.html'

class ServiceView(TemplateView):
    template_name = 'promoapp/service.html'