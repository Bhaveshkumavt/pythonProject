from django.contrib import admin
# from app1.models import Notice, Profile
from .models import Profile, Contact, Category
from django.contrib.admin.options import ModelAdmin

# Register your models here.

class UserProfile(ModelAdmin):
    list_display = ['name', 'gender', 'age']
    search_fields = ['name', 'gender', 'age']
    list_filter = ['age']


admin.site.register(Profile, UserProfile)

admin.site.register(Contact)

class CategoryAdmin(ModelAdmin):
    list_display = ['C_name', 'C_disc']
    search_fields = ['C_name']

admin.site.register(Category, CategoryAdmin)
