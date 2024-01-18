from django.urls import path
from app import views

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('item_list/', views.ItemListView.as_view(), name='item_list'),
    path('item_detail/<slug>', views.ItemDetailView.as_view(), name='item_detail'),
    path('additem/<slug>', views.addItem, name='additem'),
    path('order', views.OrderView.as_view(), name='order'),
    path('removeitem/<slug>', views.removeItem, name='removeitem'),
    path('removesingleitem/<slug>', views.removeSingleItem, name='removesingleitem'),
    path('removeallitem', views.removeAllItem, name='removeallitem'),
    path('payment/', views.PaymentView.as_view(), name='payment'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('contact_check/', views.ContactCheckView.as_view(), name='contact_check'),
    path('contact_save/', views.contactSave, name='contact_save'),
    path('contact_thanks/', views.ContactThanksView.as_view(), name='contact_thanks'),
    path('contact_comfirm/', views.ContactComfirmView.as_view(), name='contact_comfirm'),
    path('graph_index/', views.GraphIndexView.as_view(), name='graph_index'),
    path('graph_crop/', views.GraphView.as_view(), name='graph_crop'),
    path('graph_productor/', views.GraphProductorView.as_view(), name='graph_productor'),
    path('order_history', views.OrderHistoryView.as_view(), name='order_history'),

]
