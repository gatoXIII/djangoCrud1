from django import forms
from .models import Tarea

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields=['titulo','descripcion','importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'escribe un titulo de la tarea'}),
            'descripcion': forms.Textarea (attrs={'class': 'form-control', 'placeholder':'una descripcion de la tarea'}),
            'importante': forms.CheckboxInput (attrs={'class': 'form-check-input m-auto'})
        }
       
