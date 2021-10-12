from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentlogin/', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
    path('studentsignup/', views.student_signup,name='studentsignup'),
    path('studentclick/', views.studentclick, name='studentclick'),
]