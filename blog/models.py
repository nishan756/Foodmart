from django.db import models
from django_summernote.fields import SummernoteTextField
from django.utils.text import slugify
from django.core.exceptions import ValidationError



class BlogTag(models.Model):
    title = models.CharField(max_length = 20)

    def __str__(self):
        return self.title

    def clean(self):
        queryset = BlogTag.objects.filter(title__iexact = self.title)
        if self.pk:
            queryset = queryset.exclude(pk = self.pk)
        if queryset:
            raise ValidationError("Tag with this title is already exists")


class Blog(models.Model):
    title = models.CharField(max_length = 100)

    slug = models.SlugField(unique = True , blank = True , null = True)

    banner = models.ImageField(upload_to = "blog_image" , blank = True , null = True)

    short_description = models.TextField(max_length = 200)

    description = SummernoteTextField()

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self , *args , **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args , **kwargs)