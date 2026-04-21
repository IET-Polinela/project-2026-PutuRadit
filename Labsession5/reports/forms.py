from django import forms
from .models import Report

class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'location']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul laporan'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategori laporan'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deskripsi laporan'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lokasi kejadian'
            }),
        }

    # VALIDASI TAMBAHAN
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Judul minimal 5 karakter")
        return title

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc) < 10:
            raise forms.ValidationError("Deskripsi minimal 10 karakter")
        return desc