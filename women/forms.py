from django import forms
from django.core.exceptions import ValidationError
from .models import *


class AddPostForm(forms.ModelForm):
    title = forms.CharField(max_length=25, label='Заголовок')
    # content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}),
    #                            label='Статья', required=False)
    # is_published = forms.BooleanField(label='Активность', initial=True, required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='без ктегорий',
                                 label='Категория')
    
    class Meta:
        model = Women
        fields = ['title', 'content', 'is_published', 'cat', 'photo', 'tags']  # поля которые будут отображаться для заполнения
        widgets = {
            # 'title': forms.TextInput(attr={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 21}),
        }
        labels = {'is_published': 'Активность'}

    def clean_title(self):
        """
        настройка валидатора
        """
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('не менее 5 симоволов')
        return title





























class NoModelAddPostForm(forms.Form):
    """
    поля формы должны быть идентичный полям модели
    Форма не связанная с моделью
    """
    title = forms.CharField(max_length=25, label='Заголовок')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20}),
                               label='Статья', required=False)
    is_published = forms.BooleanField(label='Активность', initial=True, required=False)
    # photo = forms.ImageField()
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='без ктегорий',
                                 label='Категория')
    # user = forms.IntegerField(queryset=User.objects.get(pk=1), disabled=True)
    # tags = forms.ModelChoiceField(queryset=TagWomen.objects.all(), empty_label='без тегов', 
                                #   label='Тэги', )
    # views.py -> def add_post:
    # if form.is_valid():
    #         try:
    #             Women.objects.create(**form.cleaned_data)
    #             return redirect('home')
    #         except Error as e:
    #             print(type(e), e)
    #             form.add_error(None, 'Ошибка добавления поста')