from django.conf.urls import url, include
from django.contrib import admin

from blog import urls

from . import views

urlpatterns = [
    url(r'^$', views.Main.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'blog/', include('blog.urls', namespace='blog')),
    url(r'^logout$', views.Logout.as_view(), name='logout'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^oauth$', views.OAuth.as_view(), name='vk_auth'),
]
