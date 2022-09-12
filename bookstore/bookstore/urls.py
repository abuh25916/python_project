
from django.contrib import admin
from django.urls import path
from app import views


urlpatterns = [
    path('', views.login),
    path('admin/', admin.site.urls),
    path('signup/', views.signup),
    path('login/', views.login),
    path('booklist/', views.booklist),
    path('addbooks/', views.addbooks),
    path('updatebook/<int:id>', views.updatebook),
    path('deleteBook/<int:id>', views.deleteBook),
    path('updatebookdb/<int:id>', views.updatebookdb),
]
