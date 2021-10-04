from django import forms

class ContactForm(forms.Form):
    from_email = forms.EmailField(label='Email', required=True)
    subject = forms.CharField(max_length=255, label='Тема', required=True)
    message = forms.CharField(max_length=500, label='Сообщение', widget=forms.Textarea, required=True)