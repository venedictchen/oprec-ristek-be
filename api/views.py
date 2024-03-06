from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from money_app.models import ProfileUser
from money_app.forms import ProfileUserForm
import json
import re
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
# Create your views here.


@csrf_exempt
def login(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameters only'},status=400)

    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    print(data)
    if len(password) < 8:
        return JsonResponse({'error': 'Password needs to be at least 8 characters long',},status=400)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)

        profile_user = ProfileUser.objects.get(user=user)

        response_data = {
            'success': 'Login successful',
                'username': user.username,
                'user_id': user.id,
                'email': user.email,
                'balance': profile_user.balance,
                'income': profile_user.income,
                'expenses': profile_user.expenses,
                'last_transaction_amount': profile_user.last_transaction_amount,    
                'last_transaction_type': profile_user.last_transaction_type
        
        }

        return JsonResponse(response_data)
    else:
        print("masuksini")  
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

@csrf_exempt
def logout(request):
    username = request.user.username
    
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
@csrf_exempt
def register(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameter only'})

    data = json.loads(request.body)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        return JsonResponse({'error': 'Enter a valid email'}, status=400)

    if len(password) < 8:
        return JsonResponse({'error': 'Password needs to be at least 8 characters long'}, status=400)

    UserModel = get_user_model()
    
    if UserModel.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already taken'}, status=400)

    try:
        user = UserModel.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        ProfileUser.objects.create(user=user)
        return JsonResponse({'success': 'User created successfully'},status=201)
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid email'}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]

        except KeyError:
            return [permission() for permission in self.permission_classes]