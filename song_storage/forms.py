from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()

class EditForm(forms.Form):
    name = forms.CharField(max_length=255)
    artist = forms.CharField(max_length=255)
    album = forms.CharField(max_length=255)
