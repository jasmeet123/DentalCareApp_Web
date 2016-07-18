from rest_framework import serializers
from .models import Dentist

class DentistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dentist
        fields = ('zip','first_name','last_name','address','city','state','active','image','qualification','email','date_of_birth','is_active', 'is_admin')