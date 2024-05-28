from rest_framework import serializers
from .models import *
from users.models import *

class BasicSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Basic
        exclude = 'admission_year'

class CreditSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Credit
        fields = '__all__'
        

class MajorSubjectSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = MajorCompulsorySubject
        fields= '__all__'
   
class LiberalSubjectSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True)
    
    class Meta:
        model = LiberalCompulsorySubject
        fields = '__all__'

class ExtraSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True) # user_id는 읽기 전용

    class Meta:
        model = Extra
        fields = '__all__'