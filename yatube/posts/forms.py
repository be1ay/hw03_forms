from .models import Post
from django.forms import ValidationError, ModelForm


class PostForm(ModelForm):
    class Meta():
        model = Post
        fields = ('text', 'group')

    def clean_text(self):
        data = self.cleaned_data['text']
        if len(data) == 0:
            raise ValidationError('Обязательное поле')
        return data
