

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .serializers import ItemSerializer
from .models import Goals, Items, ProfileUser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
        profile = ProfileUser.objects.get(user=request.data['user'])
        amount = int(request.data['amount'])
        user_id = int(request.data['user'])
        if serializer.is_valid():
            serializer.save(user=User.objects.get(id=user_id))
            if request.data['itemType'] == 'income':
                profile.balance += amount
                profile.income += amount
                profile.last_transaction_amount = amount
                profile.last_transaction_type = 'income'
            elif request.data['itemType'] == 'expense':
                profile.balance -= amount
                profile.expenses += amount
                profile.last_transaction_amount = amount
                profile.last_transaction_type = 'expense'
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
def list_items(request,pk):
    items = Items.objects.filter(user=pk)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_dashboard(request,pk):
    print("masuk")
    profile = ProfileUser.objects.get(user=pk)
    user = User.objects.get(id=pk)
    return Response({
        "username": user.username,
        "user_id": user.id,
        "email": user.email,
        "balance": profile.balance,
        "income": profile.income,
        "expenses": profile.expenses,
        "last_transaction_amount": profile.last_transaction_amount,
        "last_transaction_type": profile.last_transaction_type
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

@csrf_exempt
@api_view(['DELETE'])
def delete_goal(request, pk):
    try:
        goal = Goals.objects.filter(user=request.user, id=pk)
        goal = Goals.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({
            "error": "Goal not found"
        })
    if request.method == 'DELETE':
        goal.delete()
        return Response({
            "message": "Goal deleted"
        })
    return Response({
        "error": "Invalid request"
    })

@csrf_exempt
@api_view(['PUT'])
def update_goal(request, pk):
    try:
        goal = Goals.objects.filter(user=request.user, id=pk)
        goal = Goals.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({
            "error": "Goal not found"
        })
    if request.method == 'PUT':
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        goal.title = title
        goal.description = description
        goal.amount = amount
        goal.save()
        return Response({
            "message": "Goal updated"
        })
    return Response({
        "error": "Invalid request"
    })