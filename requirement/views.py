from django.shortcuts import render, redirect, get_object_or_404
from .models import Requirement
from .serializers import RequirementSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from major.models import Major


# 기존 장고 방식
# def input(request):
#     return render(request, 'input_requirements.html')

# def show_requirements(request):
#     if request.method == 'POST':
#         학번 = request.POST.get('학번', '')
#         전공 = request.POST.get('전공', '')
#         전공_유형 = request.POST.get('전공_유형', '')
#         print("요청된 조건 값들:", 학번, 전공, 전공_유형)

#         requirements = Requirement.objects.filter(student_no=학번, major_id=전공, major_type=전공_유형)
        
#         return render(request, 'requirements.html', {'requirements': requirements})
#     else:
#         return redirect('input')  # POST 요청이 아닌 경우 input 페이지로 리디렉션

# DRF 방식


@api_view(['POST'])
def show_requirements(request):
    student_no = request.data.get('학번', '')
    major_name = request.data.get('전공', '')
    major_type = request.data.get('전공_유형', '')

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
