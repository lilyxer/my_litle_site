from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import *


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    # fields = ['отображаемые поля в админке!!!']
    # exclude = ['поля которые не будут отображаться в админек']
    # readonly_fields = ['поля которые нельзя редактировать в админке']
    # prepopulated_fields = {'slug': ('title', )}           #поле slug будет заполняться автоматически от поля title. 
    # поле должно быть редактируемым, альтернатива save() в models
    list_display = ['id', 'title', 'prev', 'is_published', 'info'] # что видим в админке
    list_display_links = ['id', 'title']                          # какая ссылка активна
    search_fields = ['title']                               # поиск по полям
    list_filter = ['time_create', 'cat_id']                 # фильтр по полям
    readonly_fields = ['slug',]                             # атрибут доступный для чтения
    list_per_page = 10                                      # пагинация
    actions = ['set_published', 'set_draft']                # устанавливаем пользовательские действия
    ordering = ['-id']
    save_on_top = True                                      # кнопка save и сверху

    
    @admin.display(description='Бесполезная инфа')
    def info(self, women: Women):
        """Добавление пользовательского столбца в админку"""
        return f'{len(women.content)} символов.' # {women.tags__title}'
    
    @admin.display(description='превью')
    def prev(self, women: Women):
        """Добавление пользовательского столбца в админку
        превью авы"""
        if women.photo:
            return mark_safe(f'<img src="{women.photo.url}" width=50>')
        return 'Без фото'

    @admin.action(description='Установить флаг Опубликовано')
    def set_published(self, request, queryset):
        queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, 'записи изменены', messages.SUCCESS)

    @admin.action(description='Установить флаг Черновик')
    def set_draft(self, request, queryset):
        queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, 'записи изменены', messages.WARNING)

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TagWomen)
class TagWomenAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

