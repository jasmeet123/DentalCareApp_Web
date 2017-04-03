from rest_framework import serializers
from models import Tip
from django.contrib.auth.models import  User

class TipsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    image = serializers.ImageField(max_length=None, allow_null= True,default="tips_image/Holiday_Party_Img4.jpg")
    class Meta:
        model = Tip
        fields = ('id','title','desc','image', 'date','owner')
