from django import forms
from allauth.account.forms import SignupForm

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="姓")
    last_name = forms.CharField(max_length=30, label="名")
    email = forms.CharField(max_length=30, label="メールアドレス")
    postal_code = forms.CharField(max_length=7, label="郵便番号", required=False)
    address = forms.CharField(max_length=50, label="住所", required=False)
    tel_number = forms.CharField(max_length=15, label="電話番号", required=False)
    department = forms.CharField(max_length=30, label="所属", required=False)

class SignupUserForm(SignupForm):
    first_name = forms.CharField(max_length=30, label="姓")
    last_name = forms.CharField(max_length=30, label="名")
    postal_code = forms.CharField(max_length=7, label="郵便番号")
    address = forms.CharField(max_length=50, label="住所")
    tel_number = forms.CharField(max_length=15, label="電話番号")

    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.postal_code = self.cleaned_data['postal_code']
        user.address = self.cleaned_data['address']
        user.tel_number = self.cleaned_data['tel_number']
        user.save()
        return user