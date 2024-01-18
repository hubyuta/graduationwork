from django import forms
from .models import Item, ContactModel
from django.forms import Textarea

class SearchForm(forms.Form):
    keyword = forms.CharField(label='Search', max_length=100)

# class ContactForm(forms.Form):
#     name = forms.CharField(required=True,max_length=30)
#     email = forms.EmailField(required=True)
#     subject = forms.CharField(max_length=30)
#     message = forms.CharField(required=True, min_length=10, max_length=500,widget=forms.Textarea)

#     def send_email(self):
#         pass

class SelectTermForm(forms.Form):
    term = forms.IntegerField(min_value=5, max_value=50)

class PriceChoiceForm(forms.Form):
    choice = forms.fields.ChoiceField(
        choices = (
            ('','選択価格以下'),
            ('1700', 1700),
            ('1850', 1850),
            ('2000', 2000)
        ),
        initial=[''],
        required=True,
        widget=forms.widgets.Select
    )

class ProductorChoiceForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Item.objects.all().values_list("title", flat=True).order_by("title").distinct(),
        to_field_name='title',
        empty_label="お米の品種を選んで下さい",
        widget=forms.widgets.Select,
    )

class ContactForm(forms.ModelForm):
    class Meta():
        model = ContactModel
        fields = ["name", "email", "product_name", "subject", "message"]
        widgets = {
            "message": Textarea(attrs={"cols": 80, "rows": 10}),
        }
        def send_email(self):
             pass