from django.shortcuts import render, redirect
from django.http import Http404

from .models import *


def home_view(request):
    return render(request, "home.html")


def hello_view(request):
    return render(request, "home.html")


# -------------------------
# Talabalar: list + sort
# -------------------------
def students_view(request):
    sort = (request.GET.get("sort") or "ism").strip()

    allowed = {
        "ism": "ism",
        "-ism": "-ism",
        "kurs": "kurs",
        "-kurs": "-kurs",
    }
    order_by = allowed.get(sort, "ism")

    talabalar = Talaba.objects.all().order_by(order_by)

    return render(request, "students.html", {
        "talabalar": talabalar,
        "sort": sort,
    })


def student_details_view(request, student_id):
    try:
        talaba = Talaba.objects.get(id=student_id)
    except Talaba.DoesNotExist:
        raise Http404("Talaba topilmadi")

    return render(request, "student.html", {"talaba": talaba})


# -------------------------
# Mualliflar: search + detail + delete
# -------------------------
def mualliflar_view(request):
    q = (request.GET.get("q") or "").strip()

    mualliflar = Muallif.objects.all()

    if q:
        mualliflar = mualliflar.filter(ism__icontains=q)

    mualliflar = mualliflar.order_by("ism")

    return render(request, "mualliflar.html", {
        "mualliflar": mualliflar,
        "q": q,
    })


def muallif_view(request, muallif_id):
    try:
        muallif = Muallif.objects.get(id=muallif_id)
    except Muallif.DoesNotExist:
        raise Http404("Muallif topilmadi")

    kitoblar = Kitob.objects.filter(muallif=muallif).order_by("nom")

    return render(request, "muallif.html", {
        "muallif": muallif,
        "kitoblar": kitoblar,
    })


def muallif_delete_view(request, muallif_id):
    try:
        muallif = Muallif.objects.get(id=muallif_id)
    except Muallif.DoesNotExist:
        raise Http404("Muallif topilmadi")

    if request.method == "POST":
        muallif.delete()
        return redirect("mualliflar")

    return render(request, "confirm_delete.html", {
        "title": "Muallifni o‘chirish",
        "object_name": muallif.ism,
        "back_url_name": "muallif_detail",
        "back_url_id": muallif.id,
    })


# -------------------------
# Recordlar: search + delete
# -------------------------
def records_view(request):
    q = (request.GET.get("q") or "").strip()

    records = Record.objects.select_related("talaba", "kitob", "kutubxonachi").all()

    if q:
        records = records.filter(talaba__ism__icontains=q)

    records = records.order_by("-olingan_sana")

    return render(request, "records.html", {
        "records": records,
        "q": q,
    })


def record_delete_view(request, record_id):
    try:
        record = Record.objects.select_related("talaba", "kitob").get(id=record_id)
    except Record.DoesNotExist:
        raise Http404("Record topilmadi")

    if request.method == "POST":
        record.delete()
        return redirect("records")

    return render(request, "confirm_delete.html", {
        "title": "Recordni o‘chirish",
        "object_name": str(record),
        "back_url_name": "records",
        "back_url_id": None,
    })


# -------------------------
# 1) Talaba qo'shish
# -------------------------
def talaba_create_view(request):
    if request.method == "POST":
        ism = (request.POST.get("ism") or "").strip()
        guruh = (request.POST.get("guruh") or "").strip()
        kurs = (request.POST.get("kurs") or "").strip()
        kitob_soni = (request.POST.get("kitob_soni") or "").strip()

        errors = []
        if not ism:
            errors.append("Ism kiritilishi shart.")
        if kurs and not kurs.isdigit():
            errors.append("Kurs faqat son bo‘lishi kerak.")
        if kitob_soni and not kitob_soni.isdigit():
            errors.append("Kitob soni faqat son bo‘lishi kerak.")

        if not errors:
            Talaba.objects.create(
                ism=ism,
                guruh=guruh or None,
                kurs=int(kurs) if kurs else 1,
                kitob_soni=int(kitob_soni) if kitob_soni else 0,
            )
            return redirect("students")

        return render(request, "talaba_create.html", {"errors": errors, "data": request.POST})

    return render(request, "talaba_create.html")


# -------------------------
# 2) Kitob qo'shish
# -------------------------
def kitob_create_view(request):
    mualliflar = Muallif.objects.all().order_by("ism")

    if request.method == "POST":
        nom = (request.POST.get("nom") or "").strip()
        janr = (request.POST.get("janr") or "").strip()
        sahifa = (request.POST.get("sahifa") or "").strip()
        muallif_id = (request.POST.get("muallif_id") or "").strip()

        errors = []
        if not nom:
            errors.append("Kitob nomi kiritilishi shart.")
        if not janr:
            errors.append("Janr kiritilishi shart.")
        if not sahifa or not sahifa.isdigit():
            errors.append("Sahifa son bo‘lishi shart.")
        if not muallif_id or not muallif_id.isdigit():
            errors.append("Muallif tanlanishi shart.")

        muallif = None
        if muallif_id.isdigit():
            try:
                muallif = Muallif.objects.get(id=int(muallif_id))
            except Muallif.DoesNotExist:
                errors.append("Muallif topilmadi.")

        if not errors:
            Kitob.objects.create(
                nom=nom,
                janr=janr,
                sahifa=int(sahifa),
                muallif=muallif,
            )
            return redirect("home")

        return render(request, "kitob_create.html", {
            "errors": errors,
            "data": request.POST,
            "mualliflar": mualliflar,
        })

    return render(request, "kitob_create.html", {"mualliflar": mualliflar})


# -------------------------
# 3) Muallif qo'shish
# -------------------------
def muallif_create_view(request):
    jins_choices = Muallif.JINS  # (("Erkak,", "Erkak"), ("Ayol","Ayol"))

    if request.method == "POST":
        ism = (request.POST.get("ism") or "").strip()
        jins = (request.POST.get("jins") or "").strip()
        t_sana = (request.POST.get("t_sana") or "").strip()
        kitob_soni = (request.POST.get("kitob_soni") or "").strip()
        tirik = request.POST.get("tirik") == "on"

        allowed_jins = [c[0] for c in jins_choices]

        errors = []
        if not ism:
            errors.append("Ism kiritilishi shart.")
        if jins not in allowed_jins:
            errors.append("Jins noto‘g‘ri tanlangan.")
        if kitob_soni and (not kitob_soni.isdigit()):
            errors.append("Kitob soni son bo‘lishi kerak.")
        # t_sana bo'sh bo'lsa ham mumkin (null)
        # format HTML date: YYYY-MM-DD

        if not errors:
            Muallif.objects.create(
                ism=ism,
                jins=jins,
                t_sana=t_sana or None,
                kitob_soni=int(kitob_soni) if kitob_soni else None,
                tirik=tirik,
            )
            return redirect("mualliflar")

        return render(request, "muallif_create.html", {
            "errors": errors,
            "data": request.POST,
            "jins_choices": jins_choices,
        })

    return render(request, "muallif_create.html", {"jins_choices": jins_choices})


# -------------------------
# 4) Record qo'shish
# -------------------------
def record_create_view(request):
    talabalar = Talaba.objects.all().order_by("ism")
    kitoblar = Kitob.objects.all().order_by("nom")
    kutubxonachilar = Kutubxonachi.objects.all().order_by("ism")

    if request.method == "POST":
        talaba_id = (request.POST.get("talaba_id") or "").strip()
        kitob_id = (request.POST.get("kitob_id") or "").strip()
        kutubxonachi_id = (request.POST.get("kutubxonachi_id") or "").strip()
        qaytargan_sana = (request.POST.get("qaytargan_sana") or "").strip()

        errors = []
        if not talaba_id.isdigit():
            errors.append("Talaba tanlanishi shart.")
        if not kitob_id.isdigit():
            errors.append("Kitob tanlanishi shart.")
        if not kutubxonachi_id.isdigit():
            errors.append("Kutubxonachi tanlanishi shart.")

        talaba = kitob = kutubxonachi = None

        if talaba_id.isdigit():
            try:
                talaba = Talaba.objects.get(id=int(talaba_id))
            except Talaba.DoesNotExist:
                errors.append("Talaba topilmadi.")

        if kitob_id.isdigit():
            try:
                kitob = Kitob.objects.get(id=int(kitob_id))
            except Kitob.DoesNotExist:
                errors.append("Kitob topilmadi.")

        if kutubxonachi_id.isdigit():
            try:
                kutubxonachi = Kutubxonachi.objects.get(id=int(kutubxonachi_id))
            except Kutubxonachi.DoesNotExist:
                errors.append("Kutubxonachi topilmadi.")

        if not errors:
            Record.objects.create(
                talaba=talaba,
                kitob=kitob,
                kutubxonachi=kutubxonachi,
                qaytargan_sana=qaytargan_sana or None,
            )
            return redirect("records")

        return render(request, "record_create.html", {
            "errors": errors,
            "data": request.POST,
            "talabalar": talabalar,
            "kitoblar": kitoblar,
            "kutubxonachilar": kutubxonachilar,
        })

    return render(request, "record_create.html", {
        "talabalar": talabalar,
        "kitoblar": kitoblar,
        "kutubxonachilar": kutubxonachilar,
    })


# -------------------------
# 5) Kutubxonachi qo'shish (ish_vaqti select)
# -------------------------
def kutubxonachi_create_view(request):
    # select uchun variantlar (HH:MM)
    time_options = [
        "08:00", "09:00", "10:00", "11:00", "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00",
    ]

    if request.method == "POST":
        ism = (request.POST.get("ism") or "").strip()
        ish_vaqti = (request.POST.get("ish_vaqti") or "").strip()

        errors = []
        if not ism:
            errors.append("Ism kiritilishi shart.")
        if ish_vaqti and ish_vaqti not in time_options:
            errors.append("Ish vaqti noto‘g‘ri tanlangan.")

        if not errors:
            Kutubxonachi.objects.create(
                ism=ism,
                ish_vaqti=ish_vaqti or None,
            )
            return redirect("home")

        return render(request, "kutubxonachi_create.html", {
            "errors": errors,
            "data": request.POST,
            "time_options": time_options,
        })

    return render(request, "kutubxonachi_create.html", {"time_options": time_options})


