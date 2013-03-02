from django import forms

class UploadForm(forms.Form):
    panel1 = forms.FileField(label='Select jpg for panel 1')
    panel2 = forms.FileField(label='Select jpg for panel 2')
    panel3 = forms.FileField(label='Select jpg for panel 3')
    name = forms.CharField(label='Your Name')
    email = forms.CharField(label='Your email')
    website = forms.CharField(label='Your website', required=False)

class ContributeForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField()
    comic_id = forms.CharField()
