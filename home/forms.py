from django import forms


class UploadFileForm(forms.Form):
    name_file = forms.CharField(max_length=30)
    file = forms.FileField(widget=forms.FileInput)

