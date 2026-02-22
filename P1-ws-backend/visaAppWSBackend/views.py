from django.forms import model_to_dict
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Pago, Tarjeta
from .pagoDB import eliminar_pago, get_pagos_from_db, registrar_pago, verificar_tarjeta
from .serializers import PagoSerializer


class PagoView(APIView):
    def delete(self, request, id_pago):
        if eliminar_pago(id_pago) is False:
            return Response(
                {"message": "Error al borrar el pago"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"message": "Pago borrado correctamente"}, status=status.HTTP_200_OK
        )

    def post(self, request, format=None):
        try:
            datosPago = request.data
            pago = registrar_pago(datosPago)
            if pago is None:
                return Response(
                    {"message": "Error al registrar el pago"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = PagoSerializer(pago)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"message": "Consulta mal formada"}, status=status.HTTP_400_BAD_REQUEST
            )


class TarjetaView(APIView):

    def post(self, request, format=None):
        tarjetaData = request.data

        if verificar_tarjeta(tarjetaData) is False:
            return Response(
                {"message": "Datos no encontrados en la base de datos"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "Datos encontrados en la base de datos"},
            status=status.HTTP_200_OK,
        )


class ComercioView(APIView):

    def get(self, request, idComercio):
        pagos = get_pagos_from_db(idComercio)

        if pagos is None:
            return Response(
                {"message": "No existen pagos para este comercio"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PagoSerializer(pagos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
