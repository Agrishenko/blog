from django.db import models
from django.utils import timezone
from django.shortcuts import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=u"Автор")
    title = models.CharField(max_length=200, verbose_name=u"Название")
    text = models.TextField(verbose_name=u"Текст")
    image = models.ImageField(upload_to='media', verbose_name=u"Изображение")
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts', verbose_name=u"Теги")
    created_date = models.DateTimeField(
            default=timezone.now, verbose_name=u"Дата создания")
    published_date = models.DateTimeField(
            blank=True, null=True, verbose_name=u"Дата публикации")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_edit_url(self):
        return reverse('post_edit', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('post_create_url')

    class Meta:
        ordering = ['-published_date']

class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name=u"Название тега")
    slug = models.SlugField(max_length=50, unique=True, verbose_name=u"Текст")

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'pk': self.pk})

    def get_edit_url(self):
        return reverse('tag_edit_url', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('tag_create_url')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']