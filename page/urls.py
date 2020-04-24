from django.urls import path
from . import views
app_name = 'page'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('page/<pk>', views.ShopList.as_view(), name='shoplist'),
    # path('', views.IndexView.as_view(), name='index'),
    path('page/<slug:slug>/', views.ShopTop.as_view(), name='shoptop'),
    # path('page/<uuid>/admin/', views.IndexView.as_view(), name='index'),
    path('page/<pk>/admin/create/', views.ShopCreateView.as_view(), name='shopcreate'),
    path('page/<pk>/<slug>/update/', views.ShopUpdateView.as_view(), name='shopupdate'),
    # path('page/<uuid>/admin/delete', views.IndexView.as_view(), name='index'),
]
