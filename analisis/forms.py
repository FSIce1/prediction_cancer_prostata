from django import forms
from analisis.models import AnalisisImagen

class AnalisisImagenForm(forms.ModelForm):

    class Meta:
        model  = AnalisisImagen
        fields = ["id", "titulo", "descripcion", "imagen"]

    dni = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Dni:", max_length=8)
    nombres = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Nombre:", max_length=150)
    apellidoMaterno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Apellido Materno:", max_length=150)
    apellidoPaterno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Apellido Paterno:", max_length=150)
    titulo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label = "Título:", max_length=150)
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), label = "Descripción:", max_length=100)
    imagen = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'imagen'}), required=False, label = "Imagen:")

