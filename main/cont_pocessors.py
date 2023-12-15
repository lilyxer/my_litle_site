def get_mainmenu(request):
    return {'mainmenu':
            (
                {'name': 'Главная страница', 'link': 'home'},
                {'name': 'О сайте', 'link': 'about'},
                {'name': 'Добавить статью', 'link': 'add_post'},
                {'name': 'Обратная связь', 'link': 'contact'},
 #               {'name': 'Войти', 'link': 'users:login'},
            )}