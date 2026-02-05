from django.contrib import admin


from main.models import *

admin.site.register(
    [
        Talaba,
        Muallif,
        Kitob,
        Kutubxonachi,
        Record
    ]
)