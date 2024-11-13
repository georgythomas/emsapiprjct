from django.shortcuts import render
from rest_framework import viewsets
from .models import Employee,Department
from django .contrib.auth.models import User
from .serializers import EmployeeSerializer,DepartmentSerializer,UserSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token,created = Token.objects.get_or_create(user=user)
            return Response({
            "user_id":user.id,
            "username":user.username,
            "token":token.key,
            "role":user.groups.all()[0].id if user.groups.exists() else None                #give back the first group id of the user if role/group exists
           },status=status.HTTP_201_CREATED)
        else:
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors} 
            return Response(response,status=status.HTTP_400_BAD_REQUEST)  
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password =   serializer.validated_data["password"]
            #if successfully authenticated
            user = authenticate(request,username=username,password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response ={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token":token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_401_UNAUTHORIZED,
                    "message":"invalid username or password",

                }   
                return Response(response,status=status.HTTP_401_UNAUTHORIZEDACCESS) 
        else:
             response ={"status":status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
             return Response(response,status=status.HTTP_400_BAD_REQUEST)
        
    


# Create your views here.
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []
        #permission classes =[IsAuthenticated] #to restrict for login user

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #add search option
    filter_backends = [filters.SearchFilter]
    search_fields = ['EmployeeName','Designation']
    permission_classes = []

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_class=[IsAuthenticated]