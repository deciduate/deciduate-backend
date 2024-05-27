from django.shortcuts import render, redirect, get_object_or_404
from .models import Requirement
from .serializers import RequirementSerializer, CompleteRequirementSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from major.models import Major



@api_view(['GET'])
def show_requirements(request):
    student_no = request.query_params.get('학번', '')
    major_name = request.query_params.get('전공', '')
    major_type = request.query_params.get('전공_유형', '')

    print("요청된 조건 값들:", student_no, major_name, major_type)

    # Major 모델에서 전공 이름으로 id 값을 찾음
    try:
        major = Major.objects.get(name=major_name)
        major_id = major.id
    except Major.DoesNotExist:
        return Response({"detail": "Major not found."}, status=status.HTTP_404_NOT_FOUND)

    requirements = Requirement.objects.filter(student_no=student_no, major_id=major_id, major_type=major_type)
    
    if not requirements.exists():
        return Response({"detail": "No requirements found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = RequirementSerializer(requirements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def requirements(request):

    student_no = request.GET.get('학번')
    major_name = request.GET.get('전공')

    print("학번:", student_no)  # 디버깅 출력 추가
    print("전공:", major_name)  # 디버깅 출력 추가
    try:
        major = Major.objects.get(name=major_name)
    except Major.DoesNotExist:
        print("Major not found:", major_name)  # 디버깅 출력 추가
        return Response({"detail": "Major not found."}, status=status.HTTP_404_NOT_FOUND)
    
    print("찾은 전공:", major)  # 디버깅 출력 추가
    
    major_compulsory = MajorCompulsory.objects.filter(grades__year=student_no)
    liberal_compulsory = LiberalCompulsory.objects.filter(grades__year=student_no)
    requirements = Requirement.objects.filter(student_no=student_no, major_id=major.id)

    if not requirements.exists():
        print("No requirements found for student:", student_no, "and major:", major_name)  # 디버깅 출력 추가
        return Response({"detail": "No requirements found."}, status=status.HTTP_404_NOT_FOUND)
    
    requirement = requirements.first()
    print("Requirement:", requirement)  # 디버깅 출력 추가

    requirement_serializer = CompleteRequirementSerializer(requirement)

    data = {
        'major_compulsory': [subject.name for subject in major_compulsory],
        'liberal_compulsory': [subject.name for subject in liberal_compulsory],
    }
    data.update(requirement_serializer.data)  # Requirement 데이터를 추가

    return Response(data, status=status.HTTP_200_OK)
