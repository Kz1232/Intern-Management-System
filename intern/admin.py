from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoAdmin
from django.contrib.auth.models import User
from .models import UserProfile,Task,Attendence
# Register your models here.

class UserAdmin(DjangoAdmin):
    list_display=('id','username')
    list_display_links = ('username',)
    search_fields = ('username','email','first_name','last_name')

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','role']
    list_display_links=['user']

admin.site.register(UserProfile,UserProfileAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display=['id','title','assigned_to','status']

admin.site.register(Task,TaskAdmin)

class AttendenceAdmin(admin.ModelAdmin):
    list_display=['user','date']
admin.site.register(Attendence,AttendenceAdmin)
