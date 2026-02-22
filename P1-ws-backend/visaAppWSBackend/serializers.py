from rest_framework import serializers

from .models import Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = [
            "id",
            "idComercio",
            "idTransaccion",
            "importe",
            "tarjeta",
            "marcaTiempo",
            "codigoRespuesta",
        ]
