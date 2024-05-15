from rest_framework import status
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser,Profile , Employer_Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login 
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from .models import Employer_Profile
import json
from rest_framework.generics import DestroyAPIView
from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserUpdateSerializer,EmployerProfileSerializer ,PostSerializer
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            auth_login(request, user) 
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'gender': user.gender, 
                'contact_number': user.contact_number, 
            }
            refresh = RefreshToken.for_user(user)
            response_data = {
                'success': True,
                'message': 'Login successful',
                'user_data': user_data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'Code': status.HTTP_200_OK}
            #return render(request,'dashboard.html')
            
            return JsonResponse(response_data)
        else:
            response_data = {
                'success': False,
                'message': 'Invalid credentials',
            }
            return JsonResponse(response_data,status=status.HTTP_404_NOT_FOUND)
    else:
        response_data = {
            'message': 'Please use POST method for login',
        }
        return render(request, 'login.html')



class PostViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = PostSerializer

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username')
            email = data.get('email')
            gender = data.get('gender')
            contact_number = data.get('contact_number')
            password1 = data.get('password1')
            password2 = data.get('password2')
            # first_name = request.POST.get('first_name')
            # last_name = request.POST.get('last_name')
            # username = request.POST.get('username')
            # email = request.POST.get('email')
            # gender = request.POST.get('gender')
            # contact_number = request.POST.get('contact_number')
            # password1 = request.POST.get('password1')
            # password2 = request.POST.get('password2')
            if password1 == password2:
                User = get_user_model()
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'error': 'Username Taken'}, status=status.HTTP_400_BAD_REQUEST)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse({'error': 'Email Taken'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = CustomUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, gender=gender, contact_number=contact_number, username=username, password=password1)
                    user.save()
                    return JsonResponse({'message': 'Successfully Registered'})
            else:
                return JsonResponse({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return render(request, 'register.html')



def dashboard(request):
    return render( 'dashboard.html')

def logout(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def EmployerProfile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile_id = data.get('profile_id')
            employer_name = data.get('employer_name')
            federal_employer_identification_number  = data.get('federal_employer_identification_number')
            email = data.get('email')
            street_name = data.get('street_name')
            city = data.get('city')
            state = data.get('state')
            country = data.get('country')  
            zipcode = data.get('zipcode')
            number_of_employer = data.get('number_of_employer')
            department = data.get('department')
            location = data.get('location')   
            # profile_id = request.POST.get('profile_id')
            # employer_name = request.POST.get('employer_name')
            # street_name = request.POST.get('street_name')
            # city = request.POST.get('city')
            # state = request.POST.get('state')
            # country = request.POST.get('country')  
            # zipcode = request.POST.get('zipcode')
            # email = request.POST.get('email')  # Corrected
            # number_of_employer = request.POST.get('number_of_employer')
            # department = request.POST.get('department')
            
            # Check if required fields are empty
            if not profile_id or not email:
                return JsonResponse({'error': 'Required fields are missing'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if profile_id already exists
            if Employer_Profile.objects.filter(profile_id=profile_id).exists():
                return JsonResponse({'error': 'Profile ID already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if email is already registered
            if Employer_Profile.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create new Employer_Profile instance
            user = Employer_Profile.objects.create(profile_id=profile_id, employer_name=employer_name,email=email,federal_employer_identification_number=federal_employer_identification_number, street_name=street_name, city=city, state=state, country=country, zipcode=zipcode, number_of_employer=number_of_employer, department=department,location=location)
            
            return JsonResponse({'message': 'Employer Detail Successfully Registered'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    #return JsonResponse({'message': 'Employer Detail Successfully Registered'})   
    return render(request, 'Employer_Profile.html')


#for Updating the Employer Profile data

class EmployerProfileEditView(RetrieveUpdateAPIView):
    model = Employer_Profile
    queryset = Employer_Profile.objects.all()
    serializer_class = EmployerProfileSerializer
    lookup_field = 'profile_id'
    @csrf_exempt 
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
                'success': True,
                'message': 'Data Updated successfully',
                'Code': status.HTTP_200_OK}
        return JsonResponse(response_data)



#For updating the Registor details

class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'username'  
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = {
                'success': True,
                'message': 'Data Updated successfully',
                'Code': status.HTTP_200_OK}
        return JsonResponse(response_data)
    

# For Deleting the Employer Profile data

class UserDeleteAPIView(DestroyAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'username' 
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        response_data = {
                'success': True,
                'message': 'Data Deleted successfully',
                'Code': status.HTTP_204_NO_CONTENT}
        return JsonResponse(response_data)
    
