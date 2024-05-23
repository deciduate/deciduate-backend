from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from users.models import *
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

class PostProfile(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() #user=request.user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCompletion(APIView):
    def post(self, request):
        credit_serializer = CreditSerializer(data=request.data)
        subject_serializer = SubjectSerializer(data=request.data)
        extra_serializer = ExtraSerializer(data=request.data)

        if credit_serializer.is_valid() and subject_serializer.is_valid() and extra_serializer.is_valid():
            credit_instance = credit_serializer.save() #user=request.user
            subject_instance = subject_serializer.save() #user=request.user
            extra_instance = extra_serializer.save() #user=request.user

            response_data = {
                'credit_data': credit_serializer.data,
                'extra_data': extra_serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = {}
            errors.update(credit_serializer.errors)
            errors.update(extra_serializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
class PutProfile(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            profile = MyUser.objects.get() #user=request.user
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MyUser.DoesNotExist:
            return Response({'detail':'입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        user = MyUser.objects.get(id=1)
        try:
            profile = MyUser.objects.get() #user=request.uesr
            serializer = ProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyUser.DoesNotExist:
            return Response({'detail': '입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
class PutCredit(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            credit = Profile.objects.get() #user=request.user
            serializer = CreditSerializer(credit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'detail': '입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        try:
            credit = Profile.objects.get() #user=request.user
            serializer = CreditSerializer(credit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'detail': '입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
                
class PutExtra(RetrieveUpdateAPIView):
    def get(self, request):
        try:
            extra = Profile.objects.get()
            serializer = ExtraSerializer(extra)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'detail': '입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            extra = Profile.objects.get() #user=request.user
            serializer = ExtraSerializer(extra, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist:
            return Response({'detail': '입력된 프로필이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)