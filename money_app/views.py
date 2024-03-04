

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Goals, Items, ProfileUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

class UserItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Items.objects.filter(user=self.request.user.id)
    
@csrf_exempt
@api_view(['POST'])
def add_item(request):
    if request.method == 'POST':
       
        serializer = ItemSerializer(data=request.data)
        profile = ProfileUser.objects.get(user=request.user)
        amount = int(request.data['amount'])
        if serializer.is_valid():
            serializer.save(user=request.user)
            if request.data['itemType'] == 'income':
                profile.balance += amount
                profile.income += amount
            elif request.data['itemType'] == 'expense':
                profile.balance -= amount
                profile.expenses += amount
            elif request.data['itemType'] == 'deposit':
                profile.balance += amount
            profile.save()
            return Response(serializer.data)
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

@login_required
@api_view(['GET'])
def user_dashboard(request):
    profile = ProfileUser.objects.get(user=request.user)
    return Response({
        "username": request.user.username,
        "user_id": request.user.id,
        "email": request.user.email,
        "balance": profile.balance,
        "income": profile.income,
        "expenses": profile.expenses,
    })
    
@csrf_exempt
@api_view(['POST'])
def user_goals(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        user = request.user
        goal = Goals(title=title, description=description, amount=amount, user=user)
        goal.save()
        return Response({
            "message": "Goal added"
        })
    return Response({
        "error": "Invalid request"
    })
    
@csrf_exempt
@api_view(['GET'])
def list_goals(request):
    goals = Goals.objects.filter(user=request.user.id)
    return Response({
        "goals": goals
    })