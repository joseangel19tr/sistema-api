from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'


class MateriasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materias
        fields = "__all__"

    def validate_nrc(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El NRC solo debe contener dígitos.")
        if len(value) not in (5, 6):
            raise serializers.ValidationError("El NRC debe tener 5 o 6 dígitos.")
        return value

    def validate_nombre_materia(self, value):
        import re
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$', value):
            raise serializers.ValidationError("El nombre solo puede contener letras y espacios.")
        return value

    def validate_seccion(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("La sección solo debe contener números.")
        if len(value) > 3:
            raise serializers.ValidationError("La sección debe tener máximo 3 dígitos.")
        return value

    def validate_salon(self, value):
        import re
        if len(value) > 15:
            raise serializers.ValidationError("El salón no puede tener más de 15 caracteres.")
        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise serializers.ValidationError("El salón solo admite caracteres alfanuméricos y espacios.")
        return value

    def validate_creditos(self, value):
        if value <= 0 or value > 99:
            raise serializers.ValidationError("Los créditos deben ser un entero positivo de máximo dos dígitos.")
        return value

    def validate(self, attrs):
        # Validar que hora_inicio < hora_fin
        hora_inicio = attrs.get('hora_inicio')
        hora_fin = attrs.get('hora_fin')
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError("La hora de inicio debe ser menor a la hora de fin.")
        # Validar que haya al menos un día
        dias = attrs.get('dias', '')
        if not dias:
            raise serializers.ValidationError("Debes seleccionar al menos un día.")
        return attrs
