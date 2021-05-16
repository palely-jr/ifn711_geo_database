from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Please Choose a File For Upload')
