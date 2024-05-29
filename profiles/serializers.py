from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from profiles.models import Basic, Credit, UserMajorCompulsory, UserLiberalCompulsory, Extra
from major.models import Major
from subject.models import Subject, MajorCompulsory, LiberalCompulsory
from users.models import MyUser

default_user = MyUser.objects.get(id=2)

class BasicSerializer(serializers.ModelSerializer):
    main_major_name = serializers.CharField(source='main_major.name', read_only=True)
    double_major_name = serializers.CharField(source='double_major.name', read_only=True)
    minor_major_name = serializers.CharField(source='minor_major.name', read_only=True)
    
    main_major = serializers.CharField(write_only=True)
    double_major = serializers.CharField(write_only=True, allow_null=True, required=False)
    minor_major = serializers.CharField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = Basic
        fields = [
            'id', 'user', 'student_no', 'major_type', 'transfer', 'foreign_st', 
            'main_major', 'double_major', 'minor_major',
            'main_major_name', 'double_major_name', 'minor_major_name'
        ]
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        main_major_name = validated_data.pop('main_major', None)
        double_major_name = validated_data.pop('double_major', None)
        minor_major_name = validated_data.pop('minor_major', None)

        user = self.context['request'].user
        if not isinstance(user, MyUser):
            user = default_user

        if main_major_name:
            try:
                main_major = Major.objects.get(name=main_major_name)
                validated_data['main_major'] = main_major
            except Major.DoesNotExist:
                raise ValidationError({"main_major": "Major with this name does not exist."})
        if double_major_name:
            try:
                double_major = Major.objects.get(name=double_major_name)
                validated_data['double_major'] = double_major
            except Major.DoesNotExist:
                raise ValidationError({"double_major": "Major with this name does not exist."})
        if minor_major_name:
            try:
                minor_major = Major.objects.get(name=minor_major_name)
                validated_data['minor_major'] = minor_major
            except Major.DoesNotExist:
                raise ValidationError({"minor_major": "Major with this name does not exist."})

        validated_data['user'] = user
        
        return Basic.objects.create(**validated_data)


    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not isinstance(user, MyUser):
            user = default_user
            
        if 'main_major' in validated_data:
            main_major_name = validated_data.pop('main_major')
            instance.main_major = Major.objects.get(name=main_major_name)

        if 'double_major' in validated_data:
            double_major_name = validated_data.pop('double_major')
            instance.double_major = Major.objects.get(name=double_major_name)

        if 'minor_major' in validated_data:
            minor_major_name = validated_data.pop('minor_major')
            instance.minor_major = Major.objects.get(name=minor_major_name)

        return super().update(instance, validated_data)
        

class CreditSerializer(serializers.ModelSerializer):
    # 사용자 필드를 식별자로 나타내기 위해 PrimaryKeyRelatedField를 사용합니다.
    # user = serializers.PrimaryKeyRelatedField(queryset=MyUser.objects.all())

    class Meta:
        model = Credit
        fields = [
            'id', 'main_major_credit', 'double_major_credit', 'second_major_credit', 
            'outside_credit', 'liberal_credit', 'minor_major_credit', 'teaching_credit', 
            'self_selection_credit', 'total_credit', 'total_score', 'user'
        ]
        read_only_fields = ['id', 'user']

class UserMajorCompulsorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject.name', read_only=True)

    class Meta:
        model = UserMajorCompulsory
        fields = ['id', 'status', 'subject_name', 'user']
        read_only_fields = ['id', 'user']

class UserLiberalCompulsorySerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject.name', read_only=True)

    class Meta:
        model = UserLiberalCompulsory
        fields = ['id', 'status', 'subject_name', 'user']
        read_only_fields = ['id', 'user']

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = [
            'id', 'main_test_pass', 'double_test_pass', 'foreign_certification', 'user'
        ]
        read_only_fields = ['id', 'user']

class CompletionSerializer(serializers.Serializer):
    credit = CreditSerializer()
    major_subject = serializers.ListField(child=serializers.CharField())
    liberal_subject = serializers.ListField(child=serializers.CharField())
    extra = ExtraSerializer()

    def create(self, validated_data):
        credit_data = validated_data.pop('credit')
        major_subject_data = validated_data.pop('major_subject')
        liberal_subject_data = validated_data.pop('liberal_subject')
        extra_data = validated_data.pop('extra')

        # Credit 저장
        user = self.context['request'].user
        if not isinstance(user, MyUser):
            user = default_user

        # Credit 객체 생성
        credit = Credit.objects.create(**credit_data, user=user)

        # UserMajorCompulsory 저장
        for subject_name in major_subject_data:
            subject = Subject.objects.get(name=subject_name)
            major_compulsories = MajorCompulsory.objects.filter(subject=subject)
            for major_compulsory in major_compulsories:
                UserMajorCompulsory.objects.create(user=user, subject=major_compulsory, status=True)

        # UserLiberalCompulsory 저장
        for subject_name in liberal_subject_data:
            subject = Subject.objects.get(name=subject_name)
            liberal_compulsories = LiberalCompulsory.objects.filter(subject=subject)
            for liberal_compulsory in liberal_compulsories:
                UserLiberalCompulsory.objects.create(user=user, subject=liberal_compulsory, status=True)


        # Extra 저장
        extra = Extra.objects.create(user=user, **extra_data)

        validated_data['user'] = user

        return {
            'credit': CreditSerializer(credit).data,
            'major_subject': major_subject_data,
            'liberal_subject': liberal_subject_data,
            'extra': ExtraSerializer(extra).data
        }