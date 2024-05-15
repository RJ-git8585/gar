from rest_framework import serializers
from .models import CustomUser ,Employer_Profile



class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'contact_number']


class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer_Profile
        fields = ['profile_id','employer_name', 'street_name','federal_employer_identification_number', 'city', 'state', 'country', 'zipcode', 'email', 'number_of_employer', 'department','location']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'