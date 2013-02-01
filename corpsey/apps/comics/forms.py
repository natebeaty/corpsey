from django import forms

class UploadForm(forms.Form):
    panel1 = forms.FileField(
        label='Select jpg for panel 1',
        # help_text='max. 42 megabytes'
    )
    panel2 = forms.FileField(
        label='Select jpg for panel 2',
        # help_text='max. 42 megabytes'
    )
    panel3 = forms.FileField(
        label='Select jpg for panel 3',
        # help_text='max. 42 megabytes'
    )
    # parent_id = forms.CharField(
    #     required=False
    # )
    name = forms.CharField(
        label='Your Name'
    )
    email = forms.CharField(
        label='Your email'
    )
    website = forms.CharField(
        label='Your website',
        required=False
    )
