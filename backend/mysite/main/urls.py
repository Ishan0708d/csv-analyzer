from django.urls import path
from .views import health_check, register, upload_csv

urlpatterns = [
    path("health/", health_check),
    path("register/", register),
    path("upload/", upload_csv)
]
