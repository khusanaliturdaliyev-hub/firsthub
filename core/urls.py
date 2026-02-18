from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.home_view, name="home"),
    path("hello/", views.hello_view, name="hello"),

    path("students/", views.students_view, name="students"),
    path("students/<int:student_id>/", views.student_details_view, name="student_detail"),

    path("mualliflar/", views.mualliflar_view, name="mualliflar"),
    path("mualliflar/<int:muallif_id>/", views.muallif_view, name="muallif_detail"),
    path("mualliflar/<int:muallif_id>/delete/", views.muallif_delete_view, name="muallif_delete"),

    path("records/", views.records_view, name="records"),
    path("records/<int:record_id>/delete/", views.record_delete_view, name="record_delete"),

    path("students/create/", views.talaba_create_view, name="talaba_create"),
    path("mualliflar/create/", views.muallif_create_view, name="muallif_create"),
    path("kitoblar/create/", views.kitob_create_view, name="kitob_create"),
    path("records/create/", views.record_create_view, name="record_create"),
    path("kutubxonachilar/create/", views.kutubxonachi_create_view, name="kutubxonachi_create"),

]
