from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Item, OrderItem, Order, Payment, ContactModel
from .forms import SearchForm, ContactForm, SelectTermForm, ProductorChoiceForm, PriceChoiceForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser
from .import graph
import stripe
from django.conf import settings
from django.core.paginator import Paginator

class IndexView(TemplateView):
    template_name = 'app/index.html'

class ItemListView(View):
    def get(self, request, *args, **kwargs):
        # item_data = Item.objects.all()

        searchform = SearchForm(request.GET or None)
        productorform = ProductorChoiceForm(request.GET or None)
        priceform = PriceChoiceForm(request.GET or None)
            
        if searchform.is_valid():
            keyword = searchform.cleaned_data['keyword']
            item_data = Item.objects.filter(description__contains=keyword)
        elif productorform.is_valid():
            keyword = productorform.cleaned_data['choice']
            item_data = Item.objects.filter(title=keyword)
        elif priceform.is_valid():
            price = priceform.cleaned_data['choice']
            item_data = Item.objects.filter(price__lte=price)
        else:
            searchform = SearchForm()
            item_data = Item.objects.all()
        
        item_data = item_data.order_by('id')
         #ページネーション用
        page = request.GET.get('page', 1)
        page_cnt = 12 #１画面当たりの表示数
        onEachSide = 3 #選択ページの両側の表示数
        onEnds = 2 #左右両端の表示数
        page_data = Paginator(item_data, page_cnt)
        page_obj = page_data.get_page(page)
        data_list = list(page_obj.paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds))
        return render(request, 'app/item_list.html', {
            # 'item_data' : item_data,
            'page_obj' : page_obj,
            'data_list' : data_list,
            'searchform' : searchform,
            'productorform' : productorform,
            'priceform' : priceform
        })

class ItemDetailView(View):
    def get(self, request, *args, **kwargs):
        item_data = Item.objects.get(slug=self.kwargs['slug'])
        qs = Item.objects.all()
        title = item_data.title
        mainx = item_data.xvalue
        mainy = item_data.yvalue
        subtitle = []
        x = [x.xvalue for x in qs]
        y = [y.yvalue for y in qs]
        for xs in qs:
            if xs.title not in subtitle:
                subtitle.append(xs.title)
        # subtitle = [x.title for x in qs]
        chart = graph.Plot_Graph(mainx, mainy, x, y, title, subtitle)
        return render(request, 'app/item_detail.html', {
            'item_data' : item_data,
            'chart' : chart,
        })

class ContactFormView(LoginRequiredMixin, FormView):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        data = {
            'name' : user_data.first_name + " " + user_data.last_name,
            'email' : user_data.email,
        }
        form = ContactForm(data, request.POST or None)
        return render(request, 'app/contact.html', {
            'form' : form,
        })

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ContactForm(request.POST or None)
            if form.is_valid():
                form.save(commit=False)
            return render(request, 'app/contact_check.html')
        
        form = ContactForm(request.POST or None)
    
        return render(request, 'app/contact.html')
    
class ContactCheckView(LoginRequiredMixin, FormView):    
    def get(self, request, *args, **kwargs):
        return render(request, 'app/contact.html')
        
    def post(self, request, *args, **kwargs):
        if (request.method == 'POST'):
            form = ContactForm(request.POST or None)
            return render(request, 'app/contact_check.html', {
            'form' : form
        })

        return render(request, 'app/contact.html')        

@login_required
def contactSave(request, *args, **kwargs):
    user_data = CustomUser.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        form = ContactForm(request.POST or None)    
        if form.is_valid():
            form.save()
            return render(request, 'app/contact_thanks.html', {
                'user_data' : user_data
            })
        
    return redirect('contact')

    
class ContactThanksView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/contact_thanks.html')

class ContactComfirmView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        objs = ContactModel.objects.all()
        objs = objs.order_by('id').reverse()
        # objs = sorted(objs, key=lambda x : x.id, reverse = True)

        #ページネーション用
        page = request.GET.get('page', 1)
        page_cnt = 5 #１画面当たりの表示数
        onEachSide = 3 #選択ページの両側の表示数
        onEnds = 2 #左右両端の表示数
        page_data = Paginator(objs, page_cnt)
        page_obj = page_data.get_page(page)
        data_list = list(page_obj.paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds))
        return render(request, 'app/contact_comfirm.html', {'objs' : objs, 'page_obj' : page_obj, 'data_list' : data_list})

class OrderHistoryView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        orders = Order.objects.filter(ordered=True).all().select_related()
        orders = orders.order_by('id').reverse()
        
        #ページネーション用
        page = request.GET.get('page', 1)
        page_cnt = 5 #１画面当たりの表示数
        onEachSide = 3 #選択ページの両側の表示数
        onEnds = 2 #左右両端の表示数
        page_data = Paginator(orders, page_cnt)
        page_obj = page_data.get_page(page)
        data_list = list(page_obj.paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds))
        return render(request, 'app/order_history.html', {'user_data' : user_data , 'page_obj' : page_obj, 'data_list' : data_list})

class GraphIndexView(TemplateView):
    template_name = "app/graph_index.html"

class GraphView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = SelectTermForm
        term = request.GET.get("term", 30)
        chart1 = graph.Crop_Condition_Graph(term)
        context = {
                    'chart1' : chart1, 
                    'form' : form,
                  }    
        return render(request, 'app/graph_crop.html', context)

class GraphProductorView(TemplateView):
    def get(self, request, *args, **kwargs):
        chart1 = graph.Productor_Statistics_Graph()[0]
        chart2 = graph.Productor_Statistics_Graph()[1]
        context = {
                'chart1' : chart1, 
                'chart2' : chart2, 
              }    
        return render(request, 'app/graph_productor.html', context)

@login_required #ログインしている時のみコールするアノテーション
def addItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item = item,
        user = request.user,
        ordered = False
    )
    order = Order.objects.filter(user=request.user, ordered=False) #オーダーモデルからログインユーザーの未オーダーデータを取得

    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user, ordered_date=timezone.now())
        order.items.add(order_item)

    return redirect('order')

class OrderView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            context = {
                'order' : order
            }
            return render(request, 'app/order.html', context)
        except ObjectDoesNotExist:
            return render(request, 'app/order.html')
        
@login_required
def removeItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            return redirect('order')
        
    return redirect('product', slug=slug)

@login_required
def removeSingleItem(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order.exists():
        order = order[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect('order')
        
    return redirect('product', slug=slug)

@login_required
def removeAllItem(request):
    order = Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order.exists():
        order = order[0]
        item = OrderItem.objects.all()       
        if order.items.exists():
            order.items.remove()
            item.delete()
            return redirect('order')
        
    return redirect('item_list')

class PaymentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(user=request.user, ordered=False)
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {
            'order' : order,
            'user_data' : user_data
        }
        return render(request, 'app/payment.html', context)
    
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order = Order.objects.get(user=request.user, ordered=False)
        token = request.POST.get('stripeToken')
        order_items = order.items.all()
        amount = order.get_total()
        item_list = []
        for order_item in order_items:
            item_list.append(str(order_item.item) + ':' + str(order_item.quantity))
        description = ' '.join(item_list)

        charge = stripe.Charge.create(
            amount = amount,
            currency = 'jpy',
            description = description,
            source = token,
        )

        payment = Payment(user=request.user)
        payment.stripe_charge_id = charge['id']
        payment.amount = amount
        payment.save()

        order_items.update(ordered=True)
        for item in order_items:
            item.save()

        order.ordered = True
        order.payment = payment
        order.save()
        return redirect('thanks')

class ThanksView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = CustomUser.objects.get(id=request.user.id)
        context = {
            'user_data' : user_data,
        }
        return render(request, 'app/thanks.html', context)