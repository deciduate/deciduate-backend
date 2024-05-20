from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse
from .models import Profile, MyUser

# result라는 앱 만들어서 get result
# 졸업 요건을 모두 충족했다면, 충족한 창 
# 부족하다면 어디가 부족한지, 무엇을 추천해주는지

# 기본 정보 입력 받기
# post(기본정보-학번~편입생/외국인전형입학)
def input_info1(request):
    if request.method == 'POST':
        form = InfoForm()
    else:
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('input_info2'))
    return render(request, 'input_info1.html', {'form':form})

# post(학점 ~ 외국어인증시험)
def input_info2(request):
    if request.method == 'POST':
        score_form = ScoreForm(request.POST)
        else_form = ElseForm(request.POST)
        if score_form.is_valid() and else_form.is_valid():
            score_form.save()
            else_form.save()
            return redirect(reverse('success'))
        context = {'score_form': score_form, 'else_form': else_form}
    else:
        score_form = ScoreForm()
        else_form = ElseForm()
        context = {'score_form': score_form, 'else_form': else_form}

    return render(request, 'input_info2.html', context)

# 잘 입력됐는지 성공했다고 알려주는 곳, 사실상 필요 없음
def success(request):
    return render(request, 'success.html')

# 마이페이지 > 취득학점 
# 로그인이 되어 있어야하기에 코드 수정 필요
def edit_info(request):
    if request.method == 'GET':
        form = InfoForm()
    else:
        form = InfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('success'))
    return render(request, 'mypage_score.html', {'form':form})

def edit_score(request):
    if request.method == 'GET':
        form = ScoreForm()
    else:
        form = ScoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('success'))
    return render(request, 'mypage_score.html', {'form':form})

# 마이페이지 > 수강과목 코드 작성 필요, 폼부터 정리되야 가능할 듯

# 마이페이지 > 졸업시험/논문|외국어인증
# 또한 로그인이 되어 있어야하기에 코드 수정 필요
def edit_else(request):
    if request.method == 'GET':
        form = ElseForm()
    else:
        form = ElseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('success'))
    return render(request, 'mypage_else.html', {'form':form})

