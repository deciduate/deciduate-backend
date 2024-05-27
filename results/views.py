from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from profiles.serializers import *
from users.models import *
from profiles.models import *
from rest_framework import status

import json, os

# 순서 조정 필요
# 학과에 따른 졸업요건 파일 가져오기
def major_requirement(major):
    major_name = major.lower()

    if major_name == 'philosophy':
        major_name = 'phil'

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dir = os.path.join(BASE_DIR, 'requirement', 'fixtures')
    filename = f'requirement-{major_name}.json'
    file_path = os.path.join(dir, filename)

    with open(file_path, 'r', encoding='utf-8') as f:
        requirement_data = json.load(f)
    
    return requirement_data

# 유저 데이터 불러오기
profiles = Basic.objects.all()
profile_serializer = BasicSerializer(profiles, many=True)

credit = Credit.objects.all()
credit_serializer = CreditSerializer(credit, many=True)

major_subject = MajorCompulsorySubject.objects.all()
major_subject_serializer = MajorSubjectSerializer(major_subject, many=True)

liberal_subject = LiberalCompulsorySubject.objects.all()
extra = Extra.objects.all()

completions = Profile.objects.all()
credit_serializer = CreditSerializer(completions, many=True)
subject_serializer = SubjectSerializer(completions, many=True)
extra_serializer = ExtraSerializer(completions, many=True)

# 유저 정보: 학번, 전공 유형, 1전공
student_no = profile_serializer.data.get('student_no')
main_major = profile_serializer.data.get('main_major')

# 1전공에 따른 졸업요건 데이터 가져오기
requirement_data = major_requirement(main_major)

# 졸업요건 계산 결과 담기
result = {}

# 졸업요건과 비교해 부족한 학점 담기
def compare_credit(type):
    requirement = entry['fields'][type]
    user_credit = credit_serializer.data.get(type)
    if user_credit < requirement:
        result[type] = requirement - user_credit

# 졸업시험/논문, 외국어인증시험 통과 여부 담기
def test_status(test):
    test_pass = extra_serializer.data.get(test)
    if test_pass == False:
        result[test] = 'F'
    return result

class GetResult(APIView):
    def get(self, request):


        # 학번, 전공 유형에 따라 졸업요건 학점 계산하기
        for entry in requirement_data:
            if entry['fields']['student_no'] == student_no[2:4]:
                if entry['fileds']['major_type'] == 1:
                    compare_credit('main_major')
                    compare_credit('liberal')
                    compare_credit('total_credit')
                elif entry['fileds']['major_type'] == 2:
                    compare_credit('main_major')
                    compare_credit('double_major')
                    compare_credit('liberal')
                    compare_credit('total_credit')
                elif entry['fileds']['major_type'] == 3 or entry['fields']['majortype'] == 4:
                    compare_credit('main_major')
                    compare_credit('minor_credit')
                    compare_credit('liberal')
                    compare_credit('total_credit')

        # 유저 정보: 총학점        
        total_score = credit_serializer.data.get('total_score')
        if total_score <= 2.00:
            result['total_score'] = 'F'
        
        # 유저 정보: 필수 과목 수강 여부, 이 부분 어떻게 되는지 정확히를 모르겠음
        subject_status = subject_serializer.data.get('status')

        # 시험 통과 여부 담기
        test_status('main_test_pass')
        test_status('double_test_pass')
        test_status('foreign_pass')

        # 이 부분을 내가 해야하는지 아니면 프론트에서 해야하는지
        # 그냥 정보만 넘기면 되는지 알아보기
        try:
            return Response(result)
            # 만약 result에 무엇이라도 담겨 있다면, 부족한 창으로 이동
        except:
            return Response(result)
            # 만약 reulst에 아무것도 담겨있지 않다면, 축하하는 창으로 이동

