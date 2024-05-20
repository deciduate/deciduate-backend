from django import forms
from .models import Profile
from users.models import MyUser

# Create the form class
class InfoForm(forms.Form):
    class Meta:
        model = MyUser
        fields = ['student_no', 'major_type', 'main_major', 'double_major', 'sub_major', 'transfer', 'foreign']
        widgets = {
            'major_type': forms.Select(),
            'transfer': forms.CheckboxInput(),
            'foreign': forms.CheckboxInput(),
        }

class ScoreForm(Profile):
    class Meta:
        model = Profile
        fields = ['main_major', 'double_major', 'minor_major', 'outside', 'liberal', 'teaching', 'self_selection']

# 수강과목 필드를 어떤 걸 가져와야 하는지
class SubjectForm(Profile):
    class Meta:
        model = MyUser
        fields = []
# form에 마이페이지 > 수강 과목 부분을 저장하려고 하는데, 
# 전공 필수 과목/교양 필수 과목 필드를 어디에 저장해야하는지 모르겠음

class ElseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['main_test_pass', 'double_test_pass', 'foreign_pass']
        widgets = {
            'main_test_pass': forms.CheckboxInput(),
            'double_test_pass': forms.CheckboxInput(),
            'foreign_pass': forms.Select(),
        }

#기본정보: 학번, 전공 구분 및 학과 / 기타사항(편입, 외국인전형)
#취득학점: 전공/이중전공, 실외, 교양, 교직, 자선
#수강과목: 전공 필수 과목, 교양 필수 과목
#기타정보: 졸업 시험/ 논문 통과 여부(전공/전공심화, 이중전공/부전공), 외국어인증점수보유및제출여부