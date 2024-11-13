from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create (user=instance)


# Create your models here.
#create a department model by inhreriting the model class
class Department(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=200)

    def __str__(self):
        return self.DepartmentName
class Employee(models.Model):   
    EmployeeID = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=200)
    Designation = models.CharField(max_length=200)
    DateOfJoining = models.DateField()
    DepartmentID = models.ForeignKey(Department, on_delete=models.CASCADE)
    Contact = models.CharField(max_length=150)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.EmployeeName