from django import template
from women.models import Category, TagWomen

register = template.Library()


@register.simple_tag
def get_cat():
    """
    создаем простой тег, чтобы его использовать:
    {% load women_tags %} - подгружем теги на страницу
    {% get_cat %} если хотим вывести содержимое
    {% get_cat as gt %} если хотим использовать содержимое
    """
    return Category.objects.all()

@register.inclusion_tag('women/cat_list.html')
def show_cat(cat_selected=0):
    """
    создаем включающий тег, чтобы его использовать:
    порописывем маршрут до шаблона в который мы передаем словарь с содержимым
    в шаблоне работаем с содержимым
    расширяем наш базовый шаблон тем что выводится из первого шаблона
    {% show_cat %}
    cat_selected должна передаваться из вью функции, расширяемы шаблон 
    так же должен её передавать в начальный шаблон:
        {% show_cat cat_selected %}
    """
    return {'cats': Category.objects.all(), 'cat_selected': cat_selected}

@register.inclusion_tag('women/tag_list.html')
def show_tag(cat_selected=0):
    return {'tags': TagWomen.objects.all(), 'tag_selected': cat_selected}
