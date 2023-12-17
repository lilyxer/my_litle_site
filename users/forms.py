from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    """Наследумеся от стандартной 
    """
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password_2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model() # возврат текущей модели пользователя
        # поля отображаемые в поле
        fields = ['username', 'password', 'password_2', 'email', 'first_name', 'last_name']
        labels  = {'email': 'E-mail', 'first_name': 'Имя', 'last_name': 'Фамилия'}

    def clean_pswd(self):
        """ Валидатор, проверяет равны ли пароли """
        cd = self.cleaned_data
        if cd['password'] != cd['password_2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']
    
    def clean_email(self):
        """ Валидатор, проверяет почту в базе данных """
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Почтовый адрес не уникален')
        return email