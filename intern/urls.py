from django.urls import path ,include 
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet,basename='task')

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('app/user_register/',views.user_register,name='user_register'),
    path('app/sign_in/',views.SignInView.as_view(),name="sign_in"),
    path('app/sign_out/',views.SignOutView.as_view(),name="sign_out"),

    path('app/mark_attendence/',views.mark_attendence,name="mark_attendence"),

    path('app/',include(router.urls)),
]