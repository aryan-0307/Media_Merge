from django import forms
from .models import MediaAsset

class MediaAssetForm(forms.ModelForm):
    class Meta:
        model = MediaAsset
        fields = [
            'title', 'description', 'media_type', 'category',
            'language', 'release_date', 'duration',
            'thumbnail', 'media_file', 'publication_status', 'is_premium'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
