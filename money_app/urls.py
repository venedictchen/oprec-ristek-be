from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'user-item', views.UserItemViewSet, basename='user-item')


urlpatterns = [
    path('', include(router.urls)),
    path('add-item/', views.add_item, name='add-item'),
    path('update-item/<int:pk>/', views.update_item, name='update-item'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete-item'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    
]
