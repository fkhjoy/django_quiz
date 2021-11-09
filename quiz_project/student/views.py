from django.shortcuts import render,redirect,reverse

from quiz_app.models import Feedback
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz_app import models as QMODEL
from django.views.decorators.csrf import csrf_exempt
from student import models as SMODEL
from student import forms as SFORM
from django.template.loader import get_template
from xhtml2pdf import pisa
from quiz_app.forms import FeedbackForm

def studentclick(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup(request):

    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save(commit=False)
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return redirect('studentlogin')
    return render(request,'student/studentsignup.html', context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def afterlogin_view(request):
    if is_student(request.user):
        return redirect('student/student-dashboard')
    else:
        return redirect('admin-dashboard')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def student_dashboard_view(request):
    dict = {

        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
    }
    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0

    student = models.Student.objects.get(user_id=request.user.id)
    level = QMODEL.Level.objects.filter(student=student, exam=course)
    lev = 0

    if len(level) == 0:
        QMODEL.Level.objects.create(student=student, exam=course)

    else:
        lev = level[0].level
    
    print("lev", lev)

    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html', {'level':lev, 'course': course, 'total_questions': total_questions, 'total_marks': total_marks})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def start_exam_view(request, pk, lv=None):
    course = QMODEL.Course.objects.get(id=pk)
    if lv == 'Beginner':
        level = 0
    elif lv == 'Expert':
        level = 2
    else:
        level = 1

    student = models.Student.objects.get(user_id=request.user.id)
    st_level = QMODEL.Level.objects.filter(student=student, exam=course)[0].level
    questions = QMODEL.Question.objects.all().filter(course=course, level=lv)
    if st_level < level:
        return redirect('student-exam')
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html',
                      {'course': course, 'questions': questions, 'level': lv, 'id':course.id})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
@csrf_exempt
def calculate_marks_view(request, lv):

    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0
        total = 0
        questions = QMODEL.Question.objects.all().filter(course=course, level=lv)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            total_marks = total_marks + questions[i].marks
            if selected_ans == actual_answer:                
                total += questions[i].marks
                
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total
        result.exam = course
        result.student = student
        level = QMODEL.Level.objects.filter(student=student, exam=course)[0]

        print(total_marks, total)
        if total_marks == total:
            level.level = min(3, level.level+1)
            level.save()

        # else:
        #     level = QMODEL.models.Level.objects.create(student=student, exam=course)
        #     if total_marks >= 0.6*total:
        #         level.level = 1
        #         level.save()


        result.save()

    if request.method == 'POST' :
        exam = QMODEL.Course.objects.get(id=course_id)
        form = FeedbackForm(request.POST)

        if form.is_valid():
            form_ = form.save(commit=False)
            form_.exam = exam
            form_.lv = lv
            form_.student = student
            form_.save()
            return redirect('view-result')

    return redirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    student = models.Student.objects.get(user_id=request.user.id)
    level = QMODEL.Level.objects.filter(student=student, exam=courses)
    return render(request, 'student/view_result.html', {'courses': courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(
        exam=course).filter(student=student)
    # difficulty = QMODEL.Level.objects.all().filter(exam=course, student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', {'courses': courses})


@login_required(login_url='studentlogin')
def update_student_view(request):

    user = SMODEL.User.objects.get(id=request.user.id)
    student = SMODEL.Student.objects.get(id=user.student.id)
    
    userForm = SFORM.StudentUserForm(instance=user)
    studentForm = SFORM.StudentForm(request.FILES, instance=student)
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = SFORM.StudentUserForm(request.POST, instance=user)
        studentForm = SFORM.StudentForm(
            request.POST, request.FILES, instance=student)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            studentForm.save()
            return redirect('student-dashboard')
    return render(request, 'student/update_student.html', context=mydict)

def get_certificate(request, pk):
    name = request.user.first_name +" "+ request.user.last_name
    course = QMODEL.Course.objects.get(id=pk)
    template = get_template('student/certificate.html')

    student = models.Student.objects.get(user_id=request.user.id)
    st_level = QMODEL.Level.objects.filter(
        student=student, exam=course)[0].level

    if st_level < 3:
        return redirect('student-exam')

    context = {
        'name':name,
        'course':course.course_name,
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{name}_{course}.pdf"'

    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@csrf_exempt
def feedback(request, pk, lv):

    # if request.method == 'POST':
    #     exam = QMODEL.Course.objects.get(id=pk)
    #     form = FeedbackForm(request.POST)
        
    #     if form.is_valid():
    #         form_ = form.save(commit=False)
    #         form_.exam = exam 
    #         form_.save()
    #         return redirect('calculate-marks', lv)
    # else:
    form = FeedbackForm()

    return render(request, 'student/feedback.html', {'form': form, 'lv':lv})

