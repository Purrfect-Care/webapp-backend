from django.db import models

# Define the 'gatunki' model
class Gatunek(models.Model):
    nazwa_gatunku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nazwa_gatunku

# Define the 'rasy' model
class Rasa(models.Model):
    nazwa_rasy = models.CharField(max_length=50, unique=True)
    rasy_id_gatunku = models.ForeignKey(Gatunek, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa_rasy

# Define the 'opiekunowie' model
class Opiekun(models.Model):
    imie_opiekuna = models.CharField(max_length=50)
    nazwisko_opiekuna = models.CharField(max_length=50)
    adres_opiekuna = models.CharField(max_length=255)
    kod_pocztowy_opiekuna = models.CharField(max_length=20)
    miasto_opiekuna = models.CharField(max_length=50)
    telefon_opiekuna = models.CharField(max_length=20, unique=True)
    email_opiekuna = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.imie_opiekuna} {self.nazwisko_opiekuna}"

# Define the 'choroby' model
class Choroba(models.Model):
    nazwa_choroby = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nazwa_choroby

# Define the 'gabinety' model
class Gabinet(models.Model):
    nazwa_gabinetu = models.CharField(max_length=150, unique=True)
    adres_gabinetu = models.CharField(max_length=255)
    kod_pocztowy_gabinetu = models.CharField(max_length=20)
    miasto_gabinetu = models.CharField(max_length=50)
    telefon_gabinetu = models.CharField(max_length=20, unique=True)
    email_gabinetu = models.EmailField(unique=True)

    def __str__(self):
        return self.nazwa_gabinetu

# Define the 'pacjenci' model
class Pacjent(models.Model):
    imie_pacjenta = models.CharField(max_length=255)
    PLEC_CHOICES = [('male', 'Male'), ('female', 'Female')]
    plec_pacjenta = models.CharField(max_length=10, choices=PLEC_CHOICES)
    data_urodzenia_pacjenta = models.DateField()
    pacjenci_id_opiekuna = models.ForeignKey(Opiekun, on_delete=models.CASCADE)
    pacjenci_id_gatunku = models.ForeignKey(Gatunek, on_delete=models.CASCADE)
    pacjenci_id_rasy = models.ForeignKey(Rasa, on_delete=models.CASCADE)

    def __str__(self):
        return self.imie_pacjenta

# Define the 'historie_chorob' model
class HistoriaChoroby(models.Model):
    historie_chorob_id_pacjenta = models.ForeignKey(Pacjent, on_delete=models.CASCADE)
    historie_chorob_id_choroby = models.ForeignKey(Choroba, on_delete=models.CASCADE)
    data_rozpoczecia_choroby = models.DateField()

# Define the 'leki' model
class Lek(models.Model):
    nazwa_leku = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nazwa_leku

# Define the 'typy_wizyty' model
class TypWizyty(models.Model):
    nazwa_typu_wizyty = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nazwa_typu_wizyty

# Define the 'podtypy_wizyty' model
class PodtypWizyty(models.Model):
    nazwa_podtypu_wizyty = models.CharField(max_length=100, unique=True)
    podtypy_wizyty_id_typu_wizyty = models.ForeignKey(TypWizyty, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa_podtypu_wizyty

# Define the 'pracownicy' model
class Pracownik(models.Model):
    rola_pracownika = models.CharField(max_length=100)
    imie_pracownika = models.CharField(max_length=50)
    nazwisko_pracownika = models.CharField(max_length=50)
    adres_pracownika = models.CharField(max_length=255)
    kod_pocztowy_pracownika = models.CharField(max_length=20)
    miasto_pracownika = models.CharField(max_length=50)
    telefon_pracownika = models.CharField(max_length=20, unique=True)
    email_pracownika = models.EmailField(unique=True)
    haslo_pracownika = models.CharField(max_length=64, unique=True)  # Store hashed passwords here
    pracownicy_id_gabinetu = models.ForeignKey(Gabinet, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.imie_pracownika} {self.nazwisko_pracownika}"

# Define the 'wizyty' model
class Wizyta(models.Model):
    data_godzina_wizyty = models.DateTimeField()
    czas_trwania_wizyty = models.TimeField()
    wizyty_id_pacjenta = models.ForeignKey(Pacjent, on_delete=models.CASCADE)
    wizyty_id_typu_wizyty = models.ForeignKey(TypWizyty, on_delete=models.CASCADE)
    wizyty_id_podtypu_wizyty = models.ForeignKey(PodtypWizyty, on_delete=models.CASCADE)
    wizyty_id_pracownika = models.ForeignKey(Pracownik, on_delete=models.CASCADE)
    STATUS_CHOICES = [('zaplanowana', 'Zaplanowana'), ('odwolana', 'Odwolana'), ('zakonczona', 'Zakonczona')]
    status_wizyty = models.CharField(max_length=20, choices=STATUS_CHOICES)
    opis_wizyty = models.TextField()
    masa_pacjenta = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    wzrost_pacjenta = models.DecimalField(max_digits=5, decimal_places=2, null=True)

# Define the 'zdjecia' model
class Zdjecie(models.Model):
    zdjecia_id_wizyty = models.ForeignKey(Wizyta, on_delete=models.CASCADE)
    opis_zdjecia = models.TextField()

# Define the 'recepty' model
class Recepta(models.Model):
    recepty_id_wizyty = models.ForeignKey(Wizyta, on_delete=models.CASCADE)
    recepty_id_pacjenta = models.ForeignKey(Pacjent, on_delete=models.CASCADE)
    data_wydania_recepty = models.DateField()

# Define the 'leki_na_recepcie' model
class LekNaRecepcji(models.Model):
    leki_na_recepcie_id_recepty = models.ForeignKey(Recepta, on_delete=models.CASCADE)
    leki_na_recepcie_id_leku = models.ForeignKey(Lek, on_delete=models.CASCADE)
    ilosc_leku = models.PositiveIntegerField()
