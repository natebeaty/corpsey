from django import forms

class UploadForm(forms.Form):
    comic_panels = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    name = forms.CharField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Corpsey Infinitus'}))
    email = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'corpsey@aol.com'}))
    website = forms.CharField(label='Your website', required=False, widget=forms.TextInput(attrs={'placeholder': 'corpsey.trubble.club'}))

class ContributeForm(forms.Form):
    email = forms.EmailField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Corpsey Infinitus', 'class': 'email required'}))
    name = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'corpsey@aol.com', 'class': 'required'}))
    comic_id = forms.CharField()
