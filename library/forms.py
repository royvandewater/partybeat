from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()

class EditForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    artist = forms.CharField(max_length=255, required=False)
    album = forms.CharField(max_length=255, required=False)
