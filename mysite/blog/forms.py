from django import forms
from .models import Tag
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image', 'tags')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название поста'}),
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Текст поста'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})

        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('Нельзя создать Тег ' + new_slug)
            return new_slug


class TagsForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('title', 'slug')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название Тега'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Описание Тега'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Нельзя создать Тег ' + new_slug)

        if Tag.objects.filter(slug=new_slug).count():
            raise ValidationError('Тег ' + new_slug + ' уже сужествует')

        return new_slug

