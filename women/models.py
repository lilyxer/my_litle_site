from django.db import models
from django.db.models.query import QuerySet
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

"""
https://docs.djangoproject.com/en/4.2/topics/db/models/
https://docs.djangoproject.com/en/4.2/ref/models/instances/
"""

class MyManager(models.Manager):
    """
    создаем кастомного менеджера (аналог objects)
    переопределяем queryset из которого сможем пеализовывать 
    остальные методы get, all, filter...
    """
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=True)


class Women(models.Model):
    class Status(models.IntegerChoices):
        """
        класс перечислений
        is_published = models.BooleanField(choices=Status.choices, 
                                           default=Status.DRAFT)
        Status.choices - [(0, 'Черновик'), (1, 'Опубликовано')]
        Status.values - [0, 1]
        Status.labels - ['Черновик', 'Опубликовано']
        """
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, 
                            verbose_name='Cлаг')  # primary_key=True, 
    content = models.TextField(blank=True, verbose_name='Содержание')
    time_create = models.DateTimeField(auto_now_add=True, 
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, 
                                       verbose_name='Дата обновление')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)), default=Status.PUBLISHED, 
                                       verbose_name='Статус')
    photo = models.ImageField(upload_to='photos/', default=None, blank=True, null=True,
                              verbose_name='Фотография') #   default='photos/default.png')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, 
                            default=1, verbose_name='Категория', related_name='womens')
                            # related_name <==> cat_set
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, 
                             verbose_name='Пользователь')
    tags = models.ManyToManyField('TagWomen', blank=True, related_name='womens')
    objects = models.Manager()      # если хотим оставить и основной менеджер и подключить кастомный
    published = MyManager()         # подключаем кастомный теперь можем обращаться Women.published.all()

    def save(self, *args, **kwargs):
        """
        есди мы не зададим слаг он автоматически возьмётся из титула
        """
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', kwargs={'w_slug': self.slug})
    
    class Meta:
        verbose_name = 'Девушка'
        verbose_name_plural = 'Женщины'
        ordering = ['title']


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.CharField(max_length=5, blank=True)
    # womens создается под капотом по названию от связанного класса по related_name
    # если имя не задано: <class>_set

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'c_slug': self.slug})
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

class TagWomen(models.Model):
    title = models.CharField(max_length=10)
    slug = models.SlugField(max_length=5, unique=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse('tag', kwargs={'t_slug': self.slug})
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тэги'
        ordering = ['title']