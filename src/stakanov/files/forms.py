from django import forms

class FolderSelectionForm(forms.Form):
    folder = forms.CharField(max_length=512, widget=forms.TextInput(attrs={'placeholder': 'Введите путь к папке'}))
