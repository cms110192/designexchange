from django import forms

class MessageForm(forms.Form):
    recipient = forms.CharField(max_length=255)
    title = forms.CharField()
    content = forms.CharField()

class MethodForm(forms.Form):
    title = forms.CharField(max_length=255)
    purpose = forms.CharField()
    procedure = forms.CharField()
    principles = forms.CharField()
