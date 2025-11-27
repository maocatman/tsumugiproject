from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label="件名")
    message = forms.CharField(widget=forms.Textarea, label="内容")
