from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({
        "users/": "list users",
        "users/": "POST JSON request to create new user",
        "users/login/": "user login",
        "users/logout/": "user logout",
        "users/<int:id>/": "PUT request to update name of a user",
        "items/list/": 'list of all items',
        "items/user-item/": 'list of all items of current user',
        "items/add-item/": 'add an item',
        "items/update-item/<int:id>/": 'update an item',
        "items/delete-item/<int:id>/": 'delete an item',
    })