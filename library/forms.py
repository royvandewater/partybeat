from django import forms

class UploadForm(forms.Form):
    file = forms.FileField()
    enqueue = forms.BooleanField(required=False, initial=True)

class EditForm(forms.Form):
    name = forms.CharField(max_length=255, required=False)
    artist = forms.CharField(max_length=255, required=False)
    album = forms.CharField(max_length=255, required=False)
    track_number = forms.IntegerField(required=False)

    def clean_track_number(self):
        if not self.cleaned_data['track_number']:
            return 0
        else:
            return self.cleaned_data['track_number']
