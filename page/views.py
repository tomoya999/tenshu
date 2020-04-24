from django.views.generic import DetailView, ListView, CreateView, UpdateView, TemplateView
from django.shortcuts import get_object_or_404, render
from .models import Shop
from .forms import ShopForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(TemplateView):
    template_name = 'page/index.html'

class ShopTop(DetailView):
    model = Shop
    template_name = 'page/shop.html'

class ShopList(LoginRequiredMixin, ListView):
    model = Shop
    template_name = 'page/shoplist.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user_list'] = User.objects.all()
        return context

class ShopCreateView(LoginRequiredMixin, CreateView):
    form_class = ShopForm
    template_name = 'page/shopcreate.html'
    success_url = '/account/'

    def form_valid(self, form):
        """ Youtube Twitter URL ウィジェット用に変換 """
        form.instance.created_by = self.request.user
        form.instance.user_id = self.request.user.id
        form.instance.youtube_url = form.instance.youtube_url.replace('https://www.youtube.com/watch?v=', 'https://www.youtube.com/embed/')
        form.instance.twitter_url = 'https://twitter.com/' + form.instance.twitter_id + '?ref_src=twsrc%5Etfw'
        return super().form_valid(form)

class ShopUpdateView(LoginRequiredMixin, UpdateView):
    """ 更新 """
    model = Shop
    form_class = ShopForm
    template_name = 'page/shopupdate.html'
    success_url = '/account/'