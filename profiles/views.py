from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from users.models import *
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

# user를 어떻게 해야하는지 고민해야함

# 기본정보입력(1)
class PostBasic(APIView):
    def post(self, request):
        serializer = BasicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 기본정보입력(2)
class PostCompletion(APIView):
    def post(self, request):
        credit_data = request.data.get('credit')
        major_subject_data = request.data.get('major_subject')
        liberal_subject_data = request.data.get('liberal_subject')
        extra_data = request.data.get('extra')

        # 학점 입력받기
        credit_serializer = CreditSerializer(data=credit_data)
        if credit_serializer.is_valid():
            credit_completion = credit_serializer.save()
        else:
            return Response(credit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 전필 입력받기
        major_subject_serializer = MajorSubjectSerializer(data=major_subject_data, many=True)
        if major_subject_serializer.is_valid():
            major_subject_completion = major_subject_serializer.save()
        else:
            return Response(major_subject_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 교필 입력받기
        liberal_subject_serializer = LiberalSubjectSerializer(data=liberal_subject_data, many=True)
        if liberal_subject_serializer.is_valid():
            liberal_subject_completion = liberal_subject_serializer.save()
        else:
            return Response(liberal_subject_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # 시험 통과 여부 입력받기
        extra_serializer = ExtraSerializer(data=extra_data)
        if extra_serializer.is_valid():
            extra_profile = extra_serializer.save()
        else:
            return Response(extra_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'credit': credit_serializer.data,
            'major_subject': major_subject_serializer.data,
            'liberal_subject': liberal_subject_serializer.data,
            'extra': extra_serializer.data
        }, status=status.HTTP_201_CREATED)
        
# 마이페이지 > 내 정보       
class GetInfo(APIView):
    def get(self, request):
        user = request.user

        # Profile 데이터 가져오기
        try:
            basic_data = Basic.objects.get(user_id=user.id)
            basic_serializer = BasicSerializer(basic_data)
        except Basic.DoesNotExist:
            return Response({'error': '입력된 유저 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Credit 데이터 가져오기
        try:
            credit_data = Credit.objects.get(user_id=user.id)
            credit_serializer = CreditSerializer(credit_data)
        except Credit.DoesNotExist:
            credit_serializer = None
        
        # MajorCompulsorySubject 데이터 가져오기
        try:
            # 여기 필터 부분이 뭔가 이상함
            major_subject_data = MajorCompulsorySubject.objects.filter(user_id=user.id)
            major_subject_serializer = MajorSubjectSerializer(major_subject_data, many=True)
        except MajorCompulsorySubject.DoesNotExist:
            major_subject_serializer = None

        # LiberalCompusory 데이터 가져오기
        try:
            liberal_subject_data = LiberalCompulsorySubject.objects.filter(user_id=user.id)
            liberal_subject_serializer = LiberalSubjectSerializer(liberal_subject_data, many=True)
        except LiberalCompulsorySubject.DoesNotExist:
            liberal_subeject_serializer = None
        
        # Extra 데이터 가져오기
        try:
            extra_data = Extra.objects.get(user_id=user.id)
            extra_serializer = ExtraSerializer(extra_data)
        except Extra.DoesNotExist:
            extra_serializer = None

        Response_data = {
            'basic': basic_serializer.data,
            'credit': credit_serializer.data if credit_serializer else None,
            'major_subject': major_subject_serializer.data if major_subject_serializer else [],
            'liberal_subject': liberal_subeject_serializer.data if liberal_subeject_serializer else [],
            'extra': extra_serializer.data if extra_serializer else None 
        }

        return Response(Response_data, status=status.HTTP_200_OK)


# 마이페이지 > 상태 3개 필요(미등록, 등록 중, 등록완료)
# post(미등록), put(등록완료)

# 마이페이지 > 기본 정보
class PutBasic(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            basic = Basic.objects.get('user_id')
            serializer = BasicSerializer(basic)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Basic.DoesNotExist:
            return Response({'detail': '입력된 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        try:
            basic = Basic.objects.get()
            serializer = BasicSerializer(basic, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Basic.DoesNotExist:
            return Response({'detail': '입력된 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
  
# 만약 null 값이 하나라도 있으면 등록중 -> put을 통해 넣을 수 있음
# 모두 null 값이라면 미등록 -> put을 통해 넣을 수 있음
# null 값이 하나라도 없으면 등록완료 -> put을 통해 수정완료
# -> 모델에서 default 다 없애고, null=True 변경
      
# 마이페이지 > 취득 학점
class PutCredit(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            credit = Credit.objects.get(user=request.user)
            serializer = CreditSerializer(credit)
            # 201: 요청 정상, 요청된 리소스 포함
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 이 부분만 약간 고치면 될듯
        except Credit.DoesNotExist:
            # 204: 요청 성공, 제공할 내용 없음 => 입력된 내용 없으니, 프론트에 줄 리소스 없다
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        try:
            credit = Credit.objects.get(user=request.user)
            serializer = CreditSerializer(credit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Credit.DoesNotExist:
            return Response({'detail': '입력된 학점이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

# 마이페이지 > 수강 과목
class PutSubject(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            major_subject = MajorCompulsorySubject.objects.get(user=request.user)
            liberal_subject = LiberalCompulsorySubject.objects.get(user=request.user)
            major_subeject_serializer = MajorSubjectSerializer(major_subject)
            liberal_subject_serializer = LiberalSubjectSerializer(liberal_subject)
            
            response_data = {
                'major_subject':major_subeject_serializer.data,
                'liberal_subject': liberal_subject_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except (MajorCompulsorySubject.DoesNotExist, LiberalCompulsorySubject.DoesNotExist):
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request):
        try:
            major_subject = MajorCompulsorySubject.objects.get(user=request.user)
            liberal_subject = LiberalCompulsorySubject.objects.get(user=request.user)
            major_subject_serializer = MajorSubjectSerializer(major_subject, data=request.data, partial=True)
            liberal_subject_serializer = LiberalSubjectSerializer(liberal_subject, data=request.data, partial=True)
            if major_subject_serializer.is_valid() and liberal_subject_serializer.is_valid():
                major_subject_serializer.save()
                liberal_subject_serializer.save()
                Response_data = {
                    'major_subject': major_subject_serializer.data,
                    'liberal_subject': liberal_subject_serializer.data
                }
                return Response(Response_data, status=status.HTTP_200_OK)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except (MajorCompulsorySubject.DoesNotExist, LiberalCompulsorySubject.DoesNotExist):
            return Response({'detail': '수강한 필수과목이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


# 마이페이지 > 졸업시험/논문 | 외국어 인증
class PutExtra(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            extra = Extra.objects.get(user=request.user)
            serializer = ExtraSerializer(extra)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Extra.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request):
        try:
            extra = Extra.objects.get(user=request.user)
            serializer = ExtraSerializer(extra, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Extra.DoesNotExist:
            return Response({'detail': '입력된 학점이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)