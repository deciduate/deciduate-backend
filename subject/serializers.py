from rest_framework import serializers
from .models import MajorCompulsory

class MajorCompulsorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCompulsory
        fields = ['id', 'area', 'grade', 'name', 'credit', 'major', 'main_compulsory', 'sub_compulsory', 'class_of']
