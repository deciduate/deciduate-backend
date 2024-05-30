from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView

from .models import *
from .serializers import *

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
    def get(self, request, pk):
        basic_data = Basic.objects.get(user_id=pk)
        credit_data = Credit.objects.filter(user_id=pk)
        major_subject_data = UserMajorCompulsory.objects.filter(user_id=pk)
        liberal_subject_data = UserLiberalCompulsory.objects.filter(user_id=pk)
        extra_data = Extra.objects.get(user_id=pk)

        basic_serializer = BasicSerializer(basic_data)
        credit_serializer = CreditSerializer(credit_data, many=True)
        major_subject_serializer = UserMajorCompulsorySerializer(major_subject_data, many=True)
        liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject_data, many=True)
        extra_serializer = ExtraSerializer(extra_data)

        major_user_data = list(set([item['subject_name'] for item in major_subject_serializer.data]))
        liberal_user_data = list(set([item['subject_name'] for item in liberal_subject_serializer.data]))

        return Response({
            'basic': basic_serializer.data,
            'credit': credit_serializer.data,
            'major_subject': major_user_data,
            'liberal_subject': liberal_user_data,
            'extra': extra_serializer.data
        })
              
# 마이페이지 > 취득 학점 
class CreditView(RetrieveUpdateAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    
# 마이페이지 > 수강 과목
#RetrievAPIView -> APIView로 수정 
class SubjectView(APIView):
    # permission_classes = [IsAuthenticated] #인증된 사용자가 뷰에 접근할 수 있도록 한다고 함
    def get(self, request, pk):
        try:
            major_subject = UserMajorCompulsory.objects.filter(user=pk)
            major_subject_serializer = UserMajorCompulsorySerializer(major_subject, many=True)
            major_user_data = list(set([item['subject_name'] for item in major_subject_serializer.data]))  # 중복된 값을 제거합니다
            
            liberal_subject = UserLiberalCompulsory.objects.filter(user=pk)
            liberal_subject_serializer = UserLiberalCompulsorySerializer(liberal_subject, many=True)
            liberal_user_data = list(set([item['subject_name'] for item in liberal_subject_serializer.data]))  # 중복된 값을 제거합니다

            response_data = {
                'major_subject': major_user_data,
                'liberal_subject': liberal_user_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except (UserMajorCompulsory.DoesNotExist, UserLiberalCompulsory.DoesNotExist):
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    # error: invalid data
    def put(self, request, pk):
        try:
            major_subject_data = request.data.get('major_subject')
            liberal_subject_data = request.data.get('liberal_subject')

            # 유저 객체 가져오기
            user = MyUser.objects.get(pk=pk)

            # 입력 데이터 유효성 검사
            if not major_subject_data or not isinstance(major_subject_data, list):
                return Response({"error": "Invalid data: 'major_subject' should be a list of subject names."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not liberal_subject_data or not isinstance(liberal_subject_data, list):
                return Response({"error": "Invalid data: 'liberal_subject' should be a list of subject names."}, status=status.HTTP_400_BAD_REQUEST)

            # Major subjects 처리
            UserMajorCompulsory.objects.filter(user=user).delete()

            for subject_name in major_subject_data:
                try:
                    subject = MajorCompulsory.objects.filter(subject__name=subject_name).first()
                    UserMajorCompulsory.objects.create(user=user, subject=subject)
                except MajorCompulsory.DoesNotExist:
                    return Response({"error": f"Invalid data: Major subject '{subject_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Liberal subjects 처리
            UserLiberalCompulsory.objects.filter(user=user).delete()
            for subject_name in liberal_subject_data:
                try:
                    subject = LiberalCompulsory.objects.filter(subject__name=subject_name).first()
                    UserLiberalCompulsory.objects.create(user=user, subject=subject)
                except LiberalCompulsory.DoesNotExist:
                    return Response({"error": f"Invalid data: Liberal subject '{subject_name}' does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # 응답 데이터 생성
            response_data = {
                'major_subject': major_subject_data,
                'liberal_subject': liberal_subject_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ExtraView(generics.ListCreateAPIView, generics.UpdateAPIView):
    queryset = Extra.objects.all()
    serializer_class = ExtraSerializer
