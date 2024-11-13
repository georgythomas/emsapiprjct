from django.test import TestCase
from rest_framework.test import APITestCase,APIClient
from .models import Department,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer
from rest_framework import status

# Create your tests here.
#creating new employeeViewSet class inheriting the APITestCase cla
class EmployeeViewSetTest( APITestCase):
    #defining a fn to setup some basic data for testing 
    def setUp(self):
        #create a sample departmrnt
        self.department = Department.objects.create(DepartmentName="HR") 


#create a sample employee object and assign the departmrnt
        self.employee = Employee.objects.create(
            EmployeeName = "Jackie chan",
            Designation = "kungfu Master",
            DateOfJoining = date(2024,11,13),
            DepartmentId = self.department,
            Contact = "China",
            IsActive = True
         )
         #since we are testing API,we  need to create an APIClient object
        self.client = APIClient()
    
    #defining fn to test employee listing api/endpoint
    def test_employee_list(self):
        #the default reverse url for Listing modelname.list
        url = reverse('employee-list')
        response = self.client.get(url) #send the api and get the response
        #get all the  employee objects
        employees = Employee.objects.all()
        #create a serializer object from employserializer
        serializer = EmployeeSerializer(employees,many=True) #get all employ

        #check and compare the response against the setup data
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data)
    def test_employee_details(self):
        url = reverse('employee-detail',args=[self.employee.EmployeeID])
        response = self.client.get(url)
        serializer = EmployeeSerializer(self.employee)

        self.assertEqual(responsw.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data,serializer.data) 