from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.views import generic

from .models import *
from .forms import *
from .utils import *


def index(request: HttpRequest):
    page = 'women/index.html'
    pagi = Paginator(Women.published.all().select_related('cat'), 5)
    page_num = int((request.GET.get('page', 1)))
    pages = pagi.get_page(page_num)
    content = {
        'menu': SITE_MENU,
        'data': pages, 
        'cat_selected': 0,
        'title': 'Главная страница',
    }
    return render(request=request, template_name=page, context=content)


class OldIndex(generic.TemplateView):
    """базовый класс наследования"""
    template_name = 'women/index.html'
    extra_context = {
        'menu': SITE_MENU,
        # 'data': pages, 
        'cat_selected': 0,
        'title': 'Главная страница',
    }
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        pagi = Paginator(Women.published.all().select_related('cat'), 5)
        page_num = int((self.request.GET.get('page', 1)))
        pages = pagi.get_page(page_num)
        context['data'] = pages
        return context


class Index(DataMixin, generic.ListView):
    """создан для работы со списочными данными возвращает object_list"""
    # context_object_name = 'data' <==> object_list
    template_name = 'women/index.html'
    # model=Women
    queryset = Women.published.all().select_related('cat')
    # paginate_by = 5     # работаем с page_obj / paginator
    title_page = 'Главная страница'  # DataMixin
    # extra_context = {             # определены в DataMixin    #     'menu': SITE_MENU,    #     'cat_selected': 0,    #     'title': 'Главная страница',    # }


def about(request: HttpRequest):
    page = 'women/about.html'
    content = {
        'menu': SITE_MENU,
        'title': 'О сайте',
    }
    return render(request=request, template_name=page, context=content)


def handle_uploaded_file(file):
    """
    запись файла по частям
    """
    with open(f"photos/{file.name}", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def add_post(request: HttpRequest):
    page = 'women/add_post.html'
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else: 
        form = AddPostForm()
    content = {
        'menu': SITE_MENU,
        'title': 'Добавить пост',
        'form': form,
    }
    return render(request=request, template_name=page, context=content)


class AddPost(DataMixin, generic.FormView):
    """Для с формами возращает form
    если используем CreateView:
    form_class + fields <==> model
    - form_valid
    """
    form_class = AddPostForm
    template_name = 'women/add_post.html'
    success_url = reverse_lazy('home')   # отложенное формирование марщрута
    title_page = 'Добавить пост'  # DataMixin

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdatePost(DataMixin, generic.UpdateView):
    model = Women
    fields = ['content', 'is_published', 'photo', 'cat', 'tags']
    template_name = 'women/add_post.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование поста'  # DataMixin


class DeletePost(DataMixin, generic.DeleteView):
    model = Women
    template_name = 'women/del_post.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление поста'  # DataMixin


def contact(request: HttpRequest):
    page = 'women/contact.html'
    content = {
        'menu': SITE_MENU,
        'title': 'Главная страница',
    }
    return HttpResponse('страница с контсактами')


def login(request: HttpRequest):
    page = 'women/login.html'
    content = {
        'menu': SITE_MENU,
        'title': 'Главная страница',
    }
    return HttpResponse('страница авторизации')


def post(request: HttpRequest, w_slug: str):
    post = get_object_or_404(Women, slug=w_slug)  # вернет 1 экз модели либо ошибку
    tags = post.tags.all()
    page = 'women/post.html'
    content = {
        'menu': SITE_MENU,
        'title': post.title,
        'post': post,
        'cat_selected': 0,
        'tags': tags
    }
    return render(request=request, template_name=page, context=content)


class Post(DataMixin, generic.DetailView):
    """Для выбора экземпляра по пк или слаг возращает object"""
    # model = Women
    template_name = 'women/post.html'
    context_object_name = 'post'  # только изза того что оно так отображается в хтмл
    slug_url_kwarg = 'w_slug' # or pk_url_kwarg
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title_page = context['object'].title
        cat_selected = context['post'].cat.id
        tags = Women.published.get(slug=self.kwargs[self.slug_url_kwarg]).tags.all()
        return self.get_mixin_context(context, title = title_page,
                                      cat_selected=cat_selected, tags=tags)
        # ^ mixin        # context.update({        #     'menu': SITE_MENU,        #     'title': context['object'].title,   # == 'post'        #     'cat_selected': context['post'].cat.id,        #     'tags': Women.published.get(slug=self.kwargs[self.slug_url_kwarg]).tags.all()        # })        # return context
    
    def get_object(self):
        """критерий отбора объекта, модель можно убрать"""
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def category(request: HttpRequest, c_slug: str):
    page = 'women/index.html'
    category = get_object_or_404(Category, slug=c_slug)   # я бы оставил Women.objects.select_related('cat').filter(cat=pk)
    data = Women.published.filter(cat=category.id).select_related('cat') # select_related('cat') join табличку чтобы ORM не делала доп запросы 
    pagi = Paginator(data, 5)
    page_num = int((request.GET.get('page', 1)))
    pages = pagi.get_page(page_num)
    content = {
        'menu': SITE_MENU,
        'data': pages,          # data =? page_obj
        'cat_selected': category.pk,
        'title': category.name,
        # 'title': data[0].cat.name  # Category.objects.get(pk=pk).name,
    }
    return render(request=request, template_name=page, context=content)

class Category(DataMixin, generic.ListView):
    template_name = 'women/index.html'
    # context_object_name = 'data'
    # paginate_by = 5
    allow_empty = False         # если стучимся по несуществующей ссылке - получим 404

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['c_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['object_list'][0].cat
        return self.get_mixin_context(context, title = category.name,
                                      cat_selected=category.id)

    # def get_context_data(self, **kwargs):  # DataMixin^    #     context = super().get_context_data(**kwargs)    #     category = context['object_list'][0].cat    #     context.update({    #         'cat_selected': category.id,    #         'title': category.name    #     })    #     return context


def tag(request: HttpRequest, t_slug: str):
    page = 'women/index.html'
    my_tag = get_object_or_404(TagWomen, slug=t_slug)
    data = my_tag.womens.filter(is_published=Women.Status.PUBLISHED).select_related('cat')#.prefetch_related('tags')
    pagi = Paginator(data, 5)
    page_num = int((request.GET.get('page', 1)))
    pages = pagi.get_page(page_num)
    content = {
        'menu': SITE_MENU,
        'data': pages, 
        # 'cat_selected': None,
        'title': my_tag.title,
    }
    return render(request=request, template_name=page, context=content)


class Tag(DataMixin, generic.ListView):
    template_name = 'women/index.html'
    # paginate_by = 5
    # extra_context = {'menu': SITE_MENU}
    allow_empty = False 

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['t_slug']).select_related('cat')#.prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagWomen.objects.get(slug=self.kwargs['t_slug'])
        return self.get_mixin_context(context, title=tag.title, tag_selected=tag.id)
        # context.update({        #     'title': TagWomen.objects.get(slug=self.kwargs['t_slug'])        # })        # return context


def page_not_found(request: HttpRequest, exception):
    """
    выводим представление при 404 (raise Http404())
    """
    return HttpResponseNotFound('Page not found')