from rest_framework import serializers
from .models import Employee,Department
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    #we will receive username hi ,password and grup name
    #at first take grup name and save in variable
    #remove it from list
    group_name = serializers.CharField(write_only=True,required=False)
    #write only means the field for input
    #function to create user
    def create(self,validated_data):
        group_name = validated_data.pop("group_name",None)
        #as part of security encrypt password aand save it
        validated_data['password'] = make_password(validated_data.get("password"))
        user = super(SignupSerializer,self).create(validated_data)
        if group_name:
          group,created= Group.objects.get_or_create(name=group_name)
          user.groups.add(group)
        return user
    class Meta:
        model = User
        fields = ['username','password','group_name']
class LoginSerializer(serializers.ModelSerializer):
    #creating custom field for username
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ('username','password')     
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('DepartmentID','DepartmentName')
        
        #add validation for employee name
def name_validation(employee_name):
    if len(employee_name)<3:
        raise serializers.ValidationError("name must atleast 3 chars")
    return employee_name

class EmployeeSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(source='DepartmentID',read_only=True)
    #add validation to employeename
    EmployeeName = serializers.CharField(max_length=200, validators=[name_validation])
    class Meta:
        model = Employee
        fields = ('EmployeeID','EmployeeName','Designation','DateOfJoining','IsActive','DepartmentID','Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')#get only two fields
