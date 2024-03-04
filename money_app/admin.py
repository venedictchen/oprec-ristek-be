from django.contrib import admin
from .models import Category, Goals, Items,ProfileUser
# Register your models here.
admin.site.register(Category)
admin.site.register(Items)
admin.site.register(ProfileUser)
admin.site.register(Goals)