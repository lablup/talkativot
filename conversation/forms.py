from django import forms
import uuid

class ConversationForm(forms.Form):
    message = forms.CharField(widget=forms.HiddenInput())
