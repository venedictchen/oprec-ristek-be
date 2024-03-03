from re import search
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.db.models import Sum
from django.contrib.auth.decorators import login_required


from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Items
import json
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

class UserItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Items.objects.filter(user=self.request.user.id)
    
    

@csrf_exempt
@api_view(['POST'])
def add_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = ItemSerializer(data=data)
        print(serializer.is_valid())
        if serializer.is_valid():
            item_type = serializer.validated_data['itemType']
            if item_type == 'income' or item_type == 'deposit':
                serializer.save(user=request.user)
                return Response(serializer.data)
            else:
                amount = serializer.validated_data['amount']
                if amount > 0:
                    serializer.save(user=request.user)
                    return Response(serializer.data)
                else:
                    return Response({
                        "error": "Invalid amount"
                    })      
        return Response(serializer.errors)
    return Response({
        "error": "Invalid request"
    })

@csrf_exempt
@api_view(['PUT'])
def update_item(request, pk):
    try:
        item = Items.objects.filter(user=request.user, id=pk)
        item = Items.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({
            "error": "Item not found"
        })
    if request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    return Response({
        "error": "Invalid request"
    })
    
@csrf_exempt
@api_view(['DELETE'])
def delete_item(request, pk):
    try:
        item = Items.objects.filter(user=request.user, id=pk)
        item = Items.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({
            "error": "Item not found"
        })
    if request.method == 'DELETE':
        item.delete()
        return Response({
            "message": "Item deleted"
        })
    return Response({
        "error": "Invalid request"
    })

@csrf_exempt
@api_view(['GET'])
def list_items(request):
    items = Items.objects.filter(user=request.user.id)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)