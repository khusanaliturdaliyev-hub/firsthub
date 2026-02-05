from django.db import models

class Talaba(models.Model):
    ism = models.CharField(max_length=255)
    guruh = models.CharField(max_length=255, blank=True, null=True)
    kurs = models.PositiveIntegerField(default=1)
    kitob_soni = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.ism

    class Meta:
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabas'

class Muallif(models.Model):
    JINS = (
        ("Erkak," , "Erkak"),
        ("Ayol", "Ayol"),
    )
    ism = models.CharField(max_length=255)
    jins = models.CharField(max_length=20, choices=JINS)
    t_sana = models.DateField(blank=True, null=True)
    kitob_soni = models.PositiveSmallIntegerField(blank=True, null=True)
    tirik = models.BooleanField(default=False)

    def __str__(self):
        return self.ism

    class Meta:
        verbose_name = 'Muallif'
        verbose_name_plural = 'Mualliflar'

class Kitob(models.Model):
    nom = models.CharField(max_length=255)
    janr = models.CharField(max_length=50)
    sahifa = models.PositiveSmallIntegerField()
    muallif = models.ForeignKey(Muallif, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'

class Kutubxonachi(models.Model):
    ism = models.CharField(max_length=255)
    ish_vaqti = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.ism

    class Meta:
        verbose_name = 'Kutubxonachi'
        verbose_name_plural = 'Kutubxonachilar'

class Record(models.Model):
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE)
    kitob = models.ForeignKey(Kitob, on_delete=models.CASCADE)
    kutubxonachi = models.ForeignKey(Kutubxonachi, on_delete=models.CASCADE)
    olingan_sana = models.DateTimeField(auto_now_add=True)
    qaytargan_sana = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.talaba.ism} -- {self.kitob.nom}"

    class Meta:
        verbose_name = 'Record Talaba'
        verbose_name_plural = 'Record Talabalar'



