from rest_framework import serializers
from .models import Requirement

class RequirementSerializer(serializers.ModelSerializer):
    major_name = serializers.SerializerMethodField()

    class Meta:
        model = Requirement
        fields = '__all__'
        extra_fields = ['major_name']

    def get_major_name(self, obj):
        return obj.major_id.name
    
class CompleteRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ['test_type', 'flex', 'flex_speaking', 'toeic', 'toeic_speaking', 'opic']
