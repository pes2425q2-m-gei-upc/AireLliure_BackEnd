from django.urls import path
from . import views

urlpatterns = [
    # Aquí irán tus URLs cuando las necesites
    
    # CATEGORIA
    path('categories/', views.get_categories, name='get_categories'),
    path('categories/<str:pk>/', views.get_category, name='get_category'),
    path('categories/<str:pk>/delete/', views.delete_category, name='delete_category'),
]
