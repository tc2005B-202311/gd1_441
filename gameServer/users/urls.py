from django.urls import path

from . import views

urlpatterns = [
    path('create-user', views.CreateUser.as_view(), name = 'create-user'),
    path('validate-user/<str:mail>/<str:password>', views.ValidateUser.as_view(), name = 'validate-user'),
    path('view-user/<str:mail>', views.ViewUser.as_view(), name = 'view-user'),
    path('update-user', views.UpdateUser.as_view(), name = 'update-user'),
    path('delete-user', views.DeleteUser.as_view(), name = 'delete-user'),
    path('create-log', views.GameLogRegister.as_view(), name = 'create-log'),
    path('view-logs-student/<int:difficulty>/<str:classroom>/<int:role_number>/', views.ViewStudentLogs.as_view(), name = 'view-logs-student'),
    path('view-logs-student-chart/<int:difficulty>/<str:classroom>/<int:role_number>/<int:level>', views.ViewStudentLogsChart.as_view(), name = 'view-logs-student-chart'),
]