from django import forms
from .models import Report


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report

        fields = ['title', 'category', 'description', 'location']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # =========================
    # VALIDASI TAMBAHAN
    # =========================
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 5:
            raise forms.ValidationError("Judul minimal 5 karakter")
        return title

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if desc and len(desc) < 10:
            raise forms.ValidationError("Deskripsi minimal 10 karakter")
        return desc
