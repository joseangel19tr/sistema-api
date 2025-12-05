from django.db.models import *
from rest_framework import permissions, generics, status
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from app_escolar_api.models import Materias, Maestros
from app_escolar_api.serializers import MateriasSerializer


def usuario_es_admin(user):
    return user.is_authenticated and user.groups.filter(name='administrador').exists()


def usuario_es_maestro(user):
    return user.is_authenticated and user.groups.filter(name='maestro').exists()


class MateriasListCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MateriasSerializer

    # GET: listar materias
    def get(self, request, *args, **kwargs):
        # Admin y maestros pueden ver la lista
        if not (usuario_es_admin(request.user) or usuario_es_maestro(request.user)):
            return Response({"detail": "No tienes permiso para ver materias."}, status=status.HTTP_403_FORBIDDEN)

        materias = Materias.objects.all().order_by("nrc")
        data = MateriasSerializer(materias, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    # POST: crear materia (solo admin)
    def post(self, request, *args, **kwargs):
        if not usuario_es_admin(request.user):
            return Response({"detail": "Solo el administrador puede registrar materias."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MateriasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MateriasDetailView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MateriasSerializer

    def get_object(self, nrc):
        return get_object_or_404(Materias, nrc=nrc)

    # GET una materia
    def get(self, request, nrc, *args, **kwargs):
        if not (usuario_es_admin(request.user) or usuario_es_maestro(request.user)):
            return Response({"detail": "No tienes permiso para ver materias."}, status=status.HTTP_403_FORBIDDEN)
        materia = self.get_object(nrc)
        data = MateriasSerializer(materia).data
        return Response(data, status=status.HTTP_200_OK)

    # PUT actualizar (solo admin)
    def put(self, request, nrc, *args, **kwargs):
        if not usuario_es_admin(request.user):
            return Response({"detail": "Solo el administrador puede editar materias."},
                            status=status.HTTP_403_FORBIDDEN)
        materia = self.get_object(nrc)
        serializer = MateriasSerializer(materia, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE eliminar (solo admin)
    def delete(self, request, nrc, *args, **kwargs):
        if not usuario_es_admin(request.user):
            return Response({"detail": "Solo el administrador puede eliminar materias."},
                            status=status.HTTP_403_FORBIDDEN)
        materia = self.get_object(nrc)
        materia.delete()
        return Response({"detail": "Materia eliminada correctamente."}, status=status.HTTP_204_NO_CONTENT)
