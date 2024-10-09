from django.contrib import admin
from django.urls import path
from ..app.views import signup_view, login_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
]
