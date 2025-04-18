from django import forms

class UploadForm(forms.Form):
    comic_panels = forms.FileField(widget=forms.ClearableFileInput(), required=False)
    name = forms.CharField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Corpsey Infinitus'}))
    email = forms.CharField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'corpsey@aol.com'}))
    website = forms.CharField(label='Your website', required=False, widget=forms.TextInput(attrs={'placeholder': 'corpsey.trubble.club'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comic_panels"].widget.attrs.update({"multiple": "true"})

class ContributeForm(forms.Form):
    name = forms.CharField(label='Your name', widget=forms.TextInput(attrs={'placeholder': 'Corpsey Infinitus', 'class': 'required'}))
    email = forms.EmailField(label='Your email', widget=forms.TextInput(attrs={'placeholder': 'corpsey@aol.com', 'class': 'email required'}))
    comic_id = forms.CharField()
