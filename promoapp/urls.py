from django.urls import path
from promoapp import views

urlpatterns  = [
    path('', views.IndexView.as_view(), name='promo_index'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('five/', views.FiveView.as_view(), name='five'),
    path('six/', views.SixView.as_view(), name='six'),
    path('seven/', views.SevenView.as_view(), name='seven'),
    path('eight/', views.EightView.as_view(), name='eight'),
    path('nine/', views.NineView.as_view(), name='nine'),
    path('ten/', views.TenView.as_view(), name='ten'),
    path('eleven/', views.ElevenView.as_view(), name='eleven'),
    path('twelve/', views.TwelveView.as_view(), name='twelve'),
    path('promo_contact/', views.ContactView.as_view(), name='promo_contact'),
    path('dining/', views.DiningView.as_view(), name='dining'),
    path('greeting/', views.GreetingView.as_view(), name='greeting'),
    path('index_en/', views.IndexEnView.as_view(), name='index_en'),
    path('nouka1/', views.Nouka1View.as_view(), name='nouka1'),
    path('nouka2/', views.Nouka2View.as_view(), name='nouka2'),
    path('resipi1/', views.Resipi1View.as_view(), name='resipi1'),
    path('resipi2/', views.Resipi2View.as_view(), name='resipi2'),
    path('resipi3/', views.Resipi3View.as_view(), name='resipi3'),
    path('resipi4/', views.Resipi4View.as_view(), name='resipi4'),
    path('service/', views.ServiceView.as_view(), name='service'),
]