
class DataMixin:
    title_page = None
    paginate_by = 5
    extra_context = {}
 
    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
 
        # if 'menu' not in self.extra_context:
        #     self.extra_context['menu'] = SITE_MENU
 
    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
 
        # context['menu'] = SITE_MENU  # добавили его впользовательский тег, 
            # в идеале его грузить из БД, конктекстный процессор
        context['cat_selected'] = None
        context.update(kwargs)
        return context
    

SITE_MENU = (
    {'name': 'Главная страница', 'link': 'home'},
    {'name': 'О сайте', 'link': 'about'},
    {'name': 'Добавить статью', 'link': 'add_post'},
    {'name': 'Обратная связь', 'link': 'contact'},
    {'name': 'Войти', 'link': 'users:login'},
)