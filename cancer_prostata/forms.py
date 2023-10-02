from django import forms

class AnalisisImagenForm(forms.Form):
    titulo = forms.CharField(
        label = "Título:", 
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    descripcion = forms.CharField(
        label = "Descripción:",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    
    imagen = forms.CharField(
        label = "Imagen:",
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'imagen'})
    )

    # def clean_name(self):
    #     if titulo == "":
    #         raise forms.ValidationError("Tan solo el valor Open está permitido para este campo")
    #     else: 
    #         return titulo

