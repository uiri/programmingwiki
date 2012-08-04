from django import forms

class PageForm(forms.Form):
    redirect = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'onclick' : 'changePagecontentWidget();'}))
    pagecontent = forms.CharField(widget=forms.Textarea)
