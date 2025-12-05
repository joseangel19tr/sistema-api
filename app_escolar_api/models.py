from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin " + self.user.first_name + " " + self.user.last_name


class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255, null=True, blank=True)
    curp = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255, null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno " + self.user.first_name + " " + self.user.last_name


class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=255, null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255, null=True, blank=True)
    cubiculo = models.CharField(max_length=255, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    area_investigacion = models.CharField(max_length=255, null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del maestro " + self.user.first_name + " " + self.user.last_name


class Materias(models.Model):
    id = models.BigAutoField(primary_key=True)
    # NRC: numérico, único
    nrc = models.CharField(max_length=6, unique=True)

    nombre_materia = models.CharField(max_length=255)
    seccion = models.CharField(max_length=3)

    # guardamos los días seleccionados como texto tipo "Lunes,Miércoles,Viernes"
    dias = models.CharField(max_length=100)

    # usamos solo hora, sin fecha
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    salon = models.CharField(max_length=15)

    # programa educativo: 3 opciones
    PROGRAMA_CHOICES = (
        ('ICC', 'Ingeniería en Ciencias de la Computación'),
        ('LCC', 'Licenciatura en Ciencias de la Computación'),
        ('ITI', 'Ingeniería en Tecnologías de la Información'),
    )
    programa_educativo = models.CharField(max_length=3, choices=PROGRAMA_CHOICES)

    # relacionamos con perfil de maestro
    profesor = models.ForeignKey('Maestros', on_delete=models.PROTECT, related_name='materias')

    creditos = models.PositiveIntegerField()

    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.nrc} - {self.nombre_materia}"
