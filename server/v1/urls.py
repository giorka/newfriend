from django.urls import path

from . import views

authorisation_urlpatterns = (
    path('register/', views.RegisterAPIView.as_view()),
    path('verify/', views.VerifyAPIView.as_view()),
    path('logout/', views.LogoutAPIView.as_view()),

)

urlpatterns = (
    *authorisation_urlpatterns,

)
