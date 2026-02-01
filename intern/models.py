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

