from django import forms

class UploadForm(forms.Form):
    panel1 = forms.FileField(label='Select jpg for panel 1')
    panel2 = forms.FileField(label='Select jpg for panel 2')
    panel3 = forms.FileField(label='Select jpg for panel 3')
    name = forms.CharField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'Your email'}))
    website = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'Your email'}))

class ContributeForm(forms.Form):
    email = forms.EmailField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Your email', 'class': 'email required'}))
    name = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'Your name', 'class': 'required'}))
    comic_id = forms.CharField()
