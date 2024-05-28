from rest_framework import serializers
from .models import *

class BasicSerializer(serializers.ModelSerializer):
    # user_id = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Basic
        fields = ['user', 'student_no', 'major_type', 'transfer', 'foreign', 'main_major', 'double_major', 'minor_major']

    def create(self, validated_data):
        main_major_name = validated_data.pop('main_major', None)
        if main_major_name:
            major = Major.objects.get(name=main_major_name)
            validated_data['main_major'] = major
        return super().create(validated_data)

class CreditSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only = True)

    class Meta:
        model = Credit
        fields = '__all__'
        

# class MajorSubjectSerializer(serializers.ModelSerializer):
#     subject_name = serializers.SerializerMethodField()

#     class Meta:
#         model = MajorCompulsorySubject
#         fields = ['id', 'status', 'subject', 'subject_name', 'user']

#     def get_subject_name(self, obj):
#         return obj.subject.name if obj.subject else None
   
# class LiberalSubjectSerializer(serializers.ModelSerializer):
#     user_id = serializers.PrimaryKeyRelatedField(read_only = True)
    
#     class Meta:
#         model = LiberalCompulsorySubject
#         fields = '__all__'

# class ExtraSerializer(serializers.ModelSerializer):
#     user_id = serializers.PrimaryKeyRelatedField(read_only = True) # user_id는 읽기 전용

#     class Meta:
#         model = Extra
#         fields = '__all__'


class MajorCompulsorySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorCompulsorySubject
        fields = ['user', 'status', 'subject']

class LiberalCompulsorySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiberalCompulsorySubject
        fields = ['user', 'status', 'subject']

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ['user', 'main_test_pass', 'double_test_pass', 'foreign_pass']

class CompletionSerializer(serializers.Serializer):
    credit = CreditSerializer(required=True)
    major_subject = serializers.ListField(child=serializers.CharField(), required=False)
    liberal_subject = serializers.ListField(child=serializers.CharField(), required=False)
    extra = ExtraSerializer(required=True)

    def create(self, validated_data):
        credit_data = validated_data.pop('credit')
        major_subject_data = validated_data.pop('major_subject', [])
        liberal_subject_data = validated_data.pop('liberal_subject', [])
        extra_data = validated_data.pop('extra')

        credit_instance = Credit.objects.create(**credit_data)
        extra_instance = Extra.objects.create(**extra_data)

        major_subject_instances = []
        for subject_name in major_subject_data:
            subject_instance = MajorCompulsorySubject.objects.create(subject=subject_name)
            major_subject_instances.append(subject_instance)

        liberal_subject_instances = []
        for subject_name in liberal_subject_data:
            subject_instance = LiberalCompulsorySubject.objects.create(subject=subject_name)
            liberal_subject_instances.append(subject_instance)

        return {
            'credit': credit_instance,
            'major_subject': major_subject_instances,
            'liberal_subject': liberal_subject_instances,
            'extra': extra_instance
        }