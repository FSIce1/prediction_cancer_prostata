from django import forms
from analisis.models import AnalisisImagen

class AnalisisImagenForm(forms.ModelForm):

    class Meta:
        model  = AnalisisImagen
        fields = ["id", "titulo", "descripcion", "imagen"]

    titulo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Título:", max_length=150)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label = "Descripción:", max_length=100)
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'imagen'}), required=False, label = "Imagen:")

