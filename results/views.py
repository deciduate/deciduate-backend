from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from profiles.serializers import *
from users.models import *
from profiles.models import *
from rest_framework import status

import json, os

def major_requirement(major):
        major_name = major.lower()

        if major_name == '철학과':
            major_name = 'phil'
        if major_name == '수학과':
            major_name = 'math'
        if major_name == '통계학과':
            major_name = 'stat'
        if major_name == '컴퓨터공학부' or major_name == '컴퓨터·전자시스템공학부':
            major_name = 'cse'
        if major_name == '반도체전자공학부(전자공학전공)':
            major_name = 'ee'
        if major_name ==  'Global Business&Technology학부':
            major_name = 'gbt'
        if major_name == '미디어커뮤니케이션학부':
            major_name = 'media'
                   
        

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dir = os.path.join(BASE_DIR, 'requirement', 'fixtures')
        filename = f'requirement-{major_name}.json'
        file_path = os.path.join(dir, filename)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                requirement_data = json.load(f)
        except FileNotFoundError:
            return None
        
        return requirement_data

class GetResult(APIView):
    def get(self, request):
        print("Get request received")
        try:
            basic = Basic.objects.get(user=request.user)
            #get_or_create는 튜플로 반환하는 함수임. 
            credit, created = Credit.objects.get_or_create(user=request.user)
            extra = Extra.objects.get(user=request.user)
            major_subject = UserMajorCompulsory.objects.filter(user=request.user, status=False)
            liberal_subject = UserLiberalCompulsory.objects.filter(user=request.user, status=False)
            print("Data fetched successfully from the database")
        except Basic.DoesNotExist:
            return Response({'detail': '입력된 기본 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Credit.DoesNotExist:
            return Response({'detail': '입력된 학점 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Extra.DoesNotExist:
            return Response({'detail': '입력된 추가 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except UserMajorCompulsory.DoesNotExist:
            return Response({'detail': '입력된 전필 과목 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except UserLiberalCompulsory.DoesNotExist:
            return Response({'detai': '입력된 교필 과목 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        basic_serializer = BasicSerializer(basic)
        credit_serializer = CreditSerializer(credit)
        extra_serializer = ExtraSerializer(extra)
        major_subject_serializer = UserMajorCompulsorySerializer(major_subject, many=True)
        liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject, many=True)

        print(f"Serialized data: Basic: {basic_serializer.data}, Credit: {credit_serializer.data}, Extra: {extra_serializer.data}")


        student_no = basic_serializer.data['student_no']
        main_major = basic_serializer.data['main_major_name'] #학과명

        print(f"Student no: {student_no}, Main major: {main_major}")

        print(f"Credit data: {credit_serializer.data}")
        if 'main_major' not in credit_serializer.data:
            print("Error: 'main_major' key is missing in credit data")
            return Response({'detail': "'main_major' key is missing in credit data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #유저데이터
        u_main_major = credit_serializer.data['main_major']
        u_double_major = credit_serializer.data.get('double_major', 0)  # 기본값 0 설정
        u_minor_major = credit_serializer.data.get('minor_major', 0)    # 기본값 0 설정
        u_liberal = credit_serializer.data['liberal']
        u_total_score = credit_serializer.data['total_score']


        requirement_data = major_requirement(main_major)

        if not requirement_data:
            print("Requirement data not found")
            return Response({'detail': '졸업 요건 데이터가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        result = {}

        for entry in requirement_data:
            print(f"Processing entry: {entry}")
            if entry['fields']['student_no'] == str(student_no):
                print(f"Matching student no: {student_no} with entry: {entry}")
                if entry['fields']['major_type'] == 1:
                    # 졸업요건
                    re_main_major = int(entry['fields']['main_major'])
                    re_liberal = int(entry['fields']['liberal'])
                
                    # 비교
                    if re_main_major > u_main_major:
                        result['main_major'] = re_main_major - u_main_major
                    if re_liberal > u_liberal:
                        result['liberal'] = re_liberal - u_liberal

                elif entry['fields']['major_type'] == 2:
                    re_main_major = int(entry['fields']['main_major'])
                    re_double_major = int(entry['fields']['double_major'])
                    re_liberal = int(entry['fields']['liberal'])

    
                    print(type(re_main_major), type(u_main_major))

                    if re_main_major > u_main_major:
                        result['main_major'] = re_main_major - u_main_major
                    if re_double_major > u_double_major:
                        result['double_major'] = re_double_major - u_double_major
                    if re_liberal > u_liberal:
                        result['liberal'] = re_liberal - u_liberal

                elif entry['fields']['major_type'] == 3 or entry['fields']['major_type'] == 4:
                    re_main_major = int(entry['fields']['main_major'])
                    re_minor_major = int(entry['fields']['minor_major'])
                    re_liberal = int(entry['fields']['liberal'])
                    

                    if re_main_major > u_main_major:
                        result['main_major'] = re_main_major - u_main_major
                    if re_minor_major > u_minor_major:
                        result['minor_major'] = re_minor_major - u_minor_major
                    if re_liberal > u_liberal:
                        result['liberal'] = re_liberal - u_liberal
        
        print(f"Intermediate result: {result}")

        # 총 학점 2.00 넘는지
        u_total_score = credit_serializer.data['total_score']
        
        if u_total_score <= 2.00:
            result['total_score'] = False

        # 전필과목 이수 여부: 수강하지 않은 과목의 이름 보내기
        result['major_compulsory'] = [item['subject'] for item in major_subject_serializer.data]

        # 교필과목 이수 여부: 수강하지 않은 과목의 이름 보내기
        result['liberal_compulsory'] = [item['subject'] for item in liberal_subject_serializer.data]
        
        # 시험 통과 여부
        u_main_test_pass = extra_serializer.data['main_test_pass']
        u_double_test_pass = extra_serializer.data['double_test_pass']
        u_foreign_pass = extra_serializer.data['foreign_certification']
        
        if u_main_test_pass == False:
            result['main_test_pass'] = False
        if u_double_test_pass == False:
            result['double_test_pass'] = False
        if u_foreign_pass == "None":
            result['foreign_certification'] = False

        print(f"Final result: {result}")
        return Response(result, status=status.HTTP_200_OK)

# 1전공, 이중전공, 교양, 부전공, 총평점, 전필과목, 교필과목, 시험통과, 외국어인증