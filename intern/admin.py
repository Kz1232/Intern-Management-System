from django.contrib import admin
from .models import UserProfile,Task,Attendence
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','role']

admin.site.register(UserProfile,UserProfileAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display=['title','assigned_to','status']

admin.site.register(Task,TaskAdmin)

class AttendenceAdmin(admin.ModelAdmin):
    list_display=['user','date']
admin.site.register(Attendence,AttendenceAdmin)
