from django.urls import path
from classrooms import views


app_name = "classrooms"
urlpatterns = [
    path("", views.home, name="home"),
    path("create_class_request/", views.create_class_request, name="create_class"),
    path("join_class_request/", views.join_class_request, name="join_class"),
    path('class/<int:id>',views.render_class,name='render_class'),
    path('create_assignment/<int:classroom_id>',views.create_assignment,name='create_assignment'),
    path('assignment_summary/<int:assignment_id>',views.assignment_summary,name='assignment_summary'),
    path('delete_assignment/<int:assignment_id>',views.delete_assignment,name='delete_assignment'),
    path('unenroll_class/<int:classroom_id>',views.unenroll_class,name='unenroll_class'),
    path('delete_class/<int:classroom_id>',views.delete_class,name='delete_class'),
    path('submit_assignment_request/<int:assignment_id>',views.submit_assignment_request,name='submit_assignment_request'),
    path('mark_submission_request/<int:submission_id>/<int:teacher_id>',views.mark_submission_request,name='mark_submission_request'),
    path('add_course/<int:classroom_id>',views.add_course,name='add_course'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('join/', views.join_room, name='join_room'),

]