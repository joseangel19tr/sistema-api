from django.db.models import *
from django.db import transaction
from app_escolar_api.serializers import UserSerializer
from app_escolar_api.serializers import *
from app_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


class AlumnosAll(generics.CreateAPIView):
    
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        alumnos = Alumnos.objects.filter(user__is_active = 1).order_by("id")
        lista = AlumnoSerializer(alumnos, many=True).data
        
        return Response(lista, 200)
    
class AlumnosView(generics.GenericAPIView):
    serializer_class = AlumnoSerializer
    queryset = Alumnos.objects.all()

    def get_permissions(self):
        if self.request.method in ["GET", "PUT", "DELETE"]:
            return [permissions.IsAuthenticated()]
        return []

    
    def get(self, request, *args, **kwargs):
        id_alumno = request.GET.get("id")
        if not id_alumno:
            return Response({"message": "Falta el ID"}, 400)

        alumno = get_object_or_404(Alumnos, id=id_alumno)
        serializer = AlumnoSerializer(alumno, many=False)
        return Response(serializer.data, 200)

    # Registrar nuevo
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            role = request.data['rol']

            existing_user = User.objects.filter(email=request.data['email']).first()
            if existing_user:
                return Response({"message": "Username taken"}, 400)

            user = User.objects.create(
                username=request.data['email'],
                email=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                is_active=1
            )
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            user.save()

            alumno = Alumnos.objects.create(
                user=user,
                matricula=request.data["matricula"],
                curp=request.data["curp"].upper(),
                rfc=request.data["rfc"].upper(),
                fecha_nacimiento=request.data["fecha_nacimiento"],
                edad=request.data["edad"],
                telefono=request.data["telefono"],
                ocupacion=request.data["ocupacion"]
            )
            alumno.save()

            return Response({"Alumno creado con ID": alumno.id}, 201)

        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)


    @transaction.atomic
    def put(self, request, *args, **kwargs):
        alumno = get_object_or_404(Alumnos, id=request.data["id"])

        alumno.matricula = request.data["matricula"]
        alumno.curp = request.data["curp"]
        alumno.rfc = request.data["rfc"]
        alumno.fecha_nacimiento = request.data["fecha_nacimiento"]
        alumno.edad = request.data["edad"]
        alumno.telefono = request.data["telefono"]
        alumno.ocupacion = request.data["ocupacion"]
        alumno.save()

        user = alumno.user
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.save()

        return Response({"message": "Alumno actualizado correctamente"}, 200)

    def delete(self, request, *args, **kwargs):
        alumno_id = request.GET.get("id")
        if not alumno_id:
            return Response({"error": "ID no proporcionado"}, status=400)

        try:
            alumno = Alumnos.objects.get(id=alumno_id)
            alumno.delete()
            return Response({"message": "Alumno eliminado"}, status=200)
        except Alumnos.DoesNotExist:
            return Response({"error": "Alumno no encontrado"}, status=404)