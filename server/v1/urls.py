from django.urls import path

from . import views

authorisation_urlpatterns = (
    path('register/', views.RegisterAPIView.as_view()),
)

urlpatterns = (
    *authorisation_urlpatterns,

)
