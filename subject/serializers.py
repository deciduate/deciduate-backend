from rest_framework import serializers
from .models import MajorCompulsory, LiberalCompulsory

class MajorCompulsorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    major_name = serializers.CharField(source='major.name', read_only=True)

    class Meta:
        model = MajorCompulsory
        fields = ['id', 'subject_name', 'major_name', 'main_compulsory', 'sub_compulsory', 'class_of']

class LiberalCompulsorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = LiberalCompulsory
        fields = ['id', 'subject_name', 'category', 'compulsory', 'class_of']
