from django.urls import path
from quiz_app import views
from django.contrib.auth.views import LogoutView, LoginView
# from .views import home_view, login, signup

urlpatterns = [

    path('', views.home_view, name=''),
    path('logout', LogoutView.as_view(
        template_name='quiz_app/logout.html'), name='logout'),
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    path('afterlogin', views.afterlogin_view, name='afterlogin'),



    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(
        template_name='quiz_app/adminlogin.html'), name='adminlogin'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    

    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-view-student', views.admin_view_student_view,
         name='admin-view-student'),
    path('admin-view-student-marks', views.admin_view_student_marks_view,
         name='admin-view-student-marks'),
    path('admin-view-marks/<int:pk>',
         views.admin_view_marks_view, name='admin-view-marks'),
    path('admin-check-marks/<int:pk>',
         views.admin_check_marks_view, name='admin-check-marks'),
    path('update-student/<int:pk>',
         views.update_student_view, name='update-student'),
    path('delete-student/<int:pk>',
         views.delete_student_view, name='delete-student'),

    path('admin-course', views.admin_course_view, name='admin-course'),
    path('admin-add-course', views.admin_add_course_view, name='admin-add-course'),
    path('admin-view-course', views.admin_view_course_view,
         name='admin-view-course'),
    path('delete-course/<int:pk>', views.delete_course_view, name='delete-course'),
    path('edit-course/<int:pk>', views.edit_course_view, name='edit-course'),

    path('admin-question', views.admin_question_view, name='admin-question'),
    path('admin-add-question', views.admin_add_question_view,
         name='admin-add-question'),
    path('admin-view-question', views.admin_view_question_view,
         name='admin-view-question'),
    path('view-question/<int:pk>', views.view_question_view, name='view-question'),
    path('edit-question/<int:pk>', views.edit_question_view, name='edit-question'),
    path('delete-question/<int:pk>',
         views.delete_question_view, name='delete-question'),
]
