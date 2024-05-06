from django.shortcuts import render
from .models import Requirement

def show_requirements(request):
    if request.method == 'POST':
        학번 = request.POST.get('학번')
        전공 = request.POST.get('전공')
        전공_유형 = request.POST.get('전공_유형')

        requirements = Requirement.objects.filter(student_no=학번, major_id=전공, major_type=전공_유형)
        
        return render(request, 'requirements.html', {'requirements': requirements})
    else:
        return render(request, 'input_requirements.html')
