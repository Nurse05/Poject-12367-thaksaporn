from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='ชื่อ-นามสกุล')
    address = forms.CharField(widget=forms.Textarea, label='ที่อยู่สำหรับจัดส่ง')
    phone_number = forms.CharField(max_length=15, label='เบอร์โทร')
