from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import *
from .serializers import *
from users.models import MyUser
from subject.models import Subject

class BasicView(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Basic.objects.all()
    serializer_class = BasicSerializer
        
class CompletionView(generics.GenericAPIView):
    serializer_class = CompletionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_201_CREATED)
      
# 마이페이지 > 내 정보 -> get 확인 필요   
class InfoView(APIView):
    def get(self, request):

        # Profile 데이터 가져오기
        try:
            basic_data = Basic.objects.get(user=request.user)
            basic_serializer = BasicSerializer(basic_data)
        except Basic.DoesNotExist:
            return Response({'error': '입력된 유저 정보가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Credit 데이터 가져오기
        try:
            credit_data = Credit.objects.get(user=request.user)
            credit_serializer = CreditSerializer(credit_data)
        except Credit.DoesNotExist:
            credit_serializer = None
        
        # UserMajorCompulsory 데이터 가져오기
        try:
            major_subject_data = UserMajorCompulsory.objects.filter(user=request.user, status=True)
            major_subject_serializer = UserMajorCompulsorySerializer(major_subject_data, many=True)
            major_true_data = [item['subject'] for item in major_subject_serializer.data]
        except UserMajorCompulsory.DoesNotExist:
            major_subject_serializer = None

        # LiberalCompusory 데이터 가져오기
        try:
            liberal_subject_data = UserLiberalCompulsory.objects.filter(user=request.user, status=True)
            liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject_data, many=True)
            liberal_true_data = [item['subject'] for item in liberal_subject_serializer.data]
        except UserLiberalCompulsory.DoesNotExist:
            liberal_subeject_serializer = None
        
        # Extra 데이터 가져오기
        try:
            extra_data = Extra.objects.get(user=request.user)
            extra_serializer = ExtraSerializer(extra_data)
        except Extra.DoesNotExist:
            extra_serializer = None

        # 전필, 교필과목은 이수한 과목만 전달하도록 수정 필요 -> serializer을 새로 만들어야함
        Response_data = {
            'basic': basic_serializer.data,
            'credit': credit_serializer.data if credit_serializer else None,
            'major_subject': major_true_data if major_subject_serializer else [],
            'liberal_subject': liberal_true_data if liberal_subeject_serializer else [],
            'extra': extra_serializer.data if extra_serializer else None 
        }

        return Response(Response_data, status=status.HTTP_200_OK)#
      
# 마이페이지 > 취득 학점 
class CreditView(RetrieveUpdateAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

# 마이페이지 > 수강 과목 -> get, put 확인 필요

# 마이페이지 > 수강 과목
#RetrievAPIView -> APIView로 수정 
class SubjectView(APIView):
    # permission_classes = [IsAuthenticated] 인증된 사용자가 뷰에 접근할 수 있도록 한다고 함
    def get(self, request):
        try:
            major_subject = UserMajorCompulsory.objects.filter(user=request.user)
            major_subeject_serializer = UserMajorCompulsorySerializer(major_subject,many = True) #many = True : 여러개의 객체를 시리얼라이즈할 때 사용함
            major_user_data = [item['subject_name'] for item in major_subeject_serializer.data] #subject -> subject_name으로 수정
            
            liberal_subject = UserLiberalCompulsory.objects.filter(user=request.user)
            liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject, many = True)
            liberal_user_data = [item['subject_name'] for item in liberal_subject_serializer.data]

            # 여기는 들은 과목, 안 들은 과목 다 보여줘야 하는건가
            response_data = {
                'major_subject': major_user_data,
                'liberal_subject': liberal_user_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except (UserMajorCompulsory.DoesNotExist, UserLiberalCompulsory.DoesNotExist):
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request):
        try:
            major_subject = UserMajorCompulsory.objects.filter(user=request.user)
            liberal_subject = UserLiberalCompulsory.objects.filter(user=request.user)

            major_subject_serializer = UserMajorCompulsorySerializer(major_subject, data=request.data.get('major_subject'), many = True, partial=True)
            liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject, data=request.data.get('liberal_subject'), many = True,  partial=True)
            
            if major_subject_serializer.is_valid() and liberal_subject_serializer.is_valid():
                major_subject_serializer.save()
                liberal_subject_serializer.save()
                Response_data = {
                    'major_subject': major_subject_serializer.data,
                    'liberal_subject': liberal_subject_serializer.data
                }
                return Response(Response_data, status=status.HTTP_200_OK)
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        except (UserMajorCompulsory.DoesNotExist, UserLiberalCompulsory.DoesNotExist):
            return Response({'detail': '수강한 필수과목이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
class ExtraView(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
