from django.db import models
from django.db.models import Q

class Post(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)


result = Post.objects.filter(Q(slug__icontains='django') | Q(slug__icontains='python')).count()