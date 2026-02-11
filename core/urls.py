from django.contrib import admin
from django.urls import path

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hello/', hello_view, name='hello'),

    path('', home_view, name='home'),

    path('students/', students_view, name='students'),

    path('students/<int:student_id>/', student_details_view),

    path('mualliflar/', mualliflar_view, name='mualliflar'),

    path('mualliflar/<int:muallif_id>/', muallif_view),

]