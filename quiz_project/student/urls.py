from django.urls import path
from student import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('studentlogin/', LoginView.as_view(template_name='student/studentlogin.html'),name='studentlogin'),
    path('studentsignup/', views.student_signup,name='studentsignup'),
    path('studentclick/', views.studentclick, name='studentclick'),
    path('student-dashboard/', views.student_dashboard_view,
         name='student-dashboard'),
    
    path('student-exam', views.student_exam_view, name='student-exam'),
    path('take-exam/<int:pk>', views.take_exam_view, name='take-exam'),
    # path('start-exam/<int:pk>/', views.start_exam_view, name='start-exam'),
    path('start-exam/<int:pk>/<str:lv>/',views.start_exam_view, name='start-exam'),

    path('calculate-marks/<str:lv>/', views.calculate_marks_view, name='calculate-marks'),
    path('view-result', views.view_result_view, name='view-result'),
    path('check-marks/<int:pk>', views.check_marks_view, name='check-marks'),
    path('student-marks', views.student_marks_view, name='student-marks'),
    path('update-profile/',
         views.update_student_view, name='update-profile'),
     
    path('certificate/<int:pk>', views.get_certificate, name='certificate'),
    path('feedback/<int:pk>/<str:lv>', views.feedback, name='feedback'),

]
