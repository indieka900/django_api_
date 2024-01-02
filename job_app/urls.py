from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.Job_list, name='Jobs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', views.UserRegistrationView.as_view(), name='users'),
    path('jobs/<str:pk>', views.get_job),
    path('job', views.searchJob),
    path('users/<str:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('bookmarks/<str:pk>', views.BookmarkView.as_view()),
    path('bookmark/delete/<str:pk>', views.delete_bookmark),
    path('job/<str:pk>', views.JobCreationView.as_view(), name='job-creation'),
    path('jobs/<str:pk>/<str:user_pk>', views.JobDetail.as_view(), name='job'),
    path('login', views.UserLoginView.as_view(), name='user-login'),
]
