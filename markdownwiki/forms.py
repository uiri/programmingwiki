from django import forms

class PageForm(forms.Form):
    redirect = forms.BooleanField(required=False)
    pagecontent = forms.CharField(widget=forms.Textarea)
