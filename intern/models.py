from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    ROLES =(
        ("INTERN",'Intern'),
        ("SUPERVISOR","Supervisor")
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=20,choices=ROLES,null=False,blank=False)

    def __str__(self):
        return self.user.username
    
class Task(models.Model):
    STATUS_CHOICE=(
        ('COMP','Completed'),
        ('PEND','Pending'),
    )

    title = models.CharField(max_length=255)
    assigned_to =models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.CharField(choices=STATUS_CHOICE,max_length=20,default="PEND")
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at =models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.title
    

