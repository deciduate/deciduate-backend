from django.shortcuts import render, redirect, get_object_or_404
from .models import Requirement
from .serializers import RequirementSerializer, CompleteRequirementSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from profiles.models import Basic
from subject.models import MajorCompulsory, LiberalCompulsory, ClassOf


@api_view(['GET'])
def show_requirements(request):

    user_id = request.query_params.get('user_id', '')

    if not user_id:
        return Response({"detail": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = Basic.objects.get(id=user_id)
    except Basic.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    # 사용자 정보에서 주요 전공, 학번, 전공 유형을 가져옴
    student_no = user.student_no
    major = user.main_major
    major_type = user.major_type

    if not major:
        return Response({"detail": "User's main major is not set."}, status=status.HTTP_400_BAD_REQUEST)

    major_id = major.id

    print("요청된 조건 값들:", student_no, major.name, major_type)
    # Major 모델에서 전공 이름으로 id 값을 찾음

    requirements = Requirement.objects.filter(student_no=student_no, major_id=major_id, major_type=major_type)
    
    if not requirements.exists():
        return Response({"detail": "No requirements found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RequirementSerializer(requirements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class RequirementView(APIView):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            basic_user = Basic.objects.get(user=user)
        except Basic.DoesNotExist:
            return Response({"detail": "Basic profile is required."}, status=status.HTTP_404_NOT_FOUND)

        #학번, 전공을 user에 맞춰서 정의
        student_no = basic_user.student_no
        major = basic_user.main_major

        if not major:
            return Response({"detail": "User's main major is not set."}, status=status.HTTP_400_BAD_REQUEST)
        
        #객체로부터 id, name 가져오기
        major_id = major.id
        major_name = major.name
        
        # 요청된 조건 값들 출력 (디버깅용)
        print("학번:", student_no)  # 디버깅 출력 추가
        print("전공:", major_name)  # 디버깅 출력 추가

        try:
            class_of = ClassOf.objects.get(year=student_no)
        except ClassOf.DoesNotExist:
            return Response({"detail": "Class of not found for the given student number."}, status=status.HTTP_404_NOT_FOUND)


        # 전공 필수 과목과 교양 필수 과목 조회
        major_compulsory = MajorCompulsory.objects.filter(class_of=class_of, major=major)
        liberal_compulsory = LiberalCompulsory.objects.filter(class_of=class_of)
        requirements = Requirement.objects.filter(student_no=student_no, major_id=major_id)

        # 요구사항이 없는 경우
        if not requirements.exists():
            print("No requirements found for student:", student_no, "and major:", major_name)  # 디버깅 출력 추가
            return Response({"detail": "No requirements found."}, status=status.HTTP_404_NOT_FOUND)

        # 첫 번째 요구사항을 가져옴
        requirement = requirements.first()
        print("Requirement:", requirement)  # 디버깅 출력 추가

        # 요구사항 시리얼라이징
        requirement_serializer = CompleteRequirementSerializer(requirement)

        # 응답 데이터 구성
        data = {
            'major_compulsory': [subject.subject.name for subject in major_compulsory],
            'liberal_compulsory': [subject.subject.name for subject in liberal_compulsory],
        }
        data.update(requirement_serializer.data)  # Requirement 데이터를 추가

        return Response(data, status=status.HTTP_200_OK)
