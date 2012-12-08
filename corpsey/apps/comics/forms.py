from django import forms

class UploadForm(forms.Form):
    panel1 = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    panel2 = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    panel3 = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    name = forms.CharField(
    	label='Your Name'
    )
    email = forms.CharField(
    	label='Your email'
    )
    website = forms.CharField(
    	label='Your website'
    )
