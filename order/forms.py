from django import forms 


class CheckOutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    phone_number = forms.CharField(max_length=20)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10)
    address = forms.CharField(widget=forms.Textarea)