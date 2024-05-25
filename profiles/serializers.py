from rest_framework import serializers
from .models import Profile
from users.models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['student_no', 'major_type', 'main_major', 'double_major',
                  'minor_major', 'transfer', 'foreign']


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['main_major', 'double_major', 'second_major', 'outside', 
                  'liberal', 'minor_major', 'teaching', 'self_selection', 
                  'total_credit', 'total_score']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['status']

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['main_test_pass', 'double_test_pass', 'foreign_pass']