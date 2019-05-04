from django import forms

class KataForm(forms.Form):
    kata = forms.CharField(widget=forms.Textarea, label='', required=False)

class KalimatForm(forms.Form):
    kalimat = forms.CharField(widget=forms.Textarea, label='', required=False)