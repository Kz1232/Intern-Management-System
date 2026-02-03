from django.urls import path ,include 
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet,basename='task')

urlpatterns = [
    path('user_register/',views.user_register,name='user_register'),
    path('sign_in/',views.SignInView.as_view(),name="sign_in"),
    path('sign_out/',views.SignOutView.as_view(),name="sign_out"),

    path('mark_attendence/',views.mark_attendence,name="mark_attendence"),

    path('',include(router.urls)),
]